
from pathlib import Path
from urllib.request import urlopen
import hashlib

ROOT = Path(__file__).resolve().parents[1]
DOWNLOAD_DIR = ROOT / "data" / "downloads"

OWID_URL = (
    "https://raw.githubusercontent.com/owid/co2-data/"
    "master/owid-co2-data.csv"
)


def download_owid():
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    destination = DOWNLOAD_DIR / "owid-co2-data.csv"

    print("Downloading OWID CO2 dataset...")

    with urlopen(OWID_URL, timeout=120) as response:
        with destination.open("wb") as output:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                output.write(chunk)

    sha256 = hashlib.sha256(destination.read_bytes()).hexdigest()

    print(f"Saved to: {destination}")
    print(f"SHA-256: {sha256}")
    print("Original raw data has not been modified.")


if __name__ == "__main__":
    download_owid()
