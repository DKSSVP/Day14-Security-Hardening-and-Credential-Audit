# Day14 - Security Hardening & Credential Audit Report

## 1. Objective
Audit the Day1-Day13 project folders for hardcoded API credentials, verify environment-variable configuration, and check Git tracking and history for sensitive files.

## 2. Tools and Technologies
- Python
- python-dotenv
- Git and GitHub
- PowerShell-based pattern scanning
- Environment variables and .gitignore

## 3. Environment Variable Configuration
The following five variables were detected by the Day14 audit script:
- OPENROUTER_API_KEY
- SHEETDB_API_URL_1
- SHEETDB_API_URL_2
- FIREBASE_CREDENTIALS_PATH_1
- FIREBASE_CREDENTIALS_PATH_2

The actual configuration values are stored in .env. The .env.example file contains placeholders only.

## 4. Git Protection
- Added .env and sensitive credential-file patterns to .gitignore.
- Verified that Git ignores .env.
- Verified that .env.example is not ignored.
- The .env file was excluded from the Day14 commits.

## 5. Security Scan Results
- The Day14 audit script reported zero potential secret matches across the scanned Day1-Day13 folders.
- The preliminary Git-history pattern scan reported no matches for the selected patterns.
- The tracked-filename scan found no matching sensitive filenames in the repositories shown.
- The Git-history filename scan found no matching sensitive filenames.
- Gitleaks was not installed, so a Gitleaks scan was not completed.

## 6. Limitations
The scans used limited patterns and filename filters. These results do not prove that all secrets are absent from source code, other file types, remote repositories, or Git history. The environment-variable check confirms that values are loaded in the Day14 environment; it does not prove that every earlier project has been migrated to use them.

## 7. Conclusion
The preliminary checks reported no potential secret matches for the patterns tested. Environment-variable detection and .gitignore verification succeeded. A broader secret scan and further review are still required before certifying that all Day1-Day13 repositories are free of exposed credentials.
