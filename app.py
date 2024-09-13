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

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    document_type = request.form.get('documentType')
    selected_option = request.form.get('selectedOption')
    age_limit = request.form.get('ageLimit')
    selected_state = request.form.get('selectedState')
    file = request.files.get('file')

    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    '''
    if document_type == 'Aadhar Card':
        if selected_option == 'age':
            subprocess.run(['python', 'age_verification_script.py', age_limit])
        elif selected_option == 'address':
            subprocess.run(['python', 'address_verification_script.py', selected_state])
        elif selected_option == 'aadharNumber':
            # subprocess.run(['python', 'aadhar_number_validation_script.py'])
            pass
    '''   
    if document_type == 'PAN Card':
        if selected_option == 'age':
            age_limit_str = str(age_limit)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            result = subprocess.run(['python', 'pancard.py', age_limit_str, file_path], capture_output=True, text=True)
            print(result.stdout)
            
        
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
    
    
    print(response_data)
    return jsonify(response_data)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)

