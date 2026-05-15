# Review DB Guide

`data/reviews.csv` is the structured replay journal. Use it as the main knowledge warehouse for scenario review, trade execution review, and repeated pattern learning.

## Core Files

- `data/reviews.csv`: one row per review.
- `scripts/add_review.py`: append one review row safely without breaking CSV quoting.
- `scripts/search_reviews.py`: search similar reviews by keyword, tag, result, action, or instrument.
- `scripts/summarize_reviews.py`: summarize repeated tags, actions, results, and next rules.

## Useful Commands

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\run_py.ps1 scripts\add_review.py `
  --review-datetime-kst "2026-05-15 13:20 KST" `
  --instrument "NQ" `
  --timeframe "5m" `
  --trade-action "숏 진입" `
  --result "수익" `
  --tags "돌파실패,되돌림저항,CVD약화"
```

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\run_py.ps1 scripts\search_reviews.py --query "돌파실패 되돌림저항 CVD약화"
```

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\run_py.ps1 scripts\search_reviews.py --tag "되돌림저항" --action "숏"
```

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\run_py.ps1 scripts\summarize_reviews.py
```

## How To Read Each Row

- `scenario_bias`: the original directional premise.
- `main_plan`: the planned entry, targets, and invalidation.
- `actual_flow`: what the market actually did.
- `entry_confirmation`: whether entry was chase or confirmed setup.
- `key_levels`: pivot, support, resistance, invalidation, and targets.
- `cvd_read`: order-flow interpretation.
- `good_decision`: what was executed well.
- `risk_check`: what still needs discipline.
- `next_rule`: the reusable rule for future trades.
- `tags`: searchable pattern labels separated by `|`.

## Tagging Rules

Use compact tags with no spaces. Prefer reusable behavior and structure tags:

- Direction/setup: `롱폐기`, `숏전환`, `돌파실패`, `지지이탈`
- Entry quality: `되돌림저항`, `추격아님`, `확인진입`
- Order flow: `CVD약화`, `CVD회복실패`, `거래량증가`
- Levels: `29_620이탈`, `29_560도달`
- Outcome: `수익`, `손실`, `시나리오성공`, `실패전환성공`

## Daily Workflow

1. Save the scenario image path and current chart image path.
2. Add one `reviews.csv` row after the trade or missed trade.
3. Search before the next session with 2-4 tags from the current setup.
4. Run the summary script weekly to find repeating strengths and mistakes.
