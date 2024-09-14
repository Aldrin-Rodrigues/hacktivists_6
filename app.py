# from flask import Flask, request, jsonify, render_template


# app = Flask(__name__)

# @app.route('/')
# def home():
#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify, render_template
import os
import subprocess
import sys
import requests

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/submit', methods=['POST'])
def submit():
    document_type = request.form.get('documentType')
    selected_option = request.form.get('selectedOption')
    age_limit = request.form.get('ageLimit')
    selected_state = request.form.get('selectedState')
    file = request.files.get('file')

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

    if document_type == 'Aadhar Card':
        if selected_option == 'age':
            age_limit_str = str(age_limit)
            result = subprocess.run(['python', 'aadhar_final_age.py', age_limit_str, file_path], capture_output=True, text=True)
            print(result.stdout)
            result_output = result.stdout
        elif selected_option == 'address':
            selected_state = str(selected_state)
            result = subprocess.run(['python', 'aadhar_final_address.py', selected_state, file_path], capture_output=True, text=True)
            print(result.stdout)
            result_output = result.stdout
        # elif selected_option == 'aadharNumber':
            # subprocess.run(['python', 'aadhar_number_validation_script.py'])

    elif document_type == 'PAN Card':
        if selected_option == 'age':
            age_limit_str = str(age_limit)
            result = subprocess.run(['python', 'pancard.py', age_limit_str, file_path], capture_output=True, text=True)
            print(result.stdout)
            result_output = result.stdout
        
    # elif document_type == 'Covid-19 Vaccination Certificate':
    #     if selected_option == 'vaccineVerification':
    #         subprocess.run(['python', 'vaccine_verification_script.py'])
        
    # Handle form data as needed
    response_data = {
        'documentType': document_type,
        'selectedOption': selected_option,
        'ageLimit': age_limit,
        'selectedState': selected_state,
        'fileName': file.filename if file else None
    }
    
    requests.post('http://localhost:5001/submit', json = {
        'validity': result_output
    })
    
    print(response_data)
    return jsonify(response_data)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)


# @app.route('/submit', methods=['POST'])
# def submit():
#     # Sending the POST request to localhost:5001
#     response = requests.post('http://localhost:5001/submit', data={'key1': 'value1', 'key2': 'value2'})
#     print(response.text)
#     return jsonify({'status': 'success', 'output': response.text})