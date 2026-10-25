# MergeFlow — File & Log Sorter

> **Group G1 Mini-Project — ISA Term Assessment**  
> **Topic:** Merge Sort + Recursion Tree Method  
> **Course:** Data Structures & Algorithms / Third Year Computer Engineering  
> **Live GitHub Repository:** [https://github.com/PixelNinja420/Merge-Sort](https://github.com/PixelNinja420/Merge-Sort)

---

## 1. Project Overview

**MergeFlow** is a client-side file and log sorting tool built using pure HTML, CSS, and modern JavaScript. It implements a top-down recursive **Merge Sort** algorithm, accompanied by an interactive **Recursion Tree Explorer**, an **Activity Feed**, and a real-time **Performance Metrics Dashboard** that measures comparisons, merge operations, recursive calls, and maximum recursion depth.

### Core Objectives
1. Sort raw log files, CSV records, and plain text files with stability.
2. Provide interactive visualization of the **Recursion Tree Method** demonstrating how $T(n) = 2T(n/2) + \Theta(n)$ unfolds step-by-step.
3. Track and verify accurate element-to-element comparison counts ($O(n \log n)$).
4. Run 100% locally with zero server, build, or database dependencies.

---

## 2. Core Algorithm: Top-Down Recursive Merge Sort

MergeFlow follows the academic formulation from reference class notes:

```
Algorithm MergeSort(arr, low, high):
    Input: Array 'arr', inclusive lower index 'low', inclusive upper index 'high'
    Output: Subarray arr[low..high] sorted in place

    Step 1 [Base Case]:
        if low >= high then
            return    // Subarray of 0 or 1 element is already sorted

    Step 2 [Find Middle]:
        mid = floor((low + high) / 2)

    Step 3 [Divide & Recursively Sort]:
        MergeSort(arr, low, mid)          // Left half
        MergeSort(arr, mid + 1, high)     // Right half

    Step 4 [Merge Sorted Halves]:
        Merge(arr, low, mid, high)        // In-place combination into sorted order
```

### Numerical Worked Example (From Academic Notes)
- **Input:** `310, 285, 179, 652, 351, 423, 861, 254, 450, 520`
- **Output (Ascending):** `179, 254, 285, 310, 351, 423, 450, 520, 652, 861`
- Built directly into the application via the **"PDF Example"** button.

---

## 3. Main Features

- **Multi-Format Ingestion:** Drag-and-drop or file picker support for `.csv`, `.log`, and `.txt` files.
- **Robust CSV Engine:** RFC-4180 compliant parser supporting headers, commas inside quoted cells, and escaped quotes (`""`). Preserves complete rows during sort.
- **Flexible Sorting Modes:**
  - *Alphabetical / Text* (A → Z or Z → A)
  - *Numeric Value* (Handles positive, negative, and decimal floats)
  - *Date / Timestamp* (ISO 8601 and standard server log timestamps with graceful fallback)
  - *Text Length* (Shorter to longer)
- **Ascending / Descending Direction:** Instant toggle for either sorting direction.
- **Header Detection Toggle:** Seamlessly treat row 1 as column labels or data records.
- **Metrics Dashboard:**
  - Element-to-element comparisons
  - Number of merge operations
  - Total recursive calls ($2n - 1$ for $n > 0$)
  - Maximum recursion depth ($\lceil \log_2 n \rceil$)
  - In-browser execution time in milliseconds
  - Record movement/placement counter
- **Interactive Recursion Tree Explorer:**
  - Visual diagram showing every recursive divide.
  - Interactive clickable nodes showing the exact record range, depth, and input values.
  - Automatically bounds render depth for large files while maintaining 100% accurate global statistics.
- **Live Activity Feed:** Chronological breakdown of splits, base cases, and merges.
- **Searchable & Paginated Results:** Clean, navigable view of sorted outputs.
- **Data & Audit Export:**
  - Export sorted records as formatted CSV or TXT.
  - Download comprehensive JSON run report detailing input metadata, parameters, performance counters, and complexity guarantees.

---

## 4. Supported File Formats

| Format | Extension | Processing Logic |
| :--- | :--- | :--- |
| **CSV** | `.csv` | Parsed into structured rows and columns. Allows choosing the target column while keeping all other columns locked to each row. |
| **Server Logs** | `.log` | Parsed line-by-line. Supports ISO timestamps (`YYYY-MM-DD HH:MM:SS`) or chronological level extraction. |
| **Plain Text** | `.txt` | Line-delimited raw records, numbers, or string keys. |

---

## 5. How to Run Locally (Zero Installation)

> **No installation, no npm, no backend, no server, and no internet connection required.**

1. Clone or download this repository.
2. Double-click `index.html` to open it in any modern web browser (Google Chrome, Mozilla Firefox, Microsoft Edge, Safari, Brave).
3. The application is immediately ready to demonstrate with pre-loaded sample datasets.

---

## 6. How to Deploy Online

### Deploying to Vercel
1. Push this repository to your GitHub account: `https://github.com/PixelNinja420/Merge-Sort`.
2. Go to [Vercel](https://vercel.com) and click **"Add New Project"**.
3. Import the `Merge-Sort` repository.
4. Leave all build settings at default (`vercel.json` will automatically configure static routing).
5. Click **"Deploy"**. Your application will be live instantly.

### Deploying to Render
1. Go to [Render](https://render.com) and click **"New +"** → **"Static Site"**.
2. Connect your GitHub repository `PixelNinja420/Merge-Sort`.
3. Set the following settings:
   - **Name:** `mergeflow-sorter`
   - **Build Command:** *(leave empty)*
   - **Publish Directory:** `.`
4. Click **"Create Static Site"**. (`render.yaml` handles the routing).

---

## 7. Sample Datasets Included

1. `sample_server.log`: Production web server logs with ISO timestamps and log levels.
2. `sample_movies.csv`: Multi-column movie dataset with title, genre, rating, and year.
3. `sample_products.csv`: E-commerce catalog with quoted commas, double quotes, and decimal prices.
4. `pdf_example.txt`: The 10 numbers from the academic reference notes.
5. `sample_large_logs.log`: 500-line server log file for demonstrating scaling.

---

## 8. Automated Testing

To run the full 15-point automated test suite:

```bash
node test_suite.js
```

All 15 test suites verify:
- Exact PDF worked example sorting
- Stability under duplicate keys
- Zero-element and single-element base cases
- Negative numbers and floating-point decimal sorting
- CSV RFC-4180 quoted fields and multi-column preservation
- Log timestamp chronological sequencing
- Metrics calculation accuracy (comparisons, merges, calls, depth)
- Tree node structure and export integrity

---

## 9. Complexity Reference

| Metric | Complexity | Explanation |
| :--- | :--- | :--- |
| **Best-Case Time** | $\mathcal{O}(n \log n)$ | Dividing into halves and merging always requires linear work per level. |
| **Average-Case Time** | $\mathcal{O}(n \log n)$ | Consistently splits input into two subproblems of size $n/2$. |
| **Worst-Case Time** | $\mathcal{O}(n \log n)$ | Independent of initial element ordering. |
| **Auxiliary Space** | $\mathcal{O}(n)$ | Temporary arrays used during the merge step to hold sorted records. |
| **Max Recursion Depth**| $\mathcal{O}(\log n)$ | Balanced binary recursion tree has $\lceil \log_2 n \rceil$ height. |

---

## 10. Known Limitations

- **Browser Memory Limits:** For files exceeding 50 MB (approx. 500,000 lines), browser memory allocation may cause temporary tab sluggishness. A warning banner alerts the user for large files.
- **Tree Visualization Bound:** For large inputs ($n > 64$), the recursion tree visualizer caps rendered levels to preserve screen readability, while exact metrics and the algorithm itself run completely over all elements.

---

## License & Academic Declaration
Developed for academic assessment as part of Third Year Computer Engineering (ISA Term Assessment).  
Author: PixelNinja420 | Group G1
