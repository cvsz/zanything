# Intent Router

## Purpose
Classify requests into the smallest useful specialist set.

## Route table

| Signal | Primary mode | Optional secondary modes |
|---|---|---|
| latest/current/find/compare sources | RESEARCH | ANALYSIS, DECISION |
| explain/analyze/evaluate | ANALYSIS | REASONING, RESEARCH |
| write/draft/rewrite | WRITING | DOCUMENT, MARKETING |
| code/build/implement | CODING | ARCHITECTURE, DEBUGGING |
| bug/error/failing | DEBUGGING | CODING, DEVOPS |
| architecture/system design | ARCHITECTURE | SECURITY, DEVOPS |
| security/audit/harden | SECURITY | CODING, DEVOPS |
| deploy/docker/k8s/ci | DEVOPS | SECURITY, DEBUGGING |
| csv/xlsx/data/stats | DATA | SPREADSHEET, ANALYSIS |
| doc/pdf/report | DOCUMENT | WRITING, ANALYSIS |
| spreadsheet/xlsx | SPREADSHEET | DATA |
| slides/pptx/deck | PRESENTATION | DESIGN, WRITING |
| image/poster/logo/concept art | IMAGE | DESIGN |
| movie poster/key art | MOVIE_POSTER | IMAGE, DESIGN |
| ux/ui/product screen | DESIGN | BUSINESS |
| campaign/seo/social/ads | MARKETING | BUSINESS, WRITING |
| strategy/business model | BUSINESS | ANALYSIS, DECISION |
| learn/teach/study | EDUCATION | REASONING |
| troubleshoot/system issue | TROUBLESHOOTING | DEBUGGING, DEVOPS |
| automate/repeat/workflow | AUTOMATION | PROJECT |
| choose/best/which | DECISION | ANALYSIS |
| multi-file/image+text | MULTIMODAL | any |
| do all/end-to-end/project | PROJECT | relevant specialists |

## Selection rule

1. Select one primary mode.
2. Add only specialists that contribute distinct value.
3. Avoid activating every mode for broad but simple questions.
4. Tool use is independent from specialist selection.
