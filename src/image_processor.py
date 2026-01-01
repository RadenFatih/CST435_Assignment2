import cv2
import numpy as np
import os

def process_single_image(image_path, output_folder):
    """
    Reads an image, applies 5 filters, and saves the result.
    Returns True if successful, False otherwise.
    """
    try:
        # 1. Read Image
        filename = os.path.basename(image_path)
        img = cv2.imread(image_path)
        
        if img is None:
            print(f"Error: Could not read {image_path}")
            return False

        # --- Filter 1: Grayscale Conversion ---
        # Requirement: Convert RGB to grayscale [cite: 24]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # --- Filter 2: Gaussian Blur ---
        # Requirement: 3x3 Gaussian kernel [cite: 25]
        blur = cv2.GaussianBlur(img, (3, 3), 0)

        # --- Filter 3: Edge Detection ---
        # Requirement: Sobel filter [cite: 26]
        # We combine Sobel X and Y to get the full edge magnitude
        sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
        edges = cv2.magnitude(sobelx, sobely)
        edges = np.uint8(edges) # Convert back to 8-bit

        # --- Filter 4: Image Sharpening ---
        # Requirement: Enhance edges and details [cite: 27]
        # Standard sharpening kernel
        kernel_sharpening = np.array([[-1,-1,-1],
                                      [-1, 9,-1],
                                      [-1,-1,-1]])
        sharpened = cv2.filter2D(img, -1, kernel_sharpening)

        # --- Filter 5: Brightness Adjustment ---
        # Requirement: Increase or decrease brightness [cite: 28]
        # We increase brightness by adding 30 to pixel values
        brightness = cv2.convertScaleAbs(img, alpha=1, beta=30)

        # --- SAVE OUTPUT ---
        # For the assignment, you might want to save just the final result 
        # or a composite. Let's save the 'Sharpened' version as the final output 
        # to demonstrate processing completion.
        
        output_path = os.path.join(output_folder, f"processed_{filename}")
        cv2.imwrite(output_path, sharpened)
        
        return True

    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return False

# Quick test block (Runs only if you execute this file directly)
if __name__ == "__main__":
    # Define paths
    input_dir = "../input_images"
    output_dir = "../output_images"
    
    # Get list of images
    images = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    print(f"Found {len(images)} images. Processing serially...")
    
    for img_path in images:
        process_single_image(img_path, output_dir)
        print(f"Processed {img_path}")
        
    print("Done! Check output_images folder.")
