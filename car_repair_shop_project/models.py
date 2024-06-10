from car_repair_shop_project import db, app
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, EmailField, SubmitField, TextAreaField, SelectField, FloatField
from wtforms.validators import DataRequired, EqualTo, Length, Email
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from wtforms.fields import DateField, DateTimeField
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    car = db.relationship('Car', back_populates='user', uselist=False)
    repairs = db.relationship('Repairs', back_populates='user', uselist=False)


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String(20), unique=True, nullable=False)
    make = db.Column(db.String(60), nullable=False)
    model = db.Column(db.String(60), nullable=False)
    problem = db.Column(db.String(1000), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='car')
    repairs = db.relationship('Repairs', back_populates='car')


class Repairs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)
    desc = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'))
    user = db.relationship('User', back_populates='repairs')
    car = db.relationship('Car', back_populates='repairs')



class RegisterForm(FlaskForm):
    email = EmailField('Email: ', validators=[DataRequired(), Email()])
    password = PasswordField('Password: ', validators=[DataRequired(), Length(min=3, max=128)])
    confirm_password = PasswordField('Confirm Password: ', validators=[DataRequired()])
    name = StringField("Name: ", validators=[Length(min=1, max=120)])
    phone = StringField("Phone: ", validators=[Length(min=4, max=20)])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = EmailField("Email: ", validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class CarForm(FlaskForm):
    plate = StringField("Plate: ", validators=[DataRequired(), Length(min=1, max=20)])
    make = StringField("Make: ", validators=[DataRequired(), Length(min=1, max=60)])
    model = StringField("Model: ", validators=[DataRequired(), Length(min=1, max=60)])
    year = SelectField("Year: ", coerce=int, validators=[DataRequired()])
    problem = TextAreaField("Problem Description: ", validators=[DataRequired(), Length(max=1000)],
                            render_kw={"rows": 8, "cols": 50})
    submit = SubmitField('Add')


class RepairForm(FlaskForm):
    service = StringField("Service: ", validators=[DataRequired(), Length(min=1, max=20)])
    price = IntegerField("Price: ", validators=[DataRequired()])
    desc = StringField("Description: ", validators=[Length(min=1, max=60)])
    year = SelectField("Year: ", coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add')


class EditCarForm(FlaskForm):
    problem = TextAreaField("Problem Description: ", validators=[DataRequired(), Length(max=1000)],
                            render_kw={"rows": 8, "cols": 50})
    submit = SubmitField('Update')


class EditProfileForm(FlaskForm):
    password = PasswordField('Password: ', validators=[DataRequired(), Length(min=3, max=128)])
    confirm_password = PasswordField('Confirm Password: ', validators=[DataRequired()])
    name = StringField("Name: ", validators=[Length(min=1, max=120)])
    phone = StringField("Phone: ", validators=[Length(min=4, max=20)])
    submit = SubmitField('Update')


class EditNameForm(FlaskForm):
    name = StringField("Name: ", validators=[Length(min=1, max=120)])
    submit = SubmitField('Update')


class EditPhoneForm(FlaskForm):
    phone = StringField("Phone: ", validators=[Length(min=4, max=20)])
    submit = SubmitField('Update')


class BookAppointmentForm(FlaskForm):
    service = SelectField('Service', coerce=int, validators=[DataRequired()])
    price = IntegerField("Price: ", validators=[DataRequired()])
    entrydate = DateTimeField('Select Date and Time', format='%Y-%m-%dT%H', validators=[DataRequired()],
                              render_kw={"type": "datetime-local", "step": "900"})
    submit = SubmitField('Book')


# admin doesn't work

# class AdminModelView(ModelView):
#     def is_accessible(self):
#         return current_user.is_authenticated and current_user.username == "admin"


# admin = Admin(app)
# admin.add_view(ModelView(User, db.session))
# admin.add_view(AdminModelView(User, db.session))

