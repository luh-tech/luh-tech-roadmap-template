# Contributing to the Ectropy Roadmap Template

This document provides comprehensive guidance for implementing the `.roadmap/` directory structure in LuhTech portfolio ventures.

## Overview

The `.roadmap/` template provides a **JSON-first documentation system** that enables:

- **Automated aggregation** across the LuhTech portfolio
- **Conflict detection** for resource allocation and dependencies
- **Slide generation** for investor pitches and accelerator reporting
- **Decision tracking** for governance and audit trails
- **Fork management** for ventures inheriting from Ectropy platform

## Directory Structure

Every venture repository should contain:

```
{venture-repo}/
├── .roadmap/
│   ├── roadmap.json              # Primary 18-month roadmap
│   ├── venture-summary.json      # Investor-ready pitch data
│   ├── decision-log.json         # Key decisions with context
│   ├── dependencies.json         # Cross-venture dependencies
│   ├── boundaries.json           # Fork inheritance (forked repos only)
│   └── metrics/
│       ├── targets.json          # Success criteria definitions
│       └── {YYYY-MM}.json        # Monthly metric snapshots
│
├── docs/
│   ├── ROADMAP.md               # Human-readable (auto-generated)
│   └── VENTURE-SUMMARY.md       # One-pager (auto-generated)
│
└── .github/
    └── workflows/
        └── roadmap-sync.yml     # CI: validate + notify aggregator
```

## Schema Files

### 1. roadmap.json (Required)

Core roadmap with venture metadata, pitch, quarters, financials, team, and milestones.
**Schema**: `schemas/roadmap.schema.json`

### 2. venture-summary.json (Required)

Investor-ready summary integrating with slide-generator.
**Schema**: `schemas/venture-summary.schema.json`

### 3. decision-log.json (Required)

Structured decisions with context, alternatives, and rationale.
**Schema**: `schemas/decision-log.schema.json`

Categories: architecture, infrastructure, api-design, governance, business, product, team, funding, legal

### 4. dependencies.json (Required)

Cross-venture dependency tracking.
**Schema**: `schemas/dependencies.schema.json`

Types: venture, template, infrastructure, api, data, team, external

### 5. boundaries.json (Forked Repos Only)

Fork tracking with inherited/removed/added paths and upstream sync config.
**Schema**: `schemas/boundaries.schema.json`

## Validation

```bash
# Install ajv-cli
npm install -g ajv-cli

# Validate roadmap
ajv validate -s schemas/roadmap.schema.json -d .roadmap/roadmap.json
```

## Integration

### roadmap-aggregator
```bash
roadmap pull --all
roadmap validate --venture ectropy
roadmap analyze --conflicts
roadmap generate --format markdown
```

### slide-generator
Uses `venture-summary.json` for automated pitch deck generation with brand assets.

### n8n Workflows
Triggers on `.roadmap/` changes, gate milestones, and dependency updates.

## Best Practices

1. **JSON as Source of Truth** - Never edit generated Markdown
2. **Quarterly Updates** - Start/end of quarter + major milestones
3. **Decision Logging** - Architectural changes, alternatives, pivots
4. **Cross-Venture Coordination** - Check conflicts, document both sides
5. **Fork Management** - Create boundaries.json immediately

## Migration Guide

1. Create directory: `mkdir -p .roadmap/metrics`
2. Copy schemas for reference
3. Create initial JSON files
4. Migrate existing docs from Notion/Google Docs
5. Set up CI validation workflow

---

*Template maintained by LuhTech Enterprise Infrastructure*
*Version 1.0.0 - December 9, 2025*
