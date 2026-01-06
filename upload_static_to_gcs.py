import mimetypes
import os
from pathlib import Path

from dotenv import load_dotenv
from google.cloud import storage

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
BUCKET_PREFIX = "static"


def resolve_credentials():
    cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not cred_path:
        return None
    path_obj = Path(cred_path)
    if not path_obj.is_absolute():
        path_obj = BASE_DIR / path_obj
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(path_obj)
    return path_obj


def upload_static():
    load_dotenv(BASE_DIR / ".env")
    resolve_credentials()

    bucket_name = os.getenv("GS_BUCKET_NAME")
    if not bucket_name:
        raise SystemExit("Falta la variable GS_BUCKET_NAME en el entorno o en .env")

    if not STATIC_DIR.exists():
        raise SystemExit("No se encontró la carpeta static/ para subir a GCS")

    client = storage.Client()
    bucket = client.bucket(bucket_name)

    uploaded = 0
    for path in STATIC_DIR.rglob("*"):
        if not path.is_file():
            continue

        blob_name = f"{BUCKET_PREFIX}/{path.relative_to(STATIC_DIR).as_posix()}"
        blob = bucket.blob(blob_name)

        content_type, _ = mimetypes.guess_type(path.name)
        if content_type:
            blob.content_type = content_type

        blob.cache_control = "public, max-age=31536000"
        blob.upload_from_filename(path)
        uploaded += 1
        print(f"Subido: gs://{bucket_name}/{blob_name}")

    print(f"Listo: {uploaded} archivos subidos a gs://{bucket_name}/{BUCKET_PREFIX}/")


if __name__ == "__main__":
    upload_static()
