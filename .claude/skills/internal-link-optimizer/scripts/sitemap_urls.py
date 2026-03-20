#!/usr/bin/env python3
import sys
import xml.etree.ElementTree as ET
from urllib.request import Request, urlopen


def fetch(url: str) -> bytes:
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=15) as resp:
        return resp.read()


def parse_sitemap(xml_bytes: bytes) -> list[str]:
    root = ET.fromstring(xml_bytes)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

    urls = [loc.text.strip() for loc in root.findall(".//sm:url/sm:loc", ns) if loc.text]
    if urls:
        return urls

    # fallback for sitemapindex or non-namespaced XML
    urls = [elem.text.strip() for elem in root.findall(".//{*}loc") if elem.text]
    return urls


def main() -> int:
    if len(sys.argv) != 2:
        print('Usage: python3 scripts/sitemap_urls.py "https://example.com/sitemap.xml"')
        return 1

    url = sys.argv[1]
    try:
        xml_bytes = fetch(url)
        urls = parse_sitemap(xml_bytes)
    except Exception as exc:
        print(f"Failed to read sitemap: {exc}")
        return 1

    if not urls:
        print("No URLs found.")
        return 1

    for item in urls:
        print(item)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
