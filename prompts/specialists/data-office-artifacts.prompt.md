# Data / Documents / Spreadsheets / Presentations Implementation Prompt

Implement production Data and Office Artifact capabilities for zanything.

## Data
- Support CSV/XLSX/Parquet/database inputs.
- Inspect schema/types/units/missing values before analysis.
- Preserve lineage and reproducible transforms.
- Separate descriptive evidence from causal claims.
- Add tenant-safe persistence and retention controls.

## Documents
- Structured report/SOP/policy/proposal/manual generation.
- Template and brand-system support.
- Accessible headings, tables and references.
- Versioned artifact metadata and export validation.

## Spreadsheets
- Auditable formulas.
- Data validation and named structures.
- Separate source data from derived calculations.
- Validate formulas, ranges and exported workbook integrity.

## Presentations
- Narrative-first planning.
- One core message per slide.
- Evidence-aware charts/tables.
- Responsive/reusable templates and accessibility considerations.

## Test requirements
- import/export round trips
- malformed inputs
- formula/reference validation
- artifact checksum/versioning
- tenant isolation
- large-file/resource limits
- deterministic transforms where required
- no false claim that an artifact was produced when export failed

## Definition of done
Implementation, automated artifact validation, docs/templates, regression tests, and release evidence are required.
