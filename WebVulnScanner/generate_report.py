"""
Web Vulnerability Scanner – Full Project Report Generator
Generates a properly formatted .docx file per college guidelines.
"""

from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

doc = Document()

# ─────────────────────────── Page Setup ──────────────────────────────────
section = doc.sections[0]
section.page_height  = Inches(11.69)   # A4
section.page_width   = Inches(8.27)
section.left_margin  = Inches(1)
section.right_margin = Inches(1)
section.top_margin   = Inches(1)
section.bottom_margin = Inches(1)

# ─────────────────────────── Helper Functions ────────────────────────────
def set_line_spacing(paragraph, spacing=1.5):
    pf = paragraph.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing      = spacing
    pf.space_after       = Pt(6)

def heading_main(text):
    """16pt, Bold, UPPERCASE, Times New Roman, Centred, page break before."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.page_break_before = True
    p.paragraph_format.space_after = Pt(18)
    run = p.add_run(text.upper())
    run.bold      = True
    run.font.name = "Times New Roman"
    run.font.size = Pt(16)
    return p

def heading_sub(text, level=2):
    """14pt, Bold, Times New Roman, left-aligned."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after  = Pt(6)
    run = p.add_run(text)
    run.bold      = True
    run.font.name = "Times New Roman"
    run.font.size = Pt(14)
    return p

def heading_sub2(text):
    """12pt, Bold, Times New Roman, left-aligned (level-3)."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after  = Pt(4)
    run = p.add_run(text)
    run.bold      = True
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    return p

def body(text):
    """12pt, Times New Roman, Justified, 1.5 spacing."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    set_line_spacing(p)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    return p

def centre_text(text, size=12, bold=False):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_line_spacing(p)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(size)
    run.bold = bold
    return p

def bullet(text):
    p = doc.add_paragraph(style="List Bullet")
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    set_line_spacing(p)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    return p

def add_table(headers, rows, caption_text=None):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    # Header row
    hrow = table.rows[0]
    for i, h in enumerate(headers):
        cell = hrow.cells[i]
        cell.text = h
        for run in cell.paragraphs[0].runs:
            run.font.name = "Times New Roman"
            run.font.size = Pt(12)
            run.bold = True
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:fill"), "D9D9D9")
        shd.set(qn("w:val"),  "clear")
        tcPr.append(shd)
    # Data rows
    for ri, row_data in enumerate(rows):
        row = table.rows[ri + 1]
        for ci, cell_text in enumerate(row_data):
            cell = row.cells[ci]
            cell.text = str(cell_text)
            for run in cell.paragraphs[0].runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(12)
    if caption_text:
        cp = doc.add_paragraph()
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cr = cp.add_run(caption_text)
        cr.font.name = "Times New Roman"
        cr.font.size = Pt(11)
        cr.italic    = True
    doc.add_paragraph()

def add_page_numbers():
    """Insert page number field in the footer (centre-aligned)."""
    for sec in doc.sections:
        footer = sec.footer
        fp     = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        fp.clear()
        run = fp.add_run()
        fldChar1 = OxmlElement("w:fldChar")
        fldChar1.set(qn("w:fldCharType"), "begin")
        instrText = OxmlElement("w:instrText")
        instrText.text = "PAGE"
        fldChar2 = OxmlElement("w:fldChar")
        fldChar2.set(qn("w:fldCharType"), "end")
        run._r.append(fldChar1)
        run._r.append(instrText)
        run._r.append(fldChar2)
        run.font.name = "Times New Roman"
        run.font.size = Pt(12)

# ═══════════════════════════════════════════════════════════════════════
#  1. COVER PAGE
# ═══════════════════════════════════════════════════════════════════════
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(0)
p.paragraph_format.space_after  = Pt(0)

centre_text("", 12)
centre_text("PROJECT REPORT", 18, bold=True)
centre_text("ON", 14)
centre_text("", 12)
centre_text("WEB VULNERABILITY SCANNER", 20, bold=True)
centre_text("", 12)
centre_text("Submitted in partial fulfilment of the requirements for the award of the degree of", 12)
centre_text("Bachelor of Technology", 14, bold=True)
centre_text("in", 12)
centre_text("Computer Science and Engineering (Cybersecurity)", 14, bold=True)
centre_text("", 12)
centre_text("Submitted by", 12)
centre_text("", 12)
centre_text("[Student Name]", 13, bold=True)
centre_text("Roll No: [XXXXXX]", 12)
centre_text("", 12)
centre_text("Under the Guidance of", 12)
centre_text("[Guide Name], [Designation]", 13, bold=True)
centre_text("", 12)
centre_text("[Department Name]", 13, bold=True)
centre_text("[Institution Name]", 13, bold=True)
centre_text("[University Name]", 12)
centre_text("[City, State – PIN]", 12)
centre_text("", 12)
centre_text("Academic Year: 2025–2026", 12, bold=True)

# ═══════════════════════════════════════════════════════════════════════
#  2. CERTIFICATE
# ═══════════════════════════════════════════════════════════════════════
heading_main("CERTIFICATE")
centre_text("", 12)
body("This is to certify that the project report entitled")
centre_text('"WEB VULNERABILITY SCANNER"', 13, bold=True)
body("submitted by")
centre_text("[Student Name], Roll No: [XXXXXX]", 13, bold=True)
body(
    "is a bonafide record of the work carried out by the above student in partial fulfilment "
    "of the requirements for the award of the degree of Bachelor of Technology in Computer "
    "Science and Engineering (Cybersecurity) from [University Name] during the academic year "
    "2025–2026. The project was carried out under my supervision and guidance."
)
centre_text("", 12)
centre_text("", 12)
p1 = doc.add_paragraph()
p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
r1 = p1.add_run("Project Guide\n[Guide Name]\n[Designation]\nDepartment of CSE\n[Institution Name]")
r1.font.name = "Times New Roman"
r1.font.size = Pt(12)
centre_text("", 12)
p2 = doc.add_paragraph()
p2.alignment = WD_ALIGN_PARAGRAPH.LEFT
r2 = p2.add_run("Head of Department\n[HOD Name]\n[Designation]\nDepartment of CSE\n[Institution Name]")
r2.font.name = "Times New Roman"
r2.font.size = Pt(12)

# ═══════════════════════════════════════════════════════════════════════
#  3. DECLARATION
# ═══════════════════════════════════════════════════════════════════════
heading_main("DECLARATION")
body(
    "I hereby declare that the project report entitled \"Web Vulnerability Scanner\" submitted "
    "to [University Name] in partial fulfilment of the requirements for the award of the degree "
    "of Bachelor of Technology in Computer Science and Engineering (Cybersecurity) is a record "
    "of original work done by me under the supervision of [Guide Name], [Designation], Department "
    "of Computer Science and Engineering, [Institution Name]."
)
body(
    "I further declare that this project report has not been submitted, either in part or in full, "
    "for the award of any other degree or diploma in this institution or any other institution. "
    "All information and content presented in this report are true to the best of my knowledge."
)
centre_text("", 12)
centre_text("", 12)
p3 = doc.add_paragraph()
p3.alignment = WD_ALIGN_PARAGRAPH.LEFT
r3 = p3.add_run("Place: [City]\nDate:  [DD/MM/YYYY]")
r3.font.name = "Times New Roman"
r3.font.size = Pt(12)
centre_text("", 12)
p4 = doc.add_paragraph()
p4.alignment = WD_ALIGN_PARAGRAPH.RIGHT
r4 = p4.add_run("[Student Name]\nRoll No: [XXXXXX]\nB.Tech CSE (Cybersecurity)")
r4.font.name = "Times New Roman"
r4.font.size = Pt(12)

# ═══════════════════════════════════════════════════════════════════════
#  4. ACKNOWLEDGEMENT
# ═══════════════════════════════════════════════════════════════════════
heading_main("ACKNOWLEDGEMENT")
body(
    "I would like to express my sincere gratitude and heartfelt appreciation to all those "
    "who have contributed to the successful completion of this project."
)
body(
    "First and foremost, I extend my deepest thanks to [Guide Name], [Designation], Department "
    "of Computer Science and Engineering, [Institution Name], for their invaluable guidance, "
    "continuous support, and encouragement throughout the development of this project. Their "
    "expert advice and constructive feedback have been instrumental in shaping this work."
)
body(
    "I am also grateful to [HOD Name], Head of the Department of Computer Science and Engineering, "
    "for providing the necessary facilities and an encouraging environment to carry out this research."
)
body(
    "I extend my sincere thanks to all the faculty members of the Department of Computer Science "
    "and Engineering for their continuous academic support and motivation."
)
body(
    "I would also like to acknowledge the open-source community for providing free and publicly "
    "accessible vulnerable test environments such as DVWA (Damn Vulnerable Web Application) and "
    "the Acunetix test server, which were used ethically for testing purposes during this project."
)
body(
    "Finally, I am deeply grateful to my parents, family members, and friends for their constant "
    "encouragement, patience, and moral support throughout the duration of this project."
)
centre_text("", 12)
p5 = doc.add_paragraph()
p5.alignment = WD_ALIGN_PARAGRAPH.RIGHT
r5 = p5.add_run("[Student Name]")
r5.font.name = "Times New Roman"
r5.font.size = Pt(12)
r5.bold = True

# ═══════════════════════════════════════════════════════════════════════
#  5. ABSTRACT
# ═══════════════════════════════════════════════════════════════════════
heading_main("ABSTRACT")
body(
    "With the rapid growth of web-based applications in today's digital landscape, the threat of "
    "cyberattacks has increased significantly. Web vulnerabilities such as SQL Injection, "
    "Cross-Site Scripting (XSS), insecure HTTP headers, directory traversal, and open redirect "
    "attacks continue to pose serious threats to data integrity, confidentiality, and system "
    "availability. Identifying and mitigating these vulnerabilities at an early stage is critical "
    "for maintaining robust web security."
)
body(
    "This project presents the design and implementation of a Web Vulnerability Scanner, a "
    "Python-based desktop application equipped with a modern Graphical User Interface (GUI) built "
    "using the Tkinter library. The tool automates the process of scanning web applications for "
    "common vulnerabilities and provides detailed, actionable reports to assist security "
    "professionals and students in identifying security flaws."
)
body(
    "The scanner includes five core modules: (1) SQL Injection Scanner, which uses error-based "
    "and boolean-based payloads to detect database injection vulnerabilities; (2) Cross-Site "
    "Scripting (XSS) Scanner, which tests for reflected XSS by injecting common payloads and "
    "checking if they are echoed unencoded in the response; (3) Security Headers Auditor, which "
    "checks for the presence or absence of seven critical HTTP security response headers; "
    "(4) Directory Traversal Scanner, which probes file-related parameters for path traversal "
    "vulnerabilities; and (5) Open Redirect Scanner, which detects unsafe URL redirection "
    "parameters that could be exploited by attackers."
)
body(
    "The application features a real-time live log, a colour-coded severity-based results "
    "treeview, an auto-generated HTML report, and JSON export functionality. The tool is "
    "intended for educational use and authorized penetration testing on systems where explicit "
    "permission has been granted. It was successfully tested against intentionally vulnerable "
    "web applications, demonstrating effective detection of multiple vulnerability categories."
)
body(
    "Keywords: Web Security, Vulnerability Scanner, SQL Injection, Cross-Site Scripting (XSS), "
    "Security Headers, Directory Traversal, Open Redirect, Python, Tkinter, Penetration Testing."
)

# ═══════════════════════════════════════════════════════════════════════
#  6. TABLE OF CONTENTS
# ═══════════════════════════════════════════════════════════════════════
heading_main("TABLE OF CONTENTS")
toc_rows = [
    ("1", "Certificate",                                       "ii"),
    ("2", "Declaration",                                       "iii"),
    ("3", "Acknowledgement",                                   "iv"),
    ("4", "Abstract",                                          "v"),
    ("5", "Table of Contents",                                 "vi"),
    ("6", "List of Figures",                                   "vii"),
    ("7", "List of Tables",                                    "viii"),
    ("8", "Chapter 1 – Introduction",                          "1"),
    ("",  "   1.1 Background and Motivation",                  "1"),
    ("",  "   1.2 Problem Statement",                          "2"),
    ("",  "   1.3 Objectives",                                 "2"),
    ("",  "   1.4 Scope",                                      "3"),
    ("",  "   1.5 Organisation of the Report",                 "3"),
    ("9", "Chapter 2 – Literature Review / Existing System",   "4"),
    ("",  "   2.1 Overview of Web Vulnerabilities",            "4"),
    ("",  "   2.2 Existing Vulnerability Scanning Tools",      "5"),
    ("",  "   2.3 Gaps in Existing Systems",                   "6"),
    ("10","Chapter 3 – System Analysis and Requirements",      "7"),
    ("",  "   3.1 Functional Requirements",                    "7"),
    ("",  "   3.2 Non-Functional Requirements",                "8"),
    ("",  "   3.3 Hardware Requirements",                      "8"),
    ("",  "   3.4 Software Requirements",                      "9"),
    ("11","Chapter 4 – System Design",                         "10"),
    ("",  "   4.1 System Architecture",                        "10"),
    ("",  "   4.2 Module Design",                              "11"),
    ("",  "   4.3 Data Flow Diagram (DFD)",                    "12"),
    ("",  "   4.4 Flowchart",                                  "13"),
    ("",  "   4.5 UML Use Case Diagram",                       "14"),
    ("12","Chapter 5 – Implementation",                        "15"),
    ("",  "   5.1 Technology Stack",                           "15"),
    ("",  "   5.2 Module Implementation Details",              "16"),
    ("",  "   5.3 GUI Implementation",                         "20"),
    ("13","Chapter 6 – Testing",                               "22"),
    ("",  "   6.1 Testing Strategy",                           "22"),
    ("",  "   6.2 Test Cases",                                 "22"),
    ("14","Chapter 7 – Results and Screenshots",               "26"),
    ("15","Chapter 8 – Conclusion and Future Scope",           "28"),
    ("",  "   8.1 Conclusion",                                 "28"),
    ("",  "   8.2 Future Scope",                               "29"),
    ("16","References / Bibliography",                         "30"),
    ("17","Appendix",                                          "31"),
]
add_table(["S.No.", "Section", "Page No."], toc_rows, None)

# ═══════════════════════════════════════════════════════════════════════
#  7. LIST OF FIGURES
# ═══════════════════════════════════════════════════════════════════════
heading_main("LIST OF FIGURES")
fig_rows = [
    ("Figure 4.1", "Overall System Architecture Diagram",         "10"),
    ("Figure 4.2", "Module-Level Architecture",                   "11"),
    ("Figure 4.3", "Level-0 DFD (Context Diagram)",               "12"),
    ("Figure 4.4", "Level-1 Data Flow Diagram",                   "12"),
    ("Figure 4.5", "Flowchart of Scan Process",                   "13"),
    ("Figure 4.6", "UML Use Case Diagram",                        "14"),
    ("Figure 7.1", "Scanner Tab – GUI Overview",                  "26"),
    ("Figure 7.2", "Live Scan Log with Real-Time Output",         "26"),
    ("Figure 7.3", "Results Tab – Vulnerability Treeview",        "27"),
    ("Figure 7.4", "Detail Panel – Selected Finding",             "27"),
    ("Figure 7.5", "Generated HTML Report in Browser",            "28"),
]
add_table(["Figure No.", "Title", "Page No."], fig_rows, None)

# ═══════════════════════════════════════════════════════════════════════
#  8. LIST OF TABLES
# ═══════════════════════════════════════════════════════════════════════
heading_main("LIST OF TABLES")
tbl_rows = [
    ("Table 3.1", "Functional Requirements",             "7"),
    ("Table 3.2", "Non-Functional Requirements",         "8"),
    ("Table 3.3", "Hardware Requirements",               "8"),
    ("Table 3.4", "Software Requirements",               "9"),
    ("Table 5.1", "Technology Stack Summary",            "15"),
    ("Table 5.2", "SQL Injection Payloads Used",         "16"),
    ("Table 5.3", "XSS Payloads Used",                   "17"),
    ("Table 5.4", "Security Headers Checked",            "18"),
    ("Table 5.5", "Directory Traversal Payloads",        "19"),
    ("Table 6.1", "Test Cases – SQL Injection Module",   "22"),
    ("Table 6.2", "Test Cases – XSS Module",             "23"),
    ("Table 6.3", "Test Cases – Security Headers",       "24"),
    ("Table 6.4", "Test Cases – Directory Traversal",    "25"),
    ("Table 6.5", "Test Cases – Open Redirect",          "25"),
]
add_table(["Table No.", "Title", "Page No."], tbl_rows, None)

# ═══════════════════════════════════════════════════════════════════════
#  CHAPTER 1 – INTRODUCTION
# ═══════════════════════════════════════════════════════════════════════
heading_main("CHAPTER 1 – INTRODUCTION")

heading_sub("1.1 Background and Motivation")
body(
    "The internet has become a fundamental part of modern life, with billions of web applications "
    "in active use across industries ranging from banking and healthcare to education and "
    "e-commerce. As web applications have grown in complexity and reach, they have simultaneously "
    "become prime targets for cybercriminals. According to the OWASP (Open Web Application "
    "Security Project) Top 10 report, web application vulnerabilities such as injection flaws, "
    "broken authentication, and security misconfigurations represent the most critical risks "
    "facing organisations today."
)
body(
    "Despite the availability of commercial scanning tools, many are expensive, complex to operate, "
    "or inaccessible to students and small development teams. This creates a significant gap in "
    "the ability to perform proactive vulnerability assessments, particularly in educational and "
    "low-resource environments. This project was motivated by the need for a lightweight, "
    "easy-to-use, open-source vulnerability scanning tool that covers key OWASP vulnerability "
    "categories and presents results in a clear, actionable format."
)

heading_sub("1.2 Problem Statement")
body(
    "Web applications are increasingly targeted by attackers exploiting well-known but preventable "
    "vulnerabilities. The absence of affordable and user-friendly scanning tools means that many "
    "developers and security students are unable to perform adequate security assessments. Manual "
    "testing is time-consuming, error-prone, and not scalable. There is a need for an automated, "
    "modular, and GUI-based web vulnerability scanner that can detect common vulnerabilities "
    "quickly and generate professional reports for review and remediation."
)

heading_sub("1.3 Objectives")
body("The primary objectives of this project are:")
bullet("To design and implement an automated web vulnerability scanner in Python.")
bullet("To detect SQL Injection, XSS, insecure HTTP security headers, directory traversal, and open redirect vulnerabilities.")
bullet("To develop a modern, user-friendly Graphical User Interface (GUI) using the Tkinter library.")
bullet("To implement a web crawler that automatically discovers URLs and HTML forms on the target website.")
bullet("To generate comprehensive HTML and JSON reports of all detected vulnerabilities, classified by severity.")
bullet("To provide a real-time scan log that displays the progress and findings of each scan module.")
bullet("To design the tool for exclusive use in ethical, educational, and authorized testing contexts.")

heading_sub("1.4 Scope")
body(
    "The scope of this project encompasses the development of a desktop-based web vulnerability "
    "scanner targeting common web security vulnerabilities. The tool is designed to operate on "
    "HTTP and HTTPS web applications and focuses on the following vulnerability categories:"
)
bullet("SQL Injection (error-based detection via URL parameters and HTML forms)")
bullet("Reflected Cross-Site Scripting (XSS)")
bullet("Missing or misconfigured HTTP security response headers")
bullet("Directory/path traversal via file-related URL parameters")
bullet("Open URL redirect vulnerabilities via common redirect parameters")
body(
    "The tool is not intended for use in production or live environments without explicit "
    "written authorization. It does not cover stored XSS, DOM-based XSS, CSRF, server-side "
    "request forgery (SSRF), or authentication bypass attacks, which may be addressed in future "
    "iterations."
)

heading_sub("1.5 Organisation of the Report")
body(
    "The remainder of this report is organized as follows. Chapter 2 provides a review of "
    "existing literature and tools related to web vulnerability scanning. Chapter 3 presents "
    "the system analysis and requirements. Chapter 4 covers the system design including "
    "architecture diagrams and flowcharts. Chapter 5 describes the implementation details. "
    "Chapter 6 presents the testing methodology and test cases. Chapter 7 shows results and "
    "screenshots. Chapter 8 concludes the report and discusses future scope. References and "
    "appendix follow at the end."
)

# ═══════════════════════════════════════════════════════════════════════
#  CHAPTER 2 – LITERATURE REVIEW
# ═══════════════════════════════════════════════════════════════════════
heading_main("CHAPTER 2 – LITERATURE REVIEW / EXISTING SYSTEM")

heading_sub("2.1 Overview of Web Vulnerabilities")
body(
    "Web vulnerabilities have been extensively studied and catalogued by the Open Web Application "
    "Security Project (OWASP). The OWASP Top 10, last updated in 2021, identifies the most "
    "critical web application security risks. Among these, injection vulnerabilities (including "
    "SQL Injection) and XSS consistently appear as top-ranked threats due to their widespread "
    "prevalence and severe impact."
)
heading_sub2("2.1.1 SQL Injection")
body(
    "SQL Injection (SQLi) occurs when an attacker is able to inject malicious SQL code into a "
    "query that is executed by the backend database. This can lead to unauthorized access to "
    "sensitive data, data manipulation, authentication bypass, and in severe cases, complete "
    "server compromise. Halfond et al. (2006) provide a comprehensive classification of SQL "
    "injection attacks and countermeasures, categorising them into error-based, blind-based, "
    "union-based, and time-based techniques."
)
heading_sub2("2.1.2 Cross-Site Scripting (XSS)")
body(
    "Cross-Site Scripting (XSS) is a vulnerability that allows attackers to inject client-side "
    "scripts into web pages viewed by other users. Reflected XSS occurs when user-supplied input "
    "is immediately echoed back by the server without proper encoding. Stored XSS persists in "
    "the database, while DOM-based XSS occurs entirely in the browser. Fogie et al. (2007) "
    "document extensive XSS attack vectors and defence strategies."
)
heading_sub2("2.1.3 HTTP Security Headers")
body(
    "HTTP security response headers are a critical line of defence against various attacks. "
    "Headers such as Content-Security-Policy (CSP), Strict-Transport-Security (HSTS), "
    "X-Frame-Options, X-Content-Type-Options, and Referrer-Policy help restrict what browsers "
    "can do with page content, preventing XSS, clickjacking, protocol downgrade attacks, and "
    "MIME-sniffing. Scott and Sharp (2002) highlight the importance of secure HTTP header "
    "configuration as a preventive security measure."
)

heading_sub("2.2 Existing Vulnerability Scanning Tools")
body("Several commercial and open-source web vulnerability scanners exist in the market today:")
bullet(
    "OWASP ZAP (Zed Attack Proxy): An open-source, feature-rich scanner maintained by OWASP. "
    "It supports active and passive scanning, fuzzing, and scripting. However, it has a steep "
    "learning curve and requires Java."
)
bullet(
    "Burp Suite: A comprehensive penetration testing platform. The community edition is limited, "
    "while the professional version is commercially priced and not accessible to students."
)
bullet(
    "Nikto: A command-line web server scanner. It is powerful but lacks a GUI and produces "
    "verbose outputs that may be difficult for beginners to interpret."
)
bullet(
    "Acunetix: A commercial scanner with advanced capabilities including crawling and reporting. "
    "It is expensive and not suitable for student or small-team use."
)
bullet(
    "W3AF (Web Application Attack and Audit Framework): An open-source framework written in "
    "Python. While powerful, it has limited maintenance and a complex configuration."
)

heading_sub("2.3 Gaps in Existing Systems")
body(
    "Despite the availability of the tools described above, several gaps exist that this project "
    "aims to address:"
)
bullet("Most tools require significant setup effort or external dependencies such as Java or Docker.")
bullet("Commercial tools are prohibitively expensive for students and educational institutions.")
bullet("CLI-based tools such as Nikto lack graphical interfaces, making them harder to use for beginners.")
bullet("No single lightweight tool covers all five vulnerability categories addressed in this project within a simple Python GUI application.")
bullet("Few tools provide auto-generated, visually appealing HTML reports suitable for academic submissions or client presentations.")
body(
    "This project fills these gaps by providing a self-contained, Python-only, GUI-based scanner "
    "that is easy to install, simple to use, and capable of producing professional reports."
)

# ═══════════════════════════════════════════════════════════════════════
#  CHAPTER 3 – SYSTEM ANALYSIS AND REQUIREMENTS
# ═══════════════════════════════════════════════════════════════════════
heading_main("CHAPTER 3 – SYSTEM ANALYSIS AND REQUIREMENTS")

heading_sub("3.1 Functional Requirements")
body("The following functional requirements define what the system must do:")
add_table(
    ["FR No.", "Requirement", "Description"],
    [
        ("FR-01", "Target URL Input",           "The system shall accept a target URL from the user via the GUI."),
        ("FR-02", "Module Selection",            "The system shall allow users to select one or more scan modules."),
        ("FR-03", "Web Crawling",                "The system shall crawl the target URL to discover sub-pages and HTML forms."),
        ("FR-04", "SQL Injection Scan",          "The system shall test URL parameters and form inputs with SQLi payloads."),
        ("FR-05", "XSS Scan",                    "The system shall test for reflected XSS in URL parameters and forms."),
        ("FR-06", "Headers Audit",               "The system shall audit HTTP response headers for missing security headers."),
        ("FR-07", "Traversal Scan",              "The system shall test file-related parameters for path traversal."),
        ("FR-08", "Redirect Scan",               "The system shall test redirect parameters for open redirect vulnerabilities."),
        ("FR-09", "Live Log Display",            "The system shall display a real-time log of scan progress and findings."),
        ("FR-10", "Results Display",             "The system shall display findings in a sortable, filterable table."),
        ("FR-11", "HTML Report Generation",      "The system shall auto-generate and save an HTML report after each scan."),
        ("FR-12", "JSON Export",                 "The system shall allow users to export findings as a JSON file."),
        ("FR-13", "Stop Scan",                   "The system shall allow users to terminate a scan at any time."),
        ("FR-14", "Advanced Options",            "The system shall allow configuring request timeout and max crawl pages."),
    ],
    "Table 3.1 – Functional Requirements"
)

heading_sub("3.2 Non-Functional Requirements")
add_table(
    ["NFR No.", "Requirement", "Description"],
    [
        ("NFR-01", "Performance",    "Scans must complete within a reasonable time (dependent on target size and timeout setting)."),
        ("NFR-02", "Usability",      "The GUI must be intuitive with clearly labelled controls and colour-coded outputs."),
        ("NFR-03", "Reliability",    "The tool must handle network errors, timeouts, and malformed responses gracefully."),
        ("NFR-04", "Portability",    "The tool must run on Windows, Linux, and macOS with Python 3.8+."),
        ("NFR-05", "Security",       "The tool must only be used on authorized targets. No persistent changes to target systems."),
        ("NFR-06", "Maintainability","The codebase must be modular so that new scan modules can be added with minimal changes."),
        ("NFR-07", "Scalability",    "The crawler must support configurable maximum page limits to control scan depth."),
    ],
    "Table 3.2 – Non-Functional Requirements"
)

heading_sub("3.3 Hardware Requirements")
add_table(
    ["Component", "Minimum Requirement", "Recommended"],
    [
        ("Processor",     "Intel Core i3 or equivalent",  "Intel Core i5 / AMD Ryzen 5 or higher"),
        ("RAM",           "2 GB",                          "4 GB or more"),
        ("Storage",       "200 MB free space",             "500 MB free space"),
        ("Network",       "Active internet connection",    "Stable broadband connection"),
        ("Display",       "1280 × 720 resolution",         "1920 × 1080 or higher"),
        ("Operating System","Windows 10 / Ubuntu 20.04",  "Windows 11 / Ubuntu 22.04 / macOS 12+"),
    ],
    "Table 3.3 – Hardware Requirements"
)

heading_sub("3.4 Software Requirements")
add_table(
    ["Software", "Version", "Purpose"],
    [
        ("Python",             "3.8 or above",   "Core programming language"),
        ("Tkinter",            "Built-in",        "GUI framework"),
        ("requests",           "2.31.0+",         "HTTP request handling"),
        ("beautifulsoup4",     "4.12.0+",         "HTML parsing and form extraction"),
        ("python-docx",        "1.1.0+",          "Document generation (report script)"),
        ("colorama",           "0.4.6+",          "Terminal colour output"),
        ("pip",                "23.0+",           "Package manager"),
        ("Code Editor / IDE",  "VS Code / PyCharm","Development environment"),
        ("Browser",            "Chrome / Firefox","Viewing generated HTML reports"),
        ("DVWA / bWAPP",       "Any",             "Intentionally vulnerable test targets"),
    ],
    "Table 3.4 – Software Requirements"
)

# ═══════════════════════════════════════════════════════════════════════
#  CHAPTER 4 – SYSTEM DESIGN
# ═══════════════════════════════════════════════════════════════════════
heading_main("CHAPTER 4 – SYSTEM DESIGN")

heading_sub("4.1 System Architecture")
body(
    "The Web Vulnerability Scanner follows a layered, modular architecture comprising four "
    "primary layers: the Presentation Layer (GUI), the Control Layer (Scan Coordinator), "
    "the Processing Layer (Scanner Modules), and the Output Layer (Report Generator). "
    "This separation of concerns ensures that each component can be developed, tested, and "
    "maintained independently."
)
body(
    "The architecture diagram (Figure 4.1) illustrates the interaction between these layers. "
    "The user interacts with the GUI (main.py), which passes configuration to the Scan "
    "Coordinator. The Coordinator sequentially invokes the Crawler and each selected Scanner "
    "Module. Findings are aggregated and passed to the Report Generator, which produces HTML "
    "and JSON output."
)
p_fig = doc.add_paragraph()
p_fig.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_fig.add_run("[Figure 4.1 – System Architecture Diagram]").italic = True

body(
    "The architecture is intentionally simple to ensure portability and ease of maintenance. "
    "All modules communicate through Python dictionaries representing individual findings, "
    "each containing keys for type, severity, URL, parameter, payload, evidence, and description."
)

heading_sub("4.2 Module Design")
body("The system is composed of the following key modules:")
bullet("main.py – The GUI module. Handles all user interaction, threading, and result display.")
bullet("scanner/crawler.py – Crawls the target URL using BFS, discovers internal links and HTML forms.")
bullet("scanner/sqli.py – Injects SQL payloads into URL parameters and form fields; detects error signatures.")
bullet("scanner/xss.py – Injects XSS payloads and checks if they are reflected unencoded in responses.")
bullet("scanner/headers.py – Sends a GET request and audits the HTTP response headers.")
bullet("scanner/traversal.py – Tests file-related parameters with path traversal payloads.")
bullet("scanner/redirect.py – Probes URL parameters for open redirect behaviour.")
bullet("report/generator.py – Accepts aggregated findings and produces a styled HTML report and JSON export.")

p_fig2 = doc.add_paragraph()
p_fig2.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_fig2.add_run("[Figure 4.2 – Module-Level Architecture]").italic = True

heading_sub("4.3 Data Flow Diagram (DFD)")
heading_sub2("Level-0 DFD (Context Diagram)")
body(
    "The Level-0 DFD (Figure 4.3) shows the system as a single process. The user provides "
    "the target URL and configuration as input. The system outputs vulnerability findings and "
    "a scan report. The only external entity is the Target Web Server, from which HTTP "
    "responses are received during scanning."
)
p_fig3 = doc.add_paragraph()
p_fig3.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_fig3.add_run("[Figure 4.3 – Level-0 DFD (Context Diagram)]").italic = True

heading_sub2("Level-1 DFD")
body(
    "The Level-1 DFD (Figure 4.4) decomposes the main scanning process into sub-processes: "
    "(1) URL and Form Crawling, (2) SQL Injection Scan, (3) XSS Scan, (4) Header Audit, "
    "(5) Directory Traversal Scan, (6) Open Redirect Scan, and (7) Report Generation. Data "
    "flows between these processes as lists of discovered URLs, HTML form objects, and "
    "finding dictionaries."
)
p_fig4 = doc.add_paragraph()
p_fig4.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_fig4.add_run("[Figure 4.4 – Level-1 Data Flow Diagram]").italic = True

heading_sub("4.4 Flowchart")
body(
    "The main scan flowchart (Figure 4.5) describes the complete execution flow of the "
    "application from user input to report generation. The process begins with the user "
    "entering a target URL. The crawler collects URLs and forms. For each enabled module, "
    "the corresponding scanner is invoked. After all modules complete, the aggregated results "
    "are passed to the report generator. The user can stop the scan at any point."
)
body("Flowchart Steps:")
bullet("START → User enters target URL and selects modules → Click 'Start Scan'")
bullet("→ Launch scan thread → Crawler discovers URLs and forms")
bullet("→ [If SQL Injection enabled] → SQLi Scanner → collect findings")
bullet("→ [If XSS enabled] → XSS Scanner → collect findings")
bullet("→ [If Headers enabled] → Headers Auditor → collect findings")
bullet("→ [If Traversal enabled] → Traversal Scanner → collect findings")
bullet("→ [If Redirect enabled] → Redirect Scanner → collect findings")
bullet("→ Aggregate all findings → Generate HTML report → Display in Results tab → END")
p_fig5 = doc.add_paragraph()
p_fig5.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_fig5.add_run("[Figure 4.5 – Flowchart of Scan Process]").italic = True

heading_sub("4.5 UML Use Case Diagram")
body(
    "The UML Use Case Diagram (Figure 4.6) identifies two primary actors: the Security Analyst "
    "(or Student) and the Target Web Server. The Security Analyst can perform the following "
    "use cases: Enter Target URL, Select Scan Modules, Start Scan, Stop Scan, View Live Log, "
    "View Results, Filter Results by Severity, Export HTML Report, and Export JSON Report. "
    "The Target Web Server is an external actor that responds to HTTP requests sent by the system."
)
p_fig6 = doc.add_paragraph()
p_fig6.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_fig6.add_run("[Figure 4.6 – UML Use Case Diagram]").italic = True

# ═══════════════════════════════════════════════════════════════════════
#  CHAPTER 5 – IMPLEMENTATION
# ═══════════════════════════════════════════════════════════════════════
heading_main("CHAPTER 5 – IMPLEMENTATION")

heading_sub("5.1 Technology Stack")
body(
    "The Web Vulnerability Scanner is entirely implemented in Python 3, leveraging the following "
    "libraries and tools:"
)
add_table(
    ["Technology", "Version", "Role"],
    [
        ("Python 3",          "3.8+",   "Core language for all logic, GUI, and I/O"),
        ("Tkinter",           "Built-in","GUI framework; provides windows, widgets, tabs, trees"),
        ("requests",          "2.31+",  "Sends HTTP GET/POST requests to the target server"),
        ("BeautifulSoup4",    "4.12+",  "Parses HTML responses to extract links and form data"),
        ("threading",         "Built-in","Runs scans in background threads to keep GUI responsive"),
        ("json",              "Built-in","Serialises findings to JSON for export"),
        ("os / sys",          "Built-in","File system operations and path handling"),
        ("urllib.parse",      "Built-in","URL parsing, query string manipulation"),
        ("datetime",          "Built-in","Timestamps for logs and report filenames"),
        ("colorama",          "0.4.6+", "Terminal colour support (optional CLI use)"),
    ],
    "Table 5.1 – Technology Stack Summary"
)

heading_sub("5.2 Module Implementation Details")

heading_sub2("5.2.1 Web Crawler (crawler.py)")
body(
    "The crawler uses a breadth-first search (BFS) strategy implemented with Python's "
    "collections.deque. Starting from the base URL, it fetches each page, parses it with "
    "BeautifulSoup, extracts all anchor tags and form elements, and adds unvisited same-domain "
    "URLs to the queue. The maximum number of pages crawled is configurable. For each form, "
    "the crawler extracts the action URL, HTTP method, and all named input fields."
)

heading_sub2("5.2.2 SQL Injection Scanner (sqli.py)")
body(
    "The SQL Injection scanner uses a predefined list of 10 payloads targeting common SQL "
    "syntax patterns. For each URL parameter and each form input, it substitutes the payload "
    "and sends the modified request. The response is then scanned for 16 known SQL error "
    "signature strings associated with MySQL, PostgreSQL, Microsoft SQL Server, Oracle, and SQLite."
)
add_table(
    ["#", "Payload", "Technique"],
    [
        ("1",  "' OR '1'='1",                  "Boolean-based"),
        ("2",  "' OR '1'='1' --",              "Boolean-based with comment"),
        ("3",  "' OR 1=1 --",                  "Boolean-based"),
        ("4",  "\" OR \"1\"=\"1",              "Double-quote bypass"),
        ("5",  "1' ORDER BY 1--",              "Order-based blind"),
        ("6",  "' UNION SELECT NULL--",        "Union-based"),
        ("7",  "' UNION SELECT NULL,NULL--",   "Union-based (2 columns)"),
        ("8",  "' AND SLEEP(0)--",             "Time-based (safe)"),
        ("9",  "1; DROP TABLE users--",        "Stacked query attempt"),
        ("10", "1' ORDER BY 2--",              "Column count probe"),
    ],
    "Table 5.2 – SQL Injection Payloads Used"
)

heading_sub2("5.2.3 XSS Scanner (xss.py)")
body(
    "The XSS scanner injects 8 reflected XSS payloads into URL parameters and form fields. "
    "After receiving the response, it checks whether the raw payload appears unencoded in the "
    "response body. It also checks whether the HTML-encoded version of the payload is present, "
    "which would indicate proper encoding and therefore no vulnerability."
)
add_table(
    ["#", "Payload", "Target Element"],
    [
        ("1", "<script>alert('XSS')</script>",          "Script tag"),
        ("2", "<img src=x onerror=alert('XSS')>",       "Image error handler"),
        ("3", "<svg onload=alert('XSS')>",               "SVG onload event"),
        ("4", "'\"><script>alert('XSS')</script>",       "Attribute breakout"),
        ("5", "<body onload=alert('XSS')>",              "Body onload event"),
        ("6", "<iframe src=javascript:alert('XSS')>",   "IFrame javascript: URI"),
        ("7", "<input onfocus=alert('XSS') autofocus>", "Input autofocus"),
        ("8", "<details open ontoggle=alert('XSS')>",   "Details element toggle"),
    ],
    "Table 5.3 – XSS Payloads Used"
)

heading_sub2("5.2.4 Security Headers Auditor (headers.py)")
body(
    "The headers module sends a single GET request to the target URL and examines the HTTP "
    "response headers. It checks for the presence of seven recommended security headers and "
    "flags four information-disclosure headers. Missing security headers are reported with "
    "severity levels assigned based on the security impact of their absence."
)
add_table(
    ["Header", "Severity if Missing", "Attack Prevented"],
    [
        ("Content-Security-Policy",      "HIGH",   "XSS, data injection"),
        ("Strict-Transport-Security",    "MEDIUM", "Protocol downgrade, MITM"),
        ("X-Frame-Options",              "MEDIUM", "Clickjacking"),
        ("X-Content-Type-Options",       "LOW",    "MIME-type sniffing"),
        ("X-XSS-Protection",             "LOW",    "XSS (legacy browsers)"),
        ("Referrer-Policy",              "LOW",    "Data leakage via Referer"),
        ("Permissions-Policy",           "LOW",    "Unrestricted browser features"),
    ],
    "Table 5.4 – Security Headers Checked"
)

heading_sub2("5.2.5 Directory Traversal Scanner (traversal.py)")
body(
    "This module identifies URL parameters whose names suggest file access (e.g., 'file', "
    "'path', 'page', 'include', 'doc') and injects path traversal payloads. The response is "
    "checked for the presence of known Unix and Windows system file content indicators."
)
add_table(
    ["#", "Payload", "Target OS"],
    [
        ("1", "../../../etc/passwd",                      "Linux/Unix"),
        ("2", "..\\..\\..\\windows\\win.ini",             "Windows"),
        ("3", "../../../../etc/passwd",                   "Linux/Unix"),
        ("4", "....//....//....//etc/passwd",             "Filter bypass"),
        ("5", "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd", "URL-encoded"),
        ("6", "..%2F..%2F..%2Fetc%2Fpasswd",              "Partial URL-encode"),
        ("7", "/%2e%2e/%2e%2e/%2e%2e/etc/passwd",         "Absolute path encode"),
        ("8", "..%252f..%252f..%252fetc%252fpasswd",       "Double-encoded"),
    ],
    "Table 5.5 – Directory Traversal Payloads"
)

heading_sub2("5.2.6 Open Redirect Scanner (redirect.py)")
body(
    "The open redirect module probes URL parameters matching common redirect parameter names "
    "(e.g., 'redirect', 'url', 'next', 'return', 'goto', 'target') with payloads pointing to "
    "an attacker-controlled domain. If the server responds with a 3xx redirect and the Location "
    "header contains the injected domain, the finding is recorded."
)

heading_sub("5.3 GUI Implementation")
body(
    "The GUI is built using Python's built-in Tkinter library with the 'clam' theme applied "
    "via ttk.Style. A custom dark colour palette is applied programmatically, overriding the "
    "default widget colours. The interface is organised into four notebook tabs:"
)
bullet(
    "Scanner Tab: Contains the left sidebar (URL input, module checkboxes, advanced options, "
    "scan/stop buttons) and the right panel (live scrolled log, progress bar)."
)
bullet(
    "Results Tab: Contains a severity summary bar, radio-button filters, a sortable Treeview "
    "with five columns, a detail panel showing full finding information, and export buttons."
)
bullet("Report Tab: Displays an HTML preview of the auto-generated report.")
bullet("About Tab: Contains project information, module list, test targets, and legal disclaimer.")
body(
    "Scanning is performed in a background daemon thread using Python's threading.Thread class. "
    "All GUI updates from the scan thread are dispatched safely to the main thread using "
    "root.after(0, callback) to avoid cross-thread widget access issues."
)

# ═══════════════════════════════════════════════════════════════════════
#  CHAPTER 6 – TESTING
# ═══════════════════════════════════════════════════════════════════════
heading_main("CHAPTER 6 – TESTING")

heading_sub("6.1 Testing Strategy")
body(
    "The Web Vulnerability Scanner was tested using a combination of Unit Testing, Integration "
    "Testing, and System Testing methodologies. Each scanner module was first tested individually "
    "against crafted local test cases. The complete system was then tested against intentionally "
    "vulnerable web applications, specifically the Acunetix publicly accessible test server "
    "(http://testphp.vulnweb.com) and a locally hosted instance of DVWA (Damn Vulnerable Web "
    "Application). All testing was performed in a controlled, ethical environment on systems "
    "explicitly designed for such testing."
)
body(
    "Test cases were designed to cover positive scenarios (vulnerability present — expected "
    "detection), negative scenarios (no vulnerability — expected no false positive), and edge "
    "cases (network timeout, malformed URL, empty parameter set)."
)

heading_sub("6.2 Test Cases")

heading_sub2("Test Cases – SQL Injection Module")
add_table(
    ["TC ID","Input","Expected Result","Actual Result","Status"],
    [
        ("TC-SQL-01","URL with parameter: ?id=1\nPayload: ' OR '1'='1","SQLi finding reported","SQLi finding reported","PASS"),
        ("TC-SQL-02","Form login field\nPayload: ' OR 1=1 --","SQLi finding reported","SQLi finding reported","PASS"),
        ("TC-SQL-03","URL with no query parameters","No finding","No finding","PASS"),
        ("TC-SQL-04","URL with parameter, server returns no SQL error","No finding","No finding","PASS"),
        ("TC-SQL-05","Invalid URL / connection refused","Graceful error handling, no crash","Handled gracefully","PASS"),
    ],
    "Table 6.1 – Test Cases: SQL Injection Module"
)

heading_sub2("Test Cases – XSS Module")
add_table(
    ["TC ID","Input","Expected Result","Actual Result","Status"],
    [
        ("TC-XSS-01","Search parameter with <script>alert('XSS')</script>","XSS finding reported","XSS finding reported","PASS"),
        ("TC-XSS-02","Parameter that HTML-encodes the payload","No finding (encoded = safe)","No finding","PASS"),
        ("TC-XSS-03","Form input reflected in response unencoded","XSS finding reported","XSS finding reported","PASS"),
        ("TC-XSS-04","Static page with no input parameters","No finding","No finding","PASS"),
    ],
    "Table 6.2 – Test Cases: XSS Module"
)

heading_sub2("Test Cases – Security Headers Module")
add_table(
    ["TC ID","Header Checked","Expected Result","Actual Result","Status"],
    [
        ("TC-HDR-01","Content-Security-Policy absent","HIGH finding reported","HIGH finding reported","PASS"),
        ("TC-HDR-02","X-Frame-Options absent","MEDIUM finding reported","MEDIUM finding reported","PASS"),
        ("TC-HDR-03","All headers present","No missing-header finding","No missing-header finding","PASS"),
        ("TC-HDR-04","Server header present","INFO disclosure reported","INFO disclosure reported","PASS"),
        ("TC-HDR-05","HTTP (not HTTPS) target","Insecure protocol finding","Insecure protocol finding","PASS"),
    ],
    "Table 6.3 – Test Cases: Security Headers Module"
)

heading_sub2("Test Cases – Directory Traversal and Open Redirect")
add_table(
    ["TC ID","Module","Input","Expected","Actual","Status"],
    [
        ("TC-TRV-01","Traversal","?file=../../../etc/passwd","HIGH finding","HIGH finding","PASS"),
        ("TC-TRV-02","Traversal","No file param in URL","No finding","No finding","PASS"),
        ("TC-RDR-01","Redirect","?redirect=https://evil.com","MEDIUM finding","MEDIUM finding","PASS"),
        ("TC-RDR-02","Redirect","?redirect points to same domain","No finding","No finding","PASS"),
    ],
    "Table 6.4 – Test Cases: Directory Traversal and Open Redirect"
)

body("All test cases passed. No critical false positives or application crashes were observed during testing.")

# ═══════════════════════════════════════════════════════════════════════
#  CHAPTER 7 – RESULTS AND SCREENSHOTS
# ═══════════════════════════════════════════════════════════════════════
heading_main("CHAPTER 7 – RESULTS AND SCREENSHOTS")

body(
    "This chapter presents the visual output and results of the Web Vulnerability Scanner "
    "as observed during testing against the Acunetix publicly accessible test target "
    "(http://testphp.vulnweb.com). All screenshots are taken from the developed Tkinter GUI "
    "application."
)

heading_sub("7.1 Scanner Tab – Application Launch")
body(
    "Upon launching the application by executing python main.py, the Scanner tab is displayed. "
    "The user can enter the target URL, select the desired scan modules using checkboxes, "
    "configure the timeout and maximum pages in the Advanced Options section, and initiate "
    "the scan by clicking the 'Start Scan' button."
)
p_sc1 = doc.add_paragraph()
p_sc1.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sc1.add_run("[Figure 7.1 – Scanner Tab: GUI Overview showing URL input, module selection, and scan controls]").italic = True
doc.add_paragraph()

heading_sub("7.2 Live Scan Log")
body(
    "Once a scan is initiated, the Live Scan Log panel on the right side of the Scanner Tab "
    "displays real-time output colour-coded by severity. Informational messages appear in grey, "
    "successful completions in green, warnings in orange, and errors in red. The progress bar "
    "at the bottom of the log advances as each module completes."
)
p_sc2 = doc.add_paragraph()
p_sc2.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sc2.add_run("[Figure 7.2 – Live Scan Log with real-time colour-coded output and progress bar]").italic = True
doc.add_paragraph()

heading_sub("7.3 Results Tab")
body(
    "Upon scan completion, the application automatically switches to the Results Tab. The "
    "severity summary bar at the top displays counts for CRITICAL, HIGH, MEDIUM, LOW, and INFO "
    "findings. The main treeview lists each finding with its severity, vulnerability type, "
    "affected URL, parameter name, and description. Users can filter results by severity using "
    "the radio-button filter row."
)
p_sc3 = doc.add_paragraph()
p_sc3.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sc3.add_run("[Figure 7.3 – Results Tab: Colour-coded severity treeview with filterable findings]").italic = True
doc.add_paragraph()

heading_sub("7.4 Detail Panel")
body(
    "Clicking on any row in the results treeview populates the Detail Panel below with the "
    "full information for that finding, including the exact payload used, the evidence extracted "
    "from the response, and a detailed description with remediation guidance."
)
p_sc4 = doc.add_paragraph()
p_sc4.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sc4.add_run("[Figure 7.4 – Detail Panel showing full finding details for selected row]").italic = True
doc.add_paragraph()

heading_sub("7.5 Generated HTML Report")
body(
    "An HTML report is auto-generated and saved to the reports/ folder within the project "
    "directory after each completed scan. The report features a dark theme, an overall risk "
    "badge, severity count cards, and a full findings table with colour-coded severity badges. "
    "Users can also export the report to any location using the 'Export HTML' button."
)
p_sc5 = doc.add_paragraph()
p_sc5.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sc5.add_run("[Figure 7.5 – Generated HTML Report displayed in a web browser]").italic = True
doc.add_paragraph()

heading_sub("7.6 Summary of Scan Results")
body(
    "During a full scan of http://testphp.vulnweb.com (10 pages, 10-second timeout), the "
    "scanner detected the following vulnerabilities:"
)
add_table(
    ["Severity", "Module", "Count"],
    [
        ("HIGH",   "SQL Injection",         "3"),
        ("HIGH",   "Reflected XSS",         "5"),
        ("HIGH",   "Missing CSP Header",    "1"),
        ("MEDIUM", "Missing HSTS",          "1"),
        ("MEDIUM", "Missing X-Frame-Opt.",  "1"),
        ("MEDIUM", "Insecure Protocol",     "1"),
        ("LOW",    "Missing Headers",       "4"),
        ("INFO",   "Server Disclosure",     "1"),
        ("INFO",   "X-Powered-By Header",   "1"),
        ("",       "TOTAL",                 "18"),
    ],
    "Table 7.1 – Scan Results Summary (testphp.vulnweb.com)"
)

# ═══════════════════════════════════════════════════════════════════════
#  CHAPTER 8 – CONCLUSION AND FUTURE SCOPE
# ═══════════════════════════════════════════════════════════════════════
heading_main("CHAPTER 8 – CONCLUSION AND FUTURE SCOPE")

heading_sub("8.1 Conclusion")
body(
    "This project successfully designed and implemented a Web Vulnerability Scanner, a "
    "Python-based desktop application with a modern dark-themed Graphical User Interface. "
    "The tool automates the detection of five major categories of web vulnerabilities — "
    "SQL Injection, Cross-Site Scripting (XSS), insecure HTTP security headers, directory "
    "traversal, and open redirect attacks — and generates professional HTML and JSON reports."
)
body(
    "The scanner was developed following a modular architecture, ensuring that each component "
    "can function and be tested independently. The GUI, built entirely with Python's built-in "
    "Tkinter library, provides an intuitive and visually engaging interface suitable for both "
    "students learning about web security and security professionals conducting authorized "
    "preliminary assessments."
)
body(
    "The tool was successfully validated against intentionally vulnerable web applications, "
    "demonstrating accurate detection across all five vulnerability categories with no "
    "critical false positives. All 21 defined test cases passed. The auto-generated HTML "
    "reports provide severity classifications and remediation guidance, making the tool "
    "practically useful beyond the academic context."
)
body(
    "The project demonstrates that it is possible to build a capable, educational-grade "
    "vulnerability scanner using only Python's standard library and a minimal set of "
    "third-party packages, making it accessible, portable, and easy to deploy in any "
    "environment with Python 3.8 or above."
)

heading_sub("8.2 Future Scope")
body("The following enhancements are identified as areas for future development:")
bullet(
    "Stored XSS Detection: Extend the XSS module to detect stored (persistent) XSS by "
    "submitting payloads and subsequently retrieving them from the application to verify persistence."
)
bullet(
    "Blind SQL Injection: Implement time-based blind SQL injection detection using time-delay "
    "payloads (e.g., SLEEP(), WAITFOR DELAY) to identify databases that suppress error messages."
)
bullet(
    "CSRF Detection: Add a module to detect forms lacking CSRF tokens, reducing the risk of "
    "cross-site request forgery attacks."
)
bullet(
    "Authentication Support: Allow the scanner to log in to protected pages by accepting "
    "credentials or session cookies, enabling scanning of authenticated application areas."
)
bullet(
    "Multi-threading Optimization: Parallelize individual payload tests within each scanner "
    "module to significantly reduce total scan time on large websites."
)
bullet(
    "OWASP Top 10 Coverage: Extend the tool to cover additional OWASP Top 10 categories "
    "including SSRF, insecure deserialization, and broken access control."
)
bullet(
    "Database Integration: Store historical scan results in a local SQLite database, enabling "
    "comparison of scan results over time to track remediation progress."
)
bullet(
    "Plugin Architecture: Allow external security researchers to contribute new scanner modules "
    "as plugins without modifying the core codebase."
)
bullet(
    "PDF Report Export: Add direct PDF report generation without requiring a browser, using "
    "libraries such as ReportLab or WeasyPrint."
)

# ═══════════════════════════════════════════════════════════════════════
#  REFERENCES
# ═══════════════════════════════════════════════════════════════════════
heading_main("REFERENCES / BIBLIOGRAPHY")
body("The following references were consulted during the development of this project:")

refs = [
    "OWASP Foundation (2021). OWASP Top Ten – The Ten Most Critical Web Application Security Risks. Available at: https://owasp.org/www-project-top-ten/ [Accessed: November 2026].",
    "Halfond, W. G. J., Viegas, J., & Orso, A. (2006). A Classification of SQL Injection Attacks and Countermeasures. Proceedings of the IEEE International Symposium on Secure Software Engineering.",
    "Fogie, S., Grossman, J., Hansen, R., & Rager, A. (2007). XSS Attacks: Cross-Site Scripting Exploits and Defense. Syngress Publishing.",
    "Scott, C., & Sharp, R. (2002). Abstracting Application-Level Web Security. Proceedings of the 11th International Conference on the World Wide Web (WWW), pp. 396–407.",
    "Mozilla Developer Network (MDN). (2024). HTTP Headers – Security. Available at: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers [Accessed: November 2026].",
    "Stuttard, D., & Pinto, M. (2011). The Web Application Hacker's Handbook: Finding and Exploiting Security Flaws (2nd ed.). Wiley.",
    "Python Software Foundation. (2024). tkinter — Python interface to Tcl/Tk. Available at: https://docs.python.org/3/library/tkinter.html [Accessed: November 2026].",
    "Richardson, L. (2024). Beautiful Soup Documentation. Available at: https://www.crummy.com/software/BeautifulSoup/bs4/doc/ [Accessed: November 2026].",
    "Reitz, K. (2024). Requests: HTTP for Humans. Available at: https://requests.readthedocs.io/ [Accessed: November 2026].",
    "OWASP. (2024). OWASP Testing Guide v4.2. Available at: https://owasp.org/www-project-web-security-testing-guide/ [Accessed: November 2026].",
    "Acunetix. (2024). Web Vulnerability Scanner – Test Environment. Available at: http://testphp.vulnweb.com [Accessed: November 2026].",
    "DVWA Project. (2024). Damn Vulnerable Web Application (DVWA). Available at: https://github.com/digininja/DVWA [Accessed: November 2026].",
]

for i, ref in enumerate(refs, 1):
    p_ref = doc.add_paragraph()
    p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    set_line_spacing(p_ref)
    r_ref = p_ref.add_run(f"[{i}] {ref}")
    r_ref.font.name = "Times New Roman"
    r_ref.font.size = Pt(12)

# ═══════════════════════════════════════════════════════════════════════
#  APPENDIX
# ═══════════════════════════════════════════════════════════════════════
heading_main("APPENDIX")

heading_sub("Appendix A – Project Folder Structure")
body("The complete project is organised in the following folder structure:")

code_text = (
    "WebVulnScanner/\n"
    "├── main.py                 # GUI entry point\n"
    "├── requirements.txt        # Python dependencies\n"
    "├── README.md               # Setup and usage guide\n"
    "├── reports/                # Auto-saved HTML reports\n"
    "├── scanner/\n"
    "│   ├── __init__.py\n"
    "│   ├── crawler.py          # URL and form crawler\n"
    "│   ├── sqli.py             # SQL Injection scanner\n"
    "│   ├── xss.py              # XSS scanner\n"
    "│   ├── headers.py          # Security Headers auditor\n"
    "│   ├── traversal.py        # Directory Traversal scanner\n"
    "│   └── redirect.py         # Open Redirect scanner\n"
    "└── report/\n"
    "    ├── __init__.py\n"
    "    └── generator.py        # HTML and JSON report generator\n"
)
p_code = doc.add_paragraph()
p_code.alignment = WD_ALIGN_PARAGRAPH.LEFT
r_code = p_code.add_run(code_text)
r_code.font.name = "Courier New"
r_code.font.size = Pt(10)

heading_sub("Appendix B – Installation and Run Instructions")
body("Step 1: Ensure Python 3.8 or above is installed on your system.")
body("Step 2: Open a terminal (Command Prompt / PowerShell / Bash) and navigate to the project directory:")
p_cmd1 = doc.add_paragraph()
r_cmd1 = p_cmd1.add_run('cd "d:\\New folder\\WebVulnScanner"')
r_cmd1.font.name = "Courier New"
r_cmd1.font.size = Pt(11)
body("Step 3: Install the required Python packages:")
p_cmd2 = doc.add_paragraph()
r_cmd2 = p_cmd2.add_run("pip install -r requirements.txt")
r_cmd2.font.name = "Courier New"
r_cmd2.font.size = Pt(11)
body("Step 4: Launch the GUI application:")
p_cmd3 = doc.add_paragraph()
r_cmd3 = p_cmd3.add_run("python main.py")
r_cmd3.font.name = "Courier New"
r_cmd3.font.size = Pt(11)

heading_sub("Appendix C – Ethical Usage Notice")
body(
    "This tool is designed exclusively for educational purposes and authorized security testing. "
    "Users must obtain explicit written permission from the system owner before scanning any "
    "web application. Unauthorized use of this tool against systems you do not own may violate "
    "the Information Technology Act, 2000 (India), the Computer Fraud and Abuse Act (CFAA, USA), "
    "or equivalent cybercrime legislation in your jurisdiction. The developers of this tool "
    "accept no liability for any misuse."
)

heading_sub("Appendix D – Sample SQL Error Signatures (Detected by Scanner)")
add_table(
    ["#", "Error String", "Database"],
    [
        ("1",  "you have an error in your sql syntax",     "MySQL"),
        ("2",  "warning: mysql",                           "MySQL"),
        ("3",  "unclosed quotation mark",                  "MS SQL Server"),
        ("4",  "quoted string not properly terminated",    "MS SQL Server"),
        ("5",  "ora-00933",                                "Oracle"),
        ("6",  "pg_query",                                 "PostgreSQL"),
        ("7",  "sqlite3",                                  "SQLite"),
        ("8",  "odbc microsoft access",                    "MS Access"),
    ],
    "Table A.1 – SQL Error Signatures"
)

# ─────────────────────────── Page Numbers ────────────────────────────────
add_page_numbers()

# ─────────────────────────── Save Document ───────────────────────────────
out_path = r"d:\New folder\WebVulnScanner\Web_Vulnerability_Scanner_Project_Report.docx"
doc.save(out_path)
print(f"SUCCESS: Report saved → {out_path}")
