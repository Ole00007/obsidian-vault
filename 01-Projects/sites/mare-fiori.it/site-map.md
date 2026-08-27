# Marefiori — Site Map

Single-page site; sections are in-page anchors. All reachable from the header nav and footer.

```
/  (index.html)
├── Header
│   ├── Brand (Marefiori)
│   ├── Nav: Story · Collections · Gallery · Visit · Journal · Book
│   ├── WhatsApp icon  (wa.me/+393450234084)
│   ├── Language toggle (🇬🇧 EN · 🇮🇹 IT · 🇷🇺 RU)
│   ├── Theme toggle (light/dark)
│   └── Mobile menu (≤900px)
├── #top  Hero
│   ├── Headline + tagline + CTAs
│   └── Background video (assets/hero.mp4) / poster fallback
├── #story  Brand story (Genova harbor) + client photo slot (assets/harbor.jpg)
├── #collections  Services
│   ├── Bouquets        (img: Pexels 29601972)
│   ├── Event florals   (img: Pexels 35130782)
│   └── Honeymoon & anniversary (img: Pexels 31052815)
├── #gallery  Gallery (clickable lightbox)
│   ├── Summer bouquet      (Pexels 35640555)
│   ├── Harbor light        (Pexels 31052815)
│   ├── Coral & gold        (Pexels 14025720)
│   ├── On the water        (client: assets/yacht.jpg)  ★ user slot
│   ├── Tied with feeling   (Pexels 17993659)           ★ NEW emotional bouquet
│   ├── A summer smile      (client: assets/happy-girl.jpg) ★ user slot
│   └── Atelier corner      (Pexels 31917406)
├── #visit  Visit + map
│   ├── Address / hours / phone / email
│   └── OpenStreetMap embed (Porto Antico 44.4056, 8.9298)
├── #blog  Journal (Q&A)
│   ├── Ligurian flowers · Types of bouquets · Event services
│   └── Prices · Flower care · Home delivery  (+ garden design)
├── #book  CTA / order form (→ SITE_CONFIG.orderEndpoint)
├── Footer
│   ├── Explore links · Contact · Follow (IG/FB/Pinterest/TikTok)
│   └── WhatsApp icon
└── Chatbot widget (bottom-right): concierge with avatar (Pexels 13975904)
```

## External pages to add later
- `/blog/<slug>` article templates (currently in-page Q&A)
- `/privacy`, `/terms` (required for Stripe + Google Business)
- `/api/*` backend endpoints (order, newsletter, chat)

## Links
- Parent: [[mare-fiori.it-INDEX]]
- Related: [[site-requirements]]
