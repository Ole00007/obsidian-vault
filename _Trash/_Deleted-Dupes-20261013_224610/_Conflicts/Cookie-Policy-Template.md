# Cookie and Tracking Technologies Policy — Universal Template

Status: Reusable template for LexFlow and future projects. Not final legal text.
Scope: Designed to be inserted as a clearly labelled section inside a Privacy Policy, or published as a standalone Cookie Policy page, depending on project needs.
Jurisdiction baseline: EU GDPR + ePrivacy Directive, aligned with Italian Garante guidance. Adapt bracketed fields per project and per applicable local law.
Legal status: This is a structural and compliance-aware template, not legal advice. Final wording must be confirmed by qualified legal counsel for each specific project, entity and jurisdiction before publication.

---

## How to use this template

1. Duplicate this file per project (e.g. `cookie-policy-lexflow.md`, `cookie-policy-<project>.md`).
2. Fill every `[BRACKETED]` field using verified data only. Never invent legal identity, VAT numbers, addresses or provider names.
3. Run an actual technical cookie/tracker audit of the live site before publishing — the audit result is the only valid source for the tables below.
4. Keep this document and the live consent banner behavior in sync. A written policy that does not match actual site behavior is not compliant.
5. Re-review this document whenever a new script, embed, analytics tool, CRM widget, chat tool, font provider, or ad pixel is added to the site.

---

## 1. Introduction

This section explains how **[PROJECT / PRODUCT NAME]** ("we", "us", "our"), operated by **[LEGAL ENTITY NAME]**, uses cookies and similar technologies on **[DOMAIN(S)]**.

This section forms part of our [Privacy Policy / standalone Cookie Policy]. It should be read together with our Privacy Policy at [LINK].

Last updated: [DATE]

---

## 2. What cookies and similar technologies are

Cookies are small text files stored on your device when you visit a website. Similar technologies include:

- local storage and session storage;
- pixels and web beacons;
- SDK-based mobile identifiers (if applicable);
- server-side tracking tied to a device or account identifier.

This policy covers all such technologies, not only cookies in the strict sense, consistent with EU ePrivacy scope.

---

## 3. Categories of cookies we use

### 3.1 Strictly necessary cookies (no consent required)

These cookies are essential for the website or application to function and cannot be disabled in our systems. Under EU ePrivacy rules, strictly necessary cookies are exempt from prior consent, but users must still be informed of their use.

| Cookie / storage name | Provider | Purpose | Duration | Type |
|---|---|---|---|---|
| [name] | [first-party / Cloudflare / hosting] | [e.g. session integrity, load balancing, security, CSRF protection] | [session / X days] | HTTP cookie / local storage |
| [name] | [provider] | [purpose] | [duration] | [type] |

### 3.2 Functional cookies (consent required unless demonstrably necessary)

| Cookie / storage name | Provider | Purpose | Duration |
|---|---|---|---|
| [name] | [provider] | [e.g. language preference, layout preference] | [duration] |

### 3.3 Analytics cookies (consent required)

| Cookie / storage name | Provider | Purpose | Duration |
|---|---|---|---|
| [name] | [provider, e.g. Cloudflare Web Analytics, Plausible, GA4] | [aggregated usage statistics] | [duration] |

### 3.4 Marketing / advertising cookies (consent required)

| Cookie / storage name | Provider | Purpose | Duration |
|---|---|---|---|
| [name] | [provider] | [ad targeting / retargeting / measurement] | [duration] |

### 3.5 Third-party embeds and widgets

| Provider | Purpose | Data shared | Provider policy |
|---|---|---|---|
| [e.g. chat widget, calendar embed, CRM intake widget] | [purpose] | [data category] | [link] |

If no non-essential cookies are used, state explicitly:

> This site currently uses only strictly necessary cookies. No consent banner is required, but this disclosure remains available for transparency.

---

## 4. Consent mechanism

Applicable only if section 3.2, 3.3, 3.4 or 3.5 contains any entry.

- Non-essential cookies and trackers are not loaded until the user provides consent.
- The consent interface offers **Accept**, **Reject**, and **Manage preferences / granular category control** with equal visual prominence.
- No optional category is pre-checked or enabled by default.
- Consent can be withdrawn at any time via [Cookie Settings link / footer control], as easily as it was given.
- Consent status is recorded where legally required, including timestamp and version of this policy accepted.
- Rejecting optional cookies does not restrict access to core site functionality.
- The consent banner and preference center are operable by keyboard and compatible with screen readers.

---

## 5. Legal basis

- Strictly necessary cookies: legitimate interest in operating a secure, functioning service.
- All other cookies and trackers: freely given, specific, informed and unambiguous consent (GDPR Art. 6(1)(a); ePrivacy Directive as implemented locally).

---

## 6. International data transfers

If any cookie or tracking provider processes data outside the EU/EEA, state the transfer mechanism:

> Where data is transferred outside the EU/EEA, we rely on [Standard Contractual Clauses / adequacy decision / other mechanism] as implemented by [provider].

Remove this section if no such transfer occurs.

---

## 7. Your rights

Data subjects may exercise applicable rights (access, rectification, erasure, restriction, portability, objection) regarding data collected via cookies, subject to the same process described in the main Privacy Policy.

---

## 8. Changes to this policy

We may update this policy to reflect changes in the cookies and trackers we use or in applicable law. Material changes will be reflected by updating the "Last updated" date and, where required, by requesting renewed consent.

---

## 9. Contact

Questions about this policy or cookie practices:

- Data controller: [LEGAL ENTITY NAME]
- Registered address: [REGISTERED ADDRESS]
- VAT number / Partita IVA: [P.IVA] *(insert only once verified — do not publish a placeholder value)*
- Codice Fiscale: [CODICE FISCALE], if applicable
- PEC / certified email: [PEC ADDRESS], if applicable
- Privacy contact: [PRIVACY EMAIL]
- Data Protection Officer (if applicable): [DPO NAME / CONTACT]
- Supervisory authority: [Garante per la protezione dei dati personali / relevant DPA] — [authority contact/link]

---

## 10. Pre-publication checklist (do not publish until all are true)

- [ ] Actual technical cookie/tracker audit performed on the live or preview deployment.
- [ ] Every table entry reflects a real, verified cookie or tracker — no placeholder rows left unresolved.
- [ ] Non-essential trackers verified not to load before consent.
- [ ] Consent banner tested for accept / reject / granular control / withdrawal.
- [ ] Legal entity name, address, VAT number and other identity fields verified and complete, or explicitly marked as pending with production blocked accordingly.
- [ ] Reviewed by qualified legal counsel for the applicable jurisdiction(s).
- [ ] Cross-checked against the Privacy Policy for consistency of terminology and links.
- [ ] Multilingual versions (if applicable) reviewed for equivalent legal meaning, not just literal translation.

---

## Appendix: Project-specific instance — LexFlow (draft, pending legal identity data)

Project: LexFlow
Domain: [pending final Cloudflare/custom domain]
Legal entity: [pending — Partita IVA and registered address to be supplied by project owner]
Known current cookies/trackers at time of drafting: not yet confirmed by live technical audit; Hermes must populate Section 3 from an actual scan of the deployed `dist/` artefact before this appendix is considered complete.
Consent requirement: to be determined by the audit result in Section 3. If only strictly necessary cookies are found, no banner is required; the disclosure section above must still be published inside the Privacy Policy.
Status: DRAFT — do not publish until the checklist in Section 10 is fully satisfied and legal identity data is finalized.
