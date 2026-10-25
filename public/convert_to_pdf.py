import os
import re
from fpdf import FPDF
from fpdf.enums import XPos, YPos

class AcademicPDF(FPDF):
    def __init__(self, doc_title):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.doc_title = doc_title
        self.set_auto_page_break(auto=True, margin=18)
        self.set_margins(16, 16, 16)

    def header(self):
        self.set_font("helvetica", "B", 8)
        self.set_text_color(100, 116, 139)
        self.cell(0, 5, "ISA MINI-PROJECT | GROUP G1: MERGE SORT & RECURSION TREE", 0, new_x=XPos.RIGHT, new_y=YPos.TOP, align="L")
        self.cell(0, 5, "DEPARTMENT OF COMPUTER ENGINEERING", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="R")
        self.set_draw_color(226, 232, 240)
        self.set_line_width(0.3)
        self.line(16, 22, 194, 22)
        self.ln(4)

    def footer(self):
        self.set_y(-14)
        self.set_draw_color(226, 232, 240)
        self.set_line_width(0.3)
        self.line(16, self.get_y(), 194, self.get_y())
        self.set_font("helvetica", "", 8)
        self.set_text_color(100, 116, 139)
        self.cell(0, 8, "MergeFlow - File & Log Sorter Tool | GitHub: PixelNinja420/Merge-Sort", 0, new_x=XPos.RIGHT, new_y=YPos.TOP, align="L")
        self.cell(0, 8, f"Page {self.page_no()}", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="R")

def clean_text(text):
    """Replace markdown math, unicode, and formatting with clean printable latin-1 text."""
    # Plain string replacements
    text = text.replace(r'\mathcal{O}', 'O')
    text = text.replace(r'\Theta', 'Theta')
    text = text.replace(r'\le', '<=')
    text = text.replace(r'\ge', '>=')
    text = text.replace(r'\approx', '~')
    text = text.replace(r'\lceil', 'ceil(')
    text = text.replace(r'\rceil', ')')
    text = text.replace(r'\lfloor', 'floor(')
    text = text.replace(r'\rfloor', ')')
    text = text.replace(r'\times', 'x')
    text = text.replace(r'\cdot', '*')
    text = text.replace(r'\log_2', 'log2')
    text = text.replace('$', '')
    text = text.replace('–', '-')
    text = text.replace('—', ' - ')
    text = text.replace('“', '"')
    text = text.replace('”', '"')
    text = text.replace('‘', "'")
    text = text.replace('’', "'")
    text = text.replace('→', '->')
    text = text.replace('↑', '(Asc)')
    text = text.replace('↓', '(Desc)')
    text = text.replace('•', '*')
    text = text.replace('≈', '~')
    text = text.replace('≥', '>=')
    text = text.replace('≤', '<=')
    text = text.replace('✓', '[PASS]')
    text = text.replace('★', '*')
    text = text.replace('👉', '->')
    text = text.replace('·', '-')
    text = text.replace('×', 'x')
    # Filter to latin-1
    return text.encode('latin-1', 'replace').decode('latin-1')

def parse_markdown_to_pdf(md_path, pdf_path, doc_title):
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    pdf = AcademicPDF(doc_title)
    pdf.add_page()
    
    in_code_block = False
    code_lines = []
    in_table = False
    table_rows = []

    def flush_table():
        nonlocal table_rows, in_table
        if not table_rows:
            in_table = False
            return
        col_count = max(len(r) for r in table_rows)
        if col_count == 0:
            in_table = False
            table_rows = []
            return
        
        avail_w = 178
        if col_count == 2:
            widths = [45, 133]
        elif col_count == 3:
            widths = [35, 35, 108]
        elif col_count == 5:
            widths = [20, 20, 45, 45, 48]
        elif col_count == 6:
            widths = [10, 42, 36, 42, 36, 12]
        else:
            w_each = avail_w / col_count
            widths = [w_each] * col_count

        pdf.set_font("helvetica", "B", 8)
        header = table_rows[0]
        pdf.set_fill_color(15, 23, 42)
        pdf.set_text_color(255, 255, 255)
        for i, cell in enumerate(header):
            w = widths[i] if i < len(widths) else 20
            clean_c = clean_text(cell)
            pdf.cell(w, 6, clean_c[:35], border=1, fill=True, align="L", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.ln(6)

        pdf.set_font("helvetica", "", 7.5)
        pdf.set_text_color(30, 41, 59)
        for row_idx, r in enumerate(table_rows[1:]):
            fill = (row_idx % 2 == 1)
            pdf.set_fill_color(248, 250, 252) if fill else pdf.set_fill_color(255, 255, 255)
            for i, cell in enumerate(r):
                w = widths[i] if i < len(widths) else 20
                clean_c = clean_text(cell)
                pdf.cell(w, 5.5, clean_c[:45], border=1, fill=fill, align="L", new_x=XPos.RIGHT, new_y=YPos.TOP)
            pdf.ln(5.5)
        
        pdf.ln(3)
        table_rows = []
        in_table = False

    def flush_code():
        nonlocal code_lines, in_code_block
        if not code_lines:
            in_code_block = False
            return
        pdf.set_font("courier", "", 7.5)
        pdf.set_fill_color(241, 245, 249)
        pdf.set_draw_color(203, 213, 225)
        pdf.set_text_color(15, 23, 42)
        for cline in code_lines:
            c_text = clean_text(cline)
            pdf.cell(178, 4.2, "  " + c_text[:95], border="LR", fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.cell(178, 1, "", border="T", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(3)
        code_lines = []
        in_code_block = False

    i = 0
    while i < len(lines):
        line = lines[i].rstrip("\r\n")

        if line.startswith("```"):
            if in_code_block:
                flush_code()
            else:
                if in_table:
                    flush_table()
                in_code_block = True
                pdf.set_draw_color(203, 213, 225)
                pdf.cell(178, 1, "", border="T", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            i += 1
            continue

        if in_code_block:
            code_lines.append(line)
            i += 1
            continue

        if line.startswith("|"):
            if re.match(r'^\|[\s\-:]+(\|[\s\-:]+)+\|?$', line):
                i += 1
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            table_rows.append(cells)
            in_table = True
            i += 1
            continue
        elif in_table:
            flush_table()

        if not line.strip():
            pdf.ln(2)
            i += 1
            continue

        if line.startswith("# "):
            pdf.ln(2)
            pdf.set_font("helvetica", "B", 14)
            pdf.set_text_color(15, 23, 42)
            pdf.multi_cell(178, 6.5, clean_text(line[2:]))
            pdf.set_draw_color(16, 185, 129)
            pdf.set_line_width(0.8)
            pdf.line(16, pdf.get_y(), 194, pdf.get_y())
            pdf.ln(3)
            i += 1
            continue

        if line.startswith("## "):
            pdf.ln(3)
            pdf.set_font("helvetica", "B", 11)
            pdf.set_text_color(15, 23, 42)
            pdf.multi_cell(178, 5.5, clean_text(line[3:]))
            pdf.set_draw_color(226, 232, 240)
            pdf.set_line_width(0.4)
            pdf.line(16, pdf.get_y(), 194, pdf.get_y())
            pdf.ln(2.5)
            i += 1
            continue

        if line.startswith("### "):
            pdf.ln(2)
            pdf.set_font("helvetica", "B", 9.5)
            pdf.set_text_color(30, 41, 59)
            pdf.multi_cell(178, 5, clean_text(line[4:]))
            pdf.ln(1)
            i += 1
            continue

        if line.startswith("> "):
            pdf.set_fill_color(240, 253, 244)
            pdf.set_draw_color(16, 185, 129)
            pdf.set_font("helvetica", "I", 8.5)
            pdf.set_text_color(6, 95, 70)
            clean_q = clean_text(line[2:].replace("**", "").replace("*", ""))
            pdf.cell(178, 5.5, "  " + clean_q[:110], border="L", fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            i += 1
            continue

        if line.startswith("---") or line.startswith("***"):
            pdf.ln(2)
            pdf.set_draw_color(226, 232, 240)
            pdf.set_line_width(0.3)
            pdf.line(16, pdf.get_y(), 194, pdf.get_y())
            pdf.ln(3)
            i += 1
            continue

        if line.strip().startswith("- ") or line.strip().startswith("* "):
            pdf.set_font("helvetica", "", 8.5)
            pdf.set_text_color(30, 41, 59)
            clean_l = clean_text(line.strip()[2:].replace("**", "").replace("*", ""))
            pdf.cell(5, 4.5, "-", 0, new_x=XPos.RIGHT, new_y=YPos.TOP, align="R")
            pdf.multi_cell(173, 4.5, " " + clean_l)
            i += 1
            continue

        num_match = re.match(r'^\s*(\d+)\.\s+(.*)$', line)
        if num_match:
            num = num_match.group(1)
            rest = clean_text(num_match.group(2).replace("**", "").replace("*", ""))
            pdf.set_font("helvetica", "B", 8.5)
            pdf.set_text_color(15, 23, 42)
            pdf.cell(6, 4.5, f"{num}.", 0, new_x=XPos.RIGHT, new_y=YPos.TOP, align="R")
            pdf.set_font("helvetica", "", 8.5)
            pdf.set_text_color(30, 41, 59)
            pdf.multi_cell(172, 4.5, " " + rest)
            i += 1
            continue

        pdf.set_font("helvetica", "", 8.5)
        pdf.set_text_color(30, 41, 59)
        clean_p = clean_text(line.replace("**", "").replace("*", "").replace("`", ""))
        pdf.multi_cell(178, 4.5, clean_p)
        i += 1

    if in_table:
        flush_table()
    if in_code_block:
        flush_code()

    pdf.output(pdf_path)
    print(f"Successfully generated {pdf_path} ({os.path.getsize(pdf_path):,} bytes)")

if __name__ == "__main__":
    docs = [
        ("COLLEGE_MINI_PROJECT_REPORT.md", "COLLEGE_MINI_PROJECT_REPORT.pdf", "College Mini-Project Report"),
        ("DEMO_AND_VIVA_GUIDE.md", "DEMO_AND_VIVA_GUIDE.pdf", "Demo and Viva Guide"),
        ("FINAL_CHANGE_SUMMARY.md", "FINAL_CHANGE_SUMMARY.pdf", "Final Change Summary & Audit")
    ]
    for md, pdf, title in docs:
        parse_markdown_to_pdf(md, pdf, title)
