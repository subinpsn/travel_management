import sys

from flask import Flask, render_template, redirect, url_for, flash, abort
from functools import wraps
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import BookingForm, RegisterForm, LoginForm, CommentForm, CancelForm, PaymentForm
from flask_gravatar import Gravatar
from district import dist_details

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
bootstrap = Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

# gravatar = Gravatar(app, size=100, rating='g', default='retro', force_default=False, force_lower=False, use_ssl=False, base_url=None)


##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel_management.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_booking_details.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CONFIGURE TABLES

# creating table for Users
class Users(UserMixin, db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    card_num = db.Column(db.String(250), nullable=False)
    cvv = db.Column(db.String(250), nullable=False)
    expiry = db.Column(db.String(250), nullable=False)

    # Relating User with their own booking details
    Booking = relationship("User_Booking_Details", back_populates='name_of_booker')

# db.create_all()

# Creating table for booking
class User_Booking_Details(db.Model):
    __tablename__ = "user_booking_details"
    id = db.Column(db.Integer, primary_key=True)

    # Creating Foreign Key , "Users.id" the users refers to tablename of User
    booking_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

    # Creating reference to  User obj , the "Booking" refers to booking property in the user class
    name_of_booker = relationship('Users', back_populates='Booking')

    name = db.Column(db.String(250), nullable=False)
    no_of_psngr = db.Column(db.String(250), nullable=False)
    Email = db.Column(db.String(250), nullable=False)
    ph_no = db.Column(db.String(250), nullable=False)
    From = db.Column(db.String(250), nullable=False)
    To = db.Column(db.String(250), nullable=False)
    Date = db.Column(db.String(250), nullable=False)
    Time = db.Column(db.String(250), nullable=False)

# db.create_all()

#Create admin-only decorator
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.id != 1:
            print(current_user.id)
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/register', methods =['GET', 'POST'])
def register():
    register_form = RegisterForm()

    if register_form.validate_on_submit():

        if Users.query.filter_by(email=register_form.email.data).first():
            flash("You've already signed in with the email, login instead!")
            return redirect(url_for('login'))

        # hashing and salting password
        hashed_password = generate_password_hash(
            register_form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        # creating new_user entry in Users table
        new_user = Users(
            name=register_form.name.data,
            email=register_form.email.data,
            password=hashed_password,
            cvv=register_form.cvv.data,
            card_num=register_form.card_num.data,
            expiry=register_form.exp_date.data
        )
        db.session.add(new_user)
        db.session.commit()

        # Log in and authenticate user after adding details to database.
        login_user(new_user)
        print(current_user.id)
        return redirect(url_for('home'))

    return render_template("register.html", form=register_form, current_user=current_user)


@app.route('/login', methods=['GET','POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data

        # find user by email
        user_need_to_login = Users.query.filter_by(email=email).first()
        print(user_need_to_login)

        # if user is not exist then show a message
        if not user_need_to_login:
            flash('That email does not exist. please try again')
            return redirect(url_for('login'))

        # check stored password hash against entered password hashed
        elif not check_password_hash(pwhash=user_need_to_login.password, password=password):
            flash('Password incorrect,please try again')
            return redirect(url_for('login'))

        # if every thing is false then the user need to be loged in
        else:
            login_user(user_need_to_login)
            return redirect(url_for('home', current_user=current_user))

    return render_template("login.html", form=login_form, current_user=current_user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/forget_password')
def forget_password():
    return render_template("forget_password.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/booking',methods=['GET','POST'])
@login_required
def booking():
    booking_form = BookingForm()
    if booking_form.validate_on_submit():
        new_booking = User_Booking_Details(
            name=booking_form.name.data,
            no_of_psngr=booking_form.nopsngr.data,
            Email=booking_form.email.data,
            ph_no=booking_form.phonenum.data,
            From=booking_form.fplace.data,
            To=booking_form.tplace.data,
            Date=booking_form.date.data,
            Time=booking_form.time.data,
      )
        db.session.add(new_booking)
        db.session.commit()

        if Users.query.filter_by(email=booking_form.email.data).first():
            return redirect(url_for('payment'))

    return render_template("booking_form.html", form=booking_form)


@app.route('/payment',methods=['GET', 'POST'])
def payment():
    payment_form = PaymentForm()

    def get_dest():
        user_details = load_user(current_user.id)
        booking_details = User_Booking_Details.query.filter_by(Email=user_details.email).all()
        current_booking = booking_details[len(booking_details)-1]
        return current_booking.To


    def get_orgin():
        user_details = load_user(current_user.id)
        booking_details = User_Booking_Details.query.filter_by(Email=user_details.email).all()
        current_booking = booking_details[len(booking_details)-1]
        return current_booking.From

    org = get_orgin()
    dest = get_dest()

    dict_name = dist_details
    vehicle = "bus"

    # To chose charge
    charges = {"car": 6, "bus": 4, "train": 2}

    def get_charge(veh):
        for key, value in charges.items():
            if key == veh:
                return value

    # To get distance
    def get_distance(origin, destination):
        for dict in dist_details:
            if dict['From'] == origin and dict['To'] == destination:
                return dict['Distance']

    # calculate amount
    amt = get_charge(vehicle) * get_distance(org, dest)
    if payment_form.validate_on_submit():
        user_card_num = int(load_user(current_user.id).card_num)

        if user_card_num == payment_form.card_num.data:
            msg = "payment successfull!!"
            return receipt(message=msg)
        else:
            msg = "invalid card number"
            return receipt(message=msg)

    return render_template("payment.html", form=payment_form, amount=amt)

@app.route('/receipt')
def receipt(message):
    return render_template("receipt.html", message=message)


@app.route('/Booking_details')
def conform_booking():
    user_details = load_user(current_user.id)
    booking_details = User_Booking_Details.query.filter_by(Email=user_details.email).all()
    current_booking = booking_details[len(booking_details)-1]
    name = current_booking.name
    email = current_booking.Email
    ph_no = current_booking.ph_no
    passenger = current_booking.no_of_psngr
    origin = current_booking.From
    dest = current_booking.To
    time = current_booking.Time
    date = current_booking.Date

    return render_template("confirm.html", Name=name, Email=email, Phone_num=ph_no, Pssg=passenger,
                           Origin=origin, Destination=dest, Time=time, Date=date)


@app.route('/cancel_booking')
def booking_cancelation():
    cancel_form = CancelForm()
    return render_template("cancelation.html", form=cancel_form)



if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)

