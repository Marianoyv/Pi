from google.cloud import storage
import os

# Ruta al archivo de credenciales
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join('credentials', 'pidevelopment-d43bb26fcbc3.json')

# Nombre del bucket
bucket_name = 'pidevelopment_static'

# Inicializar cliente de Google Cloud
client = storage.Client()
bucket = client.bucket(bucket_name)

# Crear blob (archivo) y subir contenido
blob = bucket.blob('test_upload_from_script.txt')
blob.upload_from_string('Archivo de prueba subido manualmente con Google Cloud Storage')

print(f'✅ Archivo subido correctamente a gs://{bucket_name}/test_upload_from_script.txt')
