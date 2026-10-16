import re, sys, html
from html.parser import HTMLParser
BLOK = {"p","li","h1","h2","h3","h4","h5","h6","a","button","td","th","figcaption","blockquote","summary"}
class P(HTMLParser):
    def __init__(s): super().__init__(); s.out=[]; s.cur=[]; s.skip=0; s.inmain=False
    def handle_starttag(s,t,a):
        a=dict(a)
        if t in("script","style","svg","noscript"): s.skip+=1
        if t in BLOK: s.flush()
    def handle_endtag(s,t):
        if t in("script","style","svg","noscript"): s.skip-=1
        if t in BLOK or t=="br": s.flush()
    def handle_data(s,d):
        if not s.skip: s.cur.append(d)
    def flush(s):
        t=" ".join("".join(s.cur).split()); s.cur=[]
        if len(t)>3: s.out.append(t)
def bloky(f):
    h=open(f,encoding="utf-8",errors="replace").read()
    # jen obsah stránky: bez hlavičky a patičky
    m=re.search(r'<div[^>]+data-elementor-type="wp-page".*?(?=<footer|data-elementor-type="footer"|data-elementor-type="wp-post")', h, re.S) or re.search(r'<main.*?</main>', h, re.S)
    p=P(); p.feed(m.group(0) if m else h); p.flush()
    seen=[]; [seen.append(x) for x in p.out if x not in seen]
    return seen
