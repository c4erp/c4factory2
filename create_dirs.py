import os
import sys

# Create directories
base = r"d:\C4erp-APP\c4factory2\c4factory"
dirs = [
    os.path.join(base, "c4_manufacturing", "doctype"),
    os.path.join(base, "c4_manufacturing", "doctype", "production_list"),
    os.path.join(base, "c4_manufacturing", "doctype", "production_list_item"),
]

for d in dirs:
    os.makedirs(d, exist_ok=True)
    print(f"Created: {d}")

print("\nDirectories created! Now run: python generate_all_files.py")
