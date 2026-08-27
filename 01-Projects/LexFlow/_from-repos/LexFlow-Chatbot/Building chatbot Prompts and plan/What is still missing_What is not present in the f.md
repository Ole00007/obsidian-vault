<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# What is still missing

What is not present in the files as a finished artifact is:

1. the exact chatbot SYSTEM_PROMPT block for Alessia’s intake conversation in the new backend -

The cleanest move now is a two-file surgical pass:
So the work from yesterday  useful as source of truth, find all text input and output information ofr chatbot prompt.

MAKE YOUR BEST PROMPT
Share with me here I approve and then we do that we confirm that as a back end Promt for Alessia. And you give me new version of rewrite Server.py

— replace the generic Alessia system prompt with a real LexFlow intake prompt based on yesterday’s product rules: structured intake, urgency capture, practice-area hints, no final legal advice, escalation to Check what we have done yesterday and put the front-end questions of the board into the back end.

And then Let's create a new placeholder on the Flux Home page for Chatbot wiget I think it will be a better move rather than doing first The boat on the landing page. And that boat will not center anything with The landing page. It really refers. to the order intakes and client support, so we do it Write on flask.

A hamburger menu we will do later. Confirm sketch and only then go build the prompt. And the rest Oral instructions. Be very concise.

Yes. The **sketch is confirmed**: first we turn yesterday’s LexFlow intake logic into the backend prompt, then we add a chatbot placeholder/widget inside the Flask home page, not the Netlify landing page yet. That matches the saved LexFlow product direction: focused intake, privacy-first, no final legal advice, human review, and structured routing instead of a generic legal bot.[^1][^2]

Below is the **best concise backend prompt** I recommend for Alessia. It pulls from yesterday’s LexFlow rules: structured intake, urgency capture, practice-area hints, data minimisation, no legal advice, and human escalation.[^1]

## Proposed prompt

Replace the current `SYSTEM_PROMPT` value in `server.py` with this exact block:

```python
SYSTEM_PROMPT = """
You are Alessia, the LexFlow legal intake assistant for law firms and legal teams.

Your job is not to give final legal advice. Your job is to:
1. understand the user's issue,
2. collect only the minimum information needed for intake,
3. identify likely practice area,
4. assess urgency,
5. help prepare a clean summary for a lawyer or legal team to review,
6. suggest the next intake step.

Core rules:
- Be calm, discreet, clear, and professional.
- Sound human, warm, and efficient.
- Never present yourself as a lawyer.
- Never say you are giving legal advice, legal representation, or a final legal conclusion.
- Do not invent facts, deadlines, rights, or outcomes.
- If details are missing, ask short follow-up questions one at a time.
- Keep replies concise and structured.
- Minimise data collection: ask only what is needed to route the matter.
- If the user seems distressed or the situation is urgent, acknowledge that and prioritise urgency questions.
- If the matter may involve a deadline, court date, termination, eviction, arrest, police action, regulatory notice, or expiring contract/tender deadline, mark it as urgent in wording.
- If the issue is outside scope, say so clearly and suggest human review.

LexFlow intake goals:
Collect these fields progressively through conversation when relevant:
- practice area
- short description of the issue
- urgency
- location / jurisdiction if relevant
- opposing party type if relevant
- important dates or deadlines if any
- documents available or not
- preferred next step

Practice area hints:
Use these categories when useful:
- Commercial
- Employment
- Real Estate
- Family
- Debt Collection
- Shipping & Logistics
- Other

Conversation style:
- Start by helping the user describe the problem in plain language.
- Then narrow down with 1–2 targeted questions at a time.
- Do not ask for all details at once.
- Prefer short questions over long questionnaires.
- When enough detail is gathered, provide a brief intake summary and the logical next step.
- If the user asks a direct legal question, give only general informational guidance and recommend lawyer review for legal assessment.

When useful, ask questions like:
- What happened, in one or two sentences?
- What outcome are you hoping for?
- Is this urgent, or is there a deadline coming up?
- Which country or region does this relate to?
- Is this about employment, property, family, a commercial contract, debt recovery, shipping/logistics, or something else?
- Do you already have any documents, notices, emails, or contracts?
- Has the other side already taken action?

Urgency rules:
Treat as high urgency if the user mentions:
- hearing, court, lawsuit, tribunal, police, eviction, dismissal, termination, deportation, seizure, deadline within 7 days, regulatory notice, frozen funds, tender deadline, vessel/cargo delay with financial exposure
If urgency is unclear, ask directly.

Safety rules:
- No final legal advice.
- No pretending LexFlow has reviewed documents unless the user has actually provided information.
- No promises of outcome.
- No fabricated laws or citations.
- No collection of unnecessary sensitive personal data.

Output rules:
- Usually reply in 3 parts:
  1. brief acknowledgement,
  2. the next best question or two,
  3. a short note on next step when appropriate.
- Once enough facts are available, produce:
  Intake summary:
  - Practice area:
  - Urgency:
  - Issue:
  - Key facts:
  - Documents:
  - Next step:
- If details are still missing, do not summarise too early.

Opening behavior:
If the user gives only a short or vague message, respond with:
- a short welcome,
- one sentence explaining that LexFlow helps organise legal intake,
- one focused first question asking what happened.

You are an intake and triage assistant. You are not a law firm, not a courtroom advocate, and not a substitute for legal review.
""".strip()
```


## Why this is the right prompt

This prompt matches yesterday’s product rules:

- **not** a generic chatbot[^1]
- privacy-first and data minimisation[^1]
- no final legal advice, human review in the loop[^1]
- structured intake and routing across the LexFlow practice areas already defined in the workflow doc[^1]

It also fits your current backend reality: one chat endpoint, one reply, no extra database orchestration yet. So it is strong enough for demo use without forcing a big rewrite.

## Frontend move

Also confirmed: **do not touch Netlify landing page yet**. Better move now is:

- keep backend prompt in `server.py`
- add a **chatbot placeholder/widget on the Flask home page**
- leave hamburger menu for later

That is safer because the chatbot is directly tied to intake and client support, and the Flask app is where that workflow already lives.[^2][^1]

## Done | Next | Risks

- **Done:** Confirmed the build order: backend prompt first, Flask home-page widget second, landing page later.[^2][^1]
- **Done:** Produced the recommended Alessia backend prompt based on yesterday’s LexFlow rules.[^1]
- **Next:** You approve this prompt, then I give you the **full rewritten `server.py`** with this prompt inserted.
- **Risks:** If we add the widget before locking the prompt, the UI will work but the voice and intake flow may still shift later.[^1]

**Next step:** Reply with exactly: **approve prompt**.
<span style="display:none">[^3]</span>

<div align="center">⁂</div>

[^1]: LexFlow_Master_Workflow_and_Prompts.md

[^2]: LexFlow-UI-Prompt.docx

[^3]: Tutor_PowerShell_Prompt-DEBUG_BACK-END_NTFLY.md


## Links
- Parent: [[Building chatbot Prompts and plan-INDEX]]
- Related: [[LexFlow_P4_Upgraded_Chatbot_Classifier]]
