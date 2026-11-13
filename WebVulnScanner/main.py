import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scanner.sqli import SQLiScanner
from scanner.xss import XSSScanner
from scanner.headers import HeadersScanner
from scanner.traversal import TraversalScanner
from scanner.redirect import RedirectScanner
from scanner.crawler import Crawler
from report.generator import ReportGenerator


# ─────────────────────────── Colour Palette ──────────────────────────────
BG      = "#0d1117"
PANEL   = "#161b22"
BORDER  = "#30363d"
ACCENT  = "#00ff88"
TEXT    = "#c9d1d9"
MUTED   = "#8b949e"
BLUE    = "#58a6ff"
RED     = "#ff6b6b"
ORANGE  = "#f0a500"
YELLOW  = "#ffd700"
CRIT    = "#ff4444"


class WebVulnScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🛡  Web Vulnerability Scanner  v1.0")
        self.root.geometry("1200x780")
        self.root.minsize(900, 600)
        self.root.configure(bg=BG)

        self.scanning   = False
        self.scan_thread = None
        self.results    = []

        self._setup_styles()
        self._build_ui()

    # ──────────────────────── Styles ────────────────────────────────────
    def _setup_styles(self):
        s = ttk.Style()
        s.theme_use("clam")

        s.configure(".",            background=BG,    foreground=TEXT,  font=("Consolas", 10))
        s.configure("TFrame",       background=BG)
        s.configure("Panel.TFrame", background=PANEL)

        s.configure("TLabel",       background=BG,    foreground=TEXT,  font=("Consolas", 10))
        s.configure("Title.TLabel", background=BG,    foreground=ACCENT, font=("Consolas", 17, "bold"))
        s.configure("Sub.TLabel",   background=BG,    foreground=MUTED,  font=("Consolas", 9))
        s.configure("Panel.TLabel", background=PANEL, foreground=TEXT,   font=("Consolas", 10))
        s.configure("Head.TLabel",  background=PANEL, foreground=ACCENT, font=("Consolas", 10, "bold"))

        s.configure("TCheckbutton", background=BG, foreground=TEXT, font=("Consolas", 10))
        s.map("TCheckbutton", background=[("active", BG)])

        s.configure("TRadiobutton", background=BG, foreground=TEXT, font=("Consolas", 9))
        s.map("TRadiobutton",       background=[("active", BG)])

        s.configure("Scan.TButton",
            background=ACCENT, foreground=BG,
            font=("Consolas", 11, "bold"), padding=(18, 8), relief="flat")
        s.map("Scan.TButton",
            background=[("active", "#00cc6a"), ("disabled", BORDER)])

        s.configure("Stop.TButton",
            background=RED, foreground="white",
            font=("Consolas", 11, "bold"), padding=(18, 8), relief="flat")
        s.map("Stop.TButton", background=[("active", "#cc4444")])

        s.configure("Export.TButton",
            background="#264f78", foreground="white",
            font=("Consolas", 10, "bold"), padding=(10, 6), relief="flat")
        s.map("Export.TButton", background=[("active", "#1a3a5c")])

        s.configure("Clear.TButton",
            background=BORDER, foreground=TEXT,
            font=("Consolas", 10), padding=(10, 6), relief="flat")

        s.configure("TNotebook",     background=BG,    borderwidth=0)
        s.configure("TNotebook.Tab",
            background=PANEL, foreground=MUTED,
            font=("Consolas", 10, "bold"), padding=(14, 8))
        s.map("TNotebook.Tab",
            background=[("selected", BG)],
            foreground=[("selected", ACCENT)])

        s.configure("Treeview",
            background=PANEL, foreground=TEXT,
            fieldbackground=PANEL, font=("Consolas", 9),
            rowheight=25, borderwidth=0)
        s.configure("Treeview.Heading",
            background="#21262d", foreground=ACCENT,
            font=("Consolas", 9, "bold"), padding=(8, 6))
        s.map("Treeview",
            background=[("selected", "#2d333b")],
            foreground=[("selected", ACCENT)])

        s.configure("TProgressbar",
            troughcolor=PANEL, background=ACCENT,
            thickness=6, borderwidth=0)

        s.configure("TEntry",
            fieldbackground=PANEL, foreground=TEXT,
            insertcolor=ACCENT, font=("Consolas", 11),
            borderwidth=0, padding=8)

        s.configure("TScrollbar",
            background=PANEL, troughcolor=BG,
            borderwidth=0, arrowcolor=MUTED, relief="flat")

    # ──────────────────────── Top-level UI ───────────────────────────────
    def _build_ui(self):
        # Header bar
        hdr = tk.Frame(self.root, bg=PANEL, height=56)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="🛡  Web Vulnerability Scanner",
                 bg=PANEL, fg=ACCENT, font=("Consolas", 15, "bold")).pack(side="left", padx=20, pady=12)
        tk.Label(hdr, text="v1.0  ·  For Authorized & Educational Use Only",
                 bg=PANEL, fg=MUTED, font=("Consolas", 9)).pack(side="right", padx=20)

        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x")

        # Notebook
        self.nb = ttk.Notebook(self.root)
        self.nb.pack(fill="both", expand=True, padx=14, pady=(10, 0))

        self._tab_scanner()
        self._tab_results()
        self._tab_report()
        self._tab_about()

        # Status bar
        sb = tk.Frame(self.root, bg=PANEL, height=26)
        sb.pack(fill="x", side="bottom")
        sb.pack_propagate(False)
        self.status_var = tk.StringVar(value="Ready  ·  No scan running")
        tk.Label(sb, textvariable=self.status_var,
                 bg=PANEL, fg=MUTED, font=("Consolas", 9)).pack(side="left", padx=12)
        self.clock_var = tk.StringVar()
        tk.Label(sb, textvariable=self.clock_var,
                 bg=PANEL, fg=MUTED, font=("Consolas", 9)).pack(side="right", padx=12)
        self._tick()

    # ──────────────────────── SCANNER TAB ────────────────────────────────
    def _tab_scanner(self):
        frame = ttk.Frame(self.nb)
        self.nb.add(frame, text="  🔍 Scanner  ")

        # ── Left sidebar ──────────────────────────────────────────────
        sidebar = tk.Frame(frame, bg=PANEL, width=300)
        sidebar.pack(side="left", fill="y", padx=(0, 8))
        sidebar.pack_propagate(False)

        def section(parent, title, pady=(14, 6)):
            tk.Label(parent, text=title, bg=PANEL, fg=ACCENT,
                     font=("Consolas", 10, "bold")).pack(anchor="w", padx=16, pady=pady)
            tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", padx=12)

        # Target URL
        section(sidebar, "🎯  Target URL", (14, 4))
        url_f = tk.Frame(sidebar, bg=PANEL)
        url_f.pack(fill="x", padx=12, pady=(8, 4))
        self.url_var = tk.StringVar(value="https://")
        tk.Entry(url_f, textvariable=self.url_var,
                 bg="#1c2128", fg=TEXT, insertbackground=ACCENT,
                 relief="flat", font=("Consolas", 10),
                 bd=0, highlightthickness=1,
                 highlightcolor=ACCENT, highlightbackground=BORDER
                 ).pack(fill="x", ipady=6)
        tk.Label(sidebar, text="e.g.  http://testphp.vulnweb.com",
                 bg=PANEL, fg=MUTED, font=("Consolas", 8)).pack(anchor="w", padx=16, pady=(2, 0))

        # Scan modules
        section(sidebar, "⚙  Scan Modules", (14, 4))
        self.scan_opts = {}
        modules = [
            ("sql_injection", "💉  SQL Injection",          True),
            ("xss",           "⚡  XSS (Cross-Site Script)", True),
            ("headers",       "🔒  Security Headers",        True),
            ("traversal",     "📁  Directory Traversal",     True),
            ("open_redirect", "↪   Open Redirect",           True),
        ]
        for key, label, default in modules:
            var = tk.BooleanVar(value=default)
            tk.Checkbutton(sidebar, text=label, variable=var,
                           bg=PANEL, fg=TEXT, selectcolor=BG,
                           activebackground=PANEL, activeforeground=ACCENT,
                           font=("Consolas", 10)).pack(anchor="w", padx=18, pady=3)
            self.scan_opts[key] = var

        # Advanced
        section(sidebar, "🛠  Advanced Options", (12, 4))
        adv = tk.Frame(sidebar, bg=PANEL)
        adv.pack(fill="x", padx=16, pady=8)

        def row(parent, label, var, lo, hi):
            r = tk.Frame(parent, bg=PANEL)
            r.pack(fill="x", pady=3)
            tk.Label(r, text=label, bg=PANEL, fg=TEXT,
                     font=("Consolas", 10), width=14, anchor="w").pack(side="left")
            tk.Spinbox(r, from_=lo, to=hi, textvariable=var, width=5,
                       bg="#1c2128", fg=TEXT, buttonbackground="#21262d",
                       relief="flat", font=("Consolas", 10)).pack(side="left")

        self.timeout_var   = tk.IntVar(value=10)
        self.max_pages_var = tk.IntVar(value=10)
        row(adv, "Timeout (s):", self.timeout_var, 1, 60)
        row(adv, "Max Pages:", self.max_pages_var, 1, 50)

        # Buttons
        tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x", padx=12, pady=10)
        btn_f = tk.Frame(sidebar, bg=PANEL)
        btn_f.pack(fill="x", padx=12, pady=(0, 14))

        self.scan_btn = ttk.Button(btn_f, text="▶  Start Scan",
                                   style="Scan.TButton", command=self.start_scan)
        self.scan_btn.pack(fill="x", pady=(0, 6))

        self.stop_btn = ttk.Button(btn_f, text="⏹  Stop Scan",
                                   style="Stop.TButton", command=self.stop_scan,
                                   state="disabled")
        self.stop_btn.pack(fill="x")

        # ── Right: live log ───────────────────────────────────────────
        right = ttk.Frame(frame)
        right.pack(side="left", fill="both", expand=True, pady=4)

        tk.Label(right, text="📋  Live Scan Log",
                 bg=BG, fg=ACCENT, font=("Consolas", 10, "bold")).pack(anchor="w", pady=(4, 4))

        self.log = scrolledtext.ScrolledText(
            right, bg="#0a0e14", fg=TEXT, font=("Consolas", 9),
            insertbackground=ACCENT, relief="flat", wrap="word", state="disabled")
        self.log.pack(fill="both", expand=True)

        for tag, col in [("info", MUTED), ("success", ACCENT), ("warning", ORANGE),
                         ("error", RED), ("critical", CRIT), ("heading", BLUE)]:
            self.log.tag_config(tag, foreground=col)

        self.prog_var = tk.DoubleVar(value=0)
        self.prog = ttk.Progressbar(right, variable=self.prog_var, maximum=100)
        self.prog.pack(fill="x", pady=(6, 0))

    # ──────────────────────── RESULTS TAB ────────────────────────────────
    def _tab_results(self):
        frame = ttk.Frame(self.nb)
        self.nb.add(frame, text="  🚨 Results  ")

        # Severity summary bar
        bar = tk.Frame(frame, bg=PANEL, height=72)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        self.stat_lbl = {}
        sevs = [("CRITICAL", CRIT), ("HIGH", RED), ("MEDIUM", ORANGE),
                ("LOW", YELLOW), ("INFO", BLUE)]
        for sev, col in sevs:
            sf = tk.Frame(bar, bg=PANEL)
            sf.pack(side="left", padx=16, pady=10)
            cnt = tk.Label(sf, text="0", bg=PANEL, fg=col, font=("Consolas", 22, "bold"))
            cnt.pack()
            tk.Label(sf, text=sev, bg=PANEL, fg=MUTED, font=("Consolas", 8)).pack()
            self.stat_lbl[sev] = cnt

        tk.Frame(frame, bg=BORDER, height=1).pack(fill="x")

        # Filter
        filt = tk.Frame(frame, bg=BG)
        filt.pack(fill="x", pady=6, padx=8)
        tk.Label(filt, text="Filter:", bg=BG, fg=MUTED, font=("Consolas", 9)).pack(side="left", padx=(0, 6))
        self.filt_var = tk.StringVar(value="ALL")
        for sev in ["ALL", "CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]:
            ttk.Radiobutton(filt, text=sev, variable=self.filt_var,
                            value=sev, command=self.filter_results).pack(side="left", padx=4)

        # Tree
        tree_wrap = ttk.Frame(frame)
        tree_wrap.pack(fill="both", expand=True, padx=4)

        cols = ("Severity", "Type", "URL", "Parameter", "Description")
        self.tree = ttk.Treeview(tree_wrap, columns=cols, show="headings")
        widths = [80, 155, 310, 100, 420]
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col,
                              command=lambda c=col: self._sort_tree(c))
            self.tree.column(col, width=w, minwidth=60)

        vsb = ttk.Scrollbar(tree_wrap, orient="vertical",   command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_wrap, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        tree_wrap.rowconfigure(0, weight=1)
        tree_wrap.columnconfigure(0, weight=1)

        for sev, col in [("CRITICAL", CRIT), ("HIGH", RED), ("MEDIUM", ORANGE),
                         ("LOW", YELLOW), ("INFO", BLUE)]:
            self.tree.tag_configure(sev, foreground=col)

        # Detail panel
        det = tk.Frame(frame, bg=PANEL, height=110)
        det.pack(fill="x", pady=(6, 0))
        det.pack_propagate(False)
        tk.Label(det, text="Detail", bg=PANEL, fg=ACCENT,
                 font=("Consolas", 9, "bold")).pack(anchor="w", padx=12, pady=(6, 2))
        self.detail = scrolledtext.ScrolledText(
            det, bg=PANEL, fg=TEXT, font=("Consolas", 9),
            relief="flat", height=4, state="disabled")
        self.detail.pack(fill="both", expand=True, padx=12, pady=(0, 8))
        self.tree.bind("<<TreeviewSelect>>", self._show_detail)

        # Export row
        exp = tk.Frame(frame, bg=BG)
        exp.pack(fill="x", pady=6, padx=4)
        ttk.Button(exp, text="📄  Export HTML",  style="Export.TButton",
                   command=self.export_html).pack(side="left", padx=(0, 6))
        ttk.Button(exp, text="📊  Export JSON",  style="Export.TButton",
                   command=self.export_json).pack(side="left", padx=(0, 6))
        ttk.Button(exp, text="🗑  Clear",         style="Clear.TButton",
                   command=self.clear_results).pack(side="right")

    # ──────────────────────── REPORT TAB ─────────────────────────────────
    def _tab_report(self):
        frame = ttk.Frame(self.nb)
        self.nb.add(frame, text="  📄 Report  ")
        tk.Label(frame, text="HTML Report Preview",
                 bg=BG, fg=ACCENT, font=("Consolas", 10, "bold")).pack(anchor="w", padx=14, pady=(10, 4))
        self.report_txt = scrolledtext.ScrolledText(
            frame, bg="#0a0e14", fg=TEXT, font=("Consolas", 9),
            relief="flat", wrap="word", state="disabled")
        self.report_txt.pack(fill="both", expand=True, padx=14, pady=(0, 10))
        self.report_txt.config(state="normal")
        self.report_txt.insert("1.0", "Run a scan and auto-generate a report to see it here…")
        self.report_txt.config(state="disabled")

    # ──────────────────────── ABOUT TAB ──────────────────────────────────
    def _tab_about(self):
        frame = ttk.Frame(self.nb)
        self.nb.add(frame, text="  ℹ About  ")
        about = """
  ┌──────────────────────────────────────────────────────────┐
  │                                                          │
  │   🛡   Web Vulnerability Scanner  v1.0                  │
  │        Python · Tkinter · requests · BeautifulSoup       │
  │                                                          │
  ├──────────────────────────────────────────────────────────┤
  │   SCAN MODULES                                           │
  │   ─────────────────────────────────────────────────────  │
  │   💉  SQL Injection     — error-based detection          │
  │   ⚡  XSS              — reflected XSS detection         │
  │   🔒  Security Headers  — 7 headers + 4 info-leaks       │
  │   📁  Dir Traversal    — path traversal payloads         │
  │   ↪   Open Redirect    — 9 common redirect params        │
  │                                                          │
  ├──────────────────────────────────────────────────────────┤
  │   PROJECT STRUCTURE                                      │
  │   ─────────────────────────────────────────────────────  │
  │   WebVulnScanner/                                        │
  │   ├── main.py              ← GUI entry point             │
  │   ├── scanner/                                           │
  │   │   ├── crawler.py       ← URL & form crawler          │
  │   │   ├── sqli.py          ← SQL Injection scanner       │
  │   │   ├── xss.py           ← XSS scanner                 │
  │   │   ├── headers.py       ← HTTP headers auditor        │
  │   │   ├── traversal.py     ← Directory traversal         │
  │   │   └── redirect.py      ← Open redirect scanner       │
  │   ├── report/                                            │
  │   │   └── generator.py     ← HTML & JSON reports         │
  │   ├── reports/             ← Auto-saved reports          │
  │   └── requirements.txt                                   │
  │                                                          │
  ├──────────────────────────────────────────────────────────┤
  │   ✅  SAFE TEST TARGETS (intentionally vulnerable)       │
  │   ─────────────────────────────────────────────────────  │
  │   • http://testphp.vulnweb.com   (Acunetix demo)         │
  │   • http://www.itsecgames.com    (bWAPP — local)         │
  │   • http://dvwa.local            (DVWA — local)          │
  │                                                          │
  ├──────────────────────────────────────────────────────────┤
  │   ⚠   LEGAL DISCLAIMER                                  │
  │                                                          │
  │   Only scan systems you OWN or have WRITTEN PERMISSION   │
  │   to test. Unauthorized use may violate the CFAA or      │
  │   equivalent laws in your jurisdiction.                  │
  │                                                          │
  └──────────────────────────────────────────────────────────┘
"""
        txt = tk.Text(frame, bg=BG, fg=TEXT, font=("Consolas", 10),
                      relief="flat", wrap="none", state="disabled")
        txt.pack(fill="both", expand=True, padx=20, pady=20)
        txt.config(state="normal")
        txt.insert("1.0", about)
        txt.config(state="disabled")

    # ──────────────────────── Scan Logic ─────────────────────────────────
    def start_scan(self):
        url = self.url_var.get().strip()
        if not url or url in ("https://", "http://", ""):
            messagebox.showwarning("Missing URL", "Please enter a target URL.")
            return
        if not any(v.get() for v in self.scan_opts.values()):
            messagebox.showwarning("No Modules", "Select at least one scan module.")
            return

        self.scanning = True
        self.results  = []
        self.clear_results()

        self.scan_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.prog_var.set(0)
        self.nb.select(0)

        self.log.config(state="normal")
        self.log.delete("1.0", "end")
        self.log.config(state="disabled")

        self._log(f"Target : {url}", "heading")
        self._log(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "info")
        self._log("─" * 62, "info")

        self.scan_thread = threading.Thread(
            target=self._run_scan, args=(url,), daemon=True)
        self.scan_thread.start()

    def _run_scan(self, url):
        try:
            timeout   = self.timeout_var.get()
            max_pages = self.max_pages_var.get()
            opts      = {k: v.get() for k, v in self.scan_opts.items()}

            self._log("🕷  Crawling target…", "info")
            crawler = Crawler(url, max_pages=max_pages, timeout=timeout)
            urls, forms = crawler.crawl()
            self._log(f"   ✔  {len(urls)} URL(s) · {len(forms)} form(s) found", "success")
            self._set_prog(10)

            steps = sum(opts.values())
            step  = 80 / max(steps, 1)
            prog  = 10

            scanners = [
                ("sql_injection", "💉  SQL Injection",    SQLiScanner,   (url, forms)),
                ("xss",           "⚡  XSS",              XSSScanner,    (url, forms)),
                ("headers",       "🔒  Security Headers", HeadersScanner,(url,)),
                ("traversal",     "📁  Dir Traversal",    TraversalScanner,(url, forms)),
                ("open_redirect", "↪   Open Redirect",    RedirectScanner,(url, urls)),
            ]

            for key, label, Cls, args in scanners:
                if opts.get(key) and self.scanning:
                    self._log(f"\n{label} scan…", "heading")
                    findings = Cls(timeout=timeout).scan(*args)
                    self._add_findings(findings)
                    if findings:
                        self._log(f"   ⚠  {len(findings)} issue(s) found", "warning")
                    else:
                        self._log("   ✔  No issues detected", "success")
                    prog += step
                    self._set_prog(prog)

            self._set_prog(100)

            if self.scanning:
                total = len(self.results)
                highs = sum(1 for r in self.results if r["severity"] in ("CRITICAL","HIGH"))
                self._log("\n" + "─" * 62, "info")
                self._log(f"✅  Scan complete — {total} finding(s)  ({highs} critical/high)", "success")
                self._gen_report()
                self.root.after(600, lambda: self.nb.select(1))

        except Exception as e:
            import traceback
            self._log(f"❌  Error: {e}", "error")
            self._log(traceback.format_exc(), "error")
        finally:
            self.scanning = False
            self.root.after(0, self._scan_done)

    def _add_findings(self, findings):
        level = {"CRITICAL": "critical", "HIGH": "error",
                 "MEDIUM": "warning", "LOW": "warning", "INFO": "info"}
        for f in findings:
            self.results.append(f)
            self.root.after(0, lambda x=f: self._insert_row(x))
            sev = f.get("severity", "INFO")
            self._log(f"   [{sev:8}] {f.get('type','')} — {f.get('url','')[:55]}",
                      level.get(sev, "info"))

    def _insert_row(self, f):
        sev = f.get("severity", "INFO")
        self.tree.insert("", "end", tags=(sev,),
            values=(sev, f.get("type",""), f.get("url",""),
                    f.get("parameter",""), f.get("description","")))
        self._update_stats()

    def _update_stats(self):
        cnt = {s: 0 for s in self.stat_lbl}
        for r in self.results:
            s = r.get("severity","INFO")
            if s in cnt:
                cnt[s] += 1
        for s, lbl in self.stat_lbl.items():
            lbl.config(text=str(cnt[s]))

    def _scan_done(self):
        self.scan_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.status_var.set(
            f"Scan complete  ·  {len(self.results)} finding(s)  "
            f"({sum(1 for r in self.results if r.get('severity') in ('CRITICAL','HIGH'))} critical/high)")

    def stop_scan(self):
        self.scanning = False
        self._log("\n⏹  Stopped by user.", "warning")
        self.stop_btn.config(state="disabled")
        self.scan_btn.config(state="normal")
        self.status_var.set("Scan stopped by user")

    # ──────────────────────── Results helpers ────────────────────────────
    def filter_results(self):
        sev = self.filt_var.get()
        for item in self.tree.get_children():
            self.tree.delete(item)
        for r in self.results:
            if sev == "ALL" or r.get("severity") == sev:
                s = r.get("severity","INFO")
                self.tree.insert("", "end", tags=(s,),
                    values=(s, r.get("type",""), r.get("url",""),
                            r.get("parameter",""), r.get("description","")))

    def _sort_tree(self, col):
        items = [(self.tree.set(i, col), i) for i in self.tree.get_children()]
        items.sort()
        for idx, (_, i) in enumerate(items):
            self.tree.move(i, "", idx)

    def _show_detail(self, _):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0], "values")
        self.detail.config(state="normal")
        self.detail.delete("1.0", "end")
        for r in self.results:
            if r.get("type","") == vals[1] and r.get("url","") == vals[2]:
                self.detail.insert("1.0",
                    f"Severity  : {r.get('severity','')}\n"
                    f"Type      : {r.get('type','')}\n"
                    f"URL       : {r.get('url','')}\n"
                    f"Parameter : {r.get('parameter','')}\n"
                    f"Payload   : {r.get('payload','N/A')}\n"
                    f"Evidence  : {r.get('evidence','N/A')}\n"
                    f"Detail    : {r.get('description','')}")
                break
        self.detail.config(state="disabled")

    def clear_results(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for lbl in self.stat_lbl.values():
            lbl.config(text="0")
        self.results = []

    # ──────────────────────── Report helpers ─────────────────────────────
    def _gen_report(self):
        if not self.results:
            return
        gen  = ReportGenerator(self.results, self.url_var.get())
        html = gen.generate_html()

        self.report_txt.config(state="normal")
        self.report_txt.delete("1.0", "end")
        preview = html[:6000] + "\n\n<!-- truncated — export for full report -->"
        self.report_txt.insert("1.0", preview)
        self.report_txt.config(state="disabled")

        rdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
        os.makedirs(rdir, exist_ok=True)
        fname = datetime.now().strftime("report_%Y%m%d_%H%M%S.html")
        path  = os.path.join(rdir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        self._log(f"📄  Auto-saved → {path}", "success")

    def export_html(self):
        if not self.results:
            messagebox.showinfo("No Results", "Run a scan first.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML", "*.html"), ("All", "*.*")],
            initialfile=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
        if path:
            gen = ReportGenerator(self.results, self.url_var.get())
            with open(path, "w", encoding="utf-8") as f:
                f.write(gen.generate_html())
            messagebox.showinfo("Done", f"Saved to:\n{path}")

    def export_json(self):
        if not self.results:
            messagebox.showinfo("No Results", "Run a scan first.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json"), ("All", "*.*")],
            initialfile=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        if path:
            gen = ReportGenerator(self.results, self.url_var.get())
            with open(path, "w", encoding="utf-8") as f:
                f.write(gen.generate_json())
            messagebox.showinfo("Done", f"Saved to:\n{path}")

    # ──────────────────────── Utilities ──────────────────────────────────
    def _log(self, msg, level="info"):
        def _do():
            self.log.config(state="normal")
            ts = datetime.now().strftime("%H:%M:%S")
            self.log.insert("end", f"[{ts}] ", "info")
            self.log.insert("end", f"{msg}\n", level)
            self.log.see("end")
            self.log.config(state="disabled")
        self.root.after(0, _do)

    def _set_prog(self, v):
        self.root.after(0, lambda: self.prog_var.set(min(v, 100)))

    def _tick(self):
        self.clock_var.set(datetime.now().strftime("%Y-%m-%d  %H:%M:%S"))
        self.root.after(1000, self._tick)


# ─────────────────────────────── Entry ───────────────────────────────────
def main():
    root = tk.Tk()
    app = WebVulnScannerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
