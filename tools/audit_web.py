#!/usr/bin/env python3
"""Kontrola webu (jen čtení): projde všechny adresy ze sitemap a vypíše, co jde zlepšit.

Použití: python3 tools/audit_web.py [https://sblankouzahranice.eu] > audit.json
Kontroluje: titulek a popis pro Google, počet nadpisů H1, obrázky bez popisku (alt),
nefunkční vnitřní odkazy, velikost stránky a obrázků, odkazy na www./http verzi webu.
"""
import concurrent.futures as cf
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from html.parser import HTMLParser

WEB = (sys.argv[1] if len(sys.argv) > 1 else "https://sblankouzahranice.eu").rstrip("/")
HOST = urllib.parse.urlparse(WEB).netloc
UA = {"User-Agent": "Mozilla/5.0 (audit sblankouzahranice; Claude)", "Accept": "text/html,image/webp,*/*"}


def get(url, head=False):
    req = urllib.request.Request(url, headers=UA, method="HEAD" if head else "GET")
    t = time.time()
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            body = b"" if head else r.read()
            return r.status, r.headers, body, time.time() - t, r.url
    except urllib.error.HTTPError as e:
        return e.code, e.headers, b"", time.time() - t, url
    except Exception as e:  # timeout apod.
        return str(e)[:60], {}, b"", time.time() - t, url


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title, self.desc, self.robots, self.canon = "", None, "", None
        self.h1, self.imgs, self.links = [], [], []
        self._in = None

    def handle_starttag(self, tag, a):
        a = dict(a)
        if tag == "svg":
            self._svg = True
        elif tag == "title" and not self.title and not getattr(self, "_svg", False):
            self._in = "title"
        elif tag == "h1":
            self._in = "h1"
            self.h1.append("")
        elif tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content", "")
        elif tag == "meta" and a.get("name") == "robots":
            self.robots = a.get("content", "")
        elif tag == "link" and a.get("rel") == "canonical":
            self.canon = a.get("href")
        elif tag == "img":
            self.imgs.append((a.get("src") or a.get("data-src") or "", a.get("alt")))
        elif tag == "a" and a.get("href"):
            self.links.append(a["href"])

    def handle_endtag(self, tag):
        if tag == "svg":
            self._svg = False
        if tag in ("title", "h1"):
            self._in = None

    def handle_data(self, d):
        if self._in == "title":
            self.title += d
        elif self._in == "h1":
            self.h1[-1] += d


def sitemap_urls():
    urls, todo = [], [WEB + "/sitemap_index.xml"]
    while todo:
        _, _, body, _, _ = get(todo.pop())
        locs = re.findall(r"<loc>(.*?)</loc>", body.decode("utf-8", "replace"))
        for loc in locs:
            (todo if loc.endswith(".xml") else urls).append(loc)
    return sorted(set(urls))


def audit(url):
    st, hd, body, t, final = get(url)
    p = Page()
    p.feed(body.decode("utf-8", "replace"))
    html = body.decode("utf-8", "replace")
    return {
        "url": url, "status": st, "cas_s": round(t, 2), "kb_html": round(len(body) / 1024),
        "title": " ".join(p.title.split()), "popis": p.desc, "robots": p.robots,
        "h1": [" ".join(h.split()) for h in p.h1],
        "obrazky": len(p.imgs), "bez_alt": [s for s, alt in p.imgs if not (alt or "").strip() and s][:50],
        "odkazy": sorted({urllib.parse.urljoin(url, h).split("#")[0] for h in p.links
                          if urllib.parse.urlparse(urllib.parse.urljoin(url, h)).netloc.endswith(HOST.replace("www.", ""))}),
        "www_odkazy": sorted(set(re.findall(r"https?://www\.sblankouzahranice\.eu[^\"' <)]*", html)))[:30],
        "http_odkazy": sorted(set(re.findall(r"http://(?:www\.)?sblankouzahranice\.eu[^\"' <)]*", html)))[:30],
        "obrazky_url": sorted(set(re.findall(r"https?://[^\"' )]+?/wp-content/uploads/[^\"' )]+?\.(?:jpe?g|png|gif|webp)", html))),
    }


def main():
    urls = sitemap_urls()
    with cf.ThreadPoolExecutor(4) as ex:
        pages = list(ex.map(audit, urls))
    # vnitřní odkazy: ověř každý jen jednou
    vsechny = sorted({o for p in pages for o in p["odkazy"]
                      if "/wp-content/" not in o and "/wp-admin" not in o and "?" not in o})
    with cf.ThreadPoolExecutor(4) as ex:
        stav = dict(zip(vsechny, ex.map(lambda u: get(u, head=True)[0], vsechny)))
    obr = sorted({o for p in pages for o in p["obrazky_url"]})
    with cf.ThreadPoolExecutor(6) as ex:
        velikost = dict(zip(obr, ex.map(lambda u: get(u, head=True), obr)))
    obr_info = {u: (r[0], int(r[1].get("Content-Length") or 0) if r[1] else 0) for u, r in velikost.items()}
    for p in pages:
        p["rozbite_odkazy"] = [o for o in p["odkazy"] if o in stav and stav[o] != 200]
        p["kb_obrazky"] = round(sum(obr_info[u][1] for u in p["obrazky_url"]) / 1024)
        p["nejvetsi_obrazky"] = sorted(((round(obr_info[u][1] / 1024), u) for u in p["obrazky_url"]), reverse=True)[:5]
        del p["odkazy"], p["obrazky_url"]
    json.dump({"web": WEB, "stranek": len(pages), "odkazy_stav": {u: s for u, s in stav.items() if s != 200},
               "stranky": pages}, sys.stdout, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
