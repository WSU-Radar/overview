"""Check the built site, including links under a GitHub Pages project path."""

from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids = set()
        self.links = []
        self.title = False
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "title":
            self.title = True
        for attr in ("href", "src"):
            if attrs.get(attr):
                self.links.append(attrs[attr])


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site").resolve()
    pages = {path: Page(path) for path in sorted(root.glob("*.html"))}
    errors = []
    links = 0
    if len(pages) != 19 or root / "index.html" not in pages:
        errors.append("Expected index.html and all 18 document pages")

    def check(source, link):
        nonlocal links
        url = urlsplit(link)
        if url.scheme or url.netloc:
            return
        links += 1
        label = f"{source.relative_to(root)}: {link}"
        if url.path.startswith("/"):
            errors.append(f"{label}: root-relative link breaks the /overview/ path")
            return
        target = (source.parent / unquote(url.path)).resolve() if url.path else source
        if not target.is_relative_to(root):
            errors.append(f"{label}: link escapes the published website")
        elif not target.is_file():
            errors.append(f"{label}: missing file")
        elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
            errors.append(f"{label}: missing anchor")

    for path, page in pages.items():
        if not page.title:
            errors.append(f"{path.name}: missing page title")
        for link in page.links:
            check(path, link)
    for path in sorted(root.rglob("*.css")):
        for link in re.findall(r"url\(\s*['\"]?([^)'\"\s]+)['\"]?\s*\)", path.read_text(encoding="utf-8")):
            check(path, link)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        raise SystemExit(1)
    print(f"Checked {len(pages)} pages and {links} local links, anchors and assets.")


if __name__ == "__main__":
    main()
