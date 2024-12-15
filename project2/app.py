from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

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
        'pulse': '72 bpm',
        'inpatient_room':'Not Assigned'
    }
]
rooms= {
    1:True,
    2:False,
    3:True,
    4:False,
    5:False,
    6:True,
    7:False,
    8:True,
    9:True,
    10:False
}

class LoginForm(FlaskForm):
    email= StringField('E-mail')
    mrsId = StringField('CareSync-ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        mrsId = form.mrsId.data
        password = form.password.data
        
        
        if mrsId == 'admin' and password == 'password':  
            flash('Login successful!', 'success')
            return redirect(url_for('two_factor_auth'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = LoginForm()
    if request.method == 'POST':
        
        pass
    return render_template('forgot-password.html',form=form)  

@app.route('/two-factor-auth', methods=['GET', 'POST'])
def two_factor_auth():
    if request.method == 'POST':
        code = request.form.get('code')  
        if code == "123":  
            return render_template('main_menu.html')
            
        else:
            flash('Invalid code. Please try again.', 'danger')

    return render_template('two_factor_auth.html')  



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
            'weight': request.form['weight'],
            'inpatient_room':request.form.get('inpatient_room','Not Assigned')
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
    flash('Patient not found.', 'danger')
    return render_template('find_patient.html', patients=patients)

@app.route('/patient/<tc_kimlik_no>')
def patient_detail(tc_kimlik_no):
    patient = next((p for p in patients if p['tc_kimlik_no'] == tc_kimlik_no), None)
    if patient:
        return render_template('patient_detail.html', patient=patient)
    else:
        flash('Patient not found.', 'error')
        return redirect(url_for('find_patient'))

@app.route('/assign_room', methods=['GET','POST'])
def assign_room():
    
    if request.method == 'POST':
        tc_kimlik_no = request.form['tc_kimlik_no']
        

        patient = next((p for p in patients if p['tc_kimlik_no'] == tc_kimlik_no), None)
        
        room_number = request.form['room_number']
        if patient:
            patient['inpatient_room'] = room_number
            flash(f'Room {room_number} assigned to patient {patient["name"]}.', 'success')
            rooms[int(room_number)]=False
            return redirect(url_for('main_menu'))
        else:
            flash('Patient not found.', 'danger')

    available_rooms = [room for room, is_available in rooms.items() if is_available]
    return render_template('assign_room.html',rooms=available_rooms)
    
    


if __name__ == '__main__':
    app.run(debug=True)