
from psycopg2 import connect
from flask import Flask, request, jsonify, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
import os
from datetime import date

from marshmallow import Schema, fields, ValidationError, pre_load
from flask_login import login_user, logout_user, login_required



from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, UserMixin




# Init app
app = Flask(__name__)                 
app.secret_key = "Secret Key"

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://kumlmkrpwvtffp:34ffa0b9a4e5d85ba1679d979c2ff64938edc35e2f58f18dcf68f0b76610bb97@ec2-54-157-66-140.compute-1.amazonaws.com/daj0298ke4iu1b'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)


login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# list of dates every updates
dateList = [date(2020, 5, 17)]   


##### MODEL #####
class Vaccine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    phase = db.Column(db.Text,  nullable=False)
    vaccine_type = db.Column(db.Text,  nullable=False)
    developer = db.Column(db.Text,  nullable=False)
    efficacy = db.Column(db.Text,  nullable=False)
    dose = db.Column(db.Text,  nullable=False)
    vaccine_storage = db.Column(db.Text, nullable=False)

    def __init__(self, name, phase, vaccine_type, developer, efficacy, dose, vaccine_storage): 
        self.name = name
        self.phase = phase
        self.vaccine_type = vaccine_type
        self.developer = developer
        self.efficacy = efficacy
        self.dose = dose
        self.vaccine_storage = vaccine_storage


##### SCHEMAS #####
class VaccineSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str()
    phase = fields.Str()
    vaccine_type = fields.Str()
    developer = fields.Str()
    efficacy = fields.Str()
    dose = fields.Str()
    vaccine_storage = fields.Str()

vaccine_schema = VaccineSchema()
vaccines_schema = VaccineSchema(many=True)




class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


    def __init__(self, email, password, name):      
        self.email = email
        self.password = password
        self.name = name


@app.route('/login')
def login():
    return render_template('sign-in.html')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    # remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if email == 'regine.cpalomo11@gmail.com' and check_password_hash(user.password, password):
        return redirect(url_for('home')) 
    elif user and check_password_hash(user.password, password):
        login_user(user)
        return redirect(url_for('home_client'))
    else:
        flash('Please check your login details and try again.')
        return redirect(url_for('login'))


    # if not user and not check_password_hash(user.password, password):
        # flash('Please check your login details and try again.')
        # return redirect(url_for('login'))

    # login_user(user)

    

@app.route('/signup')
def signup():
    return render_template('sign-up.html')



@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists.')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/")
def index():
    phases = ['Phase 1', 'Phase 2', 'Phase 3', 'Limited', 'Approved', 'Abandoned']
    count = []
    for phase in phases:
        counter = count_vaccine_by_phase(phase)
        count.append(counter)
    
    return render_template("index.html", count1=count[0],count2=count[1],count3=count[2],countLimited=count[3],
        countApproved=count[4],countAbandoned=count[5], date=dateList[-1])
    # return render_template("index.html")



# RENDERING TEMPLATES ADMIN
@app.route("/homeAdmin")
def home():
    phases = ['Phase 1', 'Phase 2', 'Phase 3', 'Limited', 'Approved', 'Abandoned']
    count = []
    for phase in phases:
        counter = count_vaccine_by_phase(phase)
        count.append(counter)
    
    return render_template("home.html", count1=count[0],count2=count[1],count3=count[2],countLimited=count[3],
        countApproved=count[4],countAbandoned=count[5], date=dateList[-1])
    # return render_template("home.html", count= count)

@app.route("/manage_data")
def manage_data():
    return render_template("view-all.html")

@app.route("/create")
def create():
    return render_template("create.html")

@app.route("/edit/<id>")
def edit(id):

    result = Vaccine.query.get(id)
    return render_template("edit.html", vaccine = result)



# RENDER TEMPLATES USER
@app.route("/user")
def home_client():
    phases = ['Phase 1', 'Phase 2', 'Phase 3', 'Limited', 'Approved', 'Abandoned']
    count = []
    for phase in phases:
        counter = count_vaccine_by_phase(phase)
        count.append(counter)
    
    return render_template("home-client.html", count1=count[0],count2=count[1],count3=count[2],countLimited=count[3],
        countApproved=count[4],countAbandoned=count[5], date=dateList[-1])
    # return render_template("home-client.html")

@app.route("/view")
def view_data():
    all_vaccines = Vaccine.query.order_by(Vaccine.id).all()

    return render_template("view-client.html", vaccines = all_vaccines, date= dateList[-1])

# list of vaccines by phase
@app.route('/view/<phase>', methods=['GET'])
def view_vaccine_by_phase(phase):

    vaccines = Vaccine.query.filter_by(phase= phase)
    result = vaccines_schema.dump(vaccines)

    return render_template("phase-client.html", vaccines = result)



# ROUTES FOR QUERIES
@app.route("/addVaccine", methods=["POST"])
def addVaccine():

    if request.method == 'POST':
        name = request.form['name']
        phase = request.form['phase']
        vaccine_type = request.form['vaccine_type']
        developer = request.form['developer']
        efficacy = request.form['efficacy']
        dose = request.form['dose']
        vaccine_storage = request.form['vaccine_storage']

        new_vaccine = Vaccine(name,phase,vaccine_type, developer, efficacy,dose,vaccine_storage)

        db.session.add(new_vaccine)
        db.session.commit()

        flash("Employee Inserted Successfully")

        update_date()

        return render_template("create.html")

        # return redirect(url_for('get_all_vaccines'))

    

#This is the index route where we are going to
#query on all our vaccine data
@app.route('/vaccines', methods=['GET'])
def get_all_vaccines():
    all_vaccines = Vaccine.query.order_by(Vaccine.id).all()
    # result = vaccines_schema.dump(all_vaccines)
    # return jsonify(result)
    return render_template("view-all.html", vaccines = all_vaccines, date= dateList[-1])
    # return render_template("try.html", vaccines = all_vaccines)


# list of vaccines by phase
@app.route('/vaccine/<phase>', methods=['GET'])
def get_vaccine_by_phase(phase):

    vaccines = Vaccine.query.filter_by(phase= phase)
    result = vaccines_schema.dump(vaccines)

    return render_template("vaccine-phase.html", vaccines = result)


# update date 
def update_date():   
    global currDate
    global dateList

    currDate = date.today()
    dateList.append(currDate)
        
    
    
# counter in home page
@app.route('/count/<phase>', methods=['GET'])
def count_vaccine_by_phase(phase):

    vaccine_count = Vaccine.query.filter_by(phase= phase).count()
    return vaccine_count



@app.route("/update", methods=['GET', 'POST'])
def update():

    if request.method == 'POST':

        vaccine = Vaccine.query.get(request.form.get('id'))
  

        vaccine.name = request.form['name']
        vaccine.phase = request.form['phase']
        vaccine.vaccine_type = request.form['vaccine_type']
        vaccine.developer = request.form['developer']
        vaccine.efficacy = request.form['efficacy']
        vaccine.dose = request.form['dose']
        # vaccine.vaccine_storage = request.form['vaccine_storage']


        db.session.commit()

        update_date()

        flash("Vaccine Updated Successfully")      
        return redirect(url_for('edit', id= request.form.get('id')))


@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    vaccine = Vaccine.query.get(id)
    db.session.delete(vaccine)
    db.session.commit()

    update_date()

    flash("Employee Deleted Successfully")

    return redirect(url_for('get_all_vaccines'))



# helper function
def get_phase(id):
    vaccine = Vaccine.query.get(id)

    phase = vaccine.phase
    return phase

# Run Server
if __name__ == '__main__':
    app.run(debug=True)

