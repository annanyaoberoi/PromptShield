"""
PromptShield — AI Security Gateway
Phase 1: Passthrough gateway with auth, logging, and stub shield layer.

Architecture:
  Client → POST /v1/chat → [auth] → [shield (stub)] → ShopBot → [log] → Client
"""

import hashlib
import os
import httpx

from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
import asyncpg
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

ALLOWED_API_KEY: str = os.environ["ALLOWED_API_KEY"]          # Required — fail fast if missing
DATABASE_URL: str    = os.environ["DATABASE_URL"]             # Required
SHOPBOT_URL: str     = os.getenv("SHOPBOT_URL", "http://localhost:8000/chat")
GATEWAY_PORT: int    = int(os.getenv("GATEWAY_PORT", "9000"))
HTTP_TIMEOUT: float  = float(os.getenv("HTTP_TIMEOUT_SECONDS", "30"))


# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

class Database:
    """Thin wrapper around an asyncpg connection pool."""

    pool: asyncpg.Pool | None = None

    @classmethod
    async def connect(cls) -> None:
        cls.pool = await asyncpg.create_pool(DATABASE_URL, min_size=2, max_size=10)
        await cls._ensure_schema()

    @classmethod
    async def disconnect(cls) -> None:
        if cls.pool:
            await cls.pool.close()

    @classmethod
    async def _ensure_schema(cls) -> None:
        """Create request_logs table if it doesn't already exist."""
        async with cls.pool.acquire() as conn:
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS request_logs (
                    id           SERIAL PRIMARY KEY,
                    timestamp    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    api_key_hash TEXT        NOT NULL,
                    raw_prompt   TEXT        NOT NULL,
                    raw_response TEXT,
                    blocked      BOOLEAN     NOT NULL DEFAULT FALSE,
                    block_reason TEXT
                );
                """
            )

    @classmethod
    async def log_request(
        cls,
        *,
        api_key_hash: str,
        raw_prompt: str,
        raw_response: str | None,
        blocked: bool,
        block_reason: str | None,
    ) -> int:
        """Insert one row into request_logs; returns the new row id."""
        async with cls.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                INSERT INTO request_logs
                    (timestamp, api_key_hash, raw_prompt, raw_response, blocked, block_reason)
                VALUES ($1, $2, $3, $4, $5, $6)
                RETURNING id
                """,
                datetime.now(timezone.utc),
                api_key_hash,
                raw_prompt,
                raw_response,
                blocked,
                block_reason,
            )
            return row["id"]


# ---------------------------------------------------------------------------
# Shield (stub)
# ---------------------------------------------------------------------------

class ShieldResult:
    """Result from the shield inspection layer."""

    __slots__ = ("blocked", "reason")

    def __init__(self, blocked: bool = False, reason: str | None = None):
        self.blocked = blocked
        self.reason  = reason


def inspect_prompt(prompt: str) -> ShieldResult:
    """
    Phase 1 stub — always passes through.

    TODO (Phase 2): replace with layered detection engine:
      Layer 1 — heuristic regex (cheap, fast)
      Layer 2 — ML classifier (sentence-transformers)
      Layer 3 — LLM-as-judge (for ambiguous cases only)
    """
    _ = prompt  # silence linter; used in future layers
    return ShieldResult(blocked=False, reason=None)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def sha256_hex(value: str) -> str:
    """Return the hex SHA-256 digest of a UTF-8 string."""
    return hashlib.sha256(value.encode()).hexdigest()


def validate_api_key(api_key: str) -> None:
    """Raise 401 immediately if the supplied key doesn't match."""
    if api_key != ALLOWED_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key.")


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=32_768, description="User prompt")
    api_key: str = Field(..., min_length=1, description="Gateway API key")


class ChatResponse(BaseModel):
    response:   str
    blocked:    bool  = False
    log_id:     int   | None = None
    block_reason: str | None = None


class BlockedResponse(BaseModel):
    detail:      str
    blocked:     bool = True
    block_reason: str | None = None
    log_id:      int  | None = None


# ---------------------------------------------------------------------------
# Application lifecycle
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    await Database.connect()
    yield
    await Database.disconnect()


app = FastAPI(
    title="PromptShield",
    description="AI Security Gateway — inspect, block, and log LLM traffic.",
    version="0.1.0",
    lifespan=lifespan,
)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.post(
    "/v1/chat",
    response_model=ChatResponse,
    responses={
        401: {"description": "Invalid API key"},
        400: {"description": "Prompt blocked by shield"},
        502: {"description": "ShopBot upstream error"},
    },
    summary="Send a message through the PromptShield gateway",
)
async def chat(payload: ChatRequest, request: Request) -> ChatResponse:
    """
    Main gateway endpoint.

    Flow:
      1. Validate API key (401 on failure — early return, no DB write).
      2. Run shield inspection (stub for now).
      3. If blocked: log + return 400.
      4. Forward to ShopBot.
      5. Log successful request + return response.
    """

    # ── 1. Auth ──────────────────────────────────────────────────────────────
    validate_api_key(payload.api_key)
    key_hash = sha256_hex(payload.api_key)

    # ── 2. Shield ────────────────────────────────────────────────────────────
    shield_result = inspect_prompt(payload.message)

    if shield_result.blocked:
        log_id = await Database.log_request(
            api_key_hash=key_hash,
            raw_prompt=payload.message,
            raw_response=None,
            blocked=True,
            block_reason=shield_result.reason,
        )
        raise HTTPException(
            status_code=400,
            detail={
                "detail":       "Prompt blocked by PromptShield.",
                "blocked":      True,
                "block_reason": shield_result.reason,
                "log_id":       log_id,
            },
        )

    # ── 3. Forward to ShopBot ────────────────────────────────────────────────
    try:
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            upstream = await client.post(
                SHOPBOT_URL,
                json={"message": payload.message},
            )
            upstream.raise_for_status()
            shopbot_data = upstream.json()
            bot_response: str = shopbot_data.get("response", "")

    except httpx.TimeoutException:
        raise HTTPException(status_code=502, detail="ShopBot timed out.")
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"ShopBot returned {exc.response.status_code}.",
        )
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Could not reach ShopBot: {exc}",
        )

    # ── 4. Log + return ──────────────────────────────────────────────────────
    log_id = await Database.log_request(
        api_key_hash=key_hash,
        raw_prompt=payload.message,
        raw_response=bot_response,
        blocked=False,
        block_reason=None,
    )

    return ChatResponse(
        response=bot_response,
        blocked=False,
        log_id=log_id,
    )


@app.get("/healthz", summary="Liveness probe")
async def healthz():
    """Returns 200 when the gateway is running. Used by Docker / load balancers."""
    return {"status": "ok", "service": "promptshield", "version": app.version}
