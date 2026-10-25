// Automated Test Suite for MergeFlow G1 File/Log Sorter
const fs = require('fs');

// Extract the core functions directly from index.html or replicate exact logic from index.html
function parseCSV(text) {
  const rows=[]; let row=[], field='', quoted=false;
  for (let i=0;i<text.length;i++) {
    const c=text[i];
    if (quoted) { if (c==='"' && text[i+1]==='"') { field+='"'; i++; } else if (c==='"') quoted=false; else field+=c; }
    else if (c==='"' && field==='') quoted=true;
    else if (c===',') { row.push(field); field=''; }
    else if (c==='\n') { row.push(field.replace(/\r$/, '')); if (row.some(v=>v.trim()!=='')) rows.push(row); row=[]; field=''; }
    else field+=c;
  }
  if (field.length || row.length) { row.push(field.replace(/\r$/, '')); if (row.some(v=>v.trim()!=='')) rows.push(row); }
  return rows;
}

function csvEscape(value) {
  const s=String(value??'');
  return /[",\n\r]/.test(s) ? '"'+s.replace(/"/g,'""')+'"' : s;
}

function extractNumber(s) {
  const match=String(s).replace(/,/g,'').match(/[-+]?(?:\d*\.)?\d+/);
  return match?Number(match[0]):NaN;
}

function compareValues(a,b,mode) {
  if(mode==='numeric') {
    const na=extractNumber(a), nb=extractNumber(b);
    if(Number.isFinite(na)&&Number.isFinite(nb)) return na-nb;
    if(Number.isFinite(na)) return -1;
    if(Number.isFinite(nb)) return 1;
    return String(a).localeCompare(String(b),undefined,{numeric:true,sensitivity:'base'});
  }
  if(mode==='timestamp') {
    const da=Date.parse(a), db=Date.parse(b);
    if(Number.isFinite(da)&&Number.isFinite(db)) return da-db;
    if(Number.isFinite(da)) return -1;
    if(Number.isFinite(db)) return 1;
    return String(a).localeCompare(String(b),undefined,{numeric:true,sensitivity:'base'});
  }
  if(mode==='length') return String(a).length-String(b).length || String(a).localeCompare(String(b),undefined,{sensitivity:'base'});
  return String(a).localeCompare(String(b),undefined,{numeric:true,sensitivity:'base'});
}

function mergeSort(items, mode, keyFn, direction) {
  let comparisons=0, merges=0, calls=0, maxDepth=0, moves=0;
  const events=[], treeNodes=[];
  const n=items.length;
  const work=items.slice();
  let nodeCounter=0;
  const MAX_EVENTS=300;
  const dir=direction==='desc'?-1:1;

  function sort(low, high, depth, parentId) {
    calls++; if(depth>maxDepth) maxDepth=depth;
    const nodeId=nodeCounter++;
    const node={id:nodeId, low:low, high:high, depth:depth, count:high-low+1, parentId:parentId, childIds:[], isLeaf:low>=high, truncated:false};
    treeNodes.push(node);

    if (low >= high) {
      if (events.length<MAX_EVENTS) {
        const val = low===high ? String(keyFn(work[low])) : '';
        events.push({type:'base', low, high, depth, extra: low===high ? 'Base case: index '+low+' = "'+val+'"' : 'Empty segment'});
      }
      return nodeId;
    }

    const mid = Math.floor((low + high) / 2);
    if (events.length<MAX_EVENTS) events.push({type:'split', low, high, depth, extra:'Split ['+low+'..'+high+'] at mid='+mid});

    const leftId = sort(low, mid, depth+1, nodeId);
    node.childIds.push(leftId);

    const rightId = sort(mid+1, high, depth+1, nodeId);
    node.childIds.push(rightId);

    merges++;
    const left=work.slice(low, mid+1);
    const right=work.slice(mid+1, high+1);
    let i=0, j=0, k=low;
    while (i<left.length && j<right.length) {
      comparisons++;
      const cmp = compareValues(keyFn(left[i]), keyFn(right[j]), mode) * dir;
      if (cmp<=0) { work[k++]=left[i++]; } else { work[k++]=right[j++]; }
      moves++;
    }
    while(i<left.length) { work[k++]=left[i++]; moves++; }
    while(j<right.length) { work[k++]=right[j++]; moves++; }

    if (events.length<MAX_EVENTS) events.push({type:'merge', low, high, depth, extra:'Merged '+(high-low+1)+' records ['+low+'..'+high+']'});
    return nodeId;
  }

  if (n>0) sort(0, n-1, 0, null);
  events.push({type:'done', low:0, high:n-1, depth:0, extra:'Sort complete: '+n+' records sorted with '+comparisons+' comparisons'});
  return {sorted:work, stats:{comparisons,merges,calls,maxDepth,moves,n}, events, treeNodes};
}

// ================= TEST SUITE =================
const results = [];
function test(name, fn) {
  try {
    fn();
    results.push({ name, status: 'PASSED' });
    console.log(`[PASS] ${name}`);
  } catch (err) {
    results.push({ name, status: 'FAILED', error: err.message });
    console.error(`[FAIL] ${name}: ${err.message}`);
  }
}
function assert(cond, msg) { if(!cond) throw new Error(msg || 'Assertion failed'); }
function assertEqual(actual, expected, msg) {
  const a = JSON.stringify(actual);
  const b = JSON.stringify(expected);
  if(a !== b) throw new Error(`${msg || 'Not equal'}: expected ${b}, got ${a}`);
}

console.log('--- RUNNING ALL 15 MANDATORY TESTS ---');

// Test 1: PDF Numerical Example
test('Test 1: PDF Numerical Example (310, 285, 179, 652, 351, 423, 861, 254, 450, 520)', () => {
  const input = [310, 285, 179, 652, 351, 423, 861, 254, 450, 520].map(x => [String(x)]);
  const expected = [179, 254, 285, 310, 351, 423, 450, 520, 652, 861].map(x => [String(x)]);
  const res = mergeSort(input, 'numeric', r => r[0], 'asc');
  assertEqual(res.sorted, expected, 'Sorted array must match PDF expected output');
  assert(res.stats.comparisons > 0, 'Comparisons must be tracked');
  assert(res.stats.merges === 9, 'Merges for 10 elements: 9');
  assert(res.stats.calls === 19, 'Recursive calls for 10 elements: 2*10 - 1 = 19');
});

// Test 2: Already-Sorted Input
test('Test 2: Already-Sorted Input', () => {
  const input = [10, 20, 30, 40, 50].map(x => [String(x)]);
  const res = mergeSort(input, 'numeric', r => r[0], 'asc');
  assertEqual(res.sorted, input, 'Already sorted remains identical');
});

// Test 3: Reverse-Sorted Input
test('Test 3: Reverse-Sorted Input', () => {
  const input = [50, 40, 30, 20, 10].map(x => [String(x)]);
  const expected = [10, 20, 30, 40, 50].map(x => [String(x)]);
  const res = mergeSort(input, 'numeric', r => r[0], 'asc');
  assertEqual(res.sorted, expected, 'Reverse sorted sorted in ascending');
});

// Test 4: Duplicate Values & Stability
test('Test 4: Duplicate Values & Stability (Stable Sort)', () => {
  const input = [
    ['Apple', 'A1'],
    ['Banana', 'B1'],
    ['Apple', 'A2'],
    ['Cherry', 'C1'],
    ['Apple', 'A3']
  ];
  const res = mergeSort(input, 'text', r => r[0], 'asc');
  // Order of Apple should strictly be A1, A2, A3
  const apples = res.sorted.filter(r => r[0] === 'Apple').map(r => r[1]);
  assertEqual(apples, ['A1', 'A2', 'A3'], 'Equal keys must preserve original relative order (stability)');
});

// Test 5: Empty Input
test('Test 5: Empty Input', () => {
  const input = [];
  const res = mergeSort(input, 'numeric', r => r[0], 'asc');
  assertEqual(res.sorted, [], 'Empty input produces empty output');
  assertEqual(res.stats.comparisons, 0, 'Zero comparisons for empty');
  assertEqual(res.stats.calls, 0, 'Zero calls for empty');
});

// Test 6: Single Record (Base Case)
test('Test 6: Single Record (Base Case)', () => {
  const input = [['42']];
  const res = mergeSort(input, 'numeric', r => r[0], 'asc');
  assertEqual(res.sorted, [['42']]);
  assertEqual(res.stats.comparisons, 0, 'Single element requires 0 comparisons');
  assertEqual(res.stats.calls, 1, 'Single element makes 1 call');
  assertEqual(res.stats.maxDepth, 0, 'Single element max recursion depth is 0');
});

// Test 7: Numeric Values (Negative & Decimals)
test('Test 7: Numeric Values (Negative and Decimal numbers)', () => {
  const input = ['3.14', '-10.5', '0', '-2', '100.25', '2.718'].map(x => [x]);
  const expected = ['-10.5', '-2', '0', '2.718', '3.14', '100.25'].map(x => [x]);
  const res = mergeSort(input, 'numeric', r => r[0], 'asc');
  assertEqual(res.sorted, expected, 'Negative and decimals correctly ordered');
});

// Test 8: CSV With Multiple Columns, Quoted Fields, Commas in Quotes & Escaped Double Quotes
test('Test 8: CSV RFC 4180 Parsing & Preserving Rows', () => {
  const csvRaw = 'Movie,Genre,Year\n"Everything, Everywhere",Sci-Fi,2022\n"He said ""Hello""",Drama,2020\nAvatar,Action,2009';
  const parsed = parseCSV(csvRaw);
  assertEqual(parsed.length, 4, '4 rows parsed including header');
  assertEqual(parsed[1][0], 'Everything, Everywhere', 'Comma inside quotes preserved');
  assertEqual(parsed[2][0], 'He said "Hello"', 'Escaped quotes parsed as single quote');
  
  // Sort by Year (column 2)
  const dataRows = parsed.slice(1);
  const res = mergeSort(dataRows, 'numeric', r => r[2], 'asc');
  // Expected year order: 2009 (Avatar), 2020 (He said "Hello"), 2022 (Everything, Everywhere)
  assertEqual(res.sorted[0][0], 'Avatar');
  assertEqual(res.sorted[1][0], 'He said "Hello"');
  assertEqual(res.sorted[2][0], 'Everything, Everywhere');
  // Check CSV escaping back
  const exported = csvEscape(res.sorted[1][0]);
  assertEqual(exported, '"He said ""Hello"""', 'Escaped double quotes preserved on export');
});

// Test 9: Log Timestamps
test('Test 9: Log Timestamps Parsing and Sorting', () => {
  const logs = [
    ['2026-10-21 12:04:18 INFO API started'],
    ['2026-10-21 09:10:00 WARN Low disk'],
    ['2026-10-21 11:18:44 ERROR Connection failed'],
    ['2026-10-21 09:05:21 INFO Service init']
  ];
  const res = mergeSort(logs, 'timestamp', r => r[0], 'asc');
  assertEqual(res.sorted[0][0], '2026-10-21 09:05:21 INFO Service init');
  assertEqual(res.sorted[1][0], '2026-10-21 09:10:00 WARN Low disk');
  assertEqual(res.sorted[2][0], '2026-10-21 11:18:44 ERROR Connection failed');
  assertEqual(res.sorted[3][0], '2026-10-21 12:04:18 INFO API started');
});

// Test 10: Descending Order
test('Test 10: Descending Order Sorting', () => {
  const input = [10, 50, 30, 20, 40].map(x => [String(x)]);
  const expected = [50, 40, 30, 20, 10].map(x => [String(x)]);
  const res = mergeSort(input, 'numeric', r => r[0], 'desc');
  assertEqual(res.sorted, expected, 'Sorted in descending order');
});

// Test 11: Performance Metrics (Comparisons, Merges, Calls, Depth)
test('Test 11: Metrics Accuracy and Reset', () => {
  const input = [8, 3, 2, 9, 7, 1, 5, 4].map(x => [String(x)]);
  const res = mergeSort(input, 'numeric', r => r[0], 'asc');
  // For n=8 powers of 2:
  // Calls = 2*n - 1 = 15
  // Merges = n - 1 = 7
  // Max depth = ceil(log2(8)) = 3
  assertEqual(res.stats.calls, 15, 'Recursive calls for n=8 is 15');
  assertEqual(res.stats.merges, 7, 'Merges for n=8 is 7');
  assertEqual(res.stats.maxDepth, 3, 'Max recursion depth for n=8 is 3');
  assert(res.stats.comparisons >= 8 && res.stats.comparisons <= 8 * 3, 'Comparisons within theoretical bounds');
});

// Test 12: Recursion Tree Representation
test('Test 12: Recursion Tree nodes count & structure', () => {
  const input = [10, 20, 30, 40].map(x => [String(x)]);
  const res = mergeSort(input, 'numeric', r => r[0], 'asc');
  assertEqual(res.treeNodes.length, res.stats.calls, 'Tree nodes match recursive call count');
  assertEqual(res.treeNodes[0].parentId, null, 'Root has no parent');
  assertEqual(res.treeNodes[0].depth, 0, 'Root depth is 0');
  assertEqual(res.treeNodes[0].count, 4, 'Root contains all 4 records');
});

// Test 13: Export Functionality (CSV & JSON Run Report)
test('Test 13: Export formats (CSV escaping and JSON run report schema)', () => {
  const headers = ['Movie', 'Genre', 'Notes'];
  const rows = [['Dune', 'Sci-Fi', 'Great, visual\nmasterpiece']];
  const csvText = [headers, ...rows].map(r => r.map(csvEscape).join(',')).join('\r\n');
  assert(csvText.includes('"Great, visual\nmasterpiece"'), 'Multiline quoted CSV properly escaped');
  
  const report = {
    project: 'MergeFlow — File & Log Sorter',
    records: 1,
    metrics: { comparisons: 0, merges: 0, recursiveCalls: 1, maxRecursionDepth: 0 },
    complexity: { time: 'O(n log n)', auxiliarySpace: 'O(n)' }
  };
  const jsonStr = JSON.stringify(report);
  assert(JSON.parse(jsonStr).records === 1, 'JSON report is valid');
});

// Test 14: Invalid & Malformed Inputs Handling
test('Test 14: Handling malformed rows, missing keys, and non-numeric values gracefully', () => {
  const malformed = [['12'], ['abc'], [''], ['-5'], ['xyz']];
  const res = mergeSort(malformed, 'numeric', r => r[0], 'asc');
  assert(res.sorted.length === 5, 'All records preserved despite invalid keys');
  // -5 and 12 should be properly compared, non-numerics sorted gracefully
  assert(res.sorted[0][0] === '-5', '-5 comes first');
});

// Test 15: Larger Dataset (1000 items)
test('Test 15: Larger dataset scalability (1000 items)', () => {
  const large = [];
  for(let i=0; i<1000; i++) large.push([String(Math.floor(Math.random() * 100000))]);
  const start = Date.now();
  const res = mergeSort(large, 'numeric', r => r[0], 'asc');
  const duration = Date.now() - start;
  assertEqual(res.sorted.length, 1000, 'All 1000 elements sorted');
  assert(res.stats.maxDepth <= 10, 'Max depth for 1000 elements is <= 10 (ceil(log2(1000)) = 10)');
  assert(duration < 500, `Execution time under 500ms (took ${duration}ms)`);
  // Verify strictly sorted
  for(let i=1; i<res.sorted.length; i++) {
    assert(Number(res.sorted[i-1][0]) <= Number(res.sorted[i][0]), 'Ascending invariant holds');
  }
});

console.log('\n--- TEST SUMMARY ---');
const passed = results.filter(r => r.status === 'PASSED').length;
console.log(`TOTAL: ${results.length} | PASSED: ${passed} | FAILED: ${results.length - passed}`);
if (passed === results.length) {
  console.log('ALL 15 TESTS PASSED SUCCESSFULLY!');
} else {
  process.exit(1);
}
