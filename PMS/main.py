from flask import Flask, render_template, url_for, request, flash, redirect
from flask_wtf import FlaskForm  
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, EmailField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship

# Application initialization
parking_system = Flask(__name__)
parking_system.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///instance/system.db"
parking_system.secret_key = "yi5u9yh4gn"

# Create database object
db = SQLAlchemy(parking_system)

# Login manager to add authentication functionality
login_manager = LoginManager()
login_manager.init_app(parking_system)

# User loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Database configuration
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), nullable=False)
    usr_email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    flat_no = db.Column(db.Integer, nullable=False, unique=True)
    aadhar_no = db.Column(db.Integer, nullable=False, unique=True)
    phone_no = db.Column(db.Integer, nullable=False, unique=True)
    vehicles = relationship('Vehicle', back_populates='owner')

class LicensePlate(db.Model):
    __tablename__ = 'license_plate'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    state = db.Column(db.String(20))
    number = db.Column(db.String(20), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))  # Added foreign key relationship
    vehicle = relationship('Vehicle', back_populates='plates')

class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)  
    vehicle_name = db.Column(db.String(80), nullable=False)
    vehicle_type = db.Column(db.String(80), nullable=False)
    vehicle_plate = db.Column(db.String(80), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    owner = relationship('User', back_populates='vehicles')  # Defined back reference to User
    plates = relationship('LicensePlate', back_populates='vehicle')

# Creating database
with parking_system.app_context():
    db.create_all()

# Forms
class Loginform(FlaskForm):
    """This class creates a login form."""
    email = EmailField('EMAIL-ID:', validators=[DataRequired()])
    password = PasswordField('PASSWORD:', validators=[DataRequired()])
    login = SubmitField('LOGIN')

class Signup(FlaskForm):
    """This class creates a signup form."""
    user_name = StringField("User Name:", validators=[DataRequired(), Length(min=4, max=10)])
    email = EmailField('EMAIL-ID:', validators=[DataRequired()])
    password = PasswordField('SET PASSWORD:', validators=[DataRequired()])
    flat_no = StringField('FLAT-NO:', validators=[DataRequired()])
    aadhar_no = StringField('AADHAR CARD-NO:', validators=[DataRequired()])
    phn_number = StringField('MOBIE NUMBER:', validators=[DataRequired()])
    signup = SubmitField('SIGNUP')

class VehicleForm(FlaskForm):
    """This class creates a vehicle form"""
    vehicle_name = StringField("VEHICLE NAME:", validators=[DataRequired(), Length(min=2, max=10)])
    vehicle_type = SelectField("Vehicle Type", validators=[DataRequired()], choices=['2-wheeler', '3-wheeler', '4-wheeler'])  # Dropdown
    vehicle_plate = StringField("VEHICLE PLATE NUMBER:", validators=[DataRequired(), Length(min=4, max=10)])
    add_veh = SubmitField('Add Vehicle')

class ProfileForm(FlaskForm):
    """This class represents profile form."""
    flat_no = StringField('Flat No:', validators=[DataRequired()])
    aadhar_no = StringField('Aadhar No:', validators=[DataRequired()])
    phn_no = StringField('Phone No:', validators=[DataRequired()])
    update = SubmitField('Update')

# Function to hash passwords
def hash_password(password):
    """This function hashes the user password."""
    return generate_password_hash(password)

# Function to check passwords
def check_hash(user_hash, password):
    """This function checks if the password entered by the user is correct."""
    return check_password_hash(user_hash, password)

# Routes
@parking_system.route("/")
def home():
    vehicle_list = Vehicle.query.all()
    lis_list = LicensePlate.query.all()
    return render_template('index.html', user_logged_in=current_user.is_authenticated, v_list=vehicle_list, l_list=lis_list)

@parking_system.route("/profile")
@login_required
def profile():
    user_list = User.query.all()
    return render_template("profile.html", user_logged_in=current_user.is_authenticated, u_list=user_list)

@parking_system.route("/vehicles")
@login_required
def vehicles():
    vehicle_list = Vehicle.query.all()
    return render_template("vehicles.html", user_logged_in=current_user.is_authenticated, v_list=vehicle_list)

@parking_system.route("/login", methods=['GET', 'POST'])
def login():
    form = Loginform()
    if form.validate_on_submit():
        user = User.query.filter_by(usr_email=form.email.data).first()
        if user and check_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid Email-ID or password')

    return render_template("login.html", form=form)

@parking_system.route("/signup", methods=['GET', 'POST'])
def signup():
    form = Signup()
    if form.validate_on_submit():
        hashed_password = hash_password(form.password.data)
        new_user = User(user_name=form.user_name.data, usr_email=form.email.data, password=hashed_password,
                        flat_no=form.flat_no.data, aadhar_no=form.aadhar_no.data, phone_no=form.phn_number.data)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))

    return render_template('signup.html', form=form, user_logged_in=current_user.is_authenticated)

@parking_system.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@parking_system.route("/vehicle-registration", methods=['GET', 'POST'])
@login_required
def vehicle_registration():
    form = VehicleForm()
    if form.validate_on_submit():
        new_vehicle = Vehicle(vehicle_name=form.vehicle_name.data, vehicle_type=form.vehicle_type.data,
                              vehicle_plate=form.vehicle_plate.data, owner_id=current_user.id)
        db.session.add(new_vehicle)
        db.session.commit()
        return redirect(url_for('vehicles'))

    return render_template("vehicle_details.html", form=form, user_logged_in=current_user.is_authenticated)

@parking_system.route("/edit-profile", methods=['GET', 'POST'])
@login_required
def edit_prof():
    form = ProfileForm()
    if form.validate_on_submit():
        usr_rec = User.query.get_or_404(current_user.id)
        usr_rec.flat_no = form.flat_no.data
        usr_rec.phn_no = form.phn_no.data
        usr_rec.aadhar_no = form.aadhar_no.data
        db.session.commit()
        return redirect(url_for('profile'))

    return render_template("edit_prof.html", form=form, user_logged_in=current_user.is_authenticated)

if __name__ == '__main__':
    with parking_system.app_context():
        db.create_all()
        parking_system.run(debug=True)
