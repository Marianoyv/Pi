from storages.backends.gcloud import GoogleCloudStorage
from django.conf import settings


class StaticRootGoogleCloudStorage(GoogleCloudStorage):
    """
    Ubica los archivos estáticos en gs://<bucket>/static/.
    """

    bucket_name = settings.GS_BUCKET_NAME
    location = "static"
    default_acl = None


class MediaRootGoogleCloudStorage(GoogleCloudStorage):
    """
    Ubica los archivos de media en gs://<bucket>/media/.
    """

    bucket_name = settings.GS_BUCKET_NAME
    location = "media"
    default_acl = None
