#!/usr/bin/env python3
"""
Validated document builder. Runs validate_document.py, then generates the PDF
only if validation passes.

Usage: python3 build_doc.py <generator_script.py>
"""

import subprocess
import sys
import os

VALIDATOR = os.path.join(os.path.dirname(__file__), "validate_document.py")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 build_doc.py <generator_script.py>")
        sys.exit(1)

    script = sys.argv[1]

    # Resolve relative paths
    if not os.path.isabs(script):
        script = os.path.join(os.path.dirname(__file__), script)

    if not os.path.exists(script):
        print(f"Script not found: {script}")
        sys.exit(1)

    # Step 1: Validate (checks writing rules, metadata, page fill)
    print(f"Validating {os.path.basename(script)}...")
    result = subprocess.run(
        [sys.executable, VALIDATOR, script],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr if result.stderr else result.stdout)
        print("\nFix the issues above, then re-run.")
        sys.exit(1)

    # Step 2: Generate PDF
    print(f"Generating PDF...")
    result = subprocess.run(
        [sys.executable, script],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
