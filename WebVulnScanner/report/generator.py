import json
from datetime import datetime


class ReportGenerator:
    def __init__(self, results, target_url):
        self.results = results
        self.target_url = target_url
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def generate_html(self):
        counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
        for r in self.results:
            sev = r.get("severity", "INFO")
            if sev in counts:
                counts[sev] += 1

        risk = "SAFE"
        if counts["CRITICAL"] > 0:
            risk = "CRITICAL"
        elif counts["HIGH"] > 0:
            risk = "HIGH"
        elif counts["MEDIUM"] > 0:
            risk = "MEDIUM"
        elif counts["LOW"] > 0:
            risk = "LOW"

        risk_color = {
            "CRITICAL": "#ff4444", "HIGH": "#ff6b6b",
            "MEDIUM": "#f0a500", "LOW": "#ffd700", "SAFE": "#00ff88"
        }.get(risk, "#00ff88")

        sev_colors = {
            "CRITICAL": "#ff4444", "HIGH": "#ff6b6b",
            "MEDIUM": "#f0a500", "LOW": "#ffd700", "INFO": "#58a6ff"
        }

        rows = ""
        for r in self.results:
            sev = r.get("severity", "INFO")
            color = sev_colors.get(sev, "#c9d1d9")
            rows += f"""
            <tr>
              <td><span class="badge" style="background:{color}22;color:{color};border:1px solid {color}">{sev}</span></td>
              <td>{r.get('type','')}</td>
              <td style="word-break:break-all;font-size:11px">{r.get('url','')}</td>
              <td>{r.get('parameter','')}</td>
              <td>{r.get('description','')}</td>
              <td><code>{r.get('payload','N/A')}</code></td>
            </tr>"""

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Vulnerability Scan Report — {self.target_url}</title>
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  body{{background:#0d1117;color:#c9d1d9;font-family:'Consolas',monospace;font-size:13px}}
  .header{{background:#161b22;padding:28px 40px;border-bottom:1px solid #30363d}}
  .header h1{{color:#00ff88;font-size:22px;margin-bottom:6px}}
  .header p{{color:#8b949e;font-size:12px}}
  .container{{max-width:1300px;margin:28px auto;padding:0 40px}}
  .summary{{display:flex;gap:16px;margin-bottom:28px;flex-wrap:wrap;align-items:center}}
  .risk-badge{{padding:14px 24px;border-radius:8px;font-size:16px;font-weight:bold;
    background:{risk_color}22;color:{risk_color};border:1px solid {risk_color}}}
  .stat-card{{background:#161b22;padding:16px 24px;border-radius:8px;
    border:1px solid #30363d;text-align:center;min-width:80px}}
  .stat-card .count{{font-size:32px;font-weight:bold}}
  .stat-card .label{{color:#8b949e;font-size:10px;margin-top:4px;letter-spacing:1px}}
  h2{{color:#c9d1d9;font-size:15px;margin-bottom:14px;padding-bottom:8px;
    border-bottom:1px solid #30363d}}
  table{{width:100%;border-collapse:collapse;background:#161b22;border-radius:8px;overflow:hidden}}
  th{{background:#21262d;color:#00ff88;padding:11px 14px;text-align:left;
    font-size:11px;letter-spacing:1px}}
  td{{padding:10px 14px;border-bottom:1px solid #21262d;vertical-align:top}}
  tr:last-child td{{border-bottom:none}}
  tr:hover{{background:#21262d}}
  code{{background:#21262d;padding:2px 7px;border-radius:4px;color:#f0a500;font-size:11px}}
  .badge{{padding:3px 10px;border-radius:12px;font-size:11px;font-weight:bold}}
  .footer{{text-align:center;padding:24px;color:#8b949e;font-size:11px;margin-top:20px;
    border-top:1px solid #30363d}}
  .no-findings{{background:#161b22;border:1px solid #30363d;border-radius:8px;
    padding:40px;text-align:center;color:#8b949e}}
</style>
</head>
<body>
<div class="header">
  <h1>🛡&nbsp; Web Vulnerability Scan Report</h1>
  <p>Target: <strong style="color:#c9d1d9">{self.target_url}</strong> &nbsp;|&nbsp; Scanned: {self.timestamp}</p>
</div>
<div class="container">
  <div class="summary">
    <div class="risk-badge">⚡ Overall Risk: {risk}</div>
    <div class="stat-card"><div class="count" style="color:#ff4444">{counts['CRITICAL']}</div><div class="label">CRITICAL</div></div>
    <div class="stat-card"><div class="count" style="color:#ff6b6b">{counts['HIGH']}</div><div class="label">HIGH</div></div>
    <div class="stat-card"><div class="count" style="color:#f0a500">{counts['MEDIUM']}</div><div class="label">MEDIUM</div></div>
    <div class="stat-card"><div class="count" style="color:#ffd700">{counts['LOW']}</div><div class="label">LOW</div></div>
    <div class="stat-card"><div class="count" style="color:#58a6ff">{counts['INFO']}</div><div class="label">INFO</div></div>
    <div class="stat-card"><div class="count" style="color:#00ff88">{len(self.results)}</div><div class="label">TOTAL</div></div>
  </div>

  <h2>📋 Findings ({len(self.results)} total)</h2>
  {'<table><thead><tr><th>SEVERITY</th><th>TYPE</th><th>URL</th><th>PARAMETER</th><th>DESCRIPTION</th><th>PAYLOAD</th></tr></thead><tbody>' + rows + '</tbody></table>' if self.results else '<div class="no-findings">✅ No vulnerabilities detected.</div>'}

  <div class="footer">
    <p>⚠&nbsp; This report is for educational and <strong>authorized</strong> penetration testing only.</p>
    <p style="margin-top:6px">Generated by Web Vulnerability Scanner v1.0</p>
  </div>
</div>
</body>
</html>"""

    def generate_json(self):
        return json.dumps({
            "target": self.target_url,
            "timestamp": self.timestamp,
            "summary": {
                "total": len(self.results),
                "critical": sum(1 for r in self.results if r.get("severity") == "CRITICAL"),
                "high": sum(1 for r in self.results if r.get("severity") == "HIGH"),
                "medium": sum(1 for r in self.results if r.get("severity") == "MEDIUM"),
                "low": sum(1 for r in self.results if r.get("severity") == "LOW"),
                "info": sum(1 for r in self.results if r.get("severity") == "INFO"),
            },
            "findings": self.results
        }, indent=2)
