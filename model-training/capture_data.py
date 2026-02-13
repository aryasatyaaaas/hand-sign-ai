import cv2
import os
import time
import argparse

def capture_images(label, output_dir="dataset/asl_alphabet_train/asl_alphabet_train"):
    # Create directory for the label
    label_dir = os.path.join(output_dir, label)
    if not os.path.exists(label_dir):
        os.makedirs(label_dir)
        print(f"Created directory: {label_dir}")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print(f"--- Capturing Data for Class: '{label}' ---")
    print("Press 's' to save an image.")
    print("Press 'q' to quit.")
    
    count = len(os.listdir(label_dir))
    print(f"Starting with count: {count}")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Can't receive frame (stream end?). Exiting ...")
            break

        # Display instruction
        display_frame = frame.copy()
        cv2.putText(display_frame, f"Class: {label} | Count: {count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(display_frame, "Press 's' to save, 'q' to quit", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        cv2.imshow('Data Collection', display_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            img_path = os.path.join(label_dir, f"{label}_{count}.jpg")
            cv2.imwrite(img_path, frame)
            print(f"Saved: {img_path}")
            count += 1
            # Visual feedback
            cv2.rectangle(display_frame, (0, 0), (display_frame.shape[1], display_frame.shape[0]), (0, 255, 0), 10)
            cv2.imshow('Data Collection', display_frame)
            cv2.waitKey(100) # Short pause

    cap.release()
    cv2.destroyAllWindows()
    print(f"Finished capturing {count} images for class '{label}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capture images for dataset.")
    parser.add_argument("label", type=str, help="Class label (e.g., A, B, C)")
    parser.add_argument("--output_dir", type=str, default="dataset/asl_alphabet_train/asl_alphabet_train", help="Path to save images")
    args = parser.parse_args()

    capture_images(args.label, args.output_dir)
