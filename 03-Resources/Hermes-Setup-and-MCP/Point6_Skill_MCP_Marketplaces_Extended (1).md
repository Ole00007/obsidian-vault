# Point 6 — Skill & MCP Marketplaces for Competitive-Research-Style Work (Extended)

## Direct Answer
Beyond the five general Claude-Skill directories identified earlier, there is a second, increasingly important category specific to your CRM/agentic-workflow work: **MCP (Model Context Protocol) server registries**, which host the actual tool-connectors (CRM, Airtable, databases, browser automation) that a skill's instructions ultimately call. Both categories are relevant to your work-scope and should be checked together.

## Category A — Agent Skill Directories (Instruction Sets / SKILL.md Files)

| Directory | Focus | Notes |
|---|---|---|
| **Agensi** (agensi.io) | Curated, security-scanned marketplace | 1,600+ skills, creator revenue-share model |
| **ClaudeSkills.info** | Free aggregator directory | Pulls SKILL.md files from GitHub, good for discovery/browsing by category |
| **skills.sh** | CLI-focused install directory | Large community catalog, install-by-command workflow |
| **awesome-claude-skills** (GitHub, multiple forks: travisvn, ComposioHQ, BehiSecc) | Curated open-source lists | 1,000+ production-ready skills, good for finding proven patterns to fork |
| **awesomeskill.ai** | Browsable marketplace | Also pulls from GitHub SKILL.md files |

## Category B — MCP Server Registries (Tool/Connector Layer)
This is the layer directly relevant to your CRM-builder skill's Step 4/5 (linking to Airtable, Flask, HubSpot, etc.) — these registries list the actual servers agents connect to, not just instruction text.

| Registry | Focus | Notes |
|---|---|---|
| **Smithery** (smithery.ai) | Largest public MCP server registry | Breadth-focused, lists thousands of servers with install instructions, no API key needed to browse[web:154] |
| **Glama** (glama.ai) | MCP registry + inspector + gateway | Clean categorized browsing, includes market-intelligence and business-research-oriented MCP servers (e.g. App Store/Play Store competitive intelligence servers), also lets you publish your own[web:159][web:161] |
| **mcpservers.org** | Curated MCP directory | Good for searching by keyword (e.g. "Notion," "CRM," "Airtable") to find ready connectors |
| **AgentZ Store** (emerging, community-built) | New unified marketplace for MCP servers, agents, and workflows in one place | Still early-stage but positioned to unify discovery across servers/agents/workflows[web:164] |

## Comparison: Smithery vs. Glama vs. Agensi
A direct comparison from Agensi's own research frames the three main directories as complementary rather than competing: Smithery optimizes for breadth (largest catalog, minimal curation), Glama optimizes for browsing experience and categorization, and Agensi optimizes for security-vetted quality over raw volume[web:158]. For your CRM/agentic work specifically:
- Use **Smithery or Glama** first to find existing Airtable/HubSpot/database MCP connectors you don't need to build yourself.
- Use **Agensi or awesome-claude-skills** to find proven instruction-layer skill patterns (e.g. data-collection workflows, spreadsheet-generation skills) to adapt rather than write from scratch.

## Practical Next Step for Your Work-Scope
Given your CRM-builder-analyst skill already targets Airtable and Flask integration, search Glama and mcpservers.org specifically for existing **Airtable MCP** and **HubSpot MCP** servers before building custom Flask endpoints — an existing, maintained MCP server is generally lower-maintenance than a custom-built API wrapper, and several are already indexed and ready to install[web:154][web:161].

## Links
- Parent: [[Hermes-Setup-and-MCP-INDEX]]
- Related: [[industry-competitive-analyst-skill (2)]]
