import os
import sys
from google.cloud import storage
from src.data_preprocessing import preprocess_data
from src.train import train_model
from src.evaluation import Evaluation
import pandas as pd

# Print sys.path to debug module import issues
print("Current sys.path:", sys.path)
sys.path.append(os.path.abspath(os.path.dirname(_file_)))
print("Updated sys.path:", sys.path)

def download_from_gcs(gcs_path, local_path):
    """Downloads a single file from GCS to the local filesystem."""
    client = storage.Client()
    bucket_name, blob_path = gcs_path.replace("gs://", "").split("/", 1)
    
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_path)
    
    os.makedirs(os.path.dirname(local_path), exist_ok=True)  # Ensure the directory exists
    blob.download_to_filename(local_path)
    print(f"Downloaded {gcs_path} to {local_path}")

def download_folder_from_gcs(gcs_folder_path, local_folder_path):
    """Downloads all files from a GCS folder to a local directory."""
    client = storage.Client()
    bucket_name, folder_path = gcs_folder_path.replace("gs://", "").split("/", 1)
    
    bucket = client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=folder_path)  # Get all files in the folder
    
    os.makedirs(local_folder_path, exist_ok=True)  # Ensure local folder exists
    
    for blob in blobs:
        filename = os.path.basename(blob.name)  # Extract filename
        local_file_path = os.path.join(local_folder_path, filename)
        
        if not filename:  # Skip empty folder names
            continue
        
        blob.download_to_filename(local_file_path)
        print(f"Downloaded {blob.name} to {local_file_path}")

def main():
    """Main pipeline: Downloads data, preprocesses it, trains the model, and evaluates it."""
    print("Starting data preprocessing...")
    
    # 1️ Download CSV file from GCS
    gcs_csv_path = "gs://automl-image-bucket/import_file.csv"
    processed_data_path = "data/processed"
    os.makedirs(processed_data_path, exist_ok=True)
    
    local_csv_path = os.path.join(processed_data_path, 'import_file.csv')
    download_from_gcs(gcs_csv_path, local_csv_path)
    
    # 2️ Preprocess CSV data
    preprocess_data(local_csv_path, processed_data_path)
    print("Data preprocessing completed.")
    
    # 3️ Download images from GCS
    print("Downloading images from GCS...")
    gcs_image_folder = "gs://automl-image-bucket/dogs-vs-cats"
    local_image_folder = "data/images"
    download_folder_from_gcs(gcs_image_folder, local_image_folder)
    
    print("Images downloaded successfully.")
    
    # 4️ Train the model
    print("Starting model training...")
    train_csv_path = os.path.join(processed_data_path, 'train.csv')
    model = train_model(train_csv_path, local_image_folder)
    print("Model training completed.")
    
    # 5️ Evaluate the model
    print("Evaluating the model...")
    evaluation = Evaluation(model, processed_data_path)
    evaluation.evaluate_model()
    print("Model evaluation completed.")

if __name__ == "__main__":
    main()