# Notion Setup for SEO-HERO

Create a Notion database called `SEO & AEO Tracker` with properties:
- Task_id (text)
- Task_group (select)
- Task_name (text)
- Description_ru (text)
- Owner (person/text)
- Status (select: planned, in_progress, done, needs_review)
- Frequency (select: weekly, monthly, quarterly, once)
- Data_sources (multi-select)
- Refs (url/text)

Hermes agent (SEO-HERO) should:
- Sync this Notion database with `hermes_seo_aeo_agent_tracker.xlsx` and `.csv` once per week.
- Update statuses and add new tasks based on GA4, GSC, Semrush and AI citation checks.


## Links
- Parent: [[seo_hero_alena_tracker_bundle-INDEX]]
- Related: [[seo_hero_cron_setup]]
