import sys
import ast
import datetime
import pytesseract
from pdf2image import convert_from_path
import cv2
import numpy as np
import re
import oauthlib
import requests
import json

def validate_aadhar_number(aadhar_number):
    url = "https://production.deepvue.tech/v1/verification/aadhaar"

    params = {
        'aadhaar_number': aadhar_number
    }
    headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmcmVlX3RpZXJfcGVzMTIwMjIwMjI3MF9iYjVkM2VhMjY1IiwiZXhwIjoxNzI2Mjg3NzkwfQ.N9ady8ed2GYpteOqDZTqhNRAnvFa-oY0d8rMWdP4jsY' ,
    'x-api-key': '3485849b7aea4c029ef90f166d96268f',
    'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, params=params)

    return response.text

def deskew(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    coords = np.column_stack(np.where(gray > 0))
    angle = cv2.minAreaRect(coords)[-1]
    
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return rotated




def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

def check_age_requirement(dob, age_limit):
    age_limit = int(age_limit)
    current_data = datetime.datetime.now()
    # print(dob)
    dob = datetime.datetime.strptime(dob, "%d/%m/%Y")
    #subtract two dates
    if (current_data - dob).days/365.25 >= age_limit:
        print("You are eligible")
    else:
        print("You are not eligible")
    

def main():
    # data = ast.literal_eval(sys.argv[1])
    agelimit = sys.argv[1] 
    pdf_file = sys.argv[2]
    # pdf_file = "hitha_aadhar.pdf"
    # agelimit = 18
    pages = convert_from_path(pdf_file, poppler_path='/opt/homebrew/Cellar/poppler/24.04.0_1/bin')
    
    pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'
    
    
    extracted_text=[]

    preprocessed_image = deskew(np.array(pages[0]))

    text = extract_text_from_image(preprocessed_image)
    extracted_text.append(text)
    extracted_text_str = ' '.join(extracted_text)
    
    number_pattern = r"\bXXXX\sXXXX\s\d{4}\b"
    dob_regex = r"\b\d{2}/\d{2}/\d{4}\b"
    address_regex = r"Address:\s*(.*?)(\d{6})"

    # Check if the pattern is present
    number_match = re.search(number_pattern, extracted_text_str)
    dob_match = re.search(dob_regex, extracted_text_str)
    address_match = re.search(address_regex, text, re.DOTALL)

    if number_match:
        number_match =  str(number_match.group(0)).replace("XXXX XXXX", "2462 7522")
        # print("Number found:", number_match)  # Output the matched string
        number_match = number_match.replace(" ", "")
        number_match = number_match.strip()
        # output = validate_aadhar_number(number_match)
        # if "SUCCESS" in output:
        #     pass
        # else:
        #     print("Number not valid.")
    else:
        print("Number not valid.")
           
    if dob_match:
        # print("DOB found:", dob_match.group(0))  # Output the matched string
        dob = dob_match.group(0)
        check_age_requirement(dob, age_limit=agelimit)
    else:
        print("DOB not found.")

    # if address_match:   
    #     address_match =  str(address_match.group(0)).replace("\n", " ")
    #     if address_match.startswith("Address:"):
    #         address_match = address_match[len("Address:"):]
    #     print("Address found:", address_match)  # Output the matched string
    # else:
    #     print("Address not found.")
    # print(address_match)
    
if __name__ == "__main__":
    main()
    
    
    
    
    

