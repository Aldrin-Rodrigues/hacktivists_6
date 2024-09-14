from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Store received data globally (in-memory storage for simplicity)
received_data = None

@app.route('/submit', methods=['POST'])
def receive_data():
    global received_data
    # Receive JSON data from the POST request
    received_data = request.get_json()
    print(f"Data received from localhost:5000: {received_data}")
    
    # Acknowledge the data reception
    return jsonify({'status': 'Data received successfully'})

@app.route('/check', methods=['GET'])
def display_data():
    global received_data
    if received_data:
        return render_template('templates.html', data=received_data)
    else:
        return "No data received yet.", 200

if __name__ == '__main__':
    app.run(port=5001, debug=True)




