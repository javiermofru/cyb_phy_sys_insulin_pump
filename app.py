import time
from flask import Flask, render_template, render_template_string, request
from insulin_pump import InsulinPump

app = Flask(__name__)
insulin_pump = InsulinPump()

@app.route('/')
def index():
    return render_template('index.html', insulin_pump=insulin_pump)

@app.route('/message')
def message():
    return render_template('message.html', message=insulin_pump.msg)

@app.route('/activate_dos', methods=['POST'])
def activate_dos():
    insulin_pump.dos_vulnerability = not insulin_pump.dos_vulnerability
    return render_template('index.html', insulin_pump=insulin_pump)

@app.route('/activate_data_integrity', methods=['POST'])
def activate_data_integrity():
    insulin_pump.data_integrity_vulnerability = not insulin_pump.data_integrity_vulnerability
    return render_template('index.html', insulin_pump=insulin_pump)

@app.route('/activate_eavesdropping', methods=['POST'])
def activate_eavesdropping():
    insulin_pump.eavesdropping_vulnerability = not insulin_pump.eavesdropping_vulnerability
    return render_template('index.html', insulin_pump=insulin_pump)

@app.route('/activate_unauthorized_access', methods=['POST'])
def activate_unauthorized_access():
    insulin_pump.non_authorized_access_vulnerability = not insulin_pump.non_authorized_access_vulnerability
    return render_template('index.html', insulin_pump=insulin_pump)

@app.route('/update_parameters', methods=['POST'])
def update_parameters():
    glucose_ideal = int(request.form['glucose_ideal'])
    insulin_pump.updateParameters(glucose_ideal)
    return render_template('index.html', insulin_pump=insulin_pump)

@app.route('/perform_dos_attack', methods=['POST'])
def perform_dos_attack():
    insulin_pump.dosAttack()
    return render_template('index.html', insulin_pump=insulin_pump)

@app.route('/perform_unauthorized_access_attack', methods=['POST'])
def perform_unauthorized_access_attack():
    attacker_name = request.form['attacker_name']
    insulin_pump.unauthorizedAccess(attacker_name)
    return render_template('index.html', insulin_pump=insulin_pump)

@app.route('/perform_eavesdropping_attack', methods=['POST'])
def perform_eavesdropping_attack():
    attacker_name = request.form['attacker_name']
    insulin_pump.interceptMessage(insulin_pump.message, attacker_name)
    return render_template('index.html', insulin_pump=insulin_pump)

@app.route('/perform_integrity_attack', methods=['POST'])
def perform_integrity_attack(): 
    
    insulin_pump.decryptMessage(insulin_pump.message)
    return render_template('index.html', insulin_pump=insulin_pump)

@app.route("/update_message", methods=["POST"])
def post():
    insulin_pump.msg =  request.form.get('message')

    return render_template('index.html', insulin_pump=insulin_pump)

# Simulation of changes in glucose levels and automatic insulin adjustment
def simulate_glucose():
    while True:
        new_glucose = insulin_pump.glucose_level + 5  
        # Update glucose in the insulin pump
        insulin_pump.measureGlucose(new_glucose)

        # Administer insulin automatically
        insulin_pump.administerInsulin()

        # Wait for some time before the next measurement
        time.sleep(10) 

if __name__ == '__main__':
    from threading import Thread

    # Start the simulation thread
    simulation_thread = Thread(target=simulate_glucose)
    simulation_thread.start()

    # Run the Flask application
    app.run(debug=True)
