# COLLEGE MINI-PROJECT REPORT

**Department of Computer Engineering**  
**Course:** Data Structures & Analysis of Algorithms  
**Assessment:** In-Semester Assessment (ISA) Term Project  
**Group:** G1  
**Project Title:** File/Log Sorter Tool (MergeFlow)  
**Assigned Core Algorithm:** Merge Sort + Recursion Tree Method  
**Student Name / GitHub:** PixelNinja420 ([https://github.com/PixelNinja420/Merge-Sort](https://github.com/PixelNinja420/Merge-Sort))  

---

## 1. Project Title
**MergeFlow — File & Log Sorter Tool using Merge Sort and the Recursion Tree Method**

---

## 2. Aim
To design, implement, and analyze an interactive, browser-based tool capable of sorting structured CSV records and chronological server log files using the top-down recursive Merge Sort algorithm, while visualizing the recursion tree structure, tracking algorithmic comparisons, and verifying theoretical time and space complexity.

---

## 3. Problem Statement
In real-world computing environments, debugging multi-service distributed architectures requires analyzing high-volume log streams and multi-column structured datasets. Standard browser tools or command-line scripts either sort data as a black box without exposing underlying algorithmic mechanics or fail to preserve multi-column row integrity when sorting by specific attributes. 

Students and engineers need an educational yet practical tool that can:
1. Parse complex CSV and log data without corrupting records.
2. Demonstrate how divide-and-conquer sorting works internally through step-by-step recursive decomposition.
3. Quantify exact performance metrics (comparisons, recursive call overhead, recursion tree depth) and validate the theoretical recurrence relation $T(n) = 2T(n/2) + \Theta(n)$.

---

## 4. Objectives
- **Algorithm Fidelity:** Implement an exact top-down recursive Merge Sort following academic reference standards ($low \ge high$ base case, integer floor midpoint split, recursive subproblem calls, and stable merging).
- **Format Ingestion:** Support `.csv`, `.log`, and `.txt` files with drag-and-drop and local file reading.
- **Row Integrity & RFC-4180 Compliance:** Ensure that sorting a CSV table by any column keeps all respective columns bound to that row, correctly parsing commas inside quotes and escaped quotes (`""`).
- **Educational Visualization:** Implement an interactive Recursion Tree Explorer and Activity Feed showing tree depth, node subdivisions, base cases, and subproblem merging.
- **Metric Verification:** Dynamically record element comparisons, merges, calls, and execution duration without relying on static approximations.
- **Zero-Dependency Architecture:** Ensure the system runs fully client-side inside any modern web browser without server, database, or network overhead, while supporting one-click cloud hosting on Vercel and Render.

---

## 5. Hardware and Software Requirements

### Hardware Requirements
- **Processor:** Modern multi-core x86-64 or ARM processor (Intel Core i3 / AMD Ryzen 3 / Apple Silicon or higher).
- **RAM:** Minimum 2 GB (4 GB or higher recommended for large files).
- **Storage:** < 10 MB free disk space.
- **Display:** Minimum resolution 1024×768 (responsive for laptop, tablet, and mobile displays).

### Software Requirements
- **Operating System:** Platform-independent (Windows 10/11, macOS, Linux).
- **Web Browser:** Any modern ECMAScript 2020+ compatible browser (Google Chrome, Mozilla Firefox, Microsoft Edge, Safari, Brave).
- **Runtime Dependencies:** None (Zero external libraries or npm packages required for operation).
- **Deployment Platform (Optional):** Vercel / Render static site hosting.

---

## 6. Introduction to Merge Sort
Merge Sort is a quintessential divide-and-conquer comparison-based sorting algorithm invented by John von Neumann in 1945. It breaks a problem into smaller independent subproblems of identical structure, solves the subproblems recursively, and combines the results to solve the original problem.

Unlike Quick Sort—whose worst-case time degrades to $\mathcal{O}(n^2)$ when pivots are poorly selected—Merge Sort consistently delivers an optimal worst-case time complexity of $\mathcal{O}(n \log n)$. Furthermore, Merge Sort is naturally **stable**, meaning that elements with identical sorting keys preserve their relative order from the input, a crucial property when sorting multi-attribute databases.

---

## 7. Algorithm and Pseudocode

### Academic Pseudocode (As per Reference Notes)

```
Algorithm MergeSort(arr, low, high):
    Input: Array arr, starting index low, ending index high
    Output: Subarray arr[low..high] sorted in non-decreasing order

    // Step 1: Base Case
    if low >= high then
        return

    // Step 2: Divide - Find the Middle
    mid = floor((low + high) / 2)

    // Step 3: Conquer - Recursively Sort Halves
    MergeSort(arr, low, mid)
    MergeSort(arr, mid + 1, high)

    // Step 4: Combine - Merge the Two Sorted Halves
    Merge(arr, low, mid, high)


Algorithm Merge(arr, low, mid, high):
    Input: Array arr with sorted subarrays arr[low..mid] and arr[mid+1..high]
    Output: Subarray arr[low..high] merged into sorted order

    n1 = mid - low + 1
    n2 = high - mid
    create temporary arrays L[0..n1-1] and R[0..n2-1]

    for i = 0 to n1 - 1 do
        L[i] = arr[low + i]
    for j = 0 to n2 - 1 do
        R[j] = arr[mid + 1 + j]

    i = 0, j = 0, k = low
    while i < n1 and j < n2 do
        increment comparison_count
        if compare(L[i], R[j]) <= 0 then
            arr[k] = L[i]
            i = i + 1
        else
            arr[k] = R[j]
            j = j + 1
        k = k + 1

    // Copy remaining elements
    while i < n1 do
        arr[k] = L[i]
        i = i + 1
        k = k + 1

    while j < n2 do
        arr[k] = R[j]
        j = j + 1
        k = k + 1
```

---

## 8. Recursive Splitting and Merging Process

The algorithm operates in two continuous phases:
1. **Decomposition (Top-Down Splitting):**
   The initial problem of size $n$ is split at index $\lfloor(low + high)/2\rfloor$. This divides $arr[0..n-1]$ into $arr[0..\lfloor(n-1)/2\rfloor]$ and $arr[\lfloor(n-1)/2\rfloor+1..n-1]$. This process continues recursively until subarrays contain a single record ($low == high$). No data swapping occurs during this phase.

2. **Composition (Bottom-Up Merging):**
   Once the base case is reached, recursion unrolls. The `Merge` routine takes two already-sorted adjacent lists and merges them using a two-pointer technique into an auxiliary buffer, which is then copied back into the primary array. Because the algorithm prioritizes elements from the left subarray when keys are equal (`cmp <= 0`), stability is strictly preserved.

---

## 9. Recursion Tree Explanation

The **Recursion Tree Method** is an analytical and visual technique used to solve recurrence relations.

```
Level 0:                         [   T(n)   ]                     Work = c*n
                                /            \
Level 1:                 [ T(n/2) ]        [ T(n/2) ]             Work = 2 * c*(n/2) = c*n
                         /        \        /        \
Level 2:             [T(n/4)]  [T(n/4)]  [T(n/4)]  [T(n/4)]       Work = 4 * c*(n/4) = c*n
                       ...       ...       ...       ...
Level log₂(n):       [T(1)] [T(1)] ... [T(1)] [T(1)]              Work = n * c*1 = c*n
```

### Analysis:
- **Tree Depth / Height:** Because the problem size is halved at each step, the depth from root (depth 0) to leaf is $\log_2 n$.
- **Cost per Level:** At each level $i$, there are $2^i$ subproblems, each doing work proportional to $n / 2^i$. The total work done at each level is $2^i \times c(n / 2^i) = cn$.
- **Total Cost:** Multiplying the work per level ($cn$) by the number of levels ($\log_2 n + 1$) yields total work $cn(\log_2 n + 1) = \mathcal{O}(n \log n)$.

In MergeFlow, every node in the tree is interactively rendered with its recursion depth ($D$), index range, record count, and actual input values.

---

## 10. Time and Space Complexity

| Metric | Complexity | Explanation |
| :--- | :--- | :--- |
| **Best-Case Time** | $\mathcal{O}(n \log n)$ | Splitting is unconditional; merging two lists of size $n/2$ requires between $n/2$ and $n-1$ comparisons regardless of initial order. |
| **Average-Case Time**| $\mathcal{O}(n \log n)$ | Expected case over random permutations; matches theoretical lower bound for comparison sorts. |
| **Worst-Case Time** | $\mathcal{O}(n \log n)$ | Interleaved keys require the maximum $n - 1$ comparisons per merge step, still yielding $c \cdot n \log n$. |
| **Auxiliary Space** | $\mathcal{O}(n)$ | Merging requires buffer memory proportional to the subarray size being merged. |
| **Recursion Depth** | $\mathcal{O}(\log n)$ | The balanced binary recursion tree reaches a maximum call stack depth of $\lceil \log_2 n \rceil$. |

---

## 11. Description of Implemented Modules

1. **User Interface Module (`index.html` CSS/DOM):** Dark dashboard themed with green accents, housing the overview hero, metrics cards, upload dropzone, sort workbench, results table, interactive recursion tree SVG canvas, and activity log.
2. **File Ingestion & RFC-4180 Parser:** Tokenizes raw text and CSV records, handling quoted newlines, escaped quotes, and automated column header detection.
3. **Merge Sort Engine:** Recursive sorting module keeping track of operational counters (comparisons, recursive calls, merge invocations, record shifts).
4. **Interactive Recursion Tree Visualizer:** Constructs node coordinates dynamically and generates responsive SVG elements with hover states and click inspection handlers.
5. **Activity Feed Generator:** Records discrete events (splits, base case arrivals, merges, completions) into a structured audit log.
6. **Data Export & Audit Reporter:** Encodes sorted data into downloadable CSV/TXT files and serializes an evaluation report as formatted JSON.

---

## 12. Application States and Screens

- **State 1: Initial Empty / Demo Ready State:** Displays dashboard overview with loaded sample data, ready metrics, and interactive controls.
- **State 2: Sorting Execution:** Visual progress animation while executing Merge Sort on the main thread with high-resolution performance timers (`performance.now()`).
- **State 3: Results Display:** Paginated results table with dynamic search filtering and sorting direction indicator.
- **State 4: Tree Inspection:** Interactive selection of nodes on the SVG canvas showing segment details, recursion depth, and subarray elements.
- **State 5: Export:** Triggered export downloads for formatted sorted datasets and JSON audit reports.

---

## 13. Test Cases and Verification Results

| # | Test Case Description | Input Data | Expected Result | Actual Result | Status |
| :-: | :--- | :--- | :--- | :--- | :-: |
| **1** | PDF Worked Numerical Example | `310, 285, 179, 652, 351, 423, 861, 254, 450, 520` | `179, 254, 285, 310, 351, 423, 450, 520, 652, 861` | Exactly matches expected list; 9 merges, 19 calls | **PASSED** |
| **2** | Already-Sorted Input | `10, 20, 30, 40, 50` | `10, 20, 30, 40, 50` | Preserved identical order without corruption | **PASSED** |
| **3** | Reverse-Sorted Input | `50, 40, 30, 20, 10` | `10, 20, 30, 40, 50` | Correctly reversed to ascending order | **PASSED** |
| **4** | Duplicate Values & Stability | `[Apple, 1], [Banana, 1], [Apple, 2], [Cherry, 1], [Apple, 3]` | Apple rows must strictly preserve relative order `1, 2, 3` | Apple items maintained exact original order: `1, 2, 3` | **PASSED** |
| **5** | Empty Input Handling | `""` (Empty string) | Safe exit, 0 comparisons, empty table | Handled safely without runtime exceptions | **PASSED** |
| **6** | Single Element Base Case | `[42]` | Immediately returns; 0 comparisons, depth 0 | Returned unchanged; 0 comparisons, 1 call | **PASSED** |
| **7** | Negative and Decimal Numbers | `3.14, -10.5, 0, -2, 100.25, 2.718` | `-10.5, -2, 0, 2.718, 3.14, 100.25` | Sorted correctly by numeric value | **PASSED** |
| **8** | CSV Multi-column & Quoted Commas | `"Everything, Everywhere",2022`, `"He said ""Hello""",2020` | Rows intact, commas in quotes preserved | Full rows preserved; quotes unescaped/escaped correctly | **PASSED** |
| **9** | Log Timestamps Chronological Sort | Out-of-order ISO server logs | Chronological timestamp order | Oldest logs placed first, line text intact | **PASSED** |
| **10**| Descending Direction | `10, 50, 30, 20, 40` (descending) | `50, 40, 30, 20, 10` | Output accurately sorted high to low | **PASSED** |
| **11**| Metric Accuracy Verification | 8 elements ($n = 2^3$) | Calls: 15, Merges: 7, Max Depth: 3 | Calls: 15, Merges: 7, Max Depth: 3 | **PASSED** |
| **12**| Tree Node Count Check | $n = 4$ elements | Total nodes = 7, Root depth = 0 | Exact tree matches 7 nodes, depth 2 | **PASSED** |
| **13**| File Export Verification | Sample movies CSV & Run report | Valid RFC CSV and parsable JSON | Downloaded files valid and matching dataset | **PASSED** |
| **14**| Malformed / Missing Keys | Mixed alphanumeric strings and numbers | Handled using defined fallback without crashing | All records retained and sorted gracefully | **PASSED** |
| **15**| Large Dataset Scaling | 1,000 randomized records | Sorted in $\le 10$ levels in $< 500$ ms | Sorted in 10 levels in $\approx 22$ ms | **PASSED** |

---

## 14. Limitations
1. **Single-Threaded Browser Scope:** Merge Sort runs on the main browser thread. Files with hundreds of thousands of lines ($> 50 \text{ MB}$) can cause brief UI latency.
2. **Visual Truncation on Large Displays:** When $n > 64$, displaying every individual node would overwhelm screen real estate. The visualizer intelligently caps rendered tree levels to preserve readability while maintaining exact underlying metric counters.

---

## 15. Conclusion
The **MergeFlow File & Log Sorter Tool** successfully fulfills all requirements of the Group G1 ISA assessment. The tool accurately implements top-down recursive Merge Sort strictly per reference academic notes, provides transparent empirical validation of $O(n \log n)$ comparison scaling, and renders an interactive recursion tree method diagram. Its zero-dependency, fully local architecture guarantees effortless evaluation during laboratory assessments and presentations, while its GitHub, Vercel, and Render readiness demonstrates modern production standards.
