# Execution Analytics App - User Guide

## What this app does
This Dash app provides two analytics areas:

- `TCA` (Transaction Cost Analysis)
  - `Summary`: desk and regional KPI overview
  - `Execution`: algo-level execution performance
- `ARX` (Experiment Analytics)
  - `Summary`: portfolio-level experiment status and coverage
  - `Analysis`: filtered experiment diagnostics and significance view

Each page also includes **Get AI Summary** at the bottom for a quick narrative summary.

## Start the app
From the project root:

```powershell
conda run -n dash_env python app.py
```

Then open the local URL shown in terminal (typically `http://127.0.0.1:8050`).

## Navigate the app
- Use the left sidebar to switch between TCA and ARX pages.
- Use page filters, then click page refresh buttons where applicable:
  - ARX Summary: `Refresh Summary`
  - ARX Analysis: `Refresh Breakdown`
- For AI text summary on any page:
  - Click `Get AI Summary` at the bottom.

## AI Summary behavior
- If `OPENAI_API_KEY` is configured, the app calls OpenAI and returns a generated summary.
- If not configured (or API call fails), the app returns a built-in dummy summary for that page.

## Notes
- Data in this project is currently mock/demo data.
- Summary text is informational and should be validated before external use.
