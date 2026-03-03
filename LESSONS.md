## Lesson 13: Create Demo Chart Generation Script
**Date:** 2026-03-03
**Trigger:** User requested a demo Word document showcasing all 17 chart types defined in FRONTEND_GUIDELINES.md.

**Problem:** Needed to demonstrate the custom design system (Times New Roman, Black/Orange colors, sharp corners) applied to all chart types.

**Solution:**
Created `scripts/create_demo_charts.py` that generates:
- 17 chart types as PNG images using matplotlib
- A Word document (demo_charts_collection.docx) embedding all charts
- All charts use the design system colors and typography

**Charts Generated:**
1. Combination Bar and Line Chart
2. 100% Stacked Bar Chart
3. Line Chart
4. Pie Chart
5. Radar Chart
6. Mekko Chart
7. Area Chart
8. Scatter Plot
9. Heatmap
10. Histogram
11. Box Plot
12. Violin Plot
13. Funnel Chart
14. Gauge Chart
15. Treemap
16. Sunburst Chart
17. Waterfall Chart

**Required Dependencies:**
```bash
pip install python-docx matplotlib numpy squarify
```

**Usage:**
```bash
python3 scripts/create_demo_charts.py
```

---

## Lessons Learned (Future entries will be added here)