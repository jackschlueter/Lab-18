---
name: buffett-10k
description: Use this skill to evaluate a ticker from five years of SEC 10-K facts with Buffett-style business checks and a sourced memo.
---

# Buffett 10-K

From this skill's folder, run `python3 edgar.py TICKER` and read its printed table and checks. Set `SEC_USER_AGENT` to your real name and email first, for example `Your Name you@example.com`. The script uses only the SEC's keyless ticker map and company facts API. Do not install FAskills or use its paid data sources.

The script owns all numeric selection and arithmetic: last five fiscal-year-end dates; 10-K only; one-year revenue, net income, and cash flows; latest filing for a repeated period; the specified XBRL tag fallbacks; ROE; owner earnings; and the three checks. Missing facts print `not found`; checks with missing inputs print `not known`. Do not fill gaps with estimates or other data.

After running the script, write a short Buffett-style business memo to `TICKER.md` beside this `SKILL.md`, choosing **own the business**, **watch it**, or **pass**. Use only numeric values the script printed. Say what is judgment and why; discuss business quality and cash generation, not price. If owner earnings are `not found`, say plainly that they cannot be judged from this exercise. The three checks are evidence, not an automatic decision rule. Buffett's [1986 letter](https://www.berkshirehathaway.com/letters/1986.html) explains why owner earnings matter; this classroom measure is specifically operating cash flow minus capital spending and is only a proxy for his fuller concept.

Run `python3 edgar.py TICKER --check-memo TICKER.md` from the skill folder to flag unsupported numbers before finishing. Launch `streamlit run app.py` from that folder to view the chart, table, checks, and memo.
