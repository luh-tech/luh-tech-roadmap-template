# LuhTech Infrastructure Documentation Schema System

**Version:** 1.2.0  
**Status:** Phase 1 Complete + Portfolio Workflows + Extensions  
**Date:** 2026-01-06  
**Principle:** No Shortcuts, Enterprise Excellence Always

---

## Overview

This schema system provides standardized infrastructure documentation for the LuhTech portfolio. Derived from Ectropy's production infrastructure (202KB infrastructure-catalog.json, 261KB decision-log.json, 153KB current-truth.json), these schemas enable:

- **MCP Server Governance** - Token-efficient AI agent access (97% reduction)
- **Portfolio Intelligence** - Aggregator-level visibility across 8 ventures
- **Accelerator Foundation** - Turnkey templates for new portfolio companies
- **Schema-First Architecture** - Generated models, CI enforcement, no drift
- **Cross-Repo Workflow Discovery** - Portfolio workflows referenced by $ref
- **Venture Extensions** - Explicit sharing control for venture-specific data (NEW)

---

## Schema Inventory

| Schema | Version | Size | Purpose |
|--------|---------|------|---------|
| `roadmap.schema.v2.json` | v2.0.0 | ~19KB | Venture roadmap, quarters, financials, milestones |
| `venture-summary.schema.json` | v1.0.0 | ~11KB | Investor pitch summary |
| `decision-log.schema.v2.json` | v2.0.0 | ~10KB | Enhanced ADR with voting, indexes, implementation tracking |
| `dependencies.schema.json` | v1.0.0 | ~5KB | Cross-venture dependencies |
| `boundaries.schema.json` | v1.0.0 | ~3KB | Fork configuration |
| `infrastructure-catalog.schema.json` | v1.1.0 | ~24KB | Service registry, environments, secrets, workflows |
| `tech-stack.schema.json` | v1.0.0 | ~17KB | Languages, frameworks, databases, architecture patterns |
| `evidence-session.schema.json` | v1.0.0 | ~12KB | Investigation tracking, evidence nodes, retention policies |
| `extensions.schema.v1.json` | v1.0.0 | ~2KB | **NEW**: Venture-specific extensions with share control |

### Portfolio-Level Schemas

| Schema | Version | Size | Purpose |
|--------|---------|------|---------|
| `portfolio/workflow-registry.schema.json` | v1.0.0 | ~11KB | Portfolio workflow definitions, transformers, deck types |
| `portfolio/brand.schema.json` | v1.0.0 | ~11KB | Brand assets, colors, typography |
| `portfolio/portfolio.schema.json` | v1.0.0 | ~16KB | Aggregated portfolio view |
| `portfolio/ip-assets.schema.json` | v1.0.0 | ~10KB | Intellectual property tracking |
| `portfolio/extensions-matrix.schema.v1.json` | v1.0.0 | ~2KB | **NEW**: Portfolio-level extension aggregation |

### Shared Building Blocks

| Schema | Version | Purpose |
|--------|---------|---------|
| `_enums/luhtech-enums.schema.v2.json` | v2.0.0 | Shared enumerations (ventureId, status, etc.) |
| `_definitions/definitions.schema.json` | v1.0.0 | Shared type definitions (contact, money, person, etc.) |

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
│   ├── decision-log.schema.v2.json
│   ├── infrastructure-catalog.schema.json
│   ├── tech-stack.schema.json
│   ├── evidence-session.schema.json
│   └── extensions.schema.v1.json          ← NEW
│
├── PORTFOLIO-LEVEL (Cross-venture operations)
│   ├── portfolio/workflow-registry.schema.json
│   ├── portfolio/brand.schema.json
│   ├── portfolio/portfolio.schema.json
│   ├── portfolio/ip-assets.schema.json
│   └── portfolio/extensions-matrix.schema.v1.json  ← NEW
│
├── _enums/
│   ├── luhtech-enums.schema.json
│   └── luhtech-enums.schema.v2.json
│
└── _definitions/
    └── definitions.schema.json
```

---

## File Structure Per Venture

```
{venture}/.roadmap/
├── roadmap.json                    ← Business roadmap
├── venture-summary.json            ← Investor pitch data
├── dependencies.json               ← Cross-venture links
├── boundaries.json                 ← Fork configuration
├── decision-log.json               ← Architectural decisions (v2)
├── infrastructure-catalog.json     ← Service registry
├── tech-stack.json                 ← Technology documentation
├── extensions.json                 ← Venture-specific extensions (NEW)
└── evidence/                       ← Evidence sessions directory
    └── ...
```

### Portfolio Operations (LuhTech-business)

```
LuhTech-business/.roadmap/
├── portfolio.json                  ← Aggregated portfolio view
├── ip-assets.json                  ← IP tracking
└── extensions-matrix.json          ← Shared extensions from all ventures (NEW)
```

---

## Extensions System (NEW in v1.2.0)

### Purpose

Ventures can define custom data extensions while controlling what is shared with Holdings.

### Venture extensions.json

```json
{
  "$schema": "https://luhtech.dev/schemas/extensions-v1.json",
  "ventureId": "ectropy",
  "lastUpdated": "2026-01-06T20:00:00Z",
  "extensions": {
    "mcp": {
      "share": true,
      "description": "MCP server and tool integration metrics",
      "version": "1.0.0",
      "data": {
        "serverCount": 4,
        "toolCount": 47
      }
    },
    "internal": {
      "share": false,
      "description": "Internal dev notes - not shared",
      "version": "1.0.0",
      "data": {
        "blockers": ["Repository split pending"]
      }
    }
  }
}
```

### Key Fields

| Field | Required | Purpose |
|-------|----------|---------|
| `share` | ✅ | `true` = visible to Holdings, `false` = private |
| `description` | Optional | Human-readable description |
| `version` | Optional | Extension version (semver) |
| `data` | ✅ | Extension payload (any valid JSON) |

### Holdings extensions-matrix.json

Aggregates only `share: true` extensions from all ventures:

```json
{
  "$schema": "https://luhtech.dev/schemas/portfolio/extensions-matrix-v1.json",
  "lastUpdated": "2026-01-06T20:00:00Z",
  "ventures": {
    "ectropy": ["mcp", "spatial", "decisionGraph"],
    "jobsitecontrol": ["hardware", "sensors"],
    "qullqa": ["aduDesign", "permits"],
    "hilja": [],
    "viiva": [],
    "raizal": [],
    "replique": [],
    "luhtech": []
  },
  "sharedExtensions": {
    "ectropy:mcp": { "ventureId": "ectropy", "data": {...} },
    "jobsitecontrol:hardware": { "ventureId": "jobsitecontrol", "data": {...} }
  },
  "stats": {
    "totalVentures": 8,
    "venturesWithExtensions": 3,
    "totalSharedExtensions": 7
  }
}
```

### Data Flow

```
VENTURES                              HOLDINGS
┌──────────────────┐                 ┌──────────────────────────┐
│ extensions.json  │                 │                          │
│ {                │                 │  extensions-matrix.json  │
│   "mcp": {       │──share:true───▶│  - tracks shared         │
│     share: true  │                 │  - aggregates data       │
│   },             │                 │                          │
│   "internal": {  │                 │                          │
│     share: false │──(blocked)──X   │                          │
│   }              │                 │                          │
│ }                │                 └──────────────────────────┘
└──────────────────┘
```

---

## Validation

### CI Pipeline Integration

Add to `.github/workflows/roadmap-ci.yml`:

```yaml
- name: Validate Extensions
  run: |
    if [ -f ".roadmap/extensions.json" ]; then
      npx ajv validate \
        -s schemas/extensions.schema.v1.json \
        -d .roadmap/extensions.json
    fi
```

### Local Validation

```bash
# Install ajv-cli
npm install -g ajv-cli ajv-formats

# Validate extensions
ajv validate -s schemas/extensions.schema.v1.json -d .roadmap/extensions.json
```

---

## Changelog

### v1.2.0 (2026-01-06)
- **NEW**: `extensions.schema.v1.json` v1.0.0
  - Venture-specific extensions with explicit share control
  - Supports any JSON payload in `data` field
  - Version tracking per extension
- **NEW**: `portfolio/extensions-matrix.schema.v1.json` v1.0.0
  - Aggregates shared extensions from all ventures
  - Tracks which ventures share which extensions
  - Summary statistics

### v1.1.0 (2025-12-12)
- **NEW**: `portfolio/workflow-registry.schema.json` v1.0.0
- **UPDATED**: `infrastructure-catalog.schema.json` v1.1.0
  - Added `portfolioWorkflowsRef` for cross-repo workflow discovery

### v1.0.0 (2025-12-11)
- Initial release with core schemas

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
✅ Extension system with explicit sharing (NEW)  

**No shortcuts. Enterprise excellence always.**
