# Deployment / GPT Builder Guide

## Configure

### Name
Anything v2 — Universal AI Operator

### Description
Universal AI operator for research, coding, analysis, images, documents, data, planning, troubleshooting, security, automation, and multi-step execution.

### Instructions
Paste:
`prompts/MASTER_SYSTEM.prompt.md`

### Conversation starters
Copy from:
`conversation-starters.json`

### Recommended capabilities
Enable when available:
- Web search
- Image generation
- Code / data analysis
- File handling

### Knowledge
Upload only relevant reference files.
Do not duplicate the master instructions inside Knowledge unless you intentionally want a frozen reference copy.

## Recommended rollout

1. Configure base GPT.
2. Enable only needed capabilities.
3. Run acceptance tests.
4. Add domain Knowledge.
5. Re-test.
6. Add external Actions last.
7. Re-test high-impact operations carefully.

## Production rules

- Keep Instructions versioned.
- Keep a changelog.
- Maintain a small acceptance-test suite.
- Review knowledge files for stale or contradictory content.
- Review Actions scopes and authorization before publishing.
