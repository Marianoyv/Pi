import os
from pathlib import Path
from google.cloud import storage

# Configuración
BUCKET_NAME = 'pidevelopment_static'
LOCAL_STATIC_DIR = Path('static')  # relativa a pi-1/
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(Path('credentials') / 'pidevelopment-d43bb26fcbc3.json')

# Inicializar cliente y bucket
client = storage.Client()
bucket = client.bucket(BUCKET_NAME)

# Subir cada archivo
for path in LOCAL_STATIC_DIR.rglob('*'):
    if path.is_file():
        blob_path = path.relative_to(LOCAL_STATIC_DIR).as_posix()
        blob = bucket.blob(blob_path)
        blob.upload_from_filename(str(path))
        print(f'✅ Subido: {blob_path}')
