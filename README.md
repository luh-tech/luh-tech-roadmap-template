# ectropy-roadmap-template

> JSON-first documentation system for LuhTech portfolio ventures

## Overview

This template provides the standard `.roadmap/` directory structure for all LuhTech ventures. It enables:

- **Automated aggregation** - Portfolio-wide visibility via roadmap-aggregator CLI
- **Conflict detection** - Resource allocation and cross-venture dependency conflicts
- **Slide generation** - Investor-ready decks from venture-summary.json
- **Decision tracking** - Structured governance and audit trails
- **Fork management** - Track inheritance for platform forks (JtC, Qullqa, Hilja)

## Quick Start

### 1. Create Directory Structure

```bash
mkdir -p .roadmap/metrics
```

### 2. Initialize Core Files

```bash
# Copy schemas for validation
cp -r path/to/ectropy-roadmap-template/schemas .roadmap/

# Create from examples
cp path/to/ectropy-roadmap-template/examples/roadmap.json .roadmap/
```

### 3. Customize for Your Venture

Edit `.roadmap/roadmap.json` with your venture's:
- Identity (id, name, type, architecture)
- Pitch content
- Quarterly roadmap
- Financials and team

### 4. Set Up CI Validation

```bash
cp path/to/ectropy-roadmap-template/.github/workflows/roadmap-sync.yml .github/workflows/
```

## Schemas

| Schema | Purpose | Required |
|--------|---------|----------|
| `roadmap.schema.json` | 18-month venture roadmap | Yes |
| `venture-summary.schema.json` | Investor-ready pitch data | Yes |
| `decision-log.schema.json` | Decision tracking | Yes |
| `dependencies.schema.json` | Cross-venture dependencies | Yes |
| `boundaries.schema.json` | Fork tracking | Only for forks |

## Directory Structure

```
.roadmap/
├── roadmap.json              # Primary roadmap (required)
├── venture-summary.json      # Pitch data (required)
├── decision-log.json         # Decisions (required)
├── dependencies.json         # Dependencies (required)
├── boundaries.json           # Fork tracking (if forked)
└── metrics/
    ├── targets.json          # Success criteria
    └── 2025-12.json          # Monthly snapshots
```

## Integration

### roadmap-aggregator

```bash
# Validate your roadmap
roadmap validate --venture your-venture

# Generate portfolio view
roadmap generate --format markdown
```

### slide-generator

Your `venture-summary.json` feeds directly into automated pitch deck generation with proper brand assets.

### n8n Workflows

Automated triggers for:
- Gate milestone notifications
- Dependency status updates
- Monthly metric collection

## Portfolio Ventures

| Venture | Type | Architecture | Status |
|---------|------|--------------|--------|
| Ectropy | Platform | Cloud-First | Active |
| JobsiteControl | Hardware | Edge-First | Active |
| Qullqa | SaaS | Cloud-First | Active |
| Hilja | Hardware | Edge-First | Active |
| Replique | API | API-Only | Active |
| Raizal | Marketplace | Cloud-First | Active |
| Viiva | Hardware | Edge-First | R&D |
| LuhTech | Platform | Hybrid | Active |

## Documentation

- **[CONTRIBUTING.md](./CONTRIBUTING.md)** - Complete implementation guide
- **[examples/](./examples/)** - Sample JSON files
- **[schemas/](./schemas/)** - JSON Schema definitions

## License

Proprietary - LuhTechnology Ventures

---

*Part of LuhTech Enterprise Infrastructure*
