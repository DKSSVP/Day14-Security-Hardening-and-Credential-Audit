
import os
import re
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from the Day14 .env file
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Required variables for your projects
REQUIRED_KEYS = [
    "OPENROUTER_API_KEY",
    "SHEETDB_API_URL_1",
    "SHEETDB_API_URL_2",
    "FIREBASE_CREDENTIALS_PATH_1",
    "FIREBASE_CREDENTIALS_PATH_2",
]

# Patterns for common hardcoded API keys
SECRET_PATTERNS = {
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "Google API key": re.compile(r"\bAIzaSy[A-Za-z0-9_-]{30,}\b"),
    "Generic secret assignment": re.compile(
        r"""(?i)\b(api_key|api_token|access_token|client_secret|password)\s*=\s*["'][^"']{8,}["']"""
    ),
}

# Directories that should not be scanned
EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
}


def check_environment():
    """Check required variables without displaying their values."""
    print("\n=== Environment Variable Check ===")
    missing = []

    for key in REQUIRED_KEYS:
        if os.getenv(key):
            print(f"[SET] {key}")
        else:
            print(f"[MISSING] {key}")
            missing.append(key)

    return missing


def scan_file(file_path):
    """Find possible hardcoded secrets without printing their values."""
    try:
        content = file_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )
    except OSError:
        return 0

    findings = 0

    for line_number, line in enumerate(content.splitlines(), start=1):
        for secret_type, pattern in SECRET_PATTERNS.items():
            if pattern.search(line):
                print(
                    f"[REVIEW] {secret_type}: "
                    f"{file_path}:{line_number}"
                )
                findings += 1
                break

    return findings


def scan_project(project_dir):
    """Scan source and configuration files in a project."""
    total_findings = 0
    allowed_extensions = {
        ".py", ".json", ".js", ".ts", ".yaml", ".yml",
        ".ini", ".cfg", ".toml", ".txt", ".md"
    }

    for current_dir, dirs, files in os.walk(project_dir):
        dirs[:] = [
            directory for directory in dirs
            if directory not in EXCLUDED_DIRS
        ]

        for filename in files:
            file_path = Path(current_dir) / filename

            # Never read actual environment or private credential files
            if filename == ".env" or filename.endswith(".pem"):
                continue

            if filename.lower() in {
                "firebase-service-account.json",
                "serviceaccountkey.json",
            }:
                continue

            if file_path.suffix.lower() in allowed_extensions:
                total_findings += scan_file(file_path)

    return total_findings


def main():
    print("Day14 Security Audit")
    print("====================")

    missing_keys = check_environment()

    # The parent folder contains the Day1-Day13 project directories
    projects_root = BASE_DIR.parent
    total_findings = 0

    print("\n=== Scanning Day1-Day13 Projects ===")

    for project_dir in sorted(projects_root.iterdir()):
        if not project_dir.is_dir():
            continue

        if not re.match(r"Day(?:[1-9]|1[0-3])(?:_|-|$)", project_dir.name):
            continue

        print(f"\nScanning: {project_dir.name}")
        findings = scan_project(project_dir)
        total_findings += findings
        print(f"Possible findings: {findings}")

    print("\n=== Audit Summary ===")
    print(f"Missing environment variables: {len(missing_keys)}")
    print(f"Potential secret matches: {total_findings}")
    print("Review each match manually; pattern matches are not proof of a leak.")


if __name__ == "__main__":
    main()