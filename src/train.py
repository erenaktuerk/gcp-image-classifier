import tensorflow as tf
from src.model import build_model
from src.data_preprocessing import load_data
from tensorflow.keras.preprocessing import image
from src.utils import download_images_from_gcs
import numpy as np
import os
from google.cloud import storage

# Define GCS bucket details
BUCKET_NAME = "automl-image-bucket"
IMAGE_GCS_FOLDER = "dogs-vs-cats/"
LOCAL_IMAGE_FOLDER = "data/images/"
CSV_GCS_PATH = "import_file.csv"
LOCAL_CSV_PATH = "data/import_file.csv"

def download_csv_from_gcs(bucket_name, gcs_path, local_path):
    """Downloads a CSV file from GCS to a local directory."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(gcs_path)
    blob.download_to_filename(local_path)
    print(f"Downloaded {gcs_path} to {local_path}")

def train_model(csv_path, image_directory):
    """Trains the model using the preprocessed data."""
    
    # Load the data from the CSV file
    data = load_data(csv_path)
    
    # Create training data by selecting images with the label 'cat' (example)
    train_data = data[data['label'] == 'cat']  # Modify this to select other categories as needed
    
    # Load images and resize them to (224, 224)
    train_images = [image.load_img(os.path.join(image_directory, img), target_size=(224, 224)) for img in train_data['image_path']]
    
    # Convert images to arrays
    train_images = np.array([image.img_to_array(img) for img in train_images])
    
    # Convert labels to numerical format (0 for 'cat', 1 for 'dog')
    train_labels = np.array([0 if label == 'cat' else 1 for label in train_data['label']])
    
    # Normalize pixel values to [0,1]
    train_images = train_images / 255.0

    # Define and compile the model
    model = build_model()
    
    # Train the model on the prepared images and labels
    model.fit(train_images, train_labels, epochs=5, batch_size=32, validation_split=0.2)

    return model  # Return the trained model

if __name__ == "__main__":
    # Step 1: Download CSV file from GCS
    download_csv_from_gcs(BUCKET_NAME, CSV_GCS_PATH, LOCAL_CSV_PATH)

    # Step 2: Download images from GCS
    download_images_from_gcs(BUCKET_NAME, IMAGE_GCS_FOLDER, LOCAL_IMAGE_FOLDER)

    # Step 3: Start training
    train_model(LOCAL_CSV_PATH, LOCAL_IMAGE_FOLDER)