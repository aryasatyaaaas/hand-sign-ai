import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import argparse
import pickle
import os

def train_model(data_file, model_output_path):
    # Load data
    try:
        df = pd.read_csv(data_file)
    except FileNotFoundError:
        print(f"Error: {data_file} not found.")
        return

    # Check data shape
    print(f"Data shape: {df.shape}")
    
    # Separate features and labels
    X = df.iloc[:, :-1].values
    y = df.iloc[:, -1].values
    
    # Encode labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    classes = label_encoder.classes_
    
    print(f"Classes: {classes}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
    
    # Define model - Random Forest is robust and lightweight
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    # Train model
    print("Training Random Forest model...")
    model.fit(X_train, y_train)
    
    # Evaluate
    accuracy = model.score(X_test, y_test)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    
    # Save model and label encoder
    with open(model_output_path, 'wb') as f:
        pickle.dump({'model': model, 'label_encoder': label_encoder}, f)
    
    print(f"Model saved to {model_output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a model on landmarks data using Scikit-Learn.")
    parser.add_argument("--data_file", type=str, default="landmarks_data.csv", help="Path to the landmarks CSV file")
    parser.add_argument("--model_output", type=str, default="sign_language_model_sklearn.pkl", help="Path to save the trained model")
    args = parser.parse_args()
    
    train_model(args.data_file, args.model_output)
