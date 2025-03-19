import os
import logging
from google.cloud import storage

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def download_images_from_gcs(bucket_name, source_folder, destination_folder):
    """
    Download images from a Google Cloud Storage (GCS) bucket to a local folder.

    Args:
        bucket_name (str): Name of the GCS bucket.
        source_folder (str): Folder path in the GCS bucket.
        destination_folder (str): Local folder where images should be saved.
    """
    logging.info(f"Connecting to GCS bucket: {bucket_name}")
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=source_folder)

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for blob in blobs:
        filename = os.path.join(destination_folder, os.path.basename(blob.name))
        blob.download_to_filename(filename)
        logging.info(f"Downloaded {blob.name} to {filename}")

def upload_file_to_gcs(bucket_name, source_file_path, destination_blob_name):
    """
    Upload a file to Google Cloud Storage (GCS).

    Args:
        bucket_name (str): Name of the GCS bucket.
        source_file_path (str): Path to the local file to be uploaded.
        destination_blob_name (str): Destination path in the GCS bucket.
    """
    logging.info(f"Uploading {source_file_path} to GCS bucket {bucket_name} as {destination_blob_name}")
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_path)
    logging.info(f"File {source_file_path} uploaded to {destination_blob_name} in bucket {bucket_name}")

def file_exists(file_path):
    """
    Check if a file exists.

    Args:
        file_path (str): Path to the file.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    return os.path.exists(file_path)

def folder_exists(folder_path):
    """
    Check if a folder exists.

    Args:
        folder_path (str): Path to the folder.

    Returns:
        bool: True if the folder exists, False otherwise.
    """
    return os.path.isdir(folder_path)