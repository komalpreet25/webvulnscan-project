import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

REDIRECT_PAYLOADS = [
    "https://evil.com",
    "//evil.com",
    "https://evil.com/%2F..",
    "/\\evil.com",
]

REDIRECT_PARAMS = [
    "redirect", "url", "next", "return", "returnUrl", "redir",
    "goto", "target", "destination", "continue", "forward", "back",
    "ref", "callback", "out", "view", "logoutUrl", "image_url", "to",
]


class RedirectScanner:
    def __init__(self, timeout=10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "WebVulnScanner/1.0 (Educational Tool)"
        })

    def scan(self, base_url, urls):
        findings = []
        all_urls = list(set([base_url] + urls))
        for url in all_urls:
            parsed = urlparse(url)
            params = parse_qs(parsed.query)
            # Test existing params that match redirect names
            for param in list(params.keys()):
                if any(rp.lower() == param.lower() for rp in REDIRECT_PARAMS):
                    for payload in REDIRECT_PAYLOADS:
                        result = self._test_redirect(parsed, params, param, payload)
                        if result:
                            findings.append(result)
                            break
            # Probe common redirect params
            for rp in REDIRECT_PARAMS[:6]:
                if rp not in params:
                    for payload in REDIRECT_PAYLOADS[:2]:
                        test_params = dict(params)
                        test_params[rp] = [payload]
                        new_query = urlencode(test_params, doseq=True)
                        test_url = urlunparse(parsed._replace(query=new_query))
                        try:
                            resp = self.session.get(test_url, timeout=self.timeout,
                                                    allow_redirects=False)
                            if resp.status_code in (301, 302, 303, 307, 308):
                                location = resp.headers.get("Location", "")
                                if "evil.com" in location or location.startswith("//"):
                                    findings.append({
                                        "type": "Open Redirect",
                                        "severity": "MEDIUM",
                                        "url": test_url,
                                        "parameter": rp,
                                        "payload": payload,
                                        "evidence": f"HTTP {resp.status_code} → Location: {location}",
                                        "description": f"Open redirect via '{rp}' parameter — server redirects to attacker-controlled URL"
                                    })
                                    break
                        except Exception:
                            pass
        return findings

    def _test_redirect(self, parsed, params, param, payload):
        test_params = dict(params)
        test_params[param] = [payload]
        new_query = urlencode(test_params, doseq=True)
        test_url = urlunparse(parsed._replace(query=new_query))
        try:
            resp = self.session.get(test_url, timeout=self.timeout, allow_redirects=False)
            if resp.status_code in (301, 302, 303, 307, 308):
                location = resp.headers.get("Location", "")
                if "evil.com" in location:
                    return {
                        "type": "Open Redirect",
                        "severity": "MEDIUM",
                        "url": test_url,
                        "parameter": param,
                        "payload": payload,
                        "evidence": f"HTTP {resp.status_code} → Location: {location}",
                        "description": f"Open redirect via parameter '{param}' — user can be redirected to external site"
                    }
        except Exception:
            pass
        return None
