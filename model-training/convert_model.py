import sys
from unittest.mock import MagicMock
# Mock tensorflow_decision_forests as it is not available on Windows and caused import error
sys.modules['tensorflow_decision_forests'] = MagicMock()
sys.modules['tensorflow_hub'] = MagicMock()
sys.modules['flax'] = MagicMock()

import tensorflowjs as tfjs
import tensorflow as tf
import argparse
import numpy as np
import json
import os

def convert_model(model_path, output_dir):
    # Load the Keras model
    model = tf.keras.models.load_model(model_path)
    
    # Convert to TensorFlow.js Layers format
    tfjs.converters.save_keras_model(model, output_dir)
    print(f"Model converted and saved to {output_dir}")

    # Convert classes.npy to classes.json
    classes_npy_path = os.path.join(os.path.dirname(model_path), 'classes.npy')
    # If model_path is just a filename, dirname is empty string, which join handles correctly as current dir
    if not os.path.dirname(model_path):
        classes_npy_path = 'classes.npy'
        
    if os.path.exists(classes_npy_path):
        classes = np.load(classes_npy_path, allow_pickle=True)
        # Check if classes are bytes (numpy often saves strings as bytes in mixed envs)
        # But LabelEncoder usually saves as the type of input.
        classes_list = classes.tolist()
        
        # Save as json in the output directory
        classes_json_path = os.path.join(output_dir, 'classes.json')
        with open(classes_json_path, 'w') as f:
            json.dump(classes_list, f)
        print(f"Classes saved to {classes_json_path}")
    else:
        print(f"Warning: classes.npy not found at {classes_npy_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Keras model to TensorFlow.js format.")
    parser.add_argument("--model_path", type=str, default="sign_language_model.h5", help="Path to the Keras model file")
    parser.add_argument("--output_dir", type=str, default="tfjs_model", help="Directory to save the converted model")
    args = parser.parse_args()
    
    convert_model(args.model_path, args.output_dir)
