
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


import zipfile
from io import BytesIO

WORLD_BANK_INDICATORS = {
    "gdp_per_capita.csv": "NY.GDP.PCAP.CD",
    "urban_population.csv": "SP.URB.TOTL.IN.ZS",
    "industry_including_construction.csv": "NV.IND.TOTL.ZS",
    "renewable_energy_consumption.csv": "EG.FEC.RNEW.ZS",
}

def download_world_bank():
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

    for filename, indicator in WORLD_BANK_INDICATORS.items():
        url = (
            "https://api.worldbank.org/v2/country/all/"
            f"indicator/{indicator}?downloadformat=csv"
        )

        print(f"Downloading World Bank indicator {indicator}...")

        with urlopen(url, timeout=120) as response:
            archive_bytes = response.read()

        with zipfile.ZipFile(BytesIO(archive_bytes)) as archive:
            csv_files = [
                name for name in archive.namelist()
                if name.startswith("API_") and name.endswith(".csv")
            ]

            if len(csv_files) != 1:
                raise ValueError(
                    f"Expected one indicator CSV for {indicator}, "
                    f"found {len(csv_files)}"
                )

            destination = DOWNLOAD_DIR / filename

            with archive.open(csv_files[0]) as source:
                with destination.open("wb") as output:
                    while True:
                        chunk = source.read(1024 * 1024)
                        if not chunk:
                            break
                        output.write(chunk)

        sha256 = hashlib.sha256(destination.read_bytes()).hexdigest()

        print(f"Saved to: {destination}")
        print(f"SHA-256: {sha256}")

if __name__ == "__main__":
    download_owid()
    download_world_bank()
