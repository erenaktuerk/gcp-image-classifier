import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class Evaluation:
    def __init__(self, model, data_path):
        """
        Initialize the Evaluation class.
        
        :param model: The trained model to be evaluated
        :param data_path: Path to the dataset (train/test directories)
        """
        self.model = model
        self.data_path = data_path

    def evaluate_model(self):
        """
        Evaluates the model on the test data and prints the results.
        """
        # Load the test dataset
        test_data = tf.keras.preprocessing.image_dataset_from_directory(
            self.data_path + "/test",  # Path to the test folder
            image_size=(224, 224),  # Resize images
            batch_size=32,
            label_mode='int'
        )
        
        # Evaluate the model on the test data
        print("Evaluating model on test data...")
        loss, accuracy = self.model.evaluate(test_data)
        print(f"Test Loss: {loss}")
        print(f"Test Accuracy: {accuracy}")

        # Make predictions on the test data
        print("Making predictions on test data...")
        y_true = []
        y_pred = []

        for images, labels in test_data:
            y_true.extend(labels.numpy())
            predictions = self.model.predict(images)
            y_pred.extend(np.argmax(predictions, axis=1))  # Assuming binary classification (cat, dog)
        
        # Generate and print confusion matrix
        self.plot_confusion_matrix(y_true, y_pred)

        # Classification report
        print("Classification Report:")
        print(classification_report(y_true, y_pred, target_names=["cat", "dog"]))

    def plot_confusion_matrix(self, y_true, y_pred):
        """
        Generates and plots a confusion matrix.
        
        :param y_true: True labels
        :param y_pred: Predicted labels
        """
        cm = confusion_matrix(y_true, y_pred)

        plt.figure(figsize=(6, 5))
        sns.heatmap(cm, annot=True, fmt='g', cmap="Blues", xticklabels=["cat", "dog"], yticklabels=["cat", "dog"])
        plt.title("Confusion Matrix")
        plt.xlabel('Predicted Labels')
        plt.ylabel('True Labels')
        plt.show()