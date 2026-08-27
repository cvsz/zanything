# Anything v2 — Universal AI Operator

Anything v2 is a production-oriented Custom GPT master system designed to route arbitrary user goals into the right combination of reasoning, research, tools, specialist modes, execution loops, and deliverables.

## Core architecture

User
→ Intent Router
→ Task Decomposer
→ Risk / Confirmation Gate
→ Tool Router
→ Specialist Mode(s)
→ Executor
→ Critic / Validator
→ Artifact Builder
→ Final Response

## Included

- Master system prompt
- Intent router
- 20 specialist modes
- Deep Research protocol
- Autonomous project loop
- Image / Movie Poster engine
- Coding / Debugging / DevOps / Security engines
- Data / Document / Spreadsheet / Presentation engines
- Knowledge schema
- Conversation starters
- Actions/OpenAPI architecture
- Example OpenAPI action manifest
- Output contracts
- Safety and confirmation gates
- Evaluation checklist and acceptance tests
- Deployment/configuration guide
- Example workflows

## Suggested GPT capabilities

Enable, when available:
- Web search
- Image generation
- Code interpreter / data analysis
- File handling / knowledge

Use Actions only when you have an external API you control and can secure properly.

## Start here

1. Put `prompts/MASTER_SYSTEM.prompt.md` into the GPT Instructions field.
2. Add the files under `knowledge/` as reference documents if useful.
3. Configure conversation starters from `conversation-starters.json`.
4. Enable the capabilities you want.
5. If using external Actions, adapt `actions/openapi-template.yaml`.
6. Test with `evals/acceptance-tests.md`.

## Design philosophy

Anything v2 is not one giant “answer everything” persona. It is a routing and execution system that activates the minimum specialist set required by each request.

## Version

2.0.0
