#!/bin/bash
# Cross Domain Integrator - Easy Manual Trigger
# This script runs the Cross Domain Integrator from anywhere
# Usage: bash run-cross-domain.sh  OR  ./run-cross-domain.sh

set -e

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo ""
echo "======================================================================"
echo "CROSS DOMAIN INTEGRATOR - Manual Trigger"
echo "======================================================================"
echo ""
echo "Timestamp: $(date)"
echo "Location: $(pwd)"
echo ""
echo "[RUNNING] Cross Domain Integrator..."
echo ""

# Run the integrator
python skills/cross_domain_integrator.py
EXIT_CODE=$?

echo ""
echo "======================================================================"
if [ $EXIT_CODE -eq 0 ]; then
    echo "[SUCCESS] Integration completed successfully!"
else
    echo "[ERROR] Process exited with code $EXIT_CODE"
fi
echo "======================================================================"
echo ""
echo "Next: Check /Pending_Approval/ and /Approved/ folders"
echo "Summary: Logs/cross_domain_*.md"
echo ""
