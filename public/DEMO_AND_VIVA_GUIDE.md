# MERGEFLOW — LIVE DEMO & VIVA GUIDE

> **Academic Project Guide for ISA Viva & Demonstration**  
> **Group G1:** Merge Sort + Recursion Tree Method  
> **Target Audience:** Third Year Computer Engineering Examiner / Professor  
> **Repository:** [https://github.com/PixelNinja420/Merge-Sort](https://github.com/PixelNinja420/Merge-Sort)

---

## 1. Fast 2–3 Minute Demonstration Script

Follow this exact sequence during your live presentation for maximum impact:

### Step 1: Launch & Introduction (30 seconds)
> *"Good morning, Professor. For our G1 ISA Mini-Project, we built **MergeFlow**, an educational and practical File and Log Sorter based on **Merge Sort** and the **Recursion Tree Method**.*
>
> *Our design priority was accessibility and engineering rigor: this tool runs 100% locally by opening `index.html` in any browser, requiring no server, no internet, and zero external libraries. It is also version-controlled on GitHub and deployed on Vercel and Render."*

### Step 2: Show the Numerical Example from Class Notes (45 seconds)
1. In the workbench, click the **"PDF Example"** button.
2. Point to the input preview showing the 10 numbers:  
   `310, 285, 179, 652, 351, 423, 861, 254, 450, 520`.
3. Click **"Sort with Merge Sort"**.
4. Show the sorted output:  
   `179, 254, 285, 310, 351, 423, 450, 520, 652, 861`.
> *"Here we have loaded the exact worked numerical example from our handwritten lecture notes. In a fraction of a millisecond, MergeFlow sorts all 10 records. Notice the metrics above: exactly 9 merge operations, 19 recursive calls, and a max recursion depth of 4 levels."*

### Step 3: Explain the Recursion Tree & Activity Feed (45 seconds)
1. Scroll down to the **Recursion Tree Explorer**.
2. Click the root node (Depth 0).
3. Click a child node on Depth 1 or Depth 2.
4. Point out the bottom inspection panel and the Activity Feed on the left.
> *"Here is our core topic: the Recursion Tree Method. The root node represents the entire array of 10 items. When we click any node, the inspector shows the exact indices, depth, and the actual values at that stage. At the bottom levels, we reach our base cases where each subarray contains 1 record. The Activity Feed next to it traces every split and merge chronologically."*

### Step 4: Demonstrate CSV Multi-Column Sorting & Stability (30 seconds)
1. Scroll up and click **"Sample CSV"**.
2. Show that it has columns: *Movie, Genre, Rating, Year, Tickets Sold*.
3. Change the column dropdown to **Year**.
4. Click **"Sort with Merge Sort"**.
> *"Here we sort a CSV file by 'Year'. Notice that every other column—Movie, Genre, and Tickets—moves together with its row without corrupting data. Notice also that Merge Sort is stable: movies released in the same year preserve their relative original order."*

### Step 5: Exporting & Conclusion (15 seconds)
1. Click **"Download run report"** or **"Export sorted file"**.
> *"Finally, students can export the sorted CSV or download a complete JSON run report documenting the comparison counters, merge counts, and complexity proof."*

---

## 2. Key Explanations to Practice

### How to Explain the Recursion Tree
> *"Professor, the recursion tree visually models the recurrence relation $T(n) = 2T(n/2) + \Theta(n)$. The root has size $n$. At depth 1, the problem is divided into two halves of size $n/2$. This binary division continues until depth $\log_2(n)$, where each subproblem has size 1 (the base case). The total work done across all nodes at each horizontal level equals $cn$, and there are $\log_2(n) + 1$ levels, proving why the time complexity is $\mathcal{O}(n \log n)$."*

### How to Explain the Comparison Counter
> *"Our comparison counter is not a static formula or an estimate. It is incremented directly inside the `while` loop of our `Merge` function every time two record keys are compared. For an input of size 10, the comparisons are bounded between $n/2$ and $n-1$ per merge step. This shows students the empirical difference between theoretical asymptotic bounds and actual operations on a given input."*

---

## 3. Top 15 Viva Questions and Concise Answers

### Q1: What is the divide-and-conquer strategy?
**Answer:** It is an algorithmic paradigm that breaks a problem into smaller subproblems of the same type, solves them recursively, and combines their solutions to form the solution to the original problem.

### Q2: What is the recurrence relation for Merge Sort?
**Answer:** $T(n) = 2T(n/2) + \Theta(n)$ for $n > 1$, with $T(1) = \Theta(1)$. The $2T(n/2)$ represents sorting the two halves, and $\Theta(n)$ is the linear work of merging them.

### Q3: What is the base case of Merge Sort?
**Answer:** The base case occurs when $low \ge high$, meaning the subarray contains zero or one element. A single element is already sorted by definition, so the recursive call simply returns.

### Q4: Why is mid calculated as $\lfloor(low + high) / 2\rfloor$?
**Answer:** This evenly partitions the subarray into two halves of sizes $\lceil n/2 \rceil$ and $\lfloor n/2 \rfloor$, ensuring balanced subtrees and guaranteeing a recursion depth of $\mathcal{O}(\log n)$.

### Q5: What is the best, average, and worst-case time complexity of Merge Sort?
**Answer:** All three cases are $\mathcal{O}(n \log n)$. This is because Merge Sort unconditionally divides the array into halves and always performs linear merging work regardless of initial element ordering.

### Q6: What is the auxiliary space complexity of Merge Sort?
**Answer:** $\mathcal{O}(n)$. Merging two sorted halves requires a temporary buffer or array to hold elements before copying them back to the original array.

### Q7: What does "stable sorting" mean, and is Merge Sort stable?
**Answer:** A sorting algorithm is stable if records with identical sorting keys appear in the output in the same relative order as in the input. Merge Sort is stable because when $L[i] == R[j]$, we select $L[i]$ from the left half first (`cmp <= 0`).

### Q8: How many recursive calls are made for an array of $n$ elements?
**Answer:** Exactly $2n - 1$ recursive calls (for $n \ge 1$), corresponding to the total number of nodes in a full binary recursion tree with $n$ leaves. For our 10-element PDF example, $2(10) - 1 = 19$ calls.

### Q9: How many merge operations occur for an array of $n$ elements?
**Answer:** Exactly $n - 1$ merge operations. Each merge combines two segments into one, reducing the number of distinct segments from $n$ to 1. For $n = 10$, there are $10 - 1 = 9$ merges.

### Q10: What is the maximum recursion depth for an array of size $n$?
**Answer:** $\lceil \log_2 n \rceil$. For $n = 10$, $\log_2(10) \approx 3.32$, so the maximum depth is 4 levels (levels 0, 1, 2, 3, 4).

### Q11: Why is Merge Sort preferred for sorting linked lists and large external files?
**Answer:** 
1. For linked lists, merging does not require $\mathcal{O}(n)$ auxiliary memory because pointers can be redirected in $\mathcal{O}(1)$ space.
2. For external files (External Merge Sort), sequential disk access during merge is much faster than random disk access.

### Q12: How does your tool handle CSV rows with multiple columns?
**Answer:** The CSV parser extracts rows into arrays of cell values. When the user selects a sort column, that cell is used as the key, but the entire row array is swapped and moved as an atomic unit, preventing data corruption.

### Q13: How does your tool handle commas inside quoted CSV fields?
**Answer:** It uses an RFC-4180 state machine. When inside an unclosed double quote (`"`), commas and line breaks are treated as literal text instead of field or row delimiters.

### Q14: How does your tool handle timestamp sorting?
**Answer:** It parses timestamp strings into epoch milliseconds using `Date.parse()`. If parsing fails, it gracefully falls back to natural alphanumeric comparison so that no data is lost or displaced.

### Q15: Why can Quick Sort be faster than Merge Sort in practice despite worse worst-case complexity?
**Answer:** Quick Sort sorts in place with $\mathcal{O}(1)$ auxiliary memory and has superior CPU cache locality with smaller constant factors, whereas Merge Sort requires allocating and copying memory to temporary arrays.
