# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-01-27

### Added

#### Reusable Workflow Enhancement
- **PHASE 3: Business Documentation** validation section in `roadmap-validate.yml`
- Validation for `roadmap-business.json` (business roadmap data)
- Validation for `workflow-registry.json` (CI/CD documentation)
- Validation for `metrics-pipeline.json` (observability configuration)
- Validation for `deployment-metrics.json` (Watchtower deployment tracking)
- Validation for `interfaces.json` (MCP tools and API definitions)
- Validation for `features/*.json` (feature specifications)
- Enhanced GitHub Actions summary with phase breakdown

#### Schema Promotion (6 new schemas from Ectropy)
- `feature.schema.json` - Feature specifications with milestones and ROI tracking
- `interfaces.schema.json` - MCP tools and API definitions
- `workflow-registry.schema.json` - CI/CD workflow documentation
- `metrics-pipeline.schema.json` - Observability and failure handling configuration
- `deployment-metrics.schema.json` - Watchtower deployment tracking
- `roadmap-business.schema.json` - Business roadmap with financials and team data

#### Templates
- `templates/roadmap-business.json` - Business roadmap template
- `templates/deployment-metrics.json` - Deployment metrics template
- `templates/workflow-registry.json` - Workflow registry template
- `templates/metrics-pipeline.json` - Metrics pipeline template
- `templates/feature.json` - Feature specification template
- `templates/interfaces.json` - Interfaces definition template

#### Phase 2 Infrastructure Validation
- Added `architecture.json` validation against `architecture-roadmap.schema.v1.json`
- Added `extensions.json` validation against `extensions.schema.v1.json`

### Changed
- Three-phase validation structure (Core → Infrastructure → Business)
- Enhanced summary output with validation phase breakdown
- All new validations are OPTIONAL (backwards compatible)

### Portfolio Impact
- All 8 ventures automatically inherit the enhanced validation
- Ectropy flagship venture is Phase 3 ready
- Other ventures show SKIP (not FAIL) for Phase 3 files

---

## [1.5.0] - 2026-01-27

### Added
- Venture schema rollout with `schema-refs.json` in all 8 ventures
- Comprehensive schema documentation in `schemas/README.md`
- `validate-schemas.yml` workflow template for ventures

### Changed
- Updated all venture `.roadmap/schema-refs.json` to reference v1.5.0

---

## [1.0.0] - Initial Release

### Added
- Core schema library (18 schemas)
- Roadmap schema v2 with quarterly structure
- Venture summary schema for pitch data
- Decision log schema for ADR tracking
- Dependencies and boundaries schemas
- Tech stack and infrastructure catalog schemas
- Reusable `roadmap-validate.yml` workflow
- Basic templates for venture spin-up

---

*Enterprise Excellence. Schema-First. No Shortcuts.*

*LuhTech Holdings*
