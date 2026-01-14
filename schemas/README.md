# LuhTech Infrastructure Documentation Schema System

**Version:** 1.3.0  
**Status:** Phase 1 Complete + Portfolio Workflows + Extensions + URN/Graph System  
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
- **Venture Extensions** - Explicit sharing control for venture-specific data
- **URN Identifiers & Graph System** - Cross-venture entity linking and graph queries (NEW)

---

## Schema Inventory

| Schema | Version | Size | Purpose |
|--------|---------|------|---------|
| `roadmap.schema.v2.2.json` | v2.2.0 | ~25KB | **LATEST** - Venture roadmap with resources block, vendor-agnostic features |
| `roadmap.schema.v2.1.json` | v2.1.0 | ~19KB | Features array, releases tracking |
| `roadmap.schema.v2.json` | v2.0.0 | ~19KB | Venture roadmap, quarters, financials, milestones |
| `venture-summary.schema.json` | v1.0.0 | ~11KB | Investor pitch summary |
| `decision-log.schema.v2.json` | v2.0.0 | ~10KB | Enhanced ADR with voting, indexes, implementation tracking |
| `dependencies.schema.json` | v1.0.0 | ~5KB | Cross-venture dependencies |
| `boundaries.schema.json` | v1.0.0 | ~3KB | Fork configuration |
| `infrastructure-catalog.schema.json` | v1.1.0 | ~24KB | Service registry, environments, secrets, workflows |
| `tech-stack.schema.json` | v1.0.0 | ~17KB | Languages, frameworks, databases, architecture patterns |
| `evidence-session.schema.json` | v1.0.0 | ~12KB | Investigation tracking, evidence nodes, retention policies |
| `extensions.schema.v1.json` | v1.0.0 | ~2KB | Venture-specific extensions with share control |

### Portfolio-Level Schemas

| Schema | Version | Size | Purpose |
|--------|---------|------|---------|
| `portfolio/workflow-registry.schema.json` | v1.0.0 | ~11KB | Portfolio workflow definitions, transformers, deck types |
| `portfolio/brand.schema.json` | v1.0.0 | ~11KB | Brand assets, colors, typography |
| `portfolio/portfolio.schema.json` | v1.0.0 | ~16KB | Aggregated portfolio view |
| `portfolio/ip-assets.schema.json` | v1.0.0 | ~10KB | Intellectual property tracking |
| `portfolio/extensions-matrix.schema.v1.json` | v1.0.0 | ~2KB | Portfolio-level extension aggregation |
| `portfolio/portfolio-graph.schema.v1.json` | v1.0.0 | ~5KB | **NEW**: Portfolio-wide graph structure |

### Shared Building Blocks

| Schema | Version | Purpose |
|--------|---------|---------|
| `_enums/luhtech-enums.schema.v2.json` | v2.0.0 | Shared enumerations (ventureId, status, etc.) |
| `_definitions/definitions.schema.json` | v1.1.0 | Shared type definitions + URN/graph refs |
| `_definitions/graph.schema.json` | v1.0.0 | **NEW**: URN identifiers and graph metadata |

---

## URN Identifier System (NEW in v1.3.0)

### Purpose

Enable cross-venture entity linking, bidirectional graph traversal, and portfolio-wide graph queries. Based on Ectropy V3 production patterns.

### URN Format

```
urn:luhtech:{venture}:{nodeType}:{identifier}
```

### Examples

```
urn:luhtech:ectropy:file:roadmap
urn:luhtech:ectropy:decision:d-2026-01-01-database-ha-upgrade
urn:luhtech:ectropy:service:mcp-server
urn:luhtech:jobsitecontrol:milestone:ms-hardware-v1
urn:luhtech:holdings:venture:ectropy
```

### Node Types

| Type | Description |
|------|-------------|
| `venture` | Portfolio venture |
| `file` | Roadmap file |
| `milestone` | Project milestone |
| `decision` | ADR/decision record |
| `service` | Infrastructure service |
| `evidence` | Evidence session |
| `person` | Team member or stakeholder |
| `ip-asset` | Intellectual property |
| `dependency` | Dependency record |
| `phase` | Roadmap phase |
| `task` | Deliverable/task |
| `metric` | Business metric |
| `extension` | Venture extension |

### Edge Types

| Type | Description |
|------|-------------|
| `fork` | Fork relationship (with weight) |
| `depends-on` | Dependency relationship |
| `blocks` | Blocking relationship |
| `provides` | Provider relationship |
| `consumes` | Consumer relationship |
| `synergy` | Strategic synergy |
| `supersedes` | Decision supersession |
| `references` | General reference |
| `contains` | Parent-child containment |
| `owns` | Ownership relationship |
| `implements` | Implementation relationship |
| `relates-to` | General relationship |

### Graph Metadata Block

Every entity can include bidirectional graph traversal metadata:

```json
{
  "$id": "urn:luhtech:ectropy:decision:d-2026-01-01-example",
  "graphMetadata": {
    "inEdges": [
      "urn:luhtech:ectropy:decision:d-2025-12-parent-decision"
    ],
    "outEdges": [
      "urn:luhtech:ectropy:service:service-affected"
    ]
  }
}
```

### Using URNs in Schemas

Reference URN and graph definitions in your schemas:

```json
{
  "properties": {
    "$id": {
      "$ref": "https://luhtech.dev/schemas/graph.json#/definitions/urn",
      "description": "URN identifier for this entity"
    },
    "graphMetadata": {
      "$ref": "https://luhtech.dev/schemas/graph.json#/definitions/graphMetadata",
      "description": "Graph traversal metadata"
    }
  }
}
```

### Portfolio Graph

The `portfolio-graph.schema.v1.json` enables Holdings-level graph aggregation:

```json
{
  "$schema": "https://luhtech.dev/schemas/portfolio-graph.v1.json",
  "meta": {
    "version": "1.0.0",
    "lastUpdated": "2026-01-06T20:00:00Z",
    "totalNodes": 127,
    "totalEdges": 89,
    "ventures": ["ectropy", "jobsitecontrol", "qullqa"]
  },
  "nodes": [...],
  "edges": [...],
  "indexes": {
    "byType": {
      "venture": ["urn:luhtech:holdings:venture:ectropy", ...],
      "service": ["urn:luhtech:ectropy:service:mcp-server", ...]
    },
    "byVenture": {
      "ectropy": ["urn:luhtech:ectropy:file:roadmap", ...],
      "jobsitecontrol": [...]
    }
  },
  "crossVentureRelationships": [
    {
      "from": "urn:luhtech:jobsitecontrol:venture:jobsitecontrol",
      "to": "urn:luhtech:ectropy:venture:ectropy",
      "type": "fork",
      "sourceVenture": "jobsitecontrol",
      "targetVenture": "ectropy",
      "weight": 0.85
    }
  ]
}
```

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
│   └── extensions.schema.v1.json
│
├── PORTFOLIO-LEVEL (Cross-venture operations)
│   ├── portfolio/workflow-registry.schema.json
│   ├── portfolio/brand.schema.json
│   ├── portfolio/portfolio.schema.json
│   ├── portfolio/ip-assets.schema.json
│   ├── portfolio/extensions-matrix.schema.v1.json
│   └── portfolio/portfolio-graph.schema.v1.json    ← NEW
│
├── _enums/
│   ├── luhtech-enums.schema.json
│   └── luhtech-enums.schema.v2.json
│
└── _definitions/
    ├── definitions.schema.json                      ← Updated with URN refs
    └── graph.schema.json                            ← NEW
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
├── extensions.json                 ← Venture-specific extensions
└── evidence/                       ← Evidence sessions directory
    └── ...
```

### Portfolio Operations (LuhTech-business)

```
LuhTech-business/.roadmap/
├── portfolio.json                  ← Aggregated portfolio view
├── ip-assets.json                  ← IP tracking
├── extensions-matrix.json          ← Shared extensions from all ventures
└── portfolio-graph.json            ← Portfolio-wide graph (NEW)
```

---

## Extensions System

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

---

## Validation

### CI Pipeline Integration

Add to `.github/workflows/roadmap-ci.yml`:

```yaml
- name: Validate Roadmap Files
  run: |
    # Validate core files
    npx ajv validate -s schemas/roadmap.schema.v2.json -d .roadmap/roadmap.json
    
    # Validate extensions if present
    if [ -f ".roadmap/extensions.json" ]; then
      npx ajv validate \
        -s schemas/extensions.schema.v1.json \
        -d .roadmap/extensions.json
    fi

- name: Validate URN Format
  run: |
    # Check all $id fields match URN pattern
    grep -r '"$id"' .roadmap/*.json | \
      grep -v 'urn:luhtech:' && echo "ERROR: Non-URN $id found" && exit 1 || true
```

### Local Validation

```bash
# Install ajv-cli
npm install -g ajv-cli ajv-formats

# Validate extensions
ajv validate -s schemas/extensions.schema.v1.json -d .roadmap/extensions.json

# Validate graph
ajv validate -s schemas/portfolio/portfolio-graph.schema.v1.json -d .roadmap/portfolio-graph.json
```

---

## Changelog

### v1.4.0 (2026-01-14)
- **NEW**: `roadmap.schema.v2.2.json` v2.2.0
  - Added `resources` block (compute, storage, bandwidth, physical, personnel)
  - Added `schemaChangelog` to meta for version tracking
  - Added `inheritedFrom` field for cross-venture feature inheritance
  - Added `vendorEvaluation` for vendor-agnostic features
  - Added `subdomainPattern` for multi-tenant features
  - Added `notes` field for implementation notes
  - Added new feature categories: `hardware`, `mobile`, `marketplace`
  - Added `future` status for deferred features
  - **DEPRECATED**: `financials`, `team`, `competitive` (move to roadmap-business.json)
  - Added `resourceItem` definition for infrastructure planning

### v1.3.0 (2026-01-06)
- **NEW**: `_definitions/graph.schema.json` v1.0.0
  - URN identifier pattern: `urn:luhtech:{venture}:{nodeType}:{identifier}`
  - Graph metadata with bidirectional edges (inEdges/outEdges)
  - Node type enumeration (13 types)
  - Edge type enumeration (12 types)
  - Based on Ectropy V3 production patterns
- **NEW**: `portfolio/portfolio-graph.schema.v1.json` v1.0.0
  - Portfolio-wide graph aggregation
  - Pre-computed indexes (byType, byVenture, byEdgeType, adjacency)
  - Cross-venture relationship tracking
- **UPDATED**: `_definitions/definitions.schema.json` v1.1.0
  - Added URN and graphMetadata references
  - Added $id (URN) to person and organization definitions
  - Added syncStatus for V3 compatibility

### v1.2.0 (2026-01-06)
- **NEW**: `extensions.schema.v1.json` v1.0.0
- **NEW**: `portfolio/extensions-matrix.schema.v1.json` v1.0.0

### v1.1.0 (2025-12-12)
- **NEW**: `portfolio/workflow-registry.schema.json` v1.0.0
- **UPDATED**: `infrastructure-catalog.schema.json` v1.1.0

### v1.0.0 (2025-12-11)
- Initial release with core schemas

---

## Enterprise Excellence Checkpoint

✅ Schema-first architecture (not code-first)  
✅ Single source of truth (luh-tech-roadmap-template)  
✅ Derived from proven system (Ectropy V3 production)  
✅ Comprehensive documentation  
✅ CI validation ready  
✅ Migration path documented  
✅ Backward compatible  
✅ Cross-repo reference pattern ($ref)  
✅ Self-documenting (meta.schemaFirst)  
✅ Extension system with explicit sharing  
✅ URN identifiers for entity linking (NEW)  
✅ Bidirectional graph traversal (NEW)  
✅ Portfolio-wide graph queries (NEW)  

**No shortcuts. Enterprise excellence always.**
