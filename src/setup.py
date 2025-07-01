import argparse
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.utils import load, save


def setup_project(force: bool):
    # Create sample .env
    if not os.path.exists(".env"):
        print("Creating sample .env file...")
        save(".env", load(".env.example"))
        print("Successfully created .env file...")

    print("Done!")


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="Setup project")

    parser.add_argument(
        "-f",
        "--force",
        default=False,
        action=argparse.BooleanOptionalAction,
        help="rewrite existing data if already exists (default: False)",
    )

    parser.add_argument(
        "-s",
        "--skip-scrap",
        default=False,
        action=argparse.BooleanOptionalAction,
        dest="skip_scrap",
        help="should skip scrapping phase (default: False)",
    )

    namespace = parser.parse_args()

    setup_project(namespace.force)
