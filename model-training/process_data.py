import os
import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import argparse

# Standard mediapipe import
import mediapipe as mp
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def extract_landmarks(image_path):
    with mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5) as hands:
        image = cv2.imread(image_path)
        if image is None:
            return None
        
        # Convert the BGR image to RGB before processing.
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        if not results.multi_hand_landmarks:
            return None
            
        # Extract landmarks for the first hand detected
        hand_landmarks = results.multi_hand_landmarks[0]
        landmarks = []
        for landmark in hand_landmarks.landmark:
            landmarks.extend([landmark.x, landmark.y, landmark.z])
            
        return landmarks

def process_dataset(data_dir, output_file, limit=None):
    data = []
    
    if not os.path.exists(data_dir):
        print(f"Error: Directory {data_dir} does not exist.")
        return

    # Iterate through each folder (class) in the dataset directory
    classes = sorted(os.listdir(data_dir)) # Sort for consistency
    print(f"Found classes: {classes}")
    
    for label in classes:
        class_dir = os.path.join(data_dir, label)
        if os.path.isdir(class_dir):
            print(f"Processing class: {label}")
            count = 0
            for image_name in os.listdir(class_dir):
                if limit and count >= limit:
                    break
                    
                image_path = os.path.join(class_dir, image_name)
                # Filter for image files
                if image_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                    try:
                        landmarks = extract_landmarks(image_path)
                        if landmarks:
                            data.append(landmarks + [label])
                            count += 1
                    except Exception as e:
                        print(f"Error processing {image_path}: {e}")
            print(f"  Processed {count} images for class {label}")
    
    # Create DataFrame and save to CSV
    if not data:
        print("No data extracted. Check your dataset path and images.")
        return

    # 21 landmarks * 3 coordinates = 63 columns
    columns = [f'{c}_{i}' for i in range(21) for c in ['x', 'y', 'z']] + ['label']
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(output_file, index=False)
    print(f"Data processing complete. Saved to {output_file}")
    print(f"Total samples: {len(df)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process image dataset to extract hand landmarks.")
    parser.add_argument("--data_dir", type=str, required=True, help="Path to the dataset directory")
    parser.add_argument("--output_file", type=str, default="landmarks.csv", help="Output CSV file path")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of images per class")
    args = parser.parse_args()
    
    process_dataset(args.data_dir, args.output_file, args.limit)
