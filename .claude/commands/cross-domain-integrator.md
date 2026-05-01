# @cross

Invoke the Cross Domain Integrator skill - classify and route messages from personal and business domains.

**What it does:**
- Scans `/Needs_Action/` for all incoming messages
- Classifies as PERSONAL (email/WhatsApp) or BUSINESS (LinkedIn/Twitter/Facebook)
- Routes PERSONAL → `/Pending_Approval/` (needs HITL approval)
- Routes BUSINESS → `/Approved/` (ready for Auto LinkedIn Poster)
- Creates unified summary in `/Logs/cross_domain_[date].md`

**Usage:**
```
@cross - Run the integrator once
```

**Example:**
```
@cross process Needs_Action
```

**Output:**
- Classified items routed to appropriate folders
- Summary report: `/Logs/cross_domain_[date].md`
- Console output showing results

**Note:** The skill runs automatically every 30 minutes via PM2 scheduler. Use this command for manual triggering.
