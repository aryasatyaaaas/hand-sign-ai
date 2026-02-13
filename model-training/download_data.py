import os
import requests
import zipfile
import io

# URL for a smaller version or a subset of ASL dataset. 
# Since Kaggle requires auth, we can try to find a public subset or 
# guide the user to download it manually if this fails.
# This URL is a placeholder for a public dataset if available, 
# otherwise we might need to use the kaggle API.

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)
    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)
    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

def download_and_extract():
    # Alternative: Use "kaggle" CLI if configured.
    print("Attempting to download ASL Alphabet dataset...")
    
    # Check if user has kaggle installed and configured
    try:
        import kaggle
        print("Kaggle API found. Downloading 'grassknoted/asl-alphabet'...")
        os.system("kaggle datasets download -d grassknoted/asl-alphabet -p . --unzip")
        print("Download complete!")
        return
    except ImportError:
        print("Kaggle library not found or not configured.")
    except Exception as e:
        print(f"Kaggle download failed: {e}")

    print("\n--- MANUAL DOWNLOAD REQUIRED ---")
    print("Direct download of large datasets is restricted without API keys.")
    print("Please follow these steps:")
    print("1. Go to: https://www.kaggle.com/datasets/grassknoted/asl-alphabet")
    print("2. Click 'Download' (archive.zip)")
    print("3. Extract the contents into this folder so you have 'asl_alphabet_train/asl_alphabet_train/'")
    print("--------------------------------")

if __name__ == "__main__":
    download_and_extract()
