# AI Model Training Guide

This folder contains scripts to train your custom Sign Language translation model.

## 1. Setup Environment
**Windows Users:**
1.  Double-click `setup_env.bat` to create the environment and install dependencies.
2.  Double-click `run_console.bat` to open a terminal with the environment activated.

**Mac/Linux Users:**
1.  Open a terminal in this folder.
2.  Run `python3 -m venv venv`
3.  Run `source venv/bin/activate`
4.  Run `pip install -r requirements.txt`

## 2. Prepare Dataset
1.  Download a Sign Language dataset (e.g., [ASL Alphabet from Kaggle](https://www.kaggle.com/datasets/grassknoted/asl-alphabet)).
2.  Extract it so you have a folder structure like:
    ```
    dataset/
      A/
        image1.jpg
        ...
      B/
        image1.jpg
        ...
      ...
    ```

## 3. Process Data
Run the processing script to extract hand landmarks from images. This converts images into coordinates.
```bash
python process_data.py --data_dir /path/to/dataset --output_file landmarks.csv
```
*Note: This might take a while depending on the number of images.*

## 4. Train Model
Train a neural network on the extracted landmarks.
```bash
python train_model.py --data_file landmarks.csv --model_output my_model.h5
```

## 5. Convert to Web Format
Convert the trained Keras model to TensorFlow.js format for the website.
```bash
python convert_model.py --model_path my_model.h5 --output_dir ../web-app/public/model
```
*This will place the model directly into the web app's public folder.*
