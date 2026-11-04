# Reusable Workers deployment protocol on Cloudflare

When Ole says **"deploy"** for a clearly identified project, use this protocol.
This approves only that deployment. Clarify first if the project, target, or
production impact is unclear, or if project rules require additional approval.

After deployment, always share the live URL in chat. Do not open the site in a
browser unless asked; verify it with an HTTP request. Whenever saving a file,
always state its full path in chat, even if Ole gave the destination.
For any sites/applications inventory, consult
`/Users/olesiarasing/Obsidian/01-Projects/sites/sites-INDEX.md`, include
applications as well as websites, and give the absolute local source path (or
state clearly when it could not be found) and deployment status for each item.

## Workflow

1. Inspect project instructions, source, build output, existing Cloudflare
   config, and deployment target. Preserve originals and do not overwrite an
   existing Worker unless it is clearly the intended target.
2. Use `cf` for new Workers projects. If the project already has
   `wrangler.jsonc`, `wrangler.json`, or `wrangler.toml`, keep its Wrangler
   workflow; do not use `cf deploy` or migrate unless asked. Preserve existing
   Pages hosting for maintenance unless migration is requested.
3. Check `cf --version` and `cf auth whoami`. If needed, use `cf auth login`.
   Stored OAuth credentials may refresh offline, but are not guaranteed
   timeless. Do not create a long-lived API token just to avoid reauthorization.
4. For a standalone static site, keep public output in its own directory (for
   example `public/`) and configure only that as the assets directory. Never
   publish the project root if it contains dependencies, credentials, or
   private files.
5. Before deployment, audit the actual site files against
   `/Users/olesiarasing/Obsidian/03-Resources/Reference-General/HERMES Rules/LEXFLOW-Quality-Manifesto.md`.
   Check applicable Definition of Done items, mobile/accessibility basics,
   links, forms, metadata, legal/cookie claims, and the favicon/site icons.
   Record and report any unmet or inapplicable checks; do not claim a check
   passed without verifying it.
6. Review visible copy for generic builder credits or watermarks, such as
   "Realizzato con Perplexity Computer". Remove such boilerplate and replace it
   only with accurate content that fits this site's own theme (for example,
   its value proposition, attribution, contact details, navigation, legal
   notices, or cookie notice). Use other sites only as structural examples;
   never copy their text or invent claims, contact details, or legal promises.
7. Run `cf deploy --dry-run`; make sure it succeeds and includes only intended
   assets. Then run `cf deploy`.
8. Verify the printed URL without opening a browser:

   ```sh
   curl -fsS -o /dev/null -w 'HTTP %{http_code}; %{content_type}\n' \
     'https://<worker-name>.<workers-subdomain>.workers.dev/'
   ```

9. Report the URL and HTTP result in chat, together with any audit checks that
   remain unmet or could not be verified.

## What this supports

Workers with Static Assets are suitable for:

- Static HTML/CSS/JavaScript sites, documentation, landing pages, and
  multi-page sites.
- Client-rendered single-page apps and static-site-generated sites.
- Static frontend builds from Vite, React, Vue, Svelte, and similar tools.
- Progressive web app frontends and their static service-worker files.
- Full-stack or server-rendered web apps with a supported Cloudflare framework
  adapter; follow that adapter's setup rather than deploying only HTML.
- APIs, webhooks, and form endpoints implemented as Worker code.
- AI apps and MCP endpoints built for the Workers runtime.
- Apps using Cloudflare services such as D1, KV, R2, Queues, or Workers AI,
  where required.

Workers are not a general-purpose replacement for a persistent Linux server or
unrestricted long-running processes. Add services only when the application
needs them.

## Deployment-only reference (not a quality example)

The AI & Crypto guide was deployed and verified as reachable, but it was not
audited against the quality manifesto before deployment. Do not treat it as
meeting the manifesto or as a quality model; use it only as a reference for the
basic Workers deployment flow:
<https://ai-crypto-compliance.olesya00007.workers.dev/>
