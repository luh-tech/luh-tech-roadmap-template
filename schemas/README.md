# LuhTech Infrastructure Documentation Schema System

**Version:** 1.1.0  
**Status:** Phase 1 Complete + Portfolio Workflows  
**Date:** 2025-12-12  
**Principle:** No Shortcuts, Enterprise Excellence Always

---

## Overview

This schema system provides standardized infrastructure documentation for the LuhTech portfolio. Derived from Ectropy's production infrastructure (202KB infrastructure-catalog.json, 261KB decision-log.json, 153KB current-truth.json), these schemas enable:

- **MCP Server Governance** - Token-efficient AI agent access (97% reduction)
- **Portfolio Intelligence** - Aggregator-level visibility across 8 ventures
- **Accelerator Foundation** - Turnkey templates for new portfolio companies
- **Schema-First Architecture** - Generated models, CI enforcement, no drift
- **Cross-Repo Workflow Discovery** - Portfolio workflows referenced by $ref (NEW)

---

## Schema Inventory

| Schema | Version | Size | Purpose |
|--------|---------|------|---------|
| `infrastructure-catalog.schema.json` | v1.1.0 | ~24KB | Service registry, environments, secrets, workflows, **portfolioWorkflowsRef** |
| `tech-stack.schema.json` | v1.0.0 | ~15KB | Languages, frameworks, databases, architecture patterns |
| `evidence-session.schema.json` | v1.0.0 | ~14KB | Investigation tracking, evidence nodes, retention policies |
| `decision-log.schema.v2.json` | v2.0.0 | ~12KB | Enhanced ADR with voting, indexes, implementation tracking |
| `luhtech-enums.schema.v2.json` | v2.0.0 | ~16KB | Extended shared enumerations for all schemas |

### Portfolio-Level Schemas

| Schema | Version | Size | Purpose |
|--------|---------|------|---------|
| `portfolio/workflow-registry.schema.json` | v1.0.0 | ~11KB | **NEW**: Portfolio workflow definitions, transformers, deck types |
| `portfolio/brand.schema.json` | v1.0.0 | ~11KB | Brand assets, colors, typography |
| `portfolio/portfolio.schema.json` | v1.0.0 | ~16KB | Aggregated portfolio view |
| `portfolio/ip-assets.schema.json` | v1.0.0 | ~10KB | Intellectual property tracking |

---

## Architecture

### Schema Hierarchy

```
TIER 0: CANONICAL SCHEMAS (Single Source of Truth)
luh-tech/luh-tech-roadmap-template/schemas/

├── VENTURE-LEVEL (Per-venture .roadmap/ files)
│   ├── roadmap.schema.v2.json
│   ├── venture-summary.schema.json
│   ├── dependencies.schema.json
│   ├── boundaries.schema.json
│   ├── infrastructure-catalog.schema.json  ← Updated: portfolioWorkflowsRef
│   ├── tech-stack.schema.json
│   ├── evidence-session.schema.json
│   └── decision-log.schema.v2.json
│
├── PORTFOLIO-LEVEL (Cross-venture operations)
│   ├── portfolio/workflow-registry.schema.json  ← NEW
│   ├── portfolio/brand.schema.json
│   ├── portfolio/portfolio.schema.json
│   └── portfolio/ip-assets.schema.json
│
├── _enums/
│   ├── luhtech-enums.schema.json
│   └── luhtech-enums.schema.v2.json
│
└── _definitions/
    └── definitions.schema.json
```

### Cross-Repo Reference Pattern

The **workflow-registry.schema.json** enables a powerful cross-repo discovery pattern:

```
┌─────────────────────────────────────────────────────────────────┐
│               SCHEMA-FIRST WORKFLOW ARCHITECTURE                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  luh-tech-roadmap-template/schemas/                             │
│  ├── portfolio/workflow-registry.schema.json  ← Schema (Tier 0)│
│  └── infrastructure-catalog.schema.json       ← portfolioRef   │
│                          │                                      │
│                          ▼                                      │
│  business-tools/config/                                         │
│  └── workflow-registry.json  ← Implementation (Source of Truth)│
│            │                                                    │
│            │  $ref: raw.githubusercontent.com/.../workflow...   │
│            ▼                                                    │
│  {venture}/.roadmap/infrastructure-catalog.json                 │
│  └── portfolioWorkflowsRef: { "$ref": "..." }  ← Discovery     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Benefits:**
- Ventures discover portfolio workflows by reference, not duplication
- Schema validates both the registry AND the reference
- Self-documenting via `meta.schemaFirst: true` in data files

---

## File Structure Per Venture

```
{venture}/.roadmap/
├── roadmap.json                    ← Business roadmap
├── venture-summary.json            ← Investor pitch data
├── dependencies.json               ← Cross-venture links
├── boundaries.json                 ← Fork configuration
├── decision-log.json               ← Architectural decisions (v2)
├── infrastructure-catalog.json     ← Service registry + portfolioWorkflowsRef
├── tech-stack.json                 ← Technology documentation
└── evidence/                       ← Evidence sessions directory
    ├── evidence-2025-q4.json
    └── ...
```

### Portfolio Operations (business-tools)

```
business-tools/config/
├── workflow-registry.json          ← Canonical workflow definitions
├── ventures.json                   ← Venture registry
└── brands.json                     ← Brand assets (slide-generator)
```

---

## Workflow Registry Schema

The new `workflow-registry.schema.json` defines:

### Workflows
Portfolio-level operations (validate, aggregate, generate):
```json
{
  "validate-portfolio": {
    "id": "validate-portfolio",
    "tool": "roadmap-aggregator-v3",
    "command": "python -m roadmap_aggregator validate",
    "requires": [],
    "dependencies": { "secrets": ["GITHUB_TOKEN"] }
  }
}
```

### Transformers
Mappings from roadmap.json fields to slide content:
```json
{
  "cover": {
    "id": "cover",
    "requiredFields": ["meta.ventureName", "pitch.oneLiner"],
    "outputType": "slide"
  }
}
```

### Deck Types
Slide deck composition rules:
```json
{
  "investor": {
    "id": "investor",
    "slides": ["cover", "problem", "solution", "market", "business_model", "traction", "team", "ask", "timeline"],
    "requiredCompleteness": 0.8,
    "audience": "investor"
  }
}
```

---

## Self-Documenting Pattern

All workflow registry files MUST include self-documenting metadata:

```json
{
  "$schema": "https://luhtech.dev/schemas/portfolio/workflow-registry-v1.json",
  "schemaVersion": "1.0.0",
  "meta": {
    "lastUpdated": "2025-12-12T00:00:00Z",
    "schemaFirst": true,
    "sourceOfTruth": "luh-tech/business-tools",
    "derivedFrom": "https://luhtech.dev/schemas/portfolio/workflow-registry-v1.json"
  }
}
```

The `schemaFirst: true` field is **required** and **must be true** - this self-documents that the file follows schema-first architecture.

---

## Validation

### CI Pipeline Integration

Add to `.github/workflows/roadmap-ci.yml`:

```yaml
- name: Validate Infrastructure Files
  run: |
    # Validate infrastructure-catalog.json if exists
    if [ -f ".roadmap/infrastructure-catalog.json" ]; then
      npx ajv validate \
        -s schemas/infrastructure-catalog.schema.json \
        -d .roadmap/infrastructure-catalog.json
    fi
    
    # Validate tech-stack.json if exists
    if [ -f ".roadmap/tech-stack.json" ]; then
      npx ajv validate \
        -s schemas/tech-stack.schema.json \
        -d .roadmap/tech-stack.json
    fi

- name: Validate Workflow Registry (business-tools only)
  if: github.repository == 'luh-tech/business-tools'
  run: |
    npx ajv validate \
      -s schemas/portfolio/workflow-registry.schema.json \
      -d config/workflow-registry.json
```

### Local Validation

```bash
# Install ajv-cli
npm install -g ajv-cli ajv-formats

# Validate infrastructure catalog
ajv validate -s schemas/infrastructure-catalog.schema.json -d .roadmap/infrastructure-catalog.json

# Validate workflow registry
ajv validate -s schemas/portfolio/workflow-registry.schema.json -d config/workflow-registry.json
```

---

## Migration Guide

### Adding portfolioWorkflowsRef to Existing Catalogs

For ventures with existing `infrastructure-catalog.json`:

```json
{
  "catalog": {
    "environments": [...],
    "services": [...],
    "workflows": [...],
    "portfolioWorkflowsRef": {
      "$ref": "https://raw.githubusercontent.com/luh-tech/business-tools/main/config/workflow-registry.json",
      "description": "Portfolio-level workflows (validate, aggregate, generate) from business-tools",
      "version": "1.0.0",
      "lastVerified": "2025-12-12T00:00:00Z"
    }
  }
}
```

### New File Creation

For new ventures:

```bash
# Copy template files
cp templates/infrastructure-catalog.json .roadmap/
cp templates/tech-stack.json .roadmap/
cp templates/decision-log.json .roadmap/
mkdir -p .roadmap/evidence
```

---

## Changelog

### v1.1.0 (2025-12-12)
- **NEW**: `portfolio/workflow-registry.schema.json` v1.0.0
  - Workflow definitions with tool, command, dependencies
  - Transformer mappings for slide generation
  - Deck type composition rules
  - Pipeline stage visualization
  - Self-documenting `meta.schemaFirst` pattern
- **UPDATED**: `infrastructure-catalog.schema.json` v1.1.0
  - Added `portfolioWorkflowsRef` for cross-repo workflow discovery
  - Backward compatible (new field is optional)

### v1.0.0 (2025-12-11)
- Initial release
- `infrastructure-catalog.schema.json` v1.0.0
- `tech-stack.schema.json` v1.0.0
- `evidence-session.schema.json` v1.0.0
- `decision-log.schema.v2.json` v2.0.0
- `luhtech-enums.schema.v2.json` v2.0.0

---

## Enterprise Excellence Checkpoint

✅ Schema-first architecture (not code-first)  
✅ Single source of truth (luh-tech-roadmap-template)  
✅ Derived from proven system (Ectropy production)  
✅ Comprehensive documentation  
✅ CI validation ready  
✅ Migration path documented  
✅ Backward compatible  
✅ Cross-repo reference pattern ($ref)  
✅ Self-documenting (meta.schemaFirst)  

**No shortcuts. Enterprise excellence always.**
