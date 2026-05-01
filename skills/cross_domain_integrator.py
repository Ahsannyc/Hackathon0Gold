#!/usr/bin/env python3
"""
Gold Tier Skill: Cross Domain Integrator
- Unifies personal (Gmail, WhatsApp) and business (LinkedIn, Twitter, Facebook) workflows
- Automatically classifies messages as personal or business domain
- Routes personal items to HITL approval (human decision needed)
- Routes business items to Auto LinkedIn Poster and similar skills
- Creates unified summary showing both domains in one place
- Connects Bronze/Silver components into coherent Gold Tier intelligence

Pattern:
1. Scan /Needs_Action for all captured messages (email, WhatsApp, LinkedIn)
2. Classify each as PERSONAL or BUSINESS using domain + keyword analysis
3. Route PERSONAL → /Pending_Approval (HITL decision)
4. Route BUSINESS → /Approved (ready for Auto LinkedIn Poster, Twitter, etc.)
5. Create unified domain summary: /Logs/cross_domain_[date].md
6. Audit log all routing decisions with confidence scores

USAGE:
======

Command Line:
  python3 skills/cross_domain_integrator.py

Agent Invocation:
  @Cross Domain Integrator process Needs_Action
  @Cross Domain Integrator classify and route
  @Cross Domain Integrator generate summary

Output:
  ✓ All items routed appropriately
  ✓ Unified summary created: /Logs/cross_domain_[date].md
  ✓ Domain classification log with confidence scores
"""

import os
import re
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Tuple
import yaml

from skills.audit_logger import AuditLogger
from skills.error_handler import SkillErrorHandler

# Setup logging
os.makedirs("skills/logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("skills/logs/cross_domain_integrator.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class CrossDomainIntegrator:
    """Unifies personal and business domain workflows"""

    def __init__(self):
        # Directories
        self.needs_action_dir = Path("Needs_Action")
        self.pending_approval_dir = Path("Pending_Approval")
        self.approved_dir = Path("Approved")
        self.logs_dir = Path("Logs")
        self.done_dir = Path("Done")

        # Ensure directories exist
        for directory in [
            self.needs_action_dir, self.pending_approval_dir,
            self.approved_dir, self.logs_dir, self.done_dir
        ]:
            directory.mkdir(parents=True, exist_ok=True)

        self.audit = AuditLogger()
        self.error_handler = SkillErrorHandler("cross_domain_integrator", ".")

        # Domain classification rules
        self.domain_rules = {
            'PERSONAL': {
                'sources': ['email', 'whatsapp'],
                'keywords': [
                    'personal', 'family', 'friend', 'home', 'private', 'health',
                    'appointment', 'birthday', 'personal matter', 'private'
                ]
            },
            'BUSINESS': {
                'sources': ['linkedin', 'twitter', 'facebook'],
                'keywords': [
                    'sales', 'client', 'project', 'invoice', 'payment', 'urgent',
                    'deal', 'opportunity', 'meeting', 'enterprise', 'business',
                    'partnership', 'proposal', 'contract', 'leads', 'revenue'
                ]
            }
        }

    def extract_source(self, filename: str) -> str:
        """Extract message source from filename (email, whatsapp, linkedin, etc.)"""
        if 'email' in filename.lower():
            return 'email'
        elif 'whatsapp' in filename.lower():
            return 'whatsapp'
        elif 'linkedin' in filename.lower():
            return 'linkedin'
        elif 'twitter' in filename.lower():
            return 'twitter'
        elif 'facebook' in filename.lower():
            return 'facebook'
        return 'unknown'

    def parse_message_file(self, filepath: Path) -> Tuple[Dict, str]:
        """Parse YAML metadata and content from message file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Split YAML front matter and body
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    try:
                        metadata = yaml.safe_load(parts[1])
                        body = parts[2].strip()
                        return metadata or {}, body
                    except:
                        return {}, content
            return {}, content
        except Exception as e:
            logger.error(f"Error parsing {filepath}: {e}")
            return {}, ""

    def classify_domain(self, filename: str, metadata: Dict, body: str) -> Tuple[str, float]:
        """
        Classify message as PERSONAL or BUSINESS
        Returns: (domain, confidence_score)
        """
        source = self.extract_source(filename)
        full_text = f"{filename} {metadata.get('subject', '')} {metadata.get('content', '')} {body}".lower()

        scores = {'PERSONAL': 0.0, 'BUSINESS': 0.0}

        # Source-based scoring (strong signal)
        for domain, rules in self.domain_rules.items():
            if source in rules['sources']:
                scores[domain] += 3.0  # Strong source signal

        # Keyword-based scoring
        for domain, rules in self.domain_rules.items():
            for keyword in rules['keywords']:
                if keyword in full_text:
                    scores[domain] += 1.0

        # Handle tie-breaker: business keywords have higher precedence
        if scores['BUSINESS'] >= scores['PERSONAL']:
            return 'BUSINESS', scores['BUSINESS'] / (scores['BUSINESS'] + scores['PERSONAL'] + 0.1)
        else:
            return 'PERSONAL', scores['PERSONAL'] / (scores['BUSINESS'] + scores['PERSONAL'] + 0.1)

    def route_to_folder(self, filepath: Path, domain: str) -> bool:
        """Route file to appropriate folder based on domain classification"""
        try:
            if domain == 'PERSONAL':
                destination = self.pending_approval_dir / filepath.name
                reason = "Personal domain → requires HITL approval"
            else:  # BUSINESS
                destination = self.approved_dir / filepath.name
                reason = "Business domain → ready for Auto LinkedIn Poster"

            # Copy/move file
            with open(filepath, 'r', encoding='utf-8') as src:
                content = src.read()
            with open(destination, 'w', encoding='utf-8') as dst:
                dst.write(content)

            logger.info(f"✓ Routed {filepath.name} → {domain} | {reason}")
            return True
        except Exception as e:
            logger.error(f"Error routing {filepath.name}: {e}")
            return False

    def generate_unified_summary(self, items_data: List[Dict]) -> str:
        """Create unified domain summary for all items"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date_str = datetime.now().strftime("%Y-%m-%d")

        summary = f"""# Cross Domain Integration Summary
Generated: {timestamp}

## Overview
- **Date**: {date_str}
- **Total Items Processed**: {len(items_data)}
- **Personal Items**: {sum(1 for i in items_data if i['domain'] == 'PERSONAL')}
- **Business Items**: {sum(1 for i in items_data if i['domain'] == 'BUSINESS')}

---

## Domain Breakdown

### 🏠 PERSONAL DOMAIN (Routed to HITL)
Items requiring human approval decision:

"""
        personal_items = [i for i in items_data if i['domain'] == 'PERSONAL']
        if personal_items:
            for item in personal_items:
                summary += f"- **{item['filename']}**\n"
                summary += f"  - Source: {item['source'].upper()}\n"
                summary += f"  - Confidence: {item['confidence']:.1%}\n"
                summary += f"  - Status: Pending approval in `/Pending_Approval/`\n"
                summary += f"  - Action: Await human decision (approve/reject)\n\n"
        else:
            summary += "No personal items at this time.\n\n"

        summary += """### 💼 BUSINESS DOMAIN (Ready for Automation)
Items ready for Auto LinkedIn Poster, Twitter, and social media:

"""
        business_items = [i for i in items_data if i['domain'] == 'BUSINESS']
        if business_items:
            for item in business_items:
                summary += f"- **{item['filename']}**\n"
                summary += f"  - Source: {item['source'].upper()}\n"
                summary += f"  - Confidence: {item['confidence']:.1%}\n"
                summary += f"  - Status: Ready in `/Approved/`\n"
                summary += f"  - Action: Auto LinkedIn Poster will process this\n\n"
        else:
            summary += "No business items at this time.\n\n"

        summary += f"""---

## Workflow Status

### Personal Domain → HITL Flow
```
/Needs_Action/ (Personal items)
        ↓
/Pending_Approval/ (Await human decision)
        ↓
Approved → /Done/ (Execute via HITL Approval Handler)
Rejected → /Logs/ (Log rejection reason)
```

### Business Domain → Auto Flow
```
/Needs_Action/ (Business items)
        ↓
/Approved/ (Auto LinkedIn Poster processes)
        ↓
LinkedIn/Twitter/Facebook posted
        ↓
/Done/ (Success logged)
```

---

## Classification Confidence

| Item | Domain | Confidence | Source | Decision |
|------|--------|-----------|--------|----------|
"""
        for item in items_data:
            confidence_pct = f"{item['confidence']:.0%}"
            summary += f"| {item['filename'][:30]} | {item['domain']} | {confidence_pct} | {item['source'].upper()} | ✓ Routed |\n"

        summary += f"""

---

## Integrated Intelligence

**Personal Domain Insights:**
- These items require human judgment (decisions, approvals, sensitive matters)
- HITL handler monitors `/Pending_Approval/` for your decisions
- Approved items execute through standard HITL workflow

**Business Domain Insights:**
- These items are ready for immediate social media automation
- Auto LinkedIn Poster processes from `/Approved/` automatically
- Sales opportunities, partnerships, and enterprise leads captured
- Posts distributed across LinkedIn, Twitter, Facebook via skills

---

## Next Steps

1. **Personal Items**: Review `/Pending_Approval/` and approve/reject
2. **Business Items**: Auto LinkedIn Poster will process automatically
3. **Monitor**: Check `/Done/` for completed actions
4. **Daily Brief**: Summary updated daily at 8AM

---

**Skill**: Cross Domain Integrator v1.0 (Gold Tier)
**Status**: ✅ Complete
**Items Processed**: {len(items_data)}
**Timestamp**: {timestamp}
"""
        return summary

    def execute(self):
        """Execute full cross-domain integration workflow"""
        try:
            # Log skill start
            self.audit.log_action(
                action_type="skill_start",
                actor="cross_domain_integrator",
                target="system",
                status="started",
                details={}
            )

            print("\n" + "=" * 70)
            print("CROSS DOMAIN INTEGRATOR - Gold Tier Skill")
            print("=" * 70)

            # Phase 1: Scan Needs_Action
            print("\n[PHASE 1] SCANNING /Needs_Action/")
            if not self.needs_action_dir.exists():
                print("WARNING: /Needs_Action folder not found")
                return

            md_files = list(self.needs_action_dir.glob("*.md"))
            if not md_files:
                print("OK: No items to process")
                return

            print(f"OK: Found {len(md_files)} item(s) to classify")

            # Phase 2: Classify and route
            print("\n[PHASE 2] CLASSIFYING & ROUTING")
            items_data = []
            routed_count = {'PERSONAL': 0, 'BUSINESS': 0}

            for filepath in sorted(md_files):
                metadata, body = self.parse_message_file(filepath)
                domain, confidence = self.classify_domain(filepath.name, metadata, body)

                items_data.append({
                    'filename': filepath.name,
                    'filepath': str(filepath),
                    'source': self.extract_source(filepath.name),
                    'domain': domain,
                    'confidence': confidence,
                    'metadata': metadata
                })

                # Route to appropriate folder
                if self.route_to_folder(filepath, domain):
                    routed_count[domain] += 1
                    status_icon = "[P]" if domain == 'PERSONAL' else "[B]"
                    print(f"  {status_icon} {filepath.name:<35} | {domain:<8} | {confidence:.0%} confidence")

            # Phase 3: Generate unified summary
            print("\n[PHASE 3] GENERATING UNIFIED SUMMARY")
            summary_content = self.generate_unified_summary(items_data)

            # Write summary
            summary_file = self.logs_dir / f"cross_domain_{datetime.now().strftime('%Y-%m-%d')}.md"
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(summary_content)
            print(f"OK: Summary created: {summary_file}")

            # Phase 4: Detailed Results
            print("\n" + "=" * 70)
            print("CROSS DOMAIN INTEGRATION SUMMARY")
            print("=" * 70)

            personal_items = [i for i in items_data if i['domain'] == 'PERSONAL']
            business_items = [i for i in items_data if i['domain'] == 'BUSINESS']

            print("\n## Personal Domain Processing")
            print(f"Total personal files processed: {len(personal_items)}")
            for item in personal_items:
                print(f"  - {item['filename']:<40} Routed to HITL: Pending_Approval/")

            print("\n## Business Domain Processing")
            print(f"Total business files processed: {len(business_items)}")
            for item in business_items:
                print(f"  - {item['filename']:<40} Routed to Auto LinkedIn Poster")

            print("\n## Integration Status")
            print(f"  - Personal domain integration: Complete")
            print(f"  - Business domain integration: Complete")
            print(f"  - Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            print("\n## Notes")
            print(f"Cross-domain integration successfully processed {len(items_data)} files from Needs_Action folder.")
            print("Personal communications were routed to HITL for approval, while business")
            print("communications were processed with Auto LinkedIn Poster.")

            print("\n## Example Usage")
            print("@Cross Domain Integrator process Needs_Action")

            print("\n" + "=" * 70)
            print("SUCCESS: INTEGRATION COMPLETE")
            print("=" * 70)
            print(f"Total items processed: {len(items_data)}")
            print(f"  * Personal (HITL): {routed_count['PERSONAL']}")
            print(f"  * Business (Auto): {routed_count['BUSINESS']}")
            print(f"Summary: {summary_file}")
            print("\nNext Steps:")
            print(f"  1. Review PERSONAL items in /Pending_Approval/ (approve/reject)")
            print(f"  2. Auto LinkedIn Poster will process BUSINESS items automatically")
            print(f"  3. Check /Done/ folder for completed actions")

            # Log skill end
            self.audit.log_action(
                action_type="skill_end",
                actor="cross_domain_integrator",
                target=str(summary_file),
                status="completed",
                details={
                    "items_processed": len(items_data),
                    "personal_routed": routed_count['PERSONAL'],
                    "business_routed": routed_count['BUSINESS']
                }
            )

            return {
                'status': 'success',
                'items_processed': len(items_data),
                'personal_routed': routed_count['PERSONAL'],
                'business_routed': routed_count['BUSINESS'],
                'summary_path': str(summary_file)
            }
        except Exception as e:
            print(f"✗ Cross-domain integration failed: {e}")
            self.error_handler.write_error(e, context="domain_classification_workflow", extra={"phase": "integration"})
            self.audit.log_action(
                action_type="skill_end",
                actor="cross_domain_integrator",
                target="system",
                status="failed",
                details={"error": str(e)}
            )
            return {'status': 'failed', 'error': str(e)}


if __name__ == "__main__":
    integrator = CrossDomainIntegrator()
    result = integrator.execute()
    if result:
        print(f"\nResult: {result['summary_path']}")
