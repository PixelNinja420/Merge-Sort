import os
import subprocess
import markdown

DOCS = [
    ("COLLEGE_MINI_PROJECT_REPORT.md", "COLLEGE_MINI_PROJECT_REPORT.pdf", "College Mini-Project Report"),
    ("DEMO_AND_VIVA_GUIDE.md", "DEMO_AND_VIVA_GUIDE.pdf", "Demo and Viva Guide"),
    ("FINAL_CHANGE_SUMMARY.md", "FINAL_CHANGE_SUMMARY.pdf", "Final Change Summary & Verification Audit")
]

CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
]

browser_exe = None
for p in CHROME_PATHS:
    if os.path.exists(p):
        browser_exe = p
        break

if not browser_exe:
    raise RuntimeError("Neither Chrome nor Edge executable found.")

CSS = """
@page {
    size: A4;
    margin: 18mm 16mm 18mm 16mm;
}
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.55;
    color: #1a202c;
    background: #ffffff;
    margin: 0;
    padding: 0;
}
h1 {
    font-size: 19pt;
    color: #0f172a;
    border-bottom: 2px solid #059669;
    padding-bottom: 6px;
    margin-top: 0;
    margin-bottom: 12px;
    font-weight: 800;
    letter-spacing: -0.5px;
}
h2 {
    font-size: 13pt;
    color: #0f172a;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 4px;
    margin-top: 18px;
    margin-bottom: 8px;
    font-weight: 700;
    page-break-after: avoid;
}
h3 {
    font-size: 11pt;
    color: #1e293b;
    margin-top: 14px;
    margin-bottom: 6px;
    font-weight: 700;
    page-break-after: avoid;
}
p {
    margin-top: 0;
    margin-bottom: 8px;
    text-align: justify;
}
blockquote {
    margin: 8px 0 12px 0;
    padding: 8px 14px;
    background: #f0fdf4;
    border-left: 4px solid #10b981;
    color: #065f46;
    font-size: 9.5pt;
    border-radius: 0 6px 6px 0;
}
blockquote p {
    margin: 0;
}
table {
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0 14px 0;
    font-size: 8.5pt;
    page-break-inside: avoid;
}
th, td {
    padding: 6px 8px;
    border: 1px solid #cbd5e1;
    text-align: left;
    vertical-align: top;
}
th {
    background-color: #0f172a;
    color: #ffffff;
    font-weight: 600;
}
tr:nth-child(even) {
    background-color: #f8fafc;
}
code {
    font-family: Consolas, Monaco, "Courier New", monospace;
    font-size: 8.5pt;
    background: #f1f5f9;
    color: #0f172a;
    padding: 2px 4px;
    border-radius: 4px;
    border: 1px solid #e2e8f0;
}
pre {
    background: #0f172a;
    color: #e2e8f0;
    padding: 10px 12px;
    border-radius: 6px;
    overflow-x: auto;
    font-size: 8pt;
    line-height: 1.45;
    margin: 8px 0 12px 0;
    page-break-inside: avoid;
}
pre code {
    background: transparent;
    color: inherit;
    border: none;
    padding: 0;
    font-size: inherit;
}
ul, ol {
    margin-top: 0;
    margin-bottom: 8px;
    padding-left: 20px;
}
li {
    margin-bottom: 4px;
}
hr {
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 14px 0;
}
.header-badge {
    display: inline-block;
    background: #ecfdf5;
    color: #047857;
    font-size: 8pt;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 4px;
    border: 1px solid #a7f3d0;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.footer-note {
    margin-top: 25px;
    padding-top: 8px;
    border-top: 1px solid #e2e8f0;
    color: #64748b;
    font-size: 8pt;
    display: flex;
    justify-content: space-between;
}
"""

for md_file, pdf_file, title in DOCS:
    if not os.path.exists(md_file):
        print(f"Skipping {md_file} (not found)")
        continue

    with open(md_file, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Convert markdown to html
    body_html = markdown.markdown(md_text, extensions=['tables', 'fenced_code', 'nl2br'])

    full_html = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<title>{title}</title>
<style>{CSS}</style>
</head>
<body>
<div class="header-badge">ISA Mini-Project · Group G1 · Third Year Computer Engineering</div>
{body_html}
<div class="footer-note">
    <span>MergeFlow: File & Log Sorter</span>
    <span>Department of Computer Engineering</span>
</div>
</body>
</html>"""

    temp_html = f"__temp_{pdf_file}.html"
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(full_html)

    abs_temp = os.path.abspath(temp_html)
    abs_pdf = os.path.abspath(pdf_file)

    cmd = [
        browser_exe,
        "--headless",
        "--disable-gpu",
        f"--print-to-pdf={abs_pdf}",
        "--no-pdf-header-footer",
        abs_temp
    ]

    print(f"Generating {pdf_file} using {os.path.basename(browser_exe)}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(temp_html):
        os.remove(temp_html)

    if os.path.exists(abs_pdf) and os.path.getsize(abs_pdf) > 0:
        print(f"Successfully created {pdf_file} ({os.path.getsize(abs_pdf):,} bytes)")
    else:
        print(f"Error creating {pdf_file}: {res.stderr}")
