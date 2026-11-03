"""Streamlit view of the Buffett 10-K classroom exercise."""

import os
from pathlib import Path

import pandas as pd
import streamlit as st

from edgar import METRICS, fetch_report, fmt, fmt_multiple, render_text, unsupported_numbers

ROOT = Path(__file__).resolve().parent

st.set_page_config(page_title="Buffett 10-K classroom demo", layout="wide")
st.title("Buffett 10-K classroom demo")
st.caption("Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.")

ticker = st.text_input("Ticker", value="COST").strip().upper()
agent = st.text_input("SEC User-Agent (your name and email, if not set locally)", type="password")
if agent:
    os.environ["SEC_USER_AGENT"] = agent

if ticker:
    try:
        report = fetch_report(ticker)
    except Exception as error:
        st.error(str(error))
        st.stop()

    rows = report["rows"]
    st.subheader(f"{report['company']} ({ticker})")
    st.write("Fiscal years are labelled by year-end date. Values are USD; facts come only from 10-K filings.")

    chart = pd.DataFrame([
        {"Fiscal year end": r["fiscal_year_end"], "Owner earnings": r["owner_earnings"], "Net income": r["net_income"]["value"]}
        for r in rows
    ])
    st.subheader("Owner earnings and net income")
    st.line_chart(chart, x="Fiscal year end", y=["Owner earnings", "Net income"])

    table_rows = []
    for row in rows:
        display = {"Fiscal year end": row["fiscal_year_end"]}
        for field in METRICS:
            display[field] = fmt(row[field]["value"])
            display[f"{field} tag"] = row[field]["tag"]
        display["ROE"] = row["roe_status"] or fmt(row["roe"], True)
        display["ROE tags"] = "NetIncomeLoss / StockholdersEquity"
        display["Liabilities / equity"] = row["liabilities_to_equity_status"] or fmt_multiple(row["liabilities_to_equity"])
        display["Owner earnings"] = fmt(row["owner_earnings"])
        display["Owner earnings tags"] = f"{row['operating_cash_flow']['tag']} - {row['capital_spending']['tag']}"
        table_rows.append(display)
    st.subheader("Five-year table")
    st.dataframe(pd.DataFrame(table_rows), hide_index=True, width="stretch")

    st.subheader("Buffett-style checks")
    labels = {
        "roe_15_each_year": "ROE at least 15% every year",
        "owner_earnings_positive_each_year": "Owner earnings positive every year",
        "owner_earnings_grew_first_to_last": "Owner earnings grew, first year to last",
    }
    for key, label in labels.items():
        st.write(f"**{label}:** {report['checks'][key]}")

    st.subheader("Business memo")
    memo_path = ROOT / f"{ticker}.md"
    memo = memo_path.read_text() if memo_path.exists() else ""
    if memo:
        st.markdown(memo)
        unsupported = unsupported_numbers(memo, render_text(report))
        if unsupported:
            st.error("Numbers in the memo absent from the script output: " + ", ".join(f"{number} (line {line})" for number, line in unsupported))
        else:
            st.success("Every number in the memo appears in the script output.")
    else:
        st.info("Memo not found. Use the buffett-10k skill to write and save TICKER.md for this ticker.")
    with st.expander("Edit or add the memo"):
        edited = st.text_area("Memo Markdown", value=memo, height=240)
        if st.button("Save memo"):
            memo_path.write_text(edited)
            st.rerun()
