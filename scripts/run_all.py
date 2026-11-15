
"""Run the IS 477 data processing workflow."""

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

SCRIPTS = [
    "assess_data_quality.py",
    "clean_data.py",
    "integrate_data.py",
    "assess_post_integration.py",
]

def main():
    print("Starting IS 477 data processing workflow...", flush=True)

    for script in SCRIPTS:
        path = ROOT / "scripts" / script

        if not path.exists():
            raise FileNotFoundError(f"Missing script: {path}")

        print(f"\nRunning {script}...", flush=True)

        subprocess.run(
            [sys.executable, str(path)],
            cwd=ROOT,
            check=True,
        )

        print(f"Completed {script}", flush=True)

    print("\nAll processing steps completed successfully!")

if __name__ == "__main__":
    main()
