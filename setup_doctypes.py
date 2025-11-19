"""
Temporary script to create directory structure for Production List DocTypes
Run this script once to create the necessary directories
"""
import os

base_path = r"d:\C4erp-APP\c4factory2\c4factory\c4_manufacturing\doctype"

directories = [
    base_path,
    os.path.join(base_path, "production_list"),
    os.path.join(base_path, "production_list_item"),
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f"Created: {directory}")

print("\nDirectory structure created successfully!")
print("You can now delete this setup_doctypes.py file")
