#!/bin/bash

# CFSS Security Check Script
# This script verifies that no customer data will be included in builds

echo "🔒 CFSS Security Check - Scanning for Customer Data..."
echo "=================================================="

# Check for CSV files in data directory
csv_files=$(find data -name "*.csv" 2>/dev/null || true)
if [ -n "$csv_files" ]; then
    echo "⚠️  WARNING: CSV files found in data directory:"
    echo "$csv_files"
    echo ""
    echo "These files contain customer data and should NOT be included in builds!"
    echo "Run the build script which will automatically clean them, or remove manually."
    exit 1
else
    echo "✅ No CSV files found in data directory"
fi

# Check for database files
db_files=$(find . -name "*.db" -not -path "./build/*" -not -path "./dist/*" 2>/dev/null || true)
if [ -n "$db_files" ]; then
    echo "⚠️  WARNING: Database files found:"
    echo "$db_files"
    echo ""
    echo "These may contain customer scan data!"
    echo "Consider backing up and removing before building for distribution."
fi

# Check for log files
log_files=$(find . -name "*.log" -not -path "./build/*" -not -path "./dist/*" 2>/dev/null || true)
if [ -n "$log_files" ]; then
    echo "⚠️  WARNING: Log files found:"
    echo "$log_files"
    echo ""
    echo "These may contain customer information in logs!"
fi

# Check for scan backups
backup_dirs=$(find . -name "scan_backups" -o -name "data_backup*" -not -path "./build/*" -not -path "./dist/*" 2>/dev/null || true)
if [ -n "$backup_dirs" ]; then
    echo "⚠️  WARNING: Scan backup directories found:"
    echo "$backup_dirs"
    echo ""
    echo "These contain customer scan progress data!"
fi

# Check for export directories
export_dirs=$(find . -name "sharepoint_export" -o -name "issue_reports" -not -path "./build/*" -not -path "./dist/*" 2>/dev/null || true)
if [ -n "$export_dirs" ]; then
    echo "⚠️  WARNING: Export directories found:"
    echo "$export_dirs"
    echo ""
    echo "These may contain customer data exports!"
fi

# Check for specific sensitive files
sensitive_files=(
    "sharepoint_config.json"
    "csv_hash_cache.json"
    "CFSS_ScanData_*.json"
    "CFSS_Summary_*.txt"
    "cfss_issue_report_*.txt"
)

for pattern in "${sensitive_files[@]}"; do
    files=$(find . -name "$pattern" -not -path "./build/*" -not -path "./dist/*" 2>/dev/null || true)
    if [ -n "$files" ]; then
        echo "⚠️  WARNING: Sensitive files found matching $pattern:"
        echo "$files"
        echo ""
    fi
done

echo ""
echo "🔒 Security check complete."
echo ""
echo "💡 To clean customer data before building:"
echo "   • Run ./build_macos.sh (automatically cleans data)"
echo "   • Or manually: rm -f data/*.csv"
echo "   • Consider backing up: cp -r data data_backup_\$(date +%Y%m%d)"
echo ""
echo "🚨 NEVER commit customer CSV files, databases, or scan data to git!"
