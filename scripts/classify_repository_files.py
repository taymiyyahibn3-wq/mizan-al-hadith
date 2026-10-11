import subprocess
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

def main():
    tracked = subprocess.check_output(['git', 'ls-files'], encoding='utf-8').splitlines()
    print(f"Total tracked files: {len(tracked)}")

    classification = {
        "PUBLIC": [],
        "INTERNAL": [],
        "REVIEW_REQUIRED": []
    }

    for p in tracked:
        # Core public documentation
        if p.startswith('docs/') and any(p.startswith(f'docs/{d}/') for d in ['overview', 'features', 'architecture', 'api', 'data', 'development', 'diagrams', 'github-publication', 'showcase', 'benchmarks']):
            classification["PUBLIC"].append(p)
        elif p in ['README.md', 'LICENSE', '.gitignore', '.env.example', 'docs/index.html', 'docs/index.md']:
            classification["PUBLIC"].append(p)
        # Web application frontend and backend source code
        elif p.startswith('mizan-web/'):
            classification["PUBLIC"].append(p)
        # Tests
        elif p.startswith('tests/'):
            classification["PUBLIC"].append(p)
        # Test scripts and verification tools that are essential
        elif p.startswith('scripts/') and any(t in p for t in ['test_', 'verify_', 'check_', 'run_']):
            classification["PUBLIC"].append(p)
        # Internal validation logs
        elif p.startswith('validation/'):
            classification["INTERNAL"].append(p)
        # Loose root sprint specs (01_FRONTEND_AUDIT.md through 18_FINAL_FRONTEND_CERTIFICATION.md, FRONTEND_AUDIT.md)
        elif any(p.startswith(f"{i:02d}_") for i in range(1, 19)) or p == 'FRONTEND_AUDIT.md':
            classification["INTERNAL"].append(p)
        # Loose internal sprint reports in docs/
        elif p.startswith('docs/') and any(x in p for x in ['embeddinggemma2_', 'phase6', 'phase7', 'ask-mizan/', 'ask-mizan-critical-fixes/', 'research-workspace/']):
            classification["INTERNAL"].append(p)
        # Presentation & Video READMEs
        elif p in ['presentation/README.md', 'video/README.md']:
            classification["REVIEW_REQUIRED"].append(p)
        # Other scripts
        elif p.startswith('scripts/'):
            classification["REVIEW_REQUIRED"].append(p)
        else:
            classification["REVIEW_REQUIRED"].append(p)

    print(f"\n--- CLASSIFICATION SUMMARY ---")
    print(f"PUBLIC: {len(classification['PUBLIC'])} files")
    print(f"INTERNAL: {len(classification['INTERNAL'])} files")
    print(f"REVIEW_REQUIRED: {len(classification['REVIEW_REQUIRED'])} files")

    print("\nSample INTERNAL files:")
    for f in classification["INTERNAL"][:15]:
        print("  [INTERNAL]", f)

    print("\nREVIEW_REQUIRED files:")
    for f in classification["REVIEW_REQUIRED"]:
        print("  [REVIEW_REQUIRED]", f)

if __name__ == '__main__':
    main()
