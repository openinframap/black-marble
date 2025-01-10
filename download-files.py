import httpx
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

token = os.getenv("BLACKMARBLE_TOKEN")

endpoint = "https://ladsweb.modaps.eosdis.nasa.gov"

url = f"{endpoint}/api/v1/files?product=VNP46A4&collection=5000&dateRanges=2023-01-01..2023-01-01"

response = httpx.get(url)

path = Path("./data")

for row in response.json().values():
    # download file
    file_url = endpoint + row["fileURL"]
    file_path: Path = path / row["name"]
    if file_path.exists():
        print("File already exists", file_path)
        continue
    print("Downloading", file_url)
    try:
        with httpx.stream(
            "GET",
            file_url,
            headers={"Authorization": f"Bearer {token}"},
        ) as response:
            with open(path / row["name"], "wb") as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)
    except Exception as e:
        file_path.unlink(missing_ok=True)
        print("Error downloading", file_url, e)
