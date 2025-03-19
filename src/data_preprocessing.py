import pandas as pd
import os
from sklearn.model_selection import train_test_split

def load_data(csv_path):
    """Load the CSV data with image paths and labels."""
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"The file does not exist: {csv_path}")
    
    df = pd.read_csv(csv_path, names=['image_path', 'label'])
    return df

def preprocess_data(csv_path, image_directory):
    """Preprocess the data by splitting it into training and validation sets."""
    df = load_data(csv_path)
    
    # Split data into training and validation sets (80-20)
    train_df, val_df = train_test_split(df, test_size=0.2, random_state=42)
    
    # Optional: You can save these splits into new CSV files
    train_df.to_csv(os.path.join(image_directory, 'train.csv'), index=False)
    val_df.to_csv(os.path.join(image_directory, 'val.csv'), index=False)
    
    return train_df, val_df