import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque


class Crawler:
    def __init__(self, base_url, max_pages=10, timeout=10):
        self.base_url = base_url
        self.max_pages = max_pages
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "WebVulnScanner/1.0 (Educational Tool)"
        })

    def crawl(self):
        visited = set()
        to_visit = deque([self.base_url])
        all_urls = []
        all_forms = []
        base_domain = urlparse(self.base_url).netloc

        while to_visit and len(visited) < self.max_pages:
            url = to_visit.popleft()
            if url in visited:
                continue
            visited.add(url)
            try:
                resp = self.session.get(url, timeout=self.timeout, allow_redirects=True)
                if "text/html" not in resp.headers.get("Content-Type", ""):
                    continue
                all_urls.append(url)
                soup = BeautifulSoup(resp.text, "html.parser")
                for form in soup.find_all("form"):
                    form_data = self._parse_form(form, url)
                    if form_data:
                        all_forms.append(form_data)
                for a in soup.find_all("a", href=True):
                    href = urljoin(url, a["href"])
                    parsed = urlparse(href)
                    if (parsed.netloc == base_domain and
                            href not in visited and
                            href not in to_visit and
                            "#" not in href):
                        to_visit.append(href)
            except Exception:
                pass

        return all_urls, all_forms

    def _parse_form(self, form, page_url):
        try:
            action = form.get("action", "")
            method = form.get("method", "get").upper()
            action_url = urljoin(page_url, action) if action else page_url
            inputs = []
            for inp in form.find_all(["input", "textarea", "select"]):
                name = inp.get("name", "")
                val = inp.get("value", "test")
                itype = inp.get("type", "text")
                if name and itype not in ("submit", "button", "image", "reset"):
                    inputs.append({"name": name, "value": val, "type": itype})
            if inputs:
                return {"url": action_url, "method": method,
                        "inputs": inputs, "page_url": page_url}
        except Exception:
            pass
        return None
