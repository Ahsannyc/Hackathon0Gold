---
type: task
from: accounting@vendor-services.com
subject: Invoice INV-2026-0847 - Q1 Services ($3,500)
priority: high
source: email
received: 2026-03-29T09:30:00
keywords: invoice, payment, financial, amount, due
---

# Invoice for Q1 2026 Services

Dear Valued Customer,

Please find below the details for Invoice INV-2026-0847 for services rendered in Q1 2026.

## Invoice Details

**Invoice Number:** INV-2026-0847
**Invoice Date:** 2026-03-28
**Due Date:** 2026-04-28 (Net 30)
**Total Amount Due:** $3,500.00

## Services Rendered

### Consulting Services
- Project scoping and requirements analysis: 10 hours @ $200/hr = $2,000.00
- Implementation planning and architecture review: 5 hours @ $200/hr = $1,000.00

### Training & Support
- Team training sessions: 4 hours @ $75/hr = $300.00
- Post-implementation support: 2 hours @ $100/hr = $200.00

## Summary
| Item | Quantity | Rate | Amount |
|------|----------|------|--------|
| Consulting Hours | 15 | $200 | $3,000.00 |
| Training Hours | 4 | $75 | $300.00 |
| Support Hours | 2 | $100 | $200.00 |
| **TOTAL** | | | **$3,500.00** |

## Payment Instructions

**Payment Methods Accepted:**
- Wire Transfer
- ACH Transfer
- Credit Card (2.5% processing fee applies)
- Check (mail to address below)

**Wire Transfer Details:**
- Bank Name: First National Bank
- Account Name: Vendor Services Inc
- Account Number: 1234567890
- Routing Number: 987654321
- SWIFT Code: FNBAUS33

**Mailing Address:**
Vendor Services Inc
Accounting Department
123 Business Ave
New York, NY 10001

## Terms & Conditions

Payment is due within 30 days of invoice date. Late payments may be subject to 1.5% monthly interest charges.

If you have any questions regarding this invoice or the services provided, please don't hesitate to contact us.

---

Sincerely,

**Finance Team**
Vendor Services Inc
accounting@vendor-services.com
(555) 987-6543

---

## Multi-Step Workflow Expected

This task should trigger:

1. **Classify**: Detect invoice/payment keywords → PERSONAL domain (HITL required)
2. **Extract**: Parse invoice details (amount, due date, payment methods)
3. **Draft**: Create approval request with payment details
4. **HITL**: Move to /Pending_Approval for human review and approval
5. **Approve**: Human approves payment and selects payment method
6. **Execute**: Payment processed via selected method (MCP)
7. **Log**: Complete audit trail with payment confirmation
8. **Complete**: Move files to /Done with full workflow history
