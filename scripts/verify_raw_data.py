
"""Verify raw dataset integrity using SHA-256 checksums."""

from pathlib import Path
import hashlib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw"
CHECKSUMS = (
    ROOT / "results/pre_integration_quality/observed_sha256.csv"
)

def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def main():
    if not CHECKSUMS.exists():
        raise FileNotFoundError(
            f"Expected checksum file not found: {CHECKSUMS}"
        )

    expected = pd.read_csv(CHECKSUMS)
    print("Checksum file columns:", list(expected.columns))
    print(expected.head().to_string(index=False))

    # Inspect the checksum file's structure before implementing
    # the final verification logic.
    print(
        "\nNext: map the filename and SHA-256 columns "
        "to implement checksum comparisons."
    )

if __name__ == "__main__":
    main()
