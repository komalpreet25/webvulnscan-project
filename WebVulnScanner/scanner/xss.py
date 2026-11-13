import requests
import html
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "<svg onload=alert('XSS')>",
    "'\"><script>alert('XSS')</script>",
    "<body onload=alert('XSS')>",
    "<iframe src=javascript:alert('XSS')>",
    "<input onfocus=alert('XSS') autofocus>",
    "<details open ontoggle=alert('XSS')>",
]


class XSSScanner:
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
            for payload in XSS_PAYLOADS:
                test_params = dict(params)
                test_params[param] = [payload]
                new_query = urlencode(test_params, doseq=True)
                test_url = urlunparse(parsed._replace(query=new_query))
                try:
                    resp = self.session.get(test_url, timeout=self.timeout)
                    if self._is_reflected(payload, resp.text):
                        findings.append({
                            "type": "Reflected XSS",
                            "severity": "HIGH",
                            "url": test_url,
                            "parameter": param,
                            "payload": payload,
                            "evidence": "Payload reflected unencoded in HTTP response",
                            "description": f"XSS payload reflected in URL parameter '{param}' — user input echoed without sanitization"
                        })
                        break
                except Exception:
                    pass
        return findings

    def _scan_form(self, form):
        findings = []
        for inp in form["inputs"]:
            for payload in XSS_PAYLOADS:
                data = {i["name"]: i["value"] for i in form["inputs"]}
                data[inp["name"]] = payload
                try:
                    if form["method"] == "POST":
                        resp = self.session.post(form["url"], data=data, timeout=self.timeout)
                    else:
                        resp = self.session.get(form["url"], params=data, timeout=self.timeout)
                    if self._is_reflected(payload, resp.text):
                        findings.append({
                            "type": "Reflected XSS",
                            "severity": "HIGH",
                            "url": form["url"],
                            "parameter": inp["name"],
                            "payload": payload,
                            "evidence": "XSS payload reflected unencoded in form response",
                            "description": f"Reflected XSS via form field '{inp['name']}' — no output encoding detected"
                        })
                        break
                except Exception:
                    pass
        return findings

    def _is_reflected(self, payload, response_text):
        if payload in response_text:
            encoded = html.escape(payload)
            if encoded != payload and encoded in response_text and payload not in response_text:
                return False
            return True
        return False
