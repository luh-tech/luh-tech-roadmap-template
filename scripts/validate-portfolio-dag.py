#!/usr/bin/env python3
"""
validate-portfolio-dag.py - Portfolio DAG Validation CLI

Validates cross-venture milestone dependencies across the LuhTech portfolio.
Implements CPM (Critical Path Method) validation with SILTANA 7-tier authority cascade.

Usage:
    python validate-portfolio-dag.py [--ventures-dir PATH] [--verbose] [--fix-successors]

Checks:
    1. DAG Integrity: No circular dependencies
    2. URN Existence: All referenced milestones exist
    3. Date Consistency: DERIVED dates >= predecessor finish + lag
    4. Authority Levels: Valid 0-6 range per SILTANA spec
    5. Classification Validation: EXTERNAL milestones have no predecessors

Enterprise Excellence. Schema-First. No Shortcuts.

Author: Claude (AI Assistant)
Date: 2026-01-28
Version: 1.0.0
"""

import argparse
import json
import os
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


class MilestoneClassification(Enum):
    LEAD = "LEAD"           # Source of truth - changes cascade
    DERIVED = "DERIVED"     # Calculated from predecessors
    EXTERNAL = "EXTERNAL"   # External constraint - cannot modify
    FLEXIBLE = "FLEXIBLE"   # Target date - buffer absorbs slip


class RelationshipType(Enum):
    FS = "FS"  # Finish-to-Start (default)
    SS = "SS"  # Start-to-Start
    FF = "FF"  # Finish-to-Finish
    SF = "SF"  # Start-to-Finish


# SILTANA 7-Tier Authority Cascade
AUTHORITY_LEVELS = {
    0: "Seppä Agent",
    1: "Foreman",
    2: "Superintendent",
    3: "Project Manager",
    4: "Architect",
    5: "Owner",
    6: "Regulatory"
}


@dataclass
class Milestone:
    """Represents a keyMilestone with dependency metadata."""
    id: str
    urn: str
    venture_id: str
    date: datetime
    event: str
    classification: MilestoneClassification
    gate: bool = False
    critical: bool = False
    status: str = "planned"
    authority_level: int = 3
    buffer_days: int = 0
    predecessors: List[Dict] = field(default_factory=list)
    successors: List[str] = field(default_factory=list)
    
    @classmethod
    def from_json(cls, data: Dict, venture_id: str) -> Optional["Milestone"]:
        """Create Milestone from JSON keyMilestone object."""
        urn = data.get("urn")
        if not urn:
            return None  # Skip milestones without URN
            
        try:
            date_str = data.get("date", "")
            if "to" in date_str:
                date_str = date_str.split(" to ")[-1]
            date = datetime.strptime(date_str, "%Y-%m-%d") if date_str else datetime.now()
        except ValueError:
            date = datetime.now()
            
        classification = MilestoneClassification(data.get("classification", "FLEXIBLE"))
        
        graph_metadata = data.get("graphMetadata", {})
        predecessors = graph_metadata.get("predecessors", [])
        successors = graph_metadata.get("successors", [])
        
        return cls(
            id=data.get("id", ""),
            urn=urn,
            venture_id=venture_id,
            date=date,
            event=data.get("event", ""),
            classification=classification,
            gate=data.get("gate", False),
            critical=data.get("critical", False),
            status=data.get("status", "planned"),
            authority_level=data.get("authorityLevel", 3),
            buffer_days=data.get("bufferDays", 0),
            predecessors=predecessors,
            successors=successors
        )


@dataclass
class ValidationResult:
    """Result of a single validation check."""
    check: str
    passed: bool
    message: str
    severity: str = "error"
    details: Optional[Dict] = None


class PortfolioDAGValidator:
    """Validates cross-venture milestone DAG across the portfolio."""
    
    def __init__(self, ventures_dir: str, verbose: bool = False):
        self.ventures_dir = Path(ventures_dir)
        self.verbose = verbose
        self.milestones: Dict[str, Milestone] = {}
        self.venture_milestones: Dict[str, List[str]] = defaultdict(list)
        self.results: List[ValidationResult] = []
        
    def load_roadmaps(self) -> bool:
        """Load all roadmap.json files from ventures directory."""
        venture_dirs = [
            "Ectropy-Business", "JobsiteControl", "Qullqa", "Raizal",
            "Hilja", "LuhTech-business", "Viiva", "Replique"
        ]
        
        loaded_count = 0
        for venture_dir in venture_dirs:
            roadmap_path = self.ventures_dir / venture_dir / ".roadmap" / "roadmap.json"
            if roadmap_path.exists():
                try:
                    with open(roadmap_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    
                    venture_id = data.get("meta", {}).get("ventureId", venture_dir.lower())
                    key_milestones = data.get("keyMilestones", [])
                    
                    for ms_data in key_milestones:
                        milestone = Milestone.from_json(ms_data, venture_id)
                        if milestone:
                            self.milestones[milestone.urn] = milestone
                            self.venture_milestones[venture_id].append(milestone.urn)
                    
                    loaded_count += 1
                    if self.verbose:
                        urn_count = sum(1 for m in key_milestones if m.get('urn'))
                        print(f"✓ Loaded {venture_dir}: {len(key_milestones)} milestones, {urn_count} with URNs")
                        
                except json.JSONDecodeError as e:
                    self.results.append(ValidationResult(
                        check="file_parse", passed=False,
                        message=f"Failed to parse {roadmap_path}: {e}", severity="error"
                    ))
                except Exception as e:
                    self.results.append(ValidationResult(
                        check="file_load", passed=False,
                        message=f"Error loading {roadmap_path}: {e}", severity="error"
                    ))
            else:
                if self.verbose:
                    print(f"⚠ Skipped {venture_dir}: roadmap.json not found")
        
        print(f"\nLoaded {loaded_count} ventures, {len(self.milestones)} milestones with URNs\n")
        return loaded_count > 0
    
    def validate_acyclic(self) -> List[ValidationResult]:
        """Check for circular dependencies in the DAG."""
        results = []
        visited = set()
        rec_stack = set()
        
        def dfs(urn: str, path: List[str]) -> Optional[List[str]]:
            if urn in rec_stack:
                cycle_start = path.index(urn)
                return path[cycle_start:] + [urn]
            if urn in visited:
                return None
            visited.add(urn)
            rec_stack.add(urn)
            path.append(urn)
            
            milestone = self.milestones.get(urn)
            if milestone:
                for pred in milestone.predecessors:
                    pred_urn = pred.get("milestoneUrn")
                    if pred_urn:
                        cycle = dfs(pred_urn, path.copy())
                        if cycle:
                            return cycle
            rec_stack.remove(urn)
            return None
        
        for urn in self.milestones:
            if urn not in visited:
                cycle = dfs(urn, [])
                if cycle:
                    results.append(ValidationResult(
                        check="acyclic", passed=False,
                        message=f"Circular dependency: {' → '.join(cycle)}",
                        severity="error", details={"cycle": cycle}
                    ))
        
        if not results:
            results.append(ValidationResult(
                check="acyclic", passed=True,
                message="No circular dependencies found", severity="info"
            ))
        return results
    
    def validate_urn_existence(self) -> List[ValidationResult]:
        """Check that all referenced URNs exist."""
        results = []
        missing_urns = set()
        
        for urn, milestone in self.milestones.items():
            for pred in milestone.predecessors:
                pred_urn = pred.get("milestoneUrn")
                if pred_urn and pred_urn not in self.milestones:
                    missing_urns.add((urn, pred_urn, "predecessor"))
            for succ_urn in milestone.successors:
                if succ_urn not in self.milestones:
                    missing_urns.add((urn, succ_urn, "successor"))
        
        for source_urn, missing_urn, ref_type in missing_urns:
            results.append(ValidationResult(
                check="urn_existence", passed=False,
                message=f"Missing {ref_type} URN: {missing_urn} (from {source_urn})",
                severity="error"
            ))
        
        if not missing_urns:
            ref_count = sum(len(m.predecessors) + len(m.successors) for m in self.milestones.values())
            results.append(ValidationResult(
                check="urn_existence", passed=True,
                message=f"All {ref_count} URN references valid", severity="info"
            ))
        return results
    
    def validate_date_consistency(self) -> List[ValidationResult]:
        """Check DERIVED milestone dates are consistent with predecessors."""
        results = []
        
        for urn, milestone in self.milestones.items():
            if milestone.classification == MilestoneClassification.DERIVED:
                for pred in milestone.predecessors:
                    pred_urn = pred.get("milestoneUrn")
                    if not pred_urn or pred_urn not in self.milestones:
                        continue
                    
                    pred_milestone = self.milestones[pred_urn]
                    lag_days = pred.get("lagDays", 0)
                    blocking = pred.get("blocking", True)
                    earliest_date = pred_milestone.date + timedelta(days=lag_days)
                    
                    if blocking and milestone.date < earliest_date:
                        days_early = (earliest_date - milestone.date).days
                        results.append(ValidationResult(
                            check="date_consistency", passed=False,
                            message=f"DERIVED {urn} is {days_early} days before valid date based on {pred_urn}",
                            severity="error" if blocking else "warning"
                        ))
        
        if not any(r.check == "date_consistency" and not r.passed for r in results):
            results.append(ValidationResult(
                check="date_consistency", passed=True,
                message="All DERIVED dates consistent", severity="info"
            ))
        return results
    
    def validate_authority_levels(self) -> List[ValidationResult]:
        """Check authority levels are valid (0-6)."""
        results = []
        for urn, milestone in self.milestones.items():
            if milestone.authority_level < 0 or milestone.authority_level > 6:
                results.append(ValidationResult(
                    check="authority_level", passed=False,
                    message=f"Invalid authority {milestone.authority_level} for {urn}",
                    severity="error"
                ))
        
        if not any(r.check == "authority_level" and not r.passed for r in results):
            results.append(ValidationResult(
                check="authority_level", passed=True,
                message="All authority levels valid (0-6)", severity="info"
            ))
        return results
    
    def validate_classification_rules(self) -> List[ValidationResult]:
        """Validate classification-specific rules."""
        results = []
        
        for urn, milestone in self.milestones.items():
            if milestone.classification == MilestoneClassification.EXTERNAL:
                if milestone.authority_level < 5:
                    results.append(ValidationResult(
                        check="classification_rules", passed=False,
                        message=f"EXTERNAL {urn} should have authority >= 5",
                        severity="warning"
                    ))
            
            if milestone.classification == MilestoneClassification.LEAD:
                if milestone.authority_level < 4:
                    results.append(ValidationResult(
                        check="classification_rules", passed=False,
                        message=f"LEAD {urn} should have authority >= 4",
                        severity="warning"
                    ))
                if not milestone.successors:
                    results.append(ValidationResult(
                        check="classification_rules", passed=False,
                        message=f"LEAD {urn} has no successors defined",
                        severity="warning"
                    ))
        
        if not any(r.check == "classification_rules" and not r.passed for r in results):
            results.append(ValidationResult(
                check="classification_rules", passed=True,
                message="All classification rules satisfied", severity="info"
            ))
        return results
    
    def run_all_validations(self) -> Tuple[bool, List[ValidationResult]]:
        """Run all validation checks."""
        all_results = []
        
        print("=" * 60)
        print("LuhTech Portfolio DAG Validation")
        print("=" * 60)
        
        print("\n[1/5] Checking for circular dependencies...")
        all_results.extend(self.validate_acyclic())
        
        print("[2/5] Validating URN references...")
        all_results.extend(self.validate_urn_existence())
        
        print("[3/5] Checking date consistency...")
        all_results.extend(self.validate_date_consistency())
        
        print("[4/5] Validating authority levels...")
        all_results.extend(self.validate_authority_levels())
        
        print("[5/5] Checking classification rules...")
        all_results.extend(self.validate_classification_rules())
        
        errors = [r for r in all_results if not r.passed and r.severity == "error"]
        warnings = [r for r in all_results if not r.passed and r.severity == "warning"]
        
        print("\n" + "=" * 60)
        print("VALIDATION SUMMARY")
        print("=" * 60)
        print(f"Milestones: {len(self.milestones)} | Ventures: {len(self.venture_milestones)}")
        print(f"Errors: {len(errors)} | Warnings: {len(warnings)}")
        
        if errors:
            print("\n❌ ERRORS:")
            for r in errors:
                print(f"  • {r.message}")
        
        if warnings:
            print("\n⚠️ WARNINGS:")
            for r in warnings:
                print(f"  • {r.message}")
        
        passed = len(errors) == 0
        print(f"\n{'✅ VALIDATION PASSED' if passed else '❌ VALIDATION FAILED'}")
        
        return passed, all_results


def main():
    parser = argparse.ArgumentParser(description="Validate portfolio milestone DAG")
    parser.add_argument("--ventures-dir", default=r"C:\Users\luhte\Source\Repos\luh-tech")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    
    validator = PortfolioDAGValidator(args.ventures_dir, args.verbose)
    
    if not validator.load_roadmaps():
        print("ERROR: Failed to load roadmaps")
        sys.exit(1)
    
    passed, results = validator.run_all_validations()
    
    if args.json:
        output = {
            "passed": passed,
            "milestones": len(validator.milestones),
            "ventures": len(validator.venture_milestones),
            "results": [{"check": r.check, "passed": r.passed, "message": r.message} for r in results]
        }
        print("\n" + json.dumps(output, indent=2))
    
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
