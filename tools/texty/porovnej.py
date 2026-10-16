import sys, re, json, difflib
sys.path.insert(0, sys.argv[1]); from bloky import bloky
norm = lambda s: re.findall(r"\w+", s.lower())
def porovnej(stara, nova):
    O, N = bloky(stara), bloky(nova)
    On = [norm(o) for o in O]
    vsechny_stare = set(map(lambda x: " ".join(x), On))
    radky, pouzite = [], set()
    for n in N:
        nw = norm(n)
        if not nw: continue
        best = (0, 0, 1, 0, 0)
        for i in range(len(O)):
            for k in (1, 2, 3):
                cand = sum(On[i:i+k], [])
                sm = difflib.SequenceMatcher(None, nw, cand, autojunk=False)
                m = sum(b.size for b in sm.get_matching_blocks())
                cov = m / len(nw); prec = m / max(1, len(cand))
                score = cov * 0.7 + prec * 0.3
                if score > best[0]: best = (score, i, k, cov, prec)
        sc, i, k, cov, prec = best
        txt_old = " ".join(O[i:i+k])
        if n == txt_old: pouzite.update(range(i, i+k)); continue
        if cov >= 0.55 and (len(sum(On[i:i+k], [])) <= 3 * len(nw) or " ".join(nw) in " ".join(sum(On[i:i+k], []))):
            pouzite.update(range(i, i+k))
            radky.append({"nove": n, "puvodne": txt_old, "jen_pismena": norm(n) == norm(txt_old)})
        else:
            radky.append({"nove": n, "puvodne": "", "jen_pismena": False})
    vsechny_nove = " ".join(" ".join(norm(n)) for n in N)
    vypustene = [o for j, o in enumerate(O) if j not in pouzite and len(o) > 15 and " ".join(On[j]) not in vsechny_nove]
    return radky, vypustene
r, v = porovnej(sys.argv[2], sys.argv[3])
json.dump({"radky": r, "vypustene": v}, open(sys.argv[4], "w"), ensure_ascii=False, indent=1)
print(len(r), "změn,", sum(x["jen_pismena"] for x in r), "jen písmena,", sum(not x["puvodne"] for x in r), "nových,", len(v), "vypuštěných")
