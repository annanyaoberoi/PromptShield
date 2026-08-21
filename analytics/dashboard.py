import os
import psycopg2
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv("/home/kali/promptshield/promptshield-gateway/.env")

DATABASE_URL = os.environ["DATABASE_URL"]

st.set_page_config(
    page_title="PromptShield Security Analytics",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ PromptShield Security Analytics")
st.caption("Security monitoring dashboard for detected prompt-injection attempts")


@st.cache_data(ttl=5)
def load_logs():
    conn = psycopg2.connect(DATABASE_URL)

    query = """
        SELECT
            id,
            timestamp,
            raw_prompt,
            blocked,
            block_reason
        FROM request_logs
        ORDER BY timestamp DESC
    """

    df = pd.read_sql(query, conn)
    conn.close()

    return df


try:
    df = load_logs()

    if df.empty:
        st.info("No request logs available yet.")
        st.stop()

    # Metrics
    total_requests = len(df)
    blocked_requests = int(df["blocked"].sum())
    allowed_requests = total_requests - blocked_requests
    block_rate = (
        blocked_requests / total_requests * 100
        if total_requests > 0
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Requests", total_requests)
    col2.metric("Blocked", blocked_requests)
    col3.metric("Allowed", allowed_requests)
    col4.metric("Block Rate", f"{block_rate:.1f}%")

    st.divider()

    # Attack categories
    st.subheader("Detected Attack Types")

    blocked_df = df[df["blocked"] == True].copy()

    if not blocked_df.empty:
        categories = (
            blocked_df["block_reason"]
            .fillna("unknown")
            .str.replace("heuristic:", "", regex=False)
            .value_counts()
        )

        st.bar_chart(categories)

    else:
        st.success("No blocked requests detected.")

    st.divider()

    # Recent security events
    st.subheader("Recent Security Events")

    if not blocked_df.empty:
        display_df = blocked_df[
            ["timestamp", "raw_prompt", "block_reason"]
        ].head(10)

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
        )

    st.divider()

    # All requests
    st.subheader("Recent Requests")

    st.dataframe(
        df[
            ["id", "timestamp", "raw_prompt", "blocked", "block_reason"]
        ].head(20),
        use_container_width=True,
        hide_index=True,
    )

except Exception as e:
    st.error(f"Could not connect to PostgreSQL: {e}")
