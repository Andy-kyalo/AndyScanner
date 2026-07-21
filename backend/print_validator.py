"""
print_validator.py

Displays project validation results.
"""

def print_project_validation(result):

    print("\n========== PROJECT VALIDATION ==========")

    if result["valid"]:
        print("Project Structure : VALID")
    else:
        print("Project Structure : INVALID")
        print("\nMissing:")

        for item in result["missing"]:
            print(f" - {item}")

    print("========================================")