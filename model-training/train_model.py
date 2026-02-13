import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import argparse
import os

def train_model(data_file, model_output_path):
    # Load data
    df = pd.read_csv(data_file)
    
    # Separate features and labels
    X = df.iloc[:, :-1].values
    y = df.iloc[:, -1].values
    
    # Encode labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    num_classes = len(label_encoder.classes_)
    
    # Save label mapping
    label_map = {i: label for i, label in enumerate(label_encoder.classes_)}
    print(f"Label Mapping: {label_map}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
    
    # Define model
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(num_classes, activation='softmax')
    ])
    
    # Compile model
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    
    # Train model
    model.fit(X_train, y_train, epochs=20, validation_data=(X_test, y_test))
    
    # Save model
    model.save(model_output_path)
    print(f"Model saved to {model_output_path}")

    # Also save the label encoder classes if needed for later use
    np.save(os.path.join(os.path.dirname(model_output_path), 'classes.npy'), label_encoder.classes_)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a model on landmarks data.")
    parser.add_argument("--data_file", type=str, default="landmarks_data.csv", help="Path to the landmarks CSV file")
    parser.add_argument("--model_output", type=str, default="sign_language_model.h5", help="Path to save the trained model")
    args = parser.parse_args()
    
    train_model(args.data_file, args.model_output)
