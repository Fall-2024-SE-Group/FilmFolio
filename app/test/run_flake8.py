"""
This module runs flake8 checks for code linting.
"""

import subprocess


def run_flake8():
    """
    This module runs flake8 checks for code linting.
    """
    try:
        result = subprocess.run(
            ["flake8", "."], check=True, text=True, capture_output=True
        )
        print("Flake8 passed with no issues.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Flake8 found issues:")
        print(e.stdout)
        print(e.stderr)


if __name__ == "__main__":
    run_flake8()
