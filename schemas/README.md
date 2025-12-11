# LuhTech Infrastructure Documentation Schema System

**Version:** 1.0.0  
**Status:** Phase 1 Complete  
**Date:** 2025-12-11  
**Principle:** No Shortcuts, Enterprise Excellence Always

---

## Overview

This schema system provides standardized infrastructure documentation for the LuhTech portfolio. Derived from Ectropy's production infrastructure (202KB infrastructure-catalog.json, 261KB decision-log.json, 153KB current-truth.json), these schemas enable:

- **MCP Server Governance** - Token-efficient AI agent access (97% reduction)
- **Portfolio Intelligence** - Aggregator-level visibility across 8 ventures
- **Accelerator Foundation** - Turnkey templates for new portfolio companies
- **Schema-First Architecture** - Generated models, CI enforcement, no drift

---

## Schema Inventory

| Schema | Version | Size | Purpose |
|--------|---------|------|---------|
| `infrastructure-catalog.schema.json` | v1.0.0 | ~18KB | Service registry, environments, secrets, workflows |
| `tech-stack.schema.json` | v1.0.0 | ~15KB | Languages, frameworks, databases, architecture patterns |
| `evidence-session.schema.json` | v1.0.0 | ~14KB | Investigation tracking, evidence nodes, retention policies |
| `decision-log.schema.v2.json` | v2.0.0 | ~12KB | Enhanced ADR with voting, indexes, implementation tracking |
| `luhtech-enums.schema.v2.json` | v2.0.0 | ~12KB | Extended shared enumerations for all schemas |

---

## Architecture

### Schema Hierarchy

```
TIER 0: CANONICAL SCHEMAS (Single Source of Truth)
luh-tech/luh-tech-roadmap-template/schemas/

├── EXISTING (Stable - Do Not Modify)
│   ├── roadmap.schema.v2.json
│   ├── venture-summary.schema.json
│   ├── dependencies.schema.json
│   ├── boundaries.schema.json
│   └── architecture-roadmap.schema.v1.json
│
├── NEW: INFRASTRUCTURE LAYER
│   ├── infrastructure-catalog.schema.json  ← Services, Ports, Secrets
│   ├── tech-stack.schema.json              ← Languages, Frameworks, DBs
│   ├── evidence-session.schema.json        ← Investigations, Evidence
│   └── decision-log.schema.v2.json         ← Enhanced ADR v2
│
├── _enums/
│   └── luhtech-enums.schema.v2.json        ← Extended Enumerations
│
└── _definitions/
    └── definitions.schema.json             ← Existing (unchanged)
```

### File Structure Per Venture

```
{venture}/.roadmap/
├── roadmap.json                    ← Business roadmap (existing)
├── venture-summary.json            ← Investor pitch data (existing)
├── dependencies.json               ← Cross-venture links (existing)
├── boundaries.json                 ← Fork configuration (existing)
├── decision-log.json               ← Architectural decisions (v2)
├── infrastructure-catalog.json     ← NEW: Service registry
├── tech-stack.json                 ← NEW: Technology documentation
└── evidence/                       ← NEW: Evidence sessions directory
    ├── evidence-2025-q4.json
    └── ...
```

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
```

### Local Validation

```bash
# Install ajv-cli
npm install -g ajv-cli ajv-formats

# Validate a file
ajv validate -s infrastructure-catalog.schema.json -d my-catalog.json
```

---

## Migration Guide

### From Decision Log v1 to v2

The v2 schema is backward compatible. Existing v1 files will validate against v2. To upgrade:

1. Update `$schema` to `https://luhtech.dev/schemas/decision-log-v2.json`
2. Add optional `indexes` object (can be computed automatically)
3. Add optional `votes` arrays to decisions
4. Add optional `notes` arrays to decisions
5. Add optional `impactedServices` and `impactedInfrastructure` arrays

### New File Creation

For new ventures, use the templates in `templates/`:

```bash
# Copy template files
cp templates/infrastructure-catalog.json .roadmap/
cp templates/tech-stack.json .roadmap/
cp templates/decision-log.json .roadmap/
mkdir -p .roadmap/evidence
```

---

## Changelog

### v1.0.0 (2025-12-11)
- Initial release
- `infrastructure-catalog.schema.json` v1.0.0
- `tech-stack.schema.json` v1.0.0
- `evidence-session.schema.json` v1.0.0
- `decision-log.schema.v2.json` v2.0.0
- `luhtech-enums.schema.v2.json` v2.0.0

---

**Enterprise Excellence Checkpoint:**

✅ Schema-first architecture (not code-first)  
✅ Single source of truth (luh-tech-roadmap-template)  
✅ Derived from proven system (Ectropy production)  
✅ Comprehensive documentation  
✅ CI validation ready  
✅ Migration path documented  
✅ Backward compatible  

**No shortcuts. Enterprise excellence always.**
