# Execution Analytics App - Developer Guide

## 1) Project layout

- `app.py`: Dash app bootstrap, Mantine provider, cache init, shell layout.
- `pages/`: route-level pages.
- `layouts/`: reusable layout builders (ARX currently uses this heavily).
- `components/`: shared UI components.
- `callbacks/`: callback logic modules.
- `services/`: data access/services (mock kdb, cache, AI summary).
- `utils/`: plotting/dataframe/query helpers.
- `theme.py`: shared UI theme tokens and Mantine defaults.
- `ai_summary_config.py`: per-page AI system/user prompts + dummy summaries.

## 2) Local setup

### Prerequisites
- Python 3.10+ recommended
- Conda (current project convention)

### Create/activate environment (example)

```powershell
conda create -n dash_env python=3.11 -y
conda activate dash_env
```

### Install dependencies
No lockfile is currently committed, so install the core packages:

```powershell
pip install dash dash-mantine-components plotly pandas flask-caching openai
```

### Run app

```powershell
python app.py
```

## 3) AI summary integration

AI summary is generic and page-driven:

- Config source: `ai_summary_config.py`
- Service: `services/ai_summary_service.py`
- UI component: `components/ai_summary.py`
- Callback registration: `callbacks/ai_summary_callbacks.py`

To add AI summary to a new page:

1. Add a new page key in `ai_summary_config.py` with:
   - `system_prompt`
   - `user_prompt`
   - `page_content`
   - `dummy_summary`
2. Add `ai_summary_card("<page_key>")` to that page layout.
3. Ensure callback module import remains active in `app.py`.

## 4) Coding standards for this repo

### Architecture
- Keep data access in `services/`.
- Keep page-level callback behavior in `callbacks/`.
- Keep reusable UI in `components/`; avoid copy-pasting UI blocks.
- Keep reusable constants/theme tokens in `theme.py`.
- Keep query-shape helpers in `utils/` (for example kdb query builders).

### Styling and UI consistency
- Prefer theme tokens over hardcoded values (`theme.py`).
- Reuse shared plotting helpers (`utils/plotting_utils.py`) for chart layout.
- Reuse shared table style constants from `theme.py`.

### Data and API boundaries
- Services should return stable structures (dict/DataFrame) expected by callbacks.
- For ARX/TCA, prefer wrappers that isolate future live data source swaps.
- Keep mock fallback behavior when external systems are unavailable.

### Callbacks
- Keep callback functions focused: parse inputs, call services, render outputs.
- Avoid embedding business logic directly in layout files.
- Use clear component IDs with page prefixes (existing convention).

### General Python quality
- Use type hints where practical.
- Keep functions small and single-purpose.
- Prefer explicit naming over short/ambiguous names.
- Avoid silent mutation patterns unless clearly intended.

## 5) Validation before commit

Run compile checks:

```powershell
conda run -n dash_env python -m compileall app.py callbacks components layouts pages services utils
```

Optionally run the app and manually verify:
- Page navigation works.
- Filters update charts/tables correctly.
- AI summary button returns text for each page.

## 6) Git workflow

```powershell
git status
git add .
git commit -m "Your message"
git push
```

If push/auth issues appear, verify credential helper:

```powershell
git config --global credential.helper manager-core
```
