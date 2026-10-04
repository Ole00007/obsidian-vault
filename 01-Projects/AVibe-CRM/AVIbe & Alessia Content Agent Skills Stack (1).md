# AVIbe Agency & Alessia_Code Content Drafting: Skills and Space Design

## Executive recommendation

Use a **small, curated stack rather than a large marketplace bundle**. The strongest fit is: official Hermes skills/toolsets for execution and security; selected skills from `social-media-skills/skills` for short-form video craft; `coreyhaines31/marketingskills` for mature marketing copy; and custom AVIbe skills for multilingual hooks, approvals, regulated-client safety, and the agency’s exact workflow.

Hermes skills are portable, on-demand procedure packages compatible with the Agent Skills standard. Hermes supports progressive disclosure, bundles, project-local skills, install-time scanning, audit logs, quarantine, and optional NVIDIA Tier 1 checks. Perplexity Projects also retain files, instructions, connected tools, and project context, with up to 8,000 characters of instructions.[^1][^2][^3]

This project is not merely a text-writing workspace. Existing AVIbe materials describe AI-powered Reels, human-recorded video, avatars, hooks, captions, calendars, trend monitoring, competitor analysis, performance tracking, A/B testing, and multilingual work for doctors and entrepreneurs. The project therefore needs a pipeline from research to concept, script, shot list, generation/editing brief, compliance review, approval, publishing package, and performance learning.[^4]

## Marketplace policy

Use marketplaces for **discovery**, not as a trust guarantee. Recommended trust order:

1. **Hermes bundled skills and official optional catalog** — first choice because they are maintained or shipped by Nous Research and use the native security/install pipeline.[^5][^6]
2. **Official vendor repositories** — Anthropic’s public skills repository and official product-vendor repositories are useful reference implementations of the open format.[^7][^8]
3. **skills.sh entries backed by inspectable GitHub repositories** — acceptable only after inspecting the full `SKILL.md`, scripts, references, license, commit, and permissions.[^9]
4. **Other community hubs** — discovery only; do not install directly into the production profile without review, scanning, and sandbox tests.

A skill is executable guidance that may include scripts and can operate with the user’s permissions; Microsoft explicitly recommends treating third-party skills like open-source dependencies, reviewing all files, sandboxing execution, limiting access, and logging activity. Automated scans reduce risk but cannot prove safety, especially when malicious intent is expressed as plausible natural-language instructions.[^10][^11][^12]

## Recommended core stack

| Priority | Skill/tool | Source | Why it fits AVIbe | Decision |
|---|---|---|---|---|
| P0 | `grounded-citations` | Hermes bundled | Keeps factual, medical, legal, trend, and competitor claims traceable. | Enable now |
| P0 | `social-media-content-calendar` | Hermes official optional | Converts campaign briefs into multi-platform plans through posting. | Install now |
| P0 | `humanizer` | Hermes bundled | Removes generic AI phrasing while preserving the approved brand voice. | Enable now |
| P0 | `youtube-content` | Hermes bundled | Turns source videos/transcripts into summaries and reusable content atoms. | Enable now |
| P0 | `whisper` | Hermes official optional | Transcribes and translates speech across 99 languages, useful for source videos and multilingual drafts.[^6] | Install now |
| P0 | `video_analyze` toolset | Hermes built-in | Produces captions, scene breakdowns, timestamps, and visual descriptions from video URLs/files.[^13] | Enable now |
| P0 | `short-form-video-script` | skills.sh → `social-media-skills/skills` | Dedicated short-form scripting; repository also includes Reels, TikTok and Shorts variants.[^14] | Inspect, scan, pilot |
| P0 | `hook-writer` | Same repository | Builds hooks around curiosity, tension, stakes and truthful payoff rather than empty templates.[^15] | Inspect, scan, pilot |
| P0 | `viral-reverse-engineering` | Same repository | Separates replicable mechanisms from surface imitation, timing, account size and luck.[^16] | Inspect, scan, pilot |
| P0 | `content-research-and-sourcing` | Same repository | Requires primary-source tracing, freshness checks, claim verification and sourcing before scheduling.[^17] | Inspect, scan, pilot |
| P0 | Custom `avibe-brand-profile` | Internal | Stores approved voice, audiences, offers, vocabulary, visual cues, banned claims and language variants. | Build first |
| P0 | Custom `avibe-content-gate` | Internal | Enforces human approval before generation, publishing, ads, client promises or account actions. | Build first |
| P1 | `social-content` | skills.sh → `coreyhaines31/marketingskills` | Covers Instagram, TikTok, Facebook, X and LinkedIn, plus pillars, hooks, repurposing, calendars and analytics.[^18] | Add after pilot |
| P1 | `copywriting` | Same repository | Strong fit for offers, landing pages and CTAs; emphasizes specificity, customer language, honest claims and voice consistency.[^19] | Add after pilot |
| P1 | `content-calendar`, `content-pillars`, `batch-content-plan` | `social-media-skills/skills` | Useful for batching and campaign structure; avoid if they duplicate the official Hermes calendar skill.[^14] | Select one path |
| P1 | `scripting-and-storyboarding`, `talking-head-and-piece-to-camera` | `social-media-skills/skills` | Bridges script to a shootable sequence for human or AI video.[^14] | Pilot |
| P1 | `captions-and-clipping`, `capcut` | `social-media-skills/skills` | Matches the existing CapCut workflow and turns edits into production instructions.[^14] | Pilot; no account access |
| P1 | `cross-platform-repurposing` | `social-media-skills/skills` | Adapts one approved idea across Reels, TikTok, Shorts, Facebook and LinkedIn without copy-pasting.[^14] | Pilot |
| P1 | `analytics-and-reporting`, `experimentation-and-ab-testing` | `social-media-skills/skills` | Closes the loop with test hypotheses and post-level learning.[^14] | Add when data exists |
| P1 | `instagram-seo` and `social-seo` | `social-media-skills/skills` | Improves discovery metadata and platform search structure.[^14] | Add after voice baseline |
| P1 | `seo` | skills.sh → `mblode/agent-skills` | Useful for web/answer-engine briefs and evidence-led auditing, but too new to make P0.[^20] | Limited pilot |
| P1 | `image_generate`, `vision_analyze` | Hermes built-in | Supports prompt-to-image/editing and visual QA with configured backends.[^13] | Enable with spend cap |
| P1 | `video_generate` | Hermes built-in | Supports text/image-to-video through xAI, FAL, OpenRouter or DeepInfra; includes Kling through supported backends.[^13] | Enable after approval gate |
| P1 | `ai-presenter-video` | Hermes official optional | Useful for verified presenter/avatar videos from an approved script and image.[^6] | Client-consent pilot |
| P1 | `kanban-video-orchestrator` | Hermes official optional | Designed for multi-agent video production pipelines.[^6] | Add when volume grows |
| P2 | `creative-ideation`, `seasonal-and-moment-marketing`, `trend-jacking` | Official Hermes / skills.sh | Expands ideas and timing, but should never override brand fit or verification. Seasonal skill explicitly favors fit and authenticity over posting every occasion.[^6][^21] | Controlled use |
| P2 | `watchers`, `rss-feeds`, `blogwatcher`, `competitor-news-monitor` | Hermes official/bundled | Deterministic trend and competitor monitoring; fits a low-cost “collect first, summarize only on change” workflow. | Add as scheduled jobs |
| P2 | `google-workspace`, `airtable`, `notion`, `docx`, `xlsx`, `powerpoint` | Hermes bundled | Production tracking, briefs, approvals and client deliverables.[^5] | Enable only as needed |

The `social-media-skills/skills` repository is especially aligned because its catalog includes short-form scripts, Reels, hooks, voice building, captions, Instagram growth, CapCut, calendars, audience research, storyboards, analytics, Shorts, platform validation, trend-jacking, AI voice, AI video, Kling, Canva and crisis moderation. Its security page says the repository consists primarily of Markdown skills and small build scripts with no credentials, but still advises reviewing skills like scripts before installation.[^14][^22]

`coreyhaines31/marketingskills` is a good secondary source: its social skill has broad platform and workflow coverage, the repository uses the Agent Skills specification and an MIT license, and the copywriting skill has high adoption. However, GitHub reports no repository security policy, so it should still go through Hermes inspection, scanning, pinning and sandbox evaluation.[^18][^19][^23][^24]

## Avoid redundant installs

Do not install all 100+ social skills. Too many overlapping skill descriptions can cause poor routing and inconsistent outputs. Use one primary skill per responsibility:

| Responsibility | Primary | Keep out initially |
|---|---|---|
| Brand context | Custom `avibe-brand-profile` | Multiple generic voice/profile skills |
| Strategy/calendar | Official `social-media-content-calendar` | Duplicate calendars from several repos |
| Viral analysis | `viral-reverse-engineering` | “Viral writer” skills with no evidence model |
| Script | `short-form-video-script` | Separate Reels/TikTok/Shorts skills until needed |
| Hook | `hook-writer` | Generic headline libraries |
| Research | `content-research-and-sourcing` + `grounded-citations` | Unsourced trend scrapers |
| Copy | `social-content`; `copywriting` for web | Multiple generic copywriting skills |
| Video understanding | `video_analyze` + `whisper` | Duplicate transcription wrappers |
| Video generation | Native `video_generate` | Third-party execution scripts at first |
| QA/approval | Custom `avibe-content-gate` | Autonomous publishing skills |

Perplexity recommends writing skill evaluations early, including positive, negative, and forbidden-load examples; the description is a routing trigger rather than a workflow summary. This makes a compact stack easier to test and maintain.[^25]

## Hermes setup

Create a dedicated profile or trusted project repository instead of changing the general Hermes profile. Hermes recognizes project-local skills under `.hermes/skills/` or `.agents/skills/`, gives them precedence inside that repository, and scans changed project skills before loading them.[^2]

Recommended order:

```bash
# 1. Review installed and official options
hermes skills browse --source official
hermes skills audit

# 2. Install official optional foundations
hermes skills install official/creative/social-media-content-calendar
hermes skills install official/mlops/whisper
hermes skills install official/creative/ai-presenter-video
hermes skills install official/creative/kanban-video-orchestrator

# 3. Discover, inspect, then install community skills
hermes skills search short-form-video --source skills-sh
hermes skills inspect <source-qualified-identifier>
hermes skills install <source-qualified-identifier>

# 4. Re-audit after installation or updates
hermes skills audit
hermes skills check
```

The exact source-qualified identifier returned by `hermes skills search` should be used rather than guessed. Hermes can search official, skills.sh, well-known endpoints, GitHub and other registries; its installer scans the quarantined bundle and stores source, content hash, scanner version, findings and timestamp.[^2]

Enable the toolsets required by the workflow:

- `web`, `browser`, `video`, `vision`, `image_gen`, `skills`, `file`, `clarify`, `todo`.
- Add `video_gen` only after a backend, per-run spending ceiling and approval policy are configured.
- Add `kanban` only for the orchestrator profile and reviewers.
- Keep account-writing/posting connectors disabled in the drafting profile.

Hermes’ `video` toolset is opt-in, and its `video_gen` toolset supports configurable providers rather than allowing the agent to choose any model itself. That is useful for cost control and preserving the existing preference for Kling/CapCut workflows.[^13]

## Recommended bundles

Use bundles only after individual skills pass a pilot. Hermes bundles can load several installed skills under one command and work across CLI, dashboard and messaging surfaces.[^2]

```yaml
# ~/.hermes/skill-bundles/avibe-reel.yaml
name: avibe-reel
description: Research, draft, verify and package one short-form video.
skills:
  - avibe-brand-profile
  - content-research-and-sourcing
  - viral-reverse-engineering
  - hook-writer
  - short-form-video-script
  - grounded-citations
  - avibe-content-gate
instruction: |
  Work stage by stage. Stop after concept selection and again before any generation,
  export, scheduling, posting, ad spend, or client-facing claim. Never imply guaranteed virality.
```

```yaml
# ~/.hermes/skill-bundles/avibe-campaign.yaml
name: avibe-campaign
description: Build an approved multi-platform content campaign.
skills:
  - avibe-brand-profile
  - social-media-content-calendar
  - social-content
  - cross-platform-repurposing
  - experimentation-and-ab-testing
  - avibe-content-gate
instruction: |
  Define audience, business objective, platforms, languages, proof requirements,
  resources and approval owner before drafting. Keep platform variants native.
```

## Custom AVIbe skills

### `avibe-brand-profile`

This should be the single source of truth for account-specific tone, audience, language, offers, proof, visual system and prohibited claims. It should reference separate files per brand/client so that a medical client’s elegant, trust-led voice cannot leak into Alessia’s personal creator voice or AVIbe’s agency voice.

Suggested references:

- `references/avibe-agency.md`
- `references/alessia-code.md`
- `references/client-template.md`
- `references/language-style-en-it-ru-fr.md`
- `references/claims-and-proof.md`
- `references/visual-production.md`

Existing preferences call for 5–12 word hooks in English, Italian, Russian and French, aimed at self-preneurs and SMBs with simple language, active energy and selective provocation. Encode that rule only for matching brands/tasks, not as a universal rule for regulated medical clients.

### `avibe-content-gate`

This skill should control state transitions:

`brief → evidence → concepts → human concept approval → script → fact/compliance QA → human script approval → production brief → generation/edit → final QA → human publish approval → performance snapshot → lessons`

It should fail closed when the client, account, platform, language, objective, evidence, rights, disclosure status or approval owner is missing. It must never publish, schedule, spend, message, upload client data, clone a voice, use a likeness, or change a client account without explicit task-specific approval.

### `avibe-viral-video-os`

This is the orchestrating custom skill to add only after the pilot stack works. It should not repeat all underlying skills. It should route tasks, define required artifacts, call appropriate skills/toolsets, and preserve approvals and provenance.

Minimum output contract:

- Brief and assumptions
- Evidence/trend table with date, platform, link and confidence
- 3–5 concept options with mechanism, brand fit, production cost and risk
- Approved hook variants
- Timed script with spoken words, on-screen text, B-roll/shot direction, pattern interrupts and CTA
- AI/image/video prompt pack if requested
- Caption, keywords/hashtags, thumbnail/cover text and platform variants
- Rights/disclosure/compliance checklist
- Approval status
- Measurement hypothesis and post-publication learning fields

## Risk controls

### Skills and credentials

- Prefer bundled/official skills; inspect community skills before install.
- Pin the reviewed commit or preserve Hermes’ recorded content hash; run `hermes skills audit` after updates.
- Turn on `skills.write_approval: true` so agent-created or modified skills are staged for review.[^2]
- Enable Hermes’ NVIDIA Tier 1 advisory checks, understanding that NVIDIA labels the evaluator experimental and without an SLA.[^26]
- Use a quarantine profile and least-privilege credentials; drafting agents get read access, while publishing credentials belong to a separate gated profile.
- Never expose API keys, client credentials, private drafts, raw analytics exports, patient information or personal data in prompts, logs, skills or public repositories.

### Content and truth

- “Viral” means an evidence-backed hypothesis, never a promise. A viral-analysis skill itself warns that timing, account size, unique events, survivorship and randomness may make success non-replicable.[^16]
- Verify dates, figures, quotes, medical/legal claims and competitor facts against current primary sources before client approval.
- Distinguish fact, interpretation, creative hypothesis and fictional dramatization.
- Reject fabricated testimonials, results, reviews, before/after outcomes or implied endorsements.
- For medical/aesthetic content, require qualified human review before publication; do not diagnose, prescribe, promise outcomes or invent clinical evidence.

### Rights and identity

- Record provenance and permission for every source video, image, font, music track, logo, likeness, voice and testimonial.
- Do not download/repost a viral asset merely because it is public; reverse-engineer the mechanism and create original execution.
- Voice clones, avatars and likeness transformations require documented consent, allowed uses, platforms and expiry.
- Protect minors and do not generate sexualized, humiliating, discriminatory or deceptive material.

### AI transparency

The EU AI Act’s Article 50 transparency rules apply from 2 August 2026. Deployers must disclose deepfakes, while providers must support machine-readable marking of synthetic content; disclosures must be clear and distinguishable. TikTok requires labels for realistic AI-generated image, audio and video content and may also apply labels automatically. YouTube requires disclosure when realistic content makes a person, place, event or scene appear authentic when it was altered or generated; script ideation and routine production assistance do not automatically trigger that rule.[^27][^28][^29][^30][^31]

Therefore every final package should include:

- `AI_MEDIA: none | assisted | significantly altered | synthetic`
- `REAL_PERSON_OR_EVENT: yes | no`
- `DISCLOSURE_REQUIRED: yes | no | legal review`
- `PLATFORM_TOGGLE: TikTok | YouTube | Meta | other`
- `VISIBLE_DISCLOSURE_COPY`
- `C2PA/METADATA_STATUS`
- `CONSENT_RECORD`

### Operational safety

- Separate drafting, generation and publishing identities.
- Require two approvals for regulated, paid, political, crisis, testimonial, before/after, cloned-voice or photorealistic synthetic content.
- Set cost limits before generation: maximum variants, duration, resolution and retries.
- Save versioned artifacts and source links; never overwrite an approved version silently.
- Log who approved what and when.
- Use deterministic monitoring first; invoke expensive model analysis only when a material change or relevant trend is detected.

## Success and failure

### Success definition

A task succeeds only when:

- The correct brand/client profile and latest brief were used.
- Claims are sourced, current and clearly separated from creative hypotheses.
- The concept is original, brand-fit and realistically producible.
- The hook earns attention without breaking the content’s promise.
- The script has timing, shots, spoken copy, overlays, audio notes, CTA and platform adaptation.
- Language variants preserve meaning and tone rather than translating literally.
- Rights, consent, AI disclosure and platform-policy checks are complete.
- Required human approvals are recorded before production and publication.
- Files follow naming/version conventions and remain editable.
- The measurement plan states one main objective, KPI, baseline, hypothesis and review date.
- Post-publication results are converted into durable lessons, not copied blindly.

### Failure definition

A task fails if any of these occurs:

- Unsourced or invented factual/medical/legal claims.
- Guaranteed virality, guaranteed growth or guaranteed client outcomes.
- Content published, scheduled, messaged or paid without explicit approval.
- Account, client, language or brand voice mixed up.
- Unlicensed media, undisclosed sponsorship, unapproved likeness/voice use, or missing required AI disclosure.
- A copied viral format preserves the surface but not the mechanism or brand relevance.
- Generic AI language, excessive jargon, weak hook/payoff alignment or a CTA unrelated to the objective.
- Output cannot be edited, traced to sources or reproduced.
- Sensitive information enters a third-party skill, public repository or unnecessary tool.
- A tool/skill error is hidden rather than reported with a safe fallback.

## Copy-ready Project description

> **Role and mission**
>
> You are AVIbe Agency and Alessia_Code’s multilingual Content OS for research, strategy, drafting and production planning. Create original static and video content for personal, agency and approved client accounts. Optimize for useful attention, trust, brand fit, leads and measurable learning—not empty volume or guaranteed virality.
>
> **Scope**
>
> Support content research, audience/competitor analysis, trend monitoring, campaign concepts, Reels/TikTok/YouTube Shorts, talking-head scripts, AI-video briefs, storyboards, shot lists, captions, carousels, posts, CTAs, repurposing, SEO/social discovery, A/B hypotheses, calendars and performance reviews. Use Project files as the source of truth for offers, brand identity, client requirements and prior approvals; use current web research for changing facts, trends and platform rules.
>
> **Working method**
>
> 1. Identify account/client, audience, objective, platform, format, language, deadline, offer, CTA, available assets, production method and approval owner. Ask only for missing high-impact inputs.
> 2. Check Project files before drafting. Never mix client voices, claims, assets or confidential information.
> 3. For trends or factual content, research current examples and primary sources. Record link, platform, date, observable mechanism and relevance. Separate fact, interpretation and creative hypothesis. Never promise virality.
> 4. Propose 3–5 concepts before full production. For each give: hook, core mechanism, audience tension, brand fit, production effort, risk and CTA. Stop for concept approval unless the user explicitly asks for drafts without a checkpoint.
> 5. After approval, create a production-ready package: 5–12-word hook where appropriate; timed scene/beat structure; spoken script; on-screen text; B-roll/shot directions; pattern interrupts; sound/music direction; CTA; caption; discoverability terms/hashtags; cover text; platform adaptations; and AI image/video prompts when requested.
> 6. For AVIbe/Alessia general content, default to clear simple language, active energy, tasteful humor and selective provocation. When requested, provide English, Italian, Russian and French variants that preserve intent rather than translate literally. For medical, legal, financial or other regulated clients, prefer precise, calm, trust-led language and require qualified human review.
> 7. Reverse-engineer viral mechanisms, not copyrighted execution. Do not copy scripts, footage, distinctive creative expression, music or brand assets. Produce an original angle.
> 8. Run QA before delivery: factual accuracy, source freshness, hook/payoff alignment, brand voice, timing, platform fit, rights, consent, privacy, sponsorship disclosure, AI-media disclosure, spelling, CTA and editability.
> 9. Stop before video/image generation, voice cloning, avatar use, export, scheduling, posting, messaging, ad spend or account changes unless explicit task-specific approval exists. Never treat previous approval as permanent.
> 10. After performance data is supplied, compare the result with the stated hypothesis and baseline. Save only reusable lessons; do not infer causation from one post.
>
> **Required output labels**
>
> ACCOUNT / OBJECTIVE / AUDIENCE / PLATFORM / LANGUAGE / FORMAT / STATUS / SOURCES / ASSUMPTIONS / APPROVAL NEEDED / AI DISCLOSURE / RIGHTS & CONSENT / KPI / NEXT ACTION.
>
> **Risk controls**
>
> Never fabricate sources, statistics, testimonials, patient/client outcomes, reviews, quotes or competitor facts. Never diagnose, prescribe, give individualized legal/medical/financial advice, or guarantee outcomes. Do not expose credentials, private client data, patient data, raw analytics, personal identifiers or unpublished strategy. Flag uncertainty and conflicting evidence. Use only authorized assets. Require written consent for identifiable people, avatars and voice clones. Label realistic AI-generated or materially altered media when law or platform policy requires it. Use two approvals for regulated, paid, political, crisis, testimonial, before/after, cloned-voice or photorealistic synthetic content.
>
> **Fail safely**
>
> If required information, evidence, consent, rights, policy status or approval is missing, do not guess or execute. Return: `BLOCKED`, the exact reason, the minimum information needed, and a safe draft or fallback if possible. If a tool or source fails, disclose the limitation and use a lower-risk method. Never conceal errors.
>
> **Success**
>
> Success means the right brand context was used; factual claims are current and sourced; the idea is original and producible; the hook truthfully pays off; language and platform versions feel native; the package is editable and complete; rights, consent and AI/sponsorship disclosures are resolved; approvals are recorded; and one measurable objective, KPI, hypothesis and review date are defined.
>
> **Failure**
>
> Failure includes unsourced claims, fake proof, guaranteed virality, copied creative, mixed client context, wrong language/tone, missing consent or disclosure, unauthorized publishing/spend, exposure of sensitive data, hidden tool errors, or output that cannot be edited, traced or evaluated.
>
> **Default delivery**
>
> Lead with the strongest recommendation. Use compact tables for options and checklists for production. Provide direct source/example links. End with `DECISION NEEDED` and the single next approval required; if none, end with `READY FOR NEXT STAGE`.

This block is designed to remain below Perplexity’s 8,000-character Project instruction limit.[^3]

## Direct examples and documentation

- [Hermes Skills System](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills) — official install, scanning, bundles, project-local skills and approval controls.[^1]
- [Hermes bundled catalog](https://hermes-agent.nousresearch.com/docs/reference/skills-catalog) — official built-in skills.[^5]
- [Hermes optional catalog](https://hermes-agent.nousresearch.com/docs/reference/optional-skills-catalog) — official installable optional skills.[^6]
- [Hermes tools reference](https://hermes-agent.nousresearch.com/docs/reference/tools-reference) — `video_analyze`, `video_generate`, image, browser, web and orchestration tools.[^13]
- [Anthropic official skills repository](https://github.com/anthropics/skills) — strong reference for portable skill structure.[^7]
- [skills.sh](https://www.skills.sh/) — searchable open directory; use for discovery, not automatic trust.[^9]
- [Social Media Skills catalog](https://www.skills.sh/social-media-skills/skills) — short-form, Reels, hooks, research, CapCut, analytics and video skills.[^14]
- [Viral Reverse-Engineering](https://www.skills.sh/social-media-skills/skills/viral-reverse-engineering) — mechanism-first viral analysis.[^16]
- [Hook Writer](https://www.skills.sh/social-media-skills/skills/hook-writer) — hook/payoff craft.[^15]
- [Content Research and Sourcing](https://www.skills.sh/social-media-skills/skills/content-research-and-sourcing) — pre-publication verification.[^17]
- [Marketing Skills: Social Content](https://www.skills.sh/coreyhaines31/marketingskills/social-content) — broad social strategy and production workflow.[^18]
- [Marketing Skills: Copywriting](https://www.skills.sh/coreyhaines31/marketingskills/copywriting) — conversion copy and CTA framework.[^19]
- [Perplexity Computer Skills](https://www.perplexity.ai/help-center/en/articles/13914413-how-to-use-computer-skills) — custom skill creation/upload requirements.[^32]
- [NVIDIA SkillEvaluator](https://docs.nvidia.com/skills/skillevaluator) — validation, security, overlap and live effectiveness testing.[^26]
- [EU AI-generated content transparency](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content) — Article 50 support and disclosure scope.[^30]
- [TikTok AI-generated content policy](https://support.tiktok.com/en/using-tiktok/creating-videos/ai-generated-content) — labels for realistic AI media.[^27]
- [YouTube AI disclosure help](https://support.google.com/youtube/answer/14328491) — realistic altered/synthetic content disclosure.[^29]

## Rollout plan

### Week 1: foundation

- Paste the copy-ready description into the Perplexity Project.
- Create a separate Hermes profile/project branch for AVIbe content.
- Turn on skill-write approval and install only official P0 skills.
- Create `avibe-brand-profile` and `avibe-content-gate` from approved internal rules.
- Build 10 evaluation prompts: four normal, three edge cases, three forbidden-action cases.

### Week 2: short-form pilot

- Inspect, scan and install four community skills: research/sourcing, viral reverse-engineering, hook writer and short-form video script.
- Test on one account, one audience, one offer and 5–8 Reels.
- Compare outputs with and without each skill for correctness, brand fit, edit time, safety and token/tool cost.

### Week 3: production

- Add video analysis, Whisper, storyboarding and CapCut guidance.
- Add native video generation only after spend caps and approval checkpoints are tested.
- Create the `/avibe-reel` bundle and preserve approved examples under the custom skill’s `examples/` directory.

### Week 4: learning loop

- Add analytics and A/B testing only after real performance data exists.
- Automate deterministic feed/watchlist collection; summarize only meaningful changes.
- Review false activations, duplicated guidance, unsafe behavior and production bottlenecks.
- Promote changes only after evidence, cross-test, review and a recorded 5/5 confidence decision.

## Final summary

The best fit is a **three-layer system**:

1. **Safe foundation:** official Hermes research, calendar, transcription, video-analysis, generation and orchestration capabilities.
2. **Selective craft layer:** four to eight inspected skills from `social-media-skills/skills`, plus mature copy/strategy from `coreyhaines31/marketingskills`.
3. **AVIbe control layer:** custom brand profile, content gate and viral-video orchestration skills encoding multilingual style, client separation, approvals, legal/platform disclosure, rights and success/failure rules.

Start with the copy-ready Project description and the P0 stack. Do not enable autonomous publishing or install entire marketplaces. Pilot one account and 5–8 Reels, evaluate measurable uplift and failure behavior, then add production and analytics skills only where the evidence shows a gap.

---

## References

1. [Skills System | Hermes Agent - Nous Research](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills) - On-demand knowledge documents — progressive disclosure, agent-managed skills, and the Skills Hub

2. [Skills System | Hermes Agent](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/) - All hub-installed skills go through a security scanner that checks for data exfiltration, prompt inj...

3. [What are Projects? - Perplexity Help Center](https://www.perplexity.ai/help-center/en/articles/10352961-what-are-spaces) - A Project is a persistent, shareable workspace in Perplexity that keeps everything for an ongoing ef...

4. [AVIBE Agent x Dr.Alena Krot_14 03 26 (1).pptx](AVIBE Agent x Dr.Alena Krot_14 03 26 (1).pptx)

5. [Bundled Skills Catalog | Hermes Agent - Nous Research](https://hermes-agent.nousresearch.com/docs/reference/skills-catalog) - Hermes ships with a large built-in skill library copied into ~/.hermes/skills/ on install. Each skil...

6. [Optional Skills Catalog | Hermes Agent](https://hermes-agent.nousresearch.com/docs/reference/optional-skills-catalog) - Official optional skills shipped with hermes-agent — install via hermes skills install official/<cat...

7. [GitHub - anthropics/skills: Public repository for Agent Skills](https://github.com/anthropics/skills) - Note: This repository contains Anthropic's implementation of skills for Claude. For information abou...

8. [Equipping agents for the real world with Agent Skills - Anthropic](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) - Discover how Anthropic builds AI agents with practical capabilities through modular skills, enabling...

9. [The Agent Skills Directory](https://www.skills.sh/) - Skills are reusable capabilities for AI agents. Install them with a single command to enhance your a...

10. [Agent Skill Security: Prompt Injection, Capabilities ...](https://skillmd.com/agent-skills-security) - Checks a skill against 68 vulnerability patterns across 17 categories, including prompt injection, d...

11. [Agent Skills Enable a New Class of Realistic and Trivially ...](https://aisagroup.substack.com/p/agent-skills-enable-a-new-class-of) - Agent Skills is a feature that loads instructions from markdown files to give agents task-specific a...

12. [Agent Skills | Microsoft Learn](https://learn.microsoft.com/en-us/agent-framework/agents/skills) - Learn how to extend agent capabilities with Agent Skills - portable packages of instructions, script...

13. [Built-in Tools Reference | Hermes Agent - Nous Research](https://hermes-agent.nousresearch.com/docs/reference/tools-reference) - Skills are your procedural memory. Analyze video content from a URL or file path — captions, scene b...

14. [social-media-skills/skills](https://www.skills.sh/social-media-skills/skills) - 106 agent skills from social-media-skills/skills — including short-form-video-script, hook-writer, b...

15. [hook-writer — social-media-skills/skills](https://www.skills.sh/social-media-skills/skills/hook-writer) - A hook works by opening a gap. Curiosity, tension, stakes, dissonance, self-relevance — the hook cre...

16. [viral-reverse-engineering — social-media-skills/skills](https://www.skills.sh/social-media-skills/skills/viral-reverse-engineering)

17. [content-research-and-sourcing — social-media-skills/skills](https://www.skills.sh/social-media-skills/skills/content-research-and-sourcing) - The research-and-sourcing craft — verify the substance of a piece before it publishes: trace stats t...

18. [social-content — coreyhaines31/marketingskills](https://www.skills.sh/coreyhaines31/marketingskills/social-content) - Expert social media content creation, scheduling, and optimization across all major platforms. Cover...

19. [copywriting — coreyhaines31/marketingskills](https://www.skills.sh/coreyhaines31/marketingskills/copywriting) - Copywriting. You are an expert conversion copywriter. Your goal is to write marketing copy that is c...

20. [seo — mblode/agent-skills](https://www.skills.sh/mblode/agent-skills/seo) - Audits and fixes technical SEO, researches search demand, creates content briefs, and measures SEO/A...

21. [seasonal-and-moment-marketing — social-media-skills/skills](https://www.skills.sh/social-media-skills/skills/seasonal-and-moment-marketing) - The annual moment-planning skill — map the few moments that fit, gate them for fit + authenticity, t...

22. [Overview · social-media-skills/skills · GitHub](https://github.com/social-media-skills/skills/security) - This repository contains Markdown skill files and small build scripts — no runtime code, no dependen...

23. [AGENTS.md - coreyhaines31/marketingskills - GitHub](https://github.com/coreyhaines31/marketingskills/blob/main/AGENTS.md) - This repository contains Agent Skills for AI agents following the Agent Skills specification. Skills...

24. [Security - coreyhaines31/marketingskills - GitHub](https://github.com/coreyhaines31/marketingskills/security) - No security policy detected ... This project has not set up a SECURITY.md file yet. There aren't any...

25. [Designing, Refining, and Maintaining Agent Skills at Perplexity](https://www.perplexity.ai/hub/blog/designing-refining-and-maintaining-agent-skills-at-perplexity) - How Perplexity writes, reviews, and maintains Agent Skills, plus the guide our engineers use to buil...

26. [SkillEvaluator - NVIDIA Documentation](https://docs.nvidia.com/skills/skillevaluator) - SkillEvaluator is an open-source, multi-tier framework for evaluating AI agent artifacts, starting w...

27. [About AI-generated content — TikTok Support](https://support.tiktok.com/en/using-tiktok/creating-videos/ai-generated-content)

28. [How we're helping creators disclose altered or synthetic content](https://blog.youtube/news-and-events/disclosing-ai-generated-content/) - Learn how YouTube's new tool will require creators to disclose to viewers when realistic content is ...

29. [Disclosing use of GenAI content - Android - YouTube Help](https://support.google.com/youtube/answer/14328491?hl=en&co=GENIE.Platform=Android) - To disclose content that is AI-generated or meaningfully AI-altered, the 'AI use' setting is availab...

30. [Code of Practice on Transparency of AI-generated Content](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content) - This code of practice supports compliance with the AI Act transparency obligations related to markin...

31. [Guidelines on transparency obligations for providers and deployers ...](https://digital-strategy.ec.europa.eu/en/policies/guidelines-ai-transparency-obligations) - Article 50 of the AI Act applies from 2 August 2026. It sets out transparency obligations for provid...

32. [How to use Computer Skills - Perplexity Help Center](https://www.perplexity.ai/help-center/en/articles/13914413-how-to-use-computer-skills) - Learn how skills in Perplexity Computer deploy specialist agents, how to create your own skills, and...

