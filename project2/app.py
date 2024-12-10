from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Mock patient records
patients = [
    {
        'tc_kimlik_no': '3526789456',
        'name': 'Ali',
        'age': 35,
        'gender': 'Male',
        'blood_type': 'A+',
        'phone': '555-1234',
        'height': '180 cm',
        'weight': '75 kg',
        'diagnoses': ['Asthma', 'Weight Loss', 'Gastro Reflux'],
        'visits': ['01 September 2024', '09 November 2014'],
        'allergies': ['Aspirin', 'Cats', 'Horse'],
        'pulse': '72 bpm'
    }
]

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'admin':
            return redirect(url_for('main_menu'))
        else:
            flash('Invalid credentials. Please try again.', 'error')

    return render_template('login.html')

@app.route('/main_menu')
def main_menu():
    return render_template('main_menu.html')

@app.route('/register_patient', methods=['GET', 'POST'])
def register_patient():
    if request.method == 'POST':
        patient = {
            'tc_kimlik_no': request.form['tc_kimlik_no'],
            'name': request.form['name'],
            'age': request.form['age'],
            'gender': request.form['gender'],
            'blood_type': request.form['blood_type'],
            'phone': request.form['phone'],
            'height': request.form['height'],
            'weight': request.form['weight']
        }
        patients.append(patient)
        flash(f'Patient {patient["name"]} registered successfully!', 'success')
        return redirect(url_for('main_menu'))

    return render_template('register_patient.html')

@app.route('/find_patient', methods=['GET', 'POST'])
def find_patient():
    search_tc = request.args.get('tc_kimlik_no')
    if search_tc:
        patient = next((p for p in patients if p['tc_kimlik_no'] == search_tc), None)
        return render_template('find_patient.html', patients=patients, search_tc=search_tc, found_patient=patient)
    return render_template('find_patient.html', patients=patients)

@app.route('/patient/<tc_kimlik_no>')
def patient_detail(tc_kimlik_no):
    patient = next((p for p in patients if p['tc_kimlik_no'] == tc_kimlik_no), None)
    if patient:
        return render_template('patient_detail.html', patient=patient)
    else:
        flash('Patient not found.', 'error')
        return redirect(url_for('find_patient'))

if __name__ == '__main__':
    app.run(debug=True)