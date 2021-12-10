from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired,Length
from flask_ckeditor import CKEditorField

##WTForm
class BookingForm(FlaskForm):
    name = StringField("Name:", validators=[DataRequired()])
    nopsngr = StringField("No of Passenger:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired()])
    phonenum = IntegerField("Phone Number:", validators=[DataRequired()])
    fplace = StringField("From Place:", validators=[DataRequired()])
    tplace = StringField("To Place:", validators=[DataRequired()])
    time = StringField("Time:", validators=[DataRequired()])
    date = StringField("Date:", validators=[DataRequired()])
    submit = SubmitField("Submit ")

class PaymentForm(FlaskForm):
    cvv = PasswordField("cvv:", validators=[DataRequired()])
    card_num = IntegerField("Card Number:", validators=[DataRequired()])
    submit = SubmitField('Pay')

class CancelForm(FlaskForm):
    name = StringField("Name:", validators=[DataRequired()])
    travel_id = StringField("Travel Id:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired()])
    phonenum = IntegerField("Phone Number:", validators=[DataRequired()])
    submit = SubmitField("Cancel Booking")


class RegisterForm(FlaskForm):
    email = StringField("Email:", validators=[DataRequired()])
    password = PasswordField("Password:", validators=[DataRequired(), Length(min=8, message="Minimum 8 Characters")])
    name = StringField("Name:", validators=[DataRequired()])
    card_num = IntegerField("Card Number:", validators=[DataRequired()])
    cvv = PasswordField("Cvv:", validators=[DataRequired()])
    exp_date = StringField("Expiry Date:", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")

class LoginForm(FlaskForm):
    email = StringField("Email:", validators=[DataRequired()])
    password = PasswordField("Password:", validators=[DataRequired(), Length(min=8, message="Minimum 8 Characters")])
    submit = SubmitField("Log Me In!")

class CommentForm(FlaskForm):
    comment = CKEditorField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit Comment')
