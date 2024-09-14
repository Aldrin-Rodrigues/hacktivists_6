# import cv2
# import numpy as np
# from pdf2image import convert_from_path
# import pytesseract

# pdf_file = 'hitha dl.pdf'
# pages = convert_from_path(pdf_file, poppler_path='/opt/homebrew/Cellar/poppler/24.04.0_1/bin')

# def remove_white_borders(image, tolerance=5):
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
#     binary = cv2.bitwise_not(binary)
#     contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
#     if contours:
#         x, y, w, h = cv2.boundingRect(contours[0])
#         # Ensure we're not cropping too aggressively by applying some tolerance
#         x = max(0, x - tolerance)
#         y = max(0, y - tolerance)
#         w = min(image.shape[1], x + w + tolerance)
#         h = min(image.shape[0], y + h + tolerance)
#         image = image[y:h, x:w]
#     return image

# def add_padding(image, padding_size=50):
#     # Add padding around the image to prevent loss of content during deskew
#     padded_image = cv2.copyMakeBorder(image, padding_size, padding_size, padding_size, padding_size, cv2.BORDER_CONSTANT, value=[255, 255, 255])
#     return padded_image

# def convert_blue_to_white(image):
#     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#     lower_blue = np.array([90, 50, 50])
#     upper_blue = np.array([130, 255, 255])
#     mask = cv2.inRange(hsv, lower_blue, upper_blue)
#     image[mask != 0] = [255, 255, 255]
#     cv2.imwrite("blue_to_write.png", image)
#     return image

# def deskew(image, padding=50):
#     # Add padding around the image to prevent cropping during deskewing
#     padded_image = cv2.copyMakeBorder(image, padding, padding, padding, padding, cv2.BORDER_CONSTANT, value=[255, 255, 255])

#     # Convert to grayscale and invert the colors
#     gray = cv2.cvtColor(padded_image, cv2.COLOR_BGR2GRAY)
#     gray = cv2.bitwise_not(gray)

#     # Find coordinates of non-zero pixels
#     coords = np.column_stack(np.where(gray > 0))
#     angle = cv2.minAreaRect(coords)[-1]
    
#     # Correct the angle based on its direction
#     if angle < -45:
#         angle = -(90 + angle)
#     else:
#         angle = -angle

#     # Get the height and width of the padded image
#     (h, w) = padded_image.shape[:2]
#     center = (w // 2, h // 2)

#     # Create a rotation matrix for the deskewing
#     M = cv2.getRotationMatrix2D(center, angle, 1.0)

#     # Expand the image canvas to accommodate rotation without cropping
#     cos = np.abs(M[0, 0])
#     sin = np.abs(M[0, 1])

#     # Compute the new bounding dimensions of the image after rotation
#     new_w = int((h * sin) + (w * cos))
#     new_h = int((h * cos) + (w * sin))

#     # Adjust the rotation matrix to account for the new dimensions
#     M[0, 2] += (new_w / 2) - center[0]
#     M[1, 2] += (new_h / 2) - center[1]

#     # Perform the rotation with the expanded canvas size
#     rotated = cv2.warpAffine(padded_image, M, (new_w, new_h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
    
#     cv2.imwrite("deskewed_image.png", rotated)
#     return rotated

# def enhance_text(image):
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     denoised = cv2.fastNlMeansDenoising(gray, None, 30, 7, 21)
#     enhanced = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
#     kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])
#     sharpened = cv2.filter2D(enhanced, -1, kernel)
#     cv2.imwrite("enhanced_image.png", sharpened)
#     return sharpened

# def extract_text_from_image(image):
#     text = pytesseract.image_to_string(image)
#     return text

# # Convert the first page to an image array
# page_image = np.array(pages[0])

# # Step 1: Remove white borders (with tolerance to avoid over-cropping)
# # image_no_borders = remove_white_borders(page_image)

# # Step 2: Convert blue background to white
# image_processed = convert_blue_to_white(page_image)

# # Step 3: Add padding before deskewing to prevent content loss
# image_with_padding = add_padding(image_processed)

# # Step 4: Deskew the image to correct alignment
# deskewed_image = deskew(image_with_padding)

# # Step 5: Enhance the text for better OCR
# enhanced_image = enhance_text(deskewed_image)

# # Step 6: Extract text
# text = extract_text_from_image(enhanced_image)

# # Print the extracted text
# print(text)

# # Optional: Save the enhanced image for manual inspection
# cv2.imwrite("enhanced_image_with_padding.png", enhanced_image)


# def extract_regex(text):
#     import re
#     # number  = re.findall(r'[^A-Z0-9]*?([A-Z]{5,6}\d{3}[A-Z])$', text)
#     # print("PAN Number: ", number)
#     dob = re.findall(r'\b[0-9]{2}/[0-9]{2}/[0-9]{4}\b', text)
    
    
# extract_regex(text)

import cv2
import numpy as np
from pdf2image import convert_from_path
import pytesseract
import sys
import ast
import datetime


def remove_white_borders(image, tolerance=5):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    binary = cv2.bitwise_not(binary)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        x, y, w, h = cv2.boundingRect(contours[0])
        # Ensure we're not cropping too aggressively by applying some tolerance
        x = max(0, x - tolerance)
        y = max(0, y - tolerance)
        w = min(image.shape[1], x + w + tolerance)
        h = min(image.shape[0], y + h + tolerance)
        image = image[y:h, x:w]
    return image

def add_padding(image, padding_size=50):
    # Add padding around the image to prevent loss of content during deskew
    padded_image = cv2.copyMakeBorder(image, padding_size, padding_size, padding_size, padding_size, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    return padded_image

def convert_blue_to_white(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    image[mask != 0] = [255, 255, 255]
    cv2.imwrite("blue_to_write.png", image)
    return image

def deskew(image, padding=50):
    # Add padding around the image to prevent cropping during deskewing
    padded_image = cv2.copyMakeBorder(image, padding, padding, padding, padding, cv2.BORDER_CONSTANT, value=[255, 255, 255])

    # Convert to grayscale and invert the colors
    gray = cv2.cvtColor(padded_image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)

    # Find coordinates of non-zero pixels
    coords = np.column_stack(np.where(gray > 0))
    angle = cv2.minAreaRect(coords)[-1]
    
    # Correct the angle based on its direction
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    # Get the height and width of the padded image
    (h, w) = padded_image.shape[:2]
    center = (w // 2, h // 2)

    # Create a rotation matrix for the deskewing
    M = cv2.getRotationMatrix2D(center, angle, 1.0)

    # Expand the image canvas to accommodate rotation without cropping
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # Compute the new bounding dimensions of the image after rotation
    new_w = int((h * sin) + (w * cos))
    new_h = int((h * cos) + (w * sin))

    # Adjust the rotation matrix to account for the new dimensions
    M[0, 2] += (new_w / 2) - center[0]
    M[1, 2] += (new_h / 2) - center[1]

    # Perform the rotation with the expanded canvas size
    rotated = cv2.warpAffine(padded_image, M, (new_w, new_h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
    
    cv2.imwrite("deskewed_image.png", rotated)
    return rotated

def rotate_image(image):
    # Rotate the image upside down
    rotated_image = cv2.rotate(image, cv2.ROTATE_180)
    return rotated_image

def enhance_text(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, None, 30, 7, 21)
    enhanced = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])
    sharpened = cv2.filter2D(enhanced, -1, kernel)
    cv2.imwrite("enhanced_image.png", sharpened)
    return sharpened

def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text




def extract_regex(text):
    import re
    class_of_vehicle = re.search(r'cov\s*:\s*([A-Za-z]+)', text)
    class_of_vehicle = class_of_vehicle.group(1)
    class_of_vehicle  = str(class_of_vehicle)
    class_of_vehicle = class_of_vehicle.upper().replace("cov:", "").replace(" ", "")
    return class_of_vehicle
    

def check_vehicle_class(cov, class_of_vehicle):
    cov = cov.upper()
    class_of_vehicle = class_of_vehicle.upper()
    if cov == class_of_vehicle:
        print("You are eligible")
    else:
        print("You are not eligible")
    
def main():
    cov = sys.argv[1] 
    pdf_file = sys.argv[2]
    # pdf_file = "hitha dl.pdf"
    # cov = "MCWOG"
    pages = convert_from_path(pdf_file, poppler_path='/opt/homebrew/Cellar/poppler/24.04.0_1/bin')
    
    # Convert the first page to an image array
    page_image = np.array(pages[0])

    # Step 1: Remove white borders (with tolerance to avoid over-cropping)
    # image_no_borders = remove_white_borders(page_image)

    # Step 2: Convert blue background to white
    image_processed = convert_blue_to_white(page_image)

    # Step 3: Add padding before deskewing to prevent content loss
    image_with_padding = add_padding(image_processed)

    # Step 4: Deskew the image to correct alignment
    deskewed_image = deskew(image_with_padding)

    # Step 5: Enhance the text for better OCR
    enhanced_image = enhance_text(deskewed_image)
    
    enhanced_image = rotate_image(enhanced_image)


    # Step 6: Extract text
    text = extract_text_from_image(enhanced_image)

    # Print the extracted text
    # print(text)

    # Optional: Save the enhanced image for manual inspection
    cv2.imwrite("enhanced_image_with_padding.png", enhanced_image)
    
    class_of_vehicle = extract_regex(text)
    
    check_vehicle_class(cov, class_of_vehicle)
    
    

if __name__ == "__main__":
    main()


