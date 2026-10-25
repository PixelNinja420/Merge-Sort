# FINAL CHANGE SUMMARY & PROJECT AUDIT

**Group:** G1 Mini-Project (ISA Term Assessment)  
**Project:** MergeFlow — File & Log Sorter  
**Algorithm:** Merge Sort + Recursion Tree Method  
**GitHub Repository:** [https://github.com/PixelNinja420/Merge-Sort](https://github.com/PixelNinja420/Merge-Sort)  
**Date of Audit:** October 2026  

---

## 1. What Was Already Working in the Initial ZIP
- High-level layout of the Spotify-themed dark dashboard with green accents.
- Basic client-side file reading with drag-and-drop support.
- Initial placeholder SVG for the recursion tree.
- Preliminary single-row CSV and text line parsing.
- Basic metric cards on the overview page.

---

## 2. What Was Changed and Improved

### Algorithm & Architectural Alignment
1. **Academic Merge Sort Alignment (PDF Reference Notes):**
   - Refactored `mergeSort` to strictly implement the top-down recursive formula from lecture notes using inclusive $[low..high]$ indexing with `mid = Math.floor((low + high) / 2)`.
   - Explicitly handled the $low \ge high$ base case and stable merge combining step.
2. **Interactive Recursion Tree Explorer:**
   - Transformed the tree visualization from a generic display into an **exact, live dynamic reflection** of the actual sorting execution.
   - Built interactive node click inspection displaying call depth, record range ($[low..high]$), element count, and the actual values processed at that subproblem stage.
   - Added tree bounding with an explicit badge indicator (`SHOWING X OF Y LEVELS`) for large datasets to prevent SVG DOM explosion while preserving exact global counters.
3. **Ascending and Descending Direction:**
   - Added user-selectable direction control (`asc` and `desc`), seamlessly propagating through all modes (text, numeric, timestamp, and length).
4. **Header Detection Toggle:**
   - Added an explicit toggle switch allowing users to specify whether row 1 represents column headers or regular data records.
5. **PDF Worked Example Button:**
   - Added a dedicated 1-click **"PDF Example"** button in the workbench that loads the exact 10 numbers from the handwritten reference notes (`310, 285, 179, 652, 351, 423, 861, 254, 450, 520`), allowing instant verification.
6. **Detailed Live Performance Metrics:**
   - Element comparisons directly tracked within the merge comparison step.
   - Distinct counts for merge operations ($n - 1$), total recursive calls ($2n - 1$), maximum recursion tree depth ($\lceil \log_2 n \rceil$), and record placements/moves.
   - High-precision execution timer with `performance.now()`.
7. **Large File Warnings:**
   - Added automatic file size evaluation warning banners for datasets $> 1 \text{ MB}$ and $> 5 \text{ MB}$.
8. **Cloud Deployment Readiness:**
   - Configured `vercel.json` for instant zero-config static site deployment on Vercel.
   - Configured `render.yaml` for instant static site deployment on Render.
   - Created `package.json` for npm script compatibility (`npm start`, `npm test`).

---

## 3. Bugs Fixed
1. **Index Boundary Mismatch:** Fixed previous half-open $[0, n)$ range indexing to match the academic lecture notes' inclusive $[low, high]$ bounds.
2. **Missing In-Depth Node Inspection:** Previous tree explorer lacked value visibility. Clicking a node now displays the exact data values in that segment.
3. **Double Quote Escaping in CSV Export:** Fixed an issue where quoted strings with internal double quotes were unescaped on export; implemented RFC-4180 standard `""` escaping.
4. **Metric Drift on Successive Runs:** Ensured all counters (comparisons, depth, calls, moves, events) cleanly reset before every sorting pass.
5. **Zero and Single Record Crashes:** Added explicit guards preventing empty files or single-line records from throwing recursion errors.

---

## 4. Tests Actually Performed

All 15 tests were implemented and verified with `node test_suite.js`:

| Test # | Description | Outcome |
| :---: | :--- | :---: |
| **1** | PDF Numerical Example (`310, 285, 179...`) | **PASSED** |
| **2** | Already-Sorted Input Preservation | **PASSED** |
| **3** | Reverse-Sorted Input | **PASSED** |
| **4** | Duplicate Values & Stable Sorting Verification | **PASSED** |
| **5** | Empty Input Handling | **PASSED** |
| **6** | Single Element Base Case | **PASSED** |
| **7** | Negative and Decimal Numeric Sorting | **PASSED** |
| **8** | CSV Multi-column, Quoted Commas & Escaped Quotes | **PASSED** |
| **9** | Log Timestamps Chronological Sorting | **PASSED** |
| **10**| Descending Order Sorting | **PASSED** |
| **11**| Metrics Accuracy (Comparisons, Merges, Calls, Depth) | **PASSED** |
| **12**| Recursion Tree Nodes & Depth Matching Calls | **PASSED** |
| **13**| File Export Integrity (CSV & JSON Report) | **PASSED** |
| **14**| Malformed / Missing Keys Handling | **PASSED** |
| **15**| Large Dataset Scaling (1,000 Elements) | **PASSED** |

---

## 5. How to Run the Final Application

### Method 1: Local Browser (Recommended)
1. Double-click `index.html` in file explorer.
2. The application opens instantly in your default web browser.
3. No internet connection, server, or software installation required.

### Method 2: Local Static Server (Optional)
```bash
npm start
# or
npx serve .
```

### Method 3: Cloud Deployment
- **Vercel:** Import repository `PixelNinja420/Merge-Sort` into Vercel and click Deploy.
- **Render:** Create a Static Site from `PixelNinja420/Merge-Sort` with Publish Directory set to `.`.

---

## 6. Generated Project Files Summary

| File Name | Purpose / Description |
| :--- | :--- |
| **`index.html`** | Complete, zero-dependency application (HTML, CSS, JS) with dark UI, Merge Sort engine, recursion tree SVG, activity feed, and metrics. |
| **`sample_server.log`** | Production server logs with ISO timestamps for demonstration. |
| **`sample_movies.csv`** | Multi-column CSV dataset with headers and movie records. |
| **`sample_products.csv`** | RFC-4180 test CSV with quoted commas, double quotes, and decimal prices. |
| **`pdf_example.txt`** | The 10 numbers from the academic reference lecture notes. |
| **`sample_large_logs.log`** | 500-line randomized server log file for demonstrating scaling. |
| **`test_suite.js`** | Automated 15-point test runner verifying algorithm, stability, edge cases, and metrics. |
| **`vercel.json`** | Configuration for zero-config static deployment on Vercel. |
| **`render.yaml`** | Configuration for static site deployment on Render. |
| **`package.json`** | Standard metadata and scripts for `npm start` and `npm test`. |
| **`README.md`** | Comprehensive GitHub and developer documentation. |
| **`README.txt`** | Plain-text instructions for offline viewing. |
| **`COLLEGE_MINI_PROJECT_REPORT.md`** | Formal academic mini-project submission report for ISA evaluation. |
| **`DEMO_AND_VIVA_GUIDE.md`** | 2–3 minute demonstration script and 15 top viva questions with answers. |
| **`FINAL_CHANGE_SUMMARY.md`** | Complete changelog, bug fixes, and verification audit. |
| **`mergeflow_g1_project.zip`** | Self-contained offline distribution ZIP archive. |
