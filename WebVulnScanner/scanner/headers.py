import requests

REQUIRED_HEADERS = {
    "Strict-Transport-Security": {
        "severity": "MEDIUM",
        "description": "Missing HSTS header. Prevents protocol downgrade attacks and cookie hijacking. Add: Strict-Transport-Security: max-age=31536000; includeSubDomains"
    },
    "X-Content-Type-Options": {
        "severity": "LOW",
        "description": "Missing X-Content-Type-Options. Browser may MIME-sniff responses. Add: X-Content-Type-Options: nosniff"
    },
    "X-Frame-Options": {
        "severity": "MEDIUM",
        "description": "Missing X-Frame-Options. Site may be vulnerable to Clickjacking attacks. Add: X-Frame-Options: DENY"
    },
    "Content-Security-Policy": {
        "severity": "HIGH",
        "description": "Missing Content-Security-Policy (CSP). Increases XSS attack surface. Define a strict CSP to restrict resource origins."
    },
    "X-XSS-Protection": {
        "severity": "LOW",
        "description": "Missing X-XSS-Protection (useful for older browsers). Add: X-XSS-Protection: 1; mode=block"
    },
    "Referrer-Policy": {
        "severity": "LOW",
        "description": "Missing Referrer-Policy. Sensitive URL data may leak to third parties. Add: Referrer-Policy: strict-origin-when-cross-origin"
    },
    "Permissions-Policy": {
        "severity": "LOW",
        "description": "Missing Permissions-Policy. Browser features (camera, mic, GPS) are unrestricted. Add: Permissions-Policy: geolocation=(), microphone=()"
    },
}

DANGEROUS_HEADERS = {
    "Server": "Server header exposes version info to attackers. Remove or obscure it.",
    "X-Powered-By": "X-Powered-By reveals technology stack. Remove to reduce fingerprinting.",
    "X-AspNet-Version": "X-AspNet-Version exposes .NET version. Remove this header.",
    "X-AspNetMvc-Version": "X-AspNetMvc-Version reveals MVC version. Remove this header.",
}


class HeadersScanner:
    def __init__(self, timeout=10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "WebVulnScanner/1.0 (Educational Tool)"
        })

    def scan(self, url):
        findings = []
        try:
            resp = self.session.get(url, timeout=self.timeout)
            headers_lower = {k.lower(): v for k, v in resp.headers.items()}

            for header, info in REQUIRED_HEADERS.items():
                if header.lower() not in headers_lower:
                    findings.append({
                        "type": f"Missing Header: {header}",
                        "severity": info["severity"],
                        "url": url,
                        "parameter": header,
                        "payload": "N/A",
                        "evidence": f"Header '{header}' absent from HTTP response",
                        "description": info["description"]
                    })

            for header, detail in DANGEROUS_HEADERS.items():
                if header.lower() in headers_lower:
                    findings.append({
                        "type": f"Info Disclosure: {header}",
                        "severity": "INFO",
                        "url": url,
                        "parameter": header,
                        "payload": "N/A",
                        "evidence": f"{header}: {headers_lower[header.lower()]}",
                        "description": detail
                    })

            if url.startswith("http://"):
                findings.append({
                    "type": "Insecure Protocol (HTTP)",
                    "severity": "MEDIUM",
                    "url": url,
                    "parameter": "Protocol",
                    "payload": "N/A",
                    "evidence": "Site served over HTTP instead of HTTPS",
                    "description": "HTTP transmits data in plaintext. Migrate to HTTPS with a valid TLS certificate."
                })

        except Exception:
            pass
        return findings
