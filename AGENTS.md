# NQ Scenario Replay Project Instructions

This project is an NQ / Nasdaq 100 scenario analysis and replay database.

When the user asks for chart analysis, scenario creation, scenario-map image generation, replay review, or CSV storage, follow these instructions first.

## Required Reading

- Use `rules/trading_manual_v4.md` as the highest-priority trading framework.
- Use these helper rules only as filters:
  - `rules/trading_skill_double_bollinger_1h_v1.md`
  - `rules/trading_skill_pattern_filter_mtf_v1.md`
  - `rules/trading_skill_volume_filter_nq_v1.md`
  - `rules/line_chart_scenario_output_guide.md`
- Use `prompts/codex_start_prompt.md` for the standard answer format.
- Use `.codex/skills/nq_replay/SKILL.md` for the NQ replay workflow.

## Chart Analysis Format

When the user attaches 1H, 15M, and 5M charts and asks for chart analysis, answer in this order:

1. Conclusion
   - Direction first.
   - Whether immediate entry is allowed.
   - The practical strategy in one sentence.

2. 1H Direction
   - Higher timeframe direction.
   - Double Bollinger, RSI, overextension/mean reversion, and major support/resistance.
   - Key levels in a table when useful.

3. 15M Structure
   - Execution zone, value area, box, FVG, support/resistance.
   - Separate conditions that maintain the idea from conditions that break it.

4. 5M Trigger
   - Decide whether the trigger is complete.
   - Use box break/reclaim, retest, double top/bottom, and 5M close confirmation.
   - RSI, volume, and CVD are approval filters, not standalone entry signals.

5. Trading Scenarios
   - Scenario 1: main scenario.
   - Scenario 2: secondary or countertrend scalp.
   - Scenario 3: failure/reversal scenario.
   - Each scenario must include entry zone, trigger, stop/invalidation, first target, second target, and grade.

6. Final Judgment
   - State the current action clearly: wait, wait for pullback, confirm retest after breakout, confirm retest after breakdown.
   - Explicitly warn against chasing when the trigger is extended.

## Scenario Map Image Rule

When generating a scenario-map image:

- Use the attached original 5M chart as the exact base chart.
- 1H determines direction, 15M determines structure, and 5M determines the actual scenario-map layout.
- Match the original 5M chart as closely as possible: current price, recent highs/lows, candle clusters, box top/bottom, pivot, support/resistance, and time axis.
- Do not redraw or alter past candles that are visible in the original 5M chart.
- Future expected paths must be visually separate from real candles, using dashed arrows or distinct colors.
- Save original analysis charts to `data/screenshots/before/`.
- Save generated scenario maps to `data/screenshots/scenario_maps/`.
- Save replay/result charts to `data/screenshots/after/`.

## Review DB

- Store structured replay records in `data/reviews.csv`.
- Use `scripts/add_review.py` to append reviews when possible.
- Use `scripts/search_reviews.py` for similar-case lookup.
- Use `scripts/summarize_reviews.py` for review statistics.
- Chart paths in CSV should point inside `data/screenshots/`, not to `Downloads`.

## Sync Routine

Before work:

```powershell
git pull origin master
```

After storing reviews or screenshots:

```powershell
git status
git add data/reviews.csv data/screenshots scripts REVIEW_DB.md AGENTS.md .codex/skills/nq_replay/SKILL.md prompts/codex_start_prompt.md
git commit -m "Add NQ review"
git push origin master
```
