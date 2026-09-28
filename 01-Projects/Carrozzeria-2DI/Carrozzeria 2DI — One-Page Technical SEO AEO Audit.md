# Carrozzeria 2DI — One-Page Technical SEO/AEO Audit

**Site:** `https://49-12-201-28.sslip.io/it/contatti/`  
**Audit date:** 21 September 2026  
**Scope/tooling:** Tier 1, no extensions: live HTTP headers, HTML/source, internal links, `robots.txt`, XML sitemap, TLS certificate, page assets, and a lightweight 36-URL sitemap crawl. Lighthouse, Wappalyzer and BuiltWith were **not** used.

## Verdict

**Not ready for SEO or AEO launch.** The site has a sound crawlable HTML structure, useful service/location pages, HTTPS, canonicals, bilingual `hreflang`, and a sitemap—but every checked URL returns `X-Robots-Tag: noindex, nofollow`, while `robots.txt` contains `Disallow: /`. This combination prevents normal organic discovery; Google requires a page to be indexed and snippet-eligible before it can appear as a supporting link in AI Overviews or AI Mode.[^1][^2][^3][^4]

## Audit snapshot

| Area | Live finding | Readiness | Priority action |
|---|---|---:|---|
| **Indexability** | All 36 sitemap URLs returned `200`, but also `X-Robots-Tag: noindex, nofollow`; `robots.txt` blocks `/` for every crawler. | **Blocked** | On the production domain, remove the global `X-Robots-Tag`; change robots to `User-agent: *` + `Allow: /`; retain targeted blocks only for private/account/admin paths. A crawler must be allowed to fetch a page to discover indexing directives.[^1][^2][^5] |
| **AEO crawlers** | The blanket robots rule also blocks search-oriented AI crawlers. | **Blocked** | Allow `OAI-SearchBot` and `PerplexityBot` if AI-search visibility is desired; both vendors recommend permitting their search crawlers.[^6][^7][^8] |
| **Domain/canonicals** | Canonical and Open Graph URLs point to an IP-derived `sslip.io` hostname. HTTP correctly redirects to HTTPS. | **Staging only** | Launch on the permanent branded domain, change every canonical/hreflang/OG/sitemap URL, then 301 any accessible staging URLs. `sslip.io` maps hostnames containing an IP address to that IP and is better suited to technical access than brand trust.[^9] |
| **On-page SEO** | Contact page has one H1, semantic HTML, a concise title and description, but they are generic: `Contatti | Carrozzeria 2DI` and `Contatta Carrozzeria 2DI e trova una sede.` A second H2 repeats “Contatti.” | **Partial** | Target local intent naturally: e.g. title `Contatti e preventivi carrozzeria a Genova | 2DI`; describe Sampierdarena/Sestri Ponente, services and response method. Google recommends concise, descriptive titles and relevant page summaries.[^10][^11] |
| **Local SEO/schema** | The contact page has visible addresses, hours, telephone numbers and emails for two branches, but no JSON-LD. The homepage only has minimal `Organization` markup. | **Weak** | Add one accurate `AutoRepair`/`LocalBusiness` entity per branch, with `@id`, name, URL, telephone, postal address, opening hours, geo coordinates, image, map URL and `sameAs`; keep it identical to visible page and Google Business Profile. Google says each location should be defined as a `LocalBusiness`; `AutoRepair` is the relevant Schema.org subtype.[^12][^13][^14][^15] |
| **Structured data** | FAQ page has `FAQPage` JSON-LD matching five visible answers; contact/service/location pages lack `BreadcrumbList` and service/location entities. | **Partial** | Keep FAQ markup accurate for machine understanding, but do not expect a normal automotive site to receive Google FAQ rich results; Google limits that feature to authoritative government and health sites. Add validated breadcrumbs and location/service schema where it matches visible content.[^16][^17][^18] |
| **International SEO** | Italian/English pages have self-referencing canonicals and reciprocal `hreflang` in HTML and sitemap. No `x-default` was observed. Several English descriptions remain Italian, including the English contact page. | **Partial** | Translate every English title/description/body fragment; add `x-default` where appropriate; preserve reciprocal, self-referencing language pairs. Google supports HTML and sitemap `hreflang` annotations for localized versions.[^19][^20] |
| **Sitemap** | Valid XML sitemap exposes 36 IT/EN URLs and alternate-language links, but robots does not declare its location. | **Good base** | Add `Sitemap: https://<production-domain>/sitemap.xml` to robots and submit it in Search Console after removing blocks.[^21][^22] |
| **Internal links** | All unique internal destinations linked from the contact page returned `200`; navigation reaches services, branches, FAQ, privacy and cookie pages. | **Good** | Add contextual links from each branch to its relevant services and from each service to both branch/contact conversion pages. Internal discoverability supports Google’s AI-search guidance.[^4] |
| **Content/AEO** | The FAQ contains direct, useful answers about estimates, insurance, documents, repair time and courtesy cars. Contact details are textual and machine-readable. However, phone numbers, VAT number and likely business data are placeholders. | **Promising, unsafe to launch** | Replace every placeholder; add concise branch-specific answers such as service area, emergency process, estimate requirements, insurer handling, certifications, warranty and turnaround evidence. Helpful, original, people-first content—not AEO “hacks”—is Google’s recommended foundation.[^3][^4] |
| **Social metadata** | OG title, description, URL, locale and site name exist; no `og:image` or Twitter card metadata was observed. | **Partial** | Add a production-quality 1200×630 image plus `og:image` dimensions/alt and Twitter card tags; localize them per language. |
| **Performance** | Lightweight static first load: 13 first-party requests and about 367 KB of fetched resource bodies in this HTTP-level sample. Versioned assets have long immutable caching; CSS/JS responses support compression. No lab or field CWV measurement was run. | **Unverified** | Run mobile and desktop Lighthouse/PageSpeed after production launch; confirm field LCP ≤2.5 s, INP <200 ms and CLS <0.1 at the 75th percentile.[^23] |
| **Security/privacy** | HTTPS redirect and valid Let’s Encrypt certificate; strong CSP, frame denial, MIME-sniffing protection, referrer, opener and permissions policies. Consent UI delays optional reCAPTCHA; the enquiry still works without it. No HSTS header was observed. | **Good, one gap** | Add `Strict-Transport-Security` only after the final domain and all subdomains are permanently HTTPS; keep reCAPTCHA consent-gated and verify the consent log/policy implementation. |
| **Forms/accessibility** | Form controls have associated labels and required states; CSRF and honeypot fields are present. No autocomplete attributes were observed for name, phone and email. | **Good base** | Add `autocomplete="name"`, `tel`, and `email`; test keyboard focus, errors and screen-reader announcements in a browser accessibility pass. |
| **Stack/hosting** | Nginx 1.28.3 on Ubuntu; server-rendered pages strongly indicate Django through CSRF cookie/token and `/i18n/setlang/`. Assets are first-party; Google reCAPTCHA is the only optional external service exposed in page policy/source. No GA/GTM/Meta scripts were observed in the initial HTML/assets. | **Lean** | Hide detailed server version, keep framework patched, and verify post-consent network traffic before making a definitive tracker inventory. |

## Launch sequence

1. **Replace the staging hostname and all placeholder business information**: real domain, telephone numbers, VAT number, emails, legal owner, map/profile URLs and branch details.
2. **Remove the two global discovery blockers together**: `X-Robots-Tag: noindex, nofollow` and `Disallow: /`. Do this only on production; keep staging protected, preferably with authentication rather than relying only on robots.
3. **Regenerate technical signals** on the final domain: canonicals, reciprocal `hreflang`, `x-default`, Open Graph URLs/images, XML sitemap and robots sitemap declaration.
4. **Implement entity markup**: `Organization` plus two linked `AutoRepair`/`LocalBusiness` branch entities, then `BreadcrumbList`; validate with Rich Results Test and Schema.org Validator. Structured data must describe the visible page accurately.[^12][^13][^17]
5. **Localize metadata and sharpen intent** across all 36 URLs. The English contact, service index, branch index, about, privacy and cookie descriptions currently contain Italian text.
6. **Strengthen branch evidence**: unique copy, photos, directions/parking, neighborhoods served, verified opening hours, services at that branch, certifications, warranties and authentic testimonials where legally permitted.
7. **Connect and verify** Google Business Profiles for both branches, ensuring exact name/address/phone/hours consistency; keep profile information current for conventional and AI-assisted search.[^4]
8. **Validate after release**: Search Console domain property, sitemap submission, URL Inspection on home/contact/branch/service/FAQ, Bing Webmaster Tools, mobile Lighthouse/PageSpeed, Rich Results Test and server-log checks for Googlebot, Bingbot, OAI-SearchBot and PerplexityBot.

## Suggested production robots

```txt
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /accounts/

User-agent: OAI-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /

Sitemap: https://www.example.it/sitemap.xml
```

Replace `example.it` with the final domain and adjust private paths to the real application. Do not use robots rules as access control; authenticated/private areas require actual authorization.

## Limits

This was a remote, unauthenticated Tier-1 audit with no browser extensions. It did not include rendered-browser network capture, Lighthouse scores, real-user Core Web Vitals, Search Console/Business Profile data, form submission, authenticated areas, DNS/email configuration, backlink analysis, or competitive/market analysis.

---

## References

1. [Robots Meta Tags Specifications | Google Search Central](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag) - The X-Robots-Tag can be used as an element of the HTTP header response for a given URL. Any rule tha...

2. [Block Search Indexing with noindex - Google for Developers](https://developers.google.com/search/docs/crawling-indexing/block-indexing) - A noindex tag can block Google from indexing a page so that it won't appear in Search results. Learn...

3. [Optimizing your website for generative AI features on Google Search](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) - Learn how to optimize your website for Google Search's generative AI features, including official be...

4. [AI Features and Your Website | Google Search Central](https://developers.google.com/search/docs/appearance/ai-features) - This guide covers how AI features like AI Overviews and AI Mode work in Google Search from a site ow...

5. [Robots.txt Introduction and Guide | Google Search Central](https://developers.google.com/search/docs/crawling-indexing/robots/intro) - A robots.txt file tells search engine crawlers which URLs the crawler can access on your site. This ...

6. [Overview of OpenAI Crawlers](https://developers.openai.com/api/docs/bots) - OpenAI uses OAI-SearchBot and GPTBot robots.txt tags to enable webmasters to manage how their sites ...

7. [How does Perplexity follow robots.txt? - Perplexity Help Center](https://www.perplexity.ai/help-center/en/articles/10354969-how-does-perplexity-follow-robots-txt) - Perplexity respects robots.txt directives. Our crawler, PerplexityBot, will not index the full or pa...

8. [Perplexity Crawlers](https://docs.perplexity.ai/docs/resources/perplexity-crawlers) - Webmasters can use the following robots.txt tags to manage how their sites and content interact with...

9. [GitHub - cunnie/sslip.io: Golang-based DNS server which maps ...](https://github.com/cunnie/sslip.io) - sslip.io is a DNS server that maps specially-crafted DNS A records to IP addresses (e.g. "127-0-0-1....

10. [How to Write Meta Descriptions | Google Search Central](https://developers.google.com/search/docs/appearance/snippet) - Learn how to write a quality meta description tag that may be displayed for your page in Google Sear...

11. [Influencing your title links in search results - Google for Developers](https://developers.google.com/search/docs/appearance/title-link) - Learn how you can write an SEO-rich titles for your website pages and Google Search by following the...

12. [Local Business (LocalBusiness) Structured Data | Documentation](https://developers.google.com/search/docs/appearance/structured-data/local-business) - With Local Business structured data, you can tell Google about business hours, different departments...

13. [Intro to How Structured Data Markup Works | Google Search Central](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data) - Google uses structured data markup to understand content. Explore this guide to discover how structu...

14. [AutoRepair - Schema.org Type](https://schema.org/AutoRepair) - AutoRepair - Car repair business. Usage: 10K - 100K Domains Based on monthly aggregations from Googl...

15. [LocalBusiness - Schema.org Type](https://schema.org/LocalBusiness) - Examples of LocalBusiness include a restaurant, a particular branch of a restaurant chain, a branch ...

16. [Latest Google Search Documentation Updates | What's new](https://developers.google.com/search/updates) - Updated the FAQ structured data documentation to state that the feature is only shown for well-known...

17. [How To Add Breadcrumb (BreadcrumbList) Markup | Documentation](https://developers.google.com/search/docs/appearance/structured-data/breadcrumb) - How to add structured data · Add the required properties. · Follow the guidelines. · Validate your c...

18. [Structured Data Markup that Google Search Supports](https://developers.google.com/search/docs/appearance/structured-data/search-gallery) - Structured data markup that Google Search supports ; Breadcrumb. Navigation that indicates the page'...

19. [Localized Versions of your Pages | Google Search Central](https://developers.google.com/search/docs/specialty/international/localized-versions) - Learn how you can use a sitemap and other methods to tell Google about all of the different language...

20. [Managing Multi-Regional and Multilingual Sites | Documentation](https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites) - Google supports several different methods for labeling language or region variants of a page, includ...

21. [Build and Submit a Sitemap | Google Search Central | Documentation](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap) - Google supports several sitemap formats. Follow this guide to learn about formats, how to build a si...

22. [Create and Submit a robots.txt File | Google Crawling Infrastructure](https://developers.google.com/crawling/docs/robots-txt/create-robots-txt) - A robots.txt file lives at the root of your site. Learn how to create a robots.txt file, see example...

23. [Understanding Core Web Vitals and Google search results](https://developers.google.com/search/docs/appearance/core-web-vitals) - Core Web Vitals is a set of metrics that measure real-world user experience for loading performance,...

