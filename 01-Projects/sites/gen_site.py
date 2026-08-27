import json, re, os, sys

TEMPLATE = "/Users/olesiarasing/Obsidian/mare-fiori.it/index.html"
BASE = "/Users/olesiarasing/Obsidian/"

TEMPLATE_COLORS = {
 "light": {"paper":"#FBF6F0","paper-2":"#F4EAE0","ink":"#3A2E2A","muted":"#7E6E64","line":"#E4D6C8","terracotta":"#C97B5A","terracotta-d":"#A85C3E","sea":"#2F6B7A","sea-light":"#7FB0BC","coral":"#E58E78","pink":"#F0D3CE","gold":"#C7A36A","gold-soft":"#E8D6B4"},
 "dark": {"paper":"#1B1512","paper-2":"#241C17","ink":"#F3E9E0","muted":"#B9A89C","line":"#3A2E27","terracotta":"#D98C6B","terracotta-d":"#C0704E","sea":"#7FB0BC","sea-light":"#9CC3CD","coral":"#E58E78","pink":"#5A4038","gold":"#D9B779","gold-soft":"#4A3A2A"}
}

def build(txt, cfg):
    # palette (light + dark)
    for mode in ("light","dark"):
        for var, old in TEMPLATE_COLORS[mode].items():
            txt = txt.replace(old, cfg["palette"][mode][var])
    # brand
    txt = txt.replace("Marefiori", cfg["brand"])
    txt = txt.replace('<span>Mare</span>fiori', cfg["brand"])
    # title + meta
    txt = txt.replace("<title>Marefiori — Fiori di Porto Antico di Genova</title>", "<title>"+cfg["title"]+"</title>")
    txt = txt.replace('content="Marefiori is a flower atelier on the waterfront of Porto Antico di Genova — bouquets, event florals, and honeymoon & anniversary arrangements under the warm light of an August Ligurian afternoon."', 'content="'+cfg["meta_desc"]+'"')
    txt = txt.replace('content="fiori Genova, fioraio Porto Antico, bouquet Liguria, matrimoni Genova, fiori eventi, consegna fiori"', 'content="'+cfg["meta_keys"]+'"')
    txt = txt.replace('content="Marefiori — Fiori di Porto Antico di Genova"', 'content="'+cfg["og_title"]+'"')
    txt = txt.replace('content="A flower atelier on the Ligurian waterfront — bouquets, event florals, honeymoon arrangements."', 'content="'+cfg["og_desc"]+'"')
    # contact details (BEFORE domain swaps so emails aren't clobbered)
    digits = re.sub(r"\D", "", cfg["phone"])
    txt = re.sub(r'phone:\s*"[^"]*"', 'phone: "+%s"' % digits, txt)
    txt = re.sub(r'whatsapp:\s*"[^"]*"', 'whatsapp: "+%s"' % digits, txt)
    txt = re.sub(r'"telephone":\s*"[^"]*"', '"telephone": "+%s"' % digits, txt)
    txt = txt.replace("+39 345 023 4084", cfg["phone"])     # static display + chatbot fallback text
    txt = txt.replace("ciao@mare-fiori.it", cfg["email"])
    txt = txt.replace("hello@mare-fiori.it", cfg["email"])
    txt = txt.replace("Ciao Marefiori! I'd like to ask about a bouquet.", cfg["waText"])
    # domain / slug (after contact so emails aren't clobbered)
    txt = txt.replace("https://mare-fiori.it/", cfg["domain"])
    txt = txt.replace("mare-fiori.it", cfg["domain"])
    txt = txt.replace("mare-fiori", cfg["slug"])
    # map
    txt = re.sub(r'mapEmbed:"[^"]*"', 'mapEmbed:"'+cfg["mapEmbed"]+'"', txt)
    txt = re.sub(r'src="https://www.openstreetmap.org/export/embed.html[^"]*"', 'src="'+cfg["mapEmbed"]+'"', txt)
    txt = re.sub(r'mlat=44\.4056&mlon=8\.9298#map=15/44\.4056/8\.9298', 'mlat=%s&mlon=%s#map=15/%s/%s' % (cfg["lat"],cfg["lon"],cfg["lat"],cfg["lon"]), txt)
    # JSON-LD
    txt = txt.replace('"@type": "Florist"', '"@type": "'+cfg["schema"]+'"')
    txt = txt.replace('"description": "Flower atelier at Porto Antico di Genova — bouquets, event florals, honeymoon & anniversary arrangements."', '"description": "'+cfg["jsonld_desc"]+'"')
    txt = txt.replace('https://images.pexels.com/photos/29601972/pexels-photo-29601972.jpeg', cfg["jsonld_image"])
    txt = txt.replace('"streetAddress": "Porto Antico di Genova, Calata Falcone C.A."', '"streetAddress": "'+cfg["address"]+'"')
    txt = txt.replace('"addressLocality": "Genova"', '"addressLocality": "'+cfg["city"]+'"')
    txt = txt.replace('"postalCode": "16124"', '"postalCode": "'+cfg["zip"]+'"')
    txt = txt.replace('"addressRegion": "GE"', '"addressRegion": "'+cfg["region"]+'"')
    txt = txt.replace('"latitude": 44.4056, "longitude": 8.9298', '"latitude": '+str(cfg["lat"])+', "longitude": '+str(cfg["lon"]))
    txt = txt.replace('"openingHours": ["Tu-Su 09:00-19:00"]', '"openingHours": '+json.dumps(cfg["hours"]))
    txt = txt.replace('"areaServed": "Genova, Liguria"', '"areaServed": "'+cfg["areaServed"]+'"')
    # i18n + data arrays
    txt = re.sub(r'const I18N = \{[\s\S]*?\n\};', "const I18N = " + json.dumps(cfg["i18n"], ensure_ascii=False, indent=2) + ";", txt, count=1)
    coll_js = "const COLLECTIONS = [\n" + ",\n".join(
        '  { n:"%s", img:PEX(%s), titleKey:"%s", textKey:"%s" }' % (c["n"], c["img"], c["titleKey"], c["textKey"]) for c in cfg["collections"]) + "\n];"
    txt = re.sub(r'const COLLECTIONS = \[[\s\S]*?\n\];', coll_js, txt, count=1)
    gal_js = "const GALLERY = [\n" + ",\n".join(
        '  { capKey:"%s", img:PEX(%s), full:PEX(%s,1600)%s }' % (g["capKey"], g["img"], g["img"], ", user:true" if g.get("user") else "") for g in cfg["gallery"]) + "\n];"
    txt = re.sub(r'const GALLERY = \[[\s\S]*?\n\];', gal_js, txt, count=1)
    blog_js = "const BLOG = [\n" + ",\n".join(
        '  { qKey:"%s", aKey:"%s" }' % (b["qKey"], b["aKey"]) for b in cfg["blog"]) + "\n];"
    txt = re.sub(r'const BLOG = \[[\s\S]*?\n\];', blog_js, txt, count=1)
    # hero poster + story bg
    txt = txt.replace("https://images.pexels.com/photos/22227592/pexels-photo-22227592.jpeg?auto=compress&cs=tinysrgb&w=1600&q=80", cfg["heroPoster"])
    txt = txt.replace("https://images.pexels.com/photos/11849088/pexels-photo-11849088.jpeg?auto=compress&cs=tinysrgb&w=1280&q=80", cfg["storyImg"])
    # whatsapp message
    txt = txt.replace("I'd like to ask about a bouquet.", cfg["waText"])
    return txt

def write_site(cfg):
    txt = open(TEMPLATE, encoding="utf-8").read()
    txt = build(txt, cfg)
    out = os.path.join(BASE, cfg["slug"])
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out,"index.html"),"w",encoding="utf-8").write(txt)
    initial = cfg["brand"][0]
    fav = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
           '<rect width="64" height="64" rx="14" fill="%s"/>'
           '<text x="32" y="44" font-size="34" font-family="Georgia, serif" fill="#fff" text-anchor="middle">%s</text></svg>'
           ) % (cfg["palette"]["light"]["terracotta"], initial)
    open(os.path.join(out,"favicon.svg"),"w").write(fav)
    open(os.path.join(out,"robots.txt"),"w").write("User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n" % cfg["domain"])
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for a,p in [("", "1.0"), ("#story","0.7"), ("#collections","0.8"), ("#gallery","0.7"), ("#visit","0.8"), ("#blog","0.7"), ("#book","0.9")]:
        sm += '  <url><loc>%s%s</loc><priority>%s</priority></url>\n' % (cfg["domain"], a, p)
    sm += "</urlset>\n"
    open(os.path.join(out,"sitemap.xml"),"w").write(sm)
    print("built", cfg["slug"])

if __name__ == "__main__":
    import glob
    sites = {}
    for f in glob.glob(os.path.join(BASE,"sites","*.json")):
        d = json.load(open(f, encoding="utf-8"))
        sites[d["slug"]] = d
    for slug in sys.argv[1:]:
        write_site(sites[slug])
