---
title: "02 - Fundamental Analysis Prompt"
type: prompt
status: active
updated: 2026-10-20
tags: ["investing", "prompts"]
verification: not-applicable
origin: "Stock Analysis/Prompts/Prompt 02 · The Fundamentals.md"
aliases: ["Prompt 02 · The Fundamentals"]
---

# 02 - Fundamental Analysis Prompt

Pulls the financial health snapshot AND compares against 5 competitors. This is where you find out if you are paying premium or getting a deal.

## Usage

Replace the ticker placeholder in the reusable prompt. Keep the research date and source links with any output. The saved example is retained for reference.

## Reusable prompt

```text
You are an institutional equity research analyst. For ticker
$[TICKER], do a financial health and competitive
valuation breakdown.

Search the web for current data. Cover these in order:

1. THE STOCK ITSELF
   - Current price, market cap, 30-day and YTD performance
   - Forward P/E and EV/Sales
   - Last quarter revenue growth, EPS growth, gross margin
   - Cash position, debt, and share count change YoY (dilution)
   - Last management guidance (revenue and EPS for next year)

2. THE 5 CLOSEST COMPETITORS
   Identify the 5 most relevant publicly-traded competitors.
   Build a comparison table with:
   - Ticker and company name
   - Forward P/E
   - EV/Sales (forward)
   - Revenue growth (last reported quarter)
   - Market cap
   - One-line note on positioning vs $[TICKER]

3. THE VERDICT
   Based on the peer comparison:
   - Is $[TICKER] at a premium, in line, or at a discount?
   - Show the math (e.g., "trading at 4.1x sales vs peer median
     of 6x = 30% discount")
   - Note any specific anomaly (e.g., "growing twice as fast at
     half the multiple")

End with a conditional verdict:
"If you believe [BULL THESIS], $[TICKER] is [CHEAP / FAIR /
EXPENSIVE] versus its peers because [REASON]."

Keep response under 300 words. Show numbers, not adjectives.

```

## Saved example

```text
You are an institutional equity research analyst. For ticker
$ONDS, do a financial health and competitive
valuation breakdown.

Search the web for current data. Cover these in order:

1. THE STOCK ITSELF
   - Current price, market cap, 30-day and YTD performance
   - Forward P/E and EV/Sales
   - Last quarter revenue growth, EPS growth, gross margin
   - Cash position, debt, and share count change YoY (dilution)
   - Last management guidance (revenue and EPS for next year)

2. THE 5 CLOSEST COMPETITORS
   Identify the 5 most relevant publicly-traded competitors.
   Build a comparison table with:
   - Ticker and company name
   - Forward P/E
   - EV/Sales (forward)
   - Revenue growth (last reported quarter)
   - Market cap
   - One-line note on positioning vs $ONDS

3. THE VERDICT
   Based on the peer comparison:
   - Is $[TICKER] at a premium, in line, or at a discount?
   - Show the math (e.g., "trading at 4.1x sales vs peer median
     of 6x = 30% discount")
   - Note any specific anomaly (e.g., "growing twice as fast at
     half the multiple")

End with a conditional verdict:
"If you believe [BULL THESIS], $ONDS is [CHEAP / FAIR /
EXPENSIVE] versus its peers because [REASON]."

Keep response under 300 words. Show numbers, not adjectives.

```

## Related

- [[Investing Index]]
