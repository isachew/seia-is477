
"""Verify the integrity of raw datasets using SHA-256."""

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
    expected = pd.read_csv(CHECKSUMS)

    required = {"source", "file", "sha256_observed"}
    if not required.issubset(expected.columns):
        raise ValueError("Checksum file has missing columns.")

    if expected.empty:
        raise ValueError("Checksum file contains no records.")

    if expected["file"].duplicated().any():
        raise ValueError("Duplicate filenames in checksum manifest.")

    # Ensure the manifest covers every raw file.
    raw_files = {
        p.name for p in RAW.iterdir()
        if p.is_file() and not p.name.startswith(".")
    }
    manifest_files = set(expected["file"])

    unlisted = raw_files - manifest_files
    if unlisted:
        raise ValueError(
            f"Raw files missing from checksum manifest: {sorted(unlisted)}"
        )

    results = []

    for _, row in expected.iterrows():
        filename = str(row["file"])
        expected_hash = str(row["sha256_observed"]).lower()

        # Prevent paths outside the raw data folder.
        if Path(filename).name != filename:
            raise ValueError(f"Invalid filename: {filename}")

        path = RAW / filename

        if not path.exists():
            status = "MISSING"
            actual_hash = ""
        else:
            actual_hash = sha256_file(path)
            status = (
                "PASS" if actual_hash == expected_hash
                else "FAIL"
            )

        results.append({
            "source": row["source"],
            "file": filename,
            "expected_sha256": expected_hash,
            "actual_sha256": actual_hash,
            "status": status
        })

    output = ROOT / "results/integrity"
    output.mkdir(parents=True, exist_ok=True)

    report = pd.DataFrame(results)
    report.to_csv(
        output / "verification_results.csv",
        index=False
    )

    print(report[["file", "status"]].to_string(index=False))

    if not (report["status"] == "PASS").all():
        raise RuntimeError(
            "Integrity verification failed. Review the results."
        )

    print("\nAll raw datasets passed SHA-256 verification!")

if __name__ == "__main__":
    main()
