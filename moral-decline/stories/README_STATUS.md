# Lowe Family Stories — Build Status

**Built by:** Claude Opus (POF 2828 session)
**Date:** April 13, 2026
**Theme:** Red accent (#dc2626) / Amber (#f59e0b) / Dark (#050505) — matches parent series

## Files Delivered

| File | Content | Status |
|------|---------|--------|
| `story-00-introduction.html` | Series overview, family tree, master charts (3x Chart.js) | DONE |
| `story-01-samuel-1900.html` | Samuel narrative + radar chart constraint profile | DONE |
| `story-02-henry-1926.html` | Henry narrative + comparison bar chart (1900 vs 1926) | DONE |
| `story-03-william-1950.html` | William narrative + radar + TV adoption line chart | DONE |
| `story-04-thomas-1974.html` | Thomas narrative + radar overlay (1950 vs 1974) + threshold chart | DONE |
| `story-05-jacob-1998.html` | Jacob narrative + marriage duration bars + tech timeline | DONE |
| `story-06-jacob-2025.html` | Jacob 2025 narrative + coherence line (all generations) | DONE |

## Integration

- **Series index updated:** `moral-decline-america.html` now has a "Lowe Family Stories" section with cards linking to all 7 pages
- **Nav link added:** "Stories" link in the index page nav bar
- **Footer link added:** Stories link in the index page footer
- **Stat ribbon updated:** Shows "7 Family Stories" instead of "1 Conclusion"

## Things to Check When You Get Home

1. **Open each story in browser** — verify Chart.js renders, colors match, nav links work
2. **Folder name typo:** The folder is `Stoires` — should probably be `Stories`. If you rename it, update links in:
   - `moral-decline-america.html` (7 card links + footer link all reference `Stoires/`)
   - Each story's prev/next nav links reference sibling files (those won't break on rename)
3. **Story content accuracy** — narratives were adapted from the vault markdown files. Some sensory detail was added. Check that nothing drifted from your intent
4. **Alternate versions** — `01_Samuel_1900_2.md` and `04_Thomas_1974_2.md` had additional analytical sections. Those were incorporated into the "Analyst's Commentary" blocks in the respective story pages. Verify they landed right
5. **Main series articles (Parts 01-10)** do NOT yet link back to the Stories. Could add a callout/banner at the bottom of each article pointing to the corresponding story
6. **Git:** Nothing committed or pushed yet. All changes are local in `D:\GitHub\genesis-to-quantum\`

## Source Files Used

- `C:\Users\lowes\Documents\[6.2] Moral_Decline_Series_Substack\05_Stories\00_Introduction.md`
- `01_Samuel_1900.md`, `01_Samuel_1900_2.md`
- `02_Henry_1926.md`
- `03_William_1950.md`
- `04_Thomas_1974.md`, `04_Thomas_1974_2.md`
- `05_Jacob_1998.md`
- `06_Jacob_2025.md`
