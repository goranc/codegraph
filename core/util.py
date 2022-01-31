from codecs import encode
from tarfile import open as tar_open
from os import remove, urandom
from typing import Optional
from requests import get


def download_and_unpack_tar(url: str) -> Optional[str]:
    filename = url.split("/")[-1]
    unique_id = encode(urandom(16), "hex").decode()

    try:
        with open(f"tmp/{filename}", "wb") as f:
            for chunk in get(url, stream=True).iter_content(1024**2):
                f.write(chunk)

        mode = "r:gz" if filename.endswith("tar.gz") else "r:"
        tar = tar_open(f"tmp/{filename}", mode)
        tar.extractall(f"tmp/{unique_id}")
        tar.close()
        return unique_id
    finally:
        remove(f"tmp/{filename}")
