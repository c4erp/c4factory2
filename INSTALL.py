"""
MASTER INSTALLER - Run this ONE command to create everything!
This will create ALL files needed for Production List module
"""

import subprocess
import sys

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║           PRODUCTION LIST MODULE - COMPLETE INSTALLATION                     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

# Run the file creation scripts
scripts = [
    "create_all_files.py",
    "create_python_files.py"
]

for script in scripts:
    print(f"\nRunning {script}...")
    print("="*80)
    result = subprocess.run([sys.executable, script], capture_output=False)
    if result.returncode != 0:
        print(f"ERROR: {script} failed!")
        sys.exit(1)

print("""
\n╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                        ✅ ALL FILES CREATED!                                 ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

📁 Files Created:
   ✓ Production List DocType (JSON + Python)
   ✓ Production List Item DocType (JSON + Python)
   ✓ production_list.js (UI buttons)
   ✓ production_list_stock.py (API methods)
   ✓ production_list_hooks.py (Event handlers)
   ✓ Custom field patch for Stock Entry

🚀 NEXT STEPS:

1. Navigate to your Frappe bench directory:
   cd /path/to/frappe-bench

2. Run database migration:
   bench --site your-site-name migrate

3. Clear cache:
   bench --site your-site-name clear-cache

4. Restart bench:
   bench restart

5. Login to ERPNext and test:
   - Go to Manufacturing → Production List
   - Create a Work Order
   - Create Production List from WO
   - Create Stock Entry from PL

✅ The "Create Stock Entry" button will now appear on Production List forms!

═══════════════════════════════════════════════════════════════════════════════
""")
