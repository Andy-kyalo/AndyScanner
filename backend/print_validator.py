"""
print_validator.py

Displays project validation results.

Author: Andrew Kyalo
Project: Andy Scanner
"""


def print_project_validation(result: dict) -> None:
    """
    Display project structure validation results.

    Parameters
    ----------
    result : dict
        Validation result returned by ProjectValidator.
    """

    print("\n========== PROJECT VALIDATION ==========")

    if result["valid"]:

        print("Status             : VALID")
        print("Project Structure  : COMPLETE")

    else:

        print("Status             : INVALID")
        print("Project Structure  : INCOMPLETE")
        print()

        print("Missing Resources:")

        for item in result["missing"]:
            print(f"  • {item}")

    print("========================================")