from flask import render_template, flash, redirect, request, url_for, session, flash
from car_repair_shop_project import app, db, login_manager, bcrypt
from car_repair_shop_project.models import (User, Car, Repairs,  RegisterForm, LoginForm, CarForm, EditCarForm,
                                            EditProfileForm, EditNameForm, EditPhoneForm, BookAppointmentForm, RepairForm)

from datetime import date, datetime, timedelta

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import query


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    form = BookAppointmentForm()
    services = Repairs.query.all()
    service_choices = [(repair.id, f"{repair.service} - ${repair.price}") for repair in services]
    form.service.choices = service_choices
    if form.validate_on_submit():
        selected_service_id = form.service.data
        selected_service = Repairs.query.get(selected_service_id)
        entrydate = form.entrydate.data
        flash(f'Appointment booked for {entrydate.strftime("%Y-%m-%d %H")}, with service {selected_service.service} at ${selected_service.price}', 'success')
        return redirect(url_for('appointment'))
    return render_template('appointment.html', form=form)










@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        name = form.name.data
        phone = form.phone.data
        user = User.query.filter_by(email=email).first()
        if user:
            flash('User with this email already exists', 'danger')
            return render_template('register.html', form=form)
        if password != confirm_password:
            flash('Confirm password, didn\'t match password!', 'danger')
            return render_template('register.html', form=form)
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(email=email, password=hashed_password, name=name, phone=phone)
        db.session.add(new_user)
        db.session.commit()
        flash('You have successfully registered! Login now', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')
            return render_template('login.html', form=form)
    return render_template('login.html', form=form, user=current_user)


@app.route('/profile')
@login_required
def profile():
    user = current_user
    cars = Car.query.filter_by(user_id=user.id).all()
    for car in cars:
        total_price = sum(service.price for service in car.repairs)
        car.total_price = total_price
    return render_template("profile.html", user=user, cars=cars)


@app.route('/edit_profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_profile(user_id):
    user = User.query.get_or_404(user_id)
    form = EditProfileForm(obj=user)
    if form.validate_on_submit():
        user.password = form.password.data
        user.confirm_password = form.confirm_password.data
        user.name = form.name.data
        user.phone = form.phone.data
        db.session.commit()
        flash('You have successfully updated your information!', 'success')
        return redirect(url_for('profile'))
    return render_template('edit_profile.html', form=form, user=user)

@app.route('/edit_name/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_name(user_id):
    user = User.query.get_or_404(user_id)
    form = EditNameForm(obj=user)
    if form.validate_on_submit():
        print("Form data:", form.data)  # Debugging line
        user.name = form.name.data
        db.session.commit()
        flash('You have successfully updated your name!', 'success')
        return redirect(url_for('profile'))
    return render_template('edit_name.html', form=form, user=user)

@app.route('/edit_phone/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_phone(user_id):
    user = User.query.get_or_404(user_id)
    form = EditPhoneForm(obj=user)
    if form.validate_on_submit():
        print("Form data:", form.data)  # Debugging line
        user.phone = form.phone.data
        db.session.commit()
        flash('You have successfully updated your phone!', 'success')
        return redirect(url_for('profile'))
    return render_template('edit_phone.html', form=form, user=user)


@app.route('/car')
@login_required
def car():
    return render_template('car.html')

def get_year_choices():
    current_year = datetime.now().year
    return [(year, str(year)) for year in range(current_year, current_year - 100, -1)]


@app.route('/add_car', methods=['GET', 'POST'])
@login_required
def add_car():
    form = CarForm()
    form.year.choices = get_year_choices()
    if form.validate_on_submit():
        plate = form.plate.data
        make = form.make.data
        model = form.model.data
        year = form.year.data
        problem = form.problem.data
        check_car = Car.query.filter_by(plate=plate).first()
        if check_car:
            flash('Car with this plates already exists', 'danger')
            return render_template('add_car.html', form=form)
        new_car = Car(plate=plate, make=make, model=model, year=year, problem=problem, user_id=current_user.id)
        db.session.add(new_car)
        db.session.commit()
        flash('You have successfully added new car!', 'success')
        return redirect(url_for('profile'))
    return render_template('add_car.html', form=form)


@app.route('/edit_issue/<int:car_id>', methods=['GET', 'POST'])
@login_required
def edit_issue(car_id):
    car = Car.query.get_or_404(car_id)
    form = EditCarForm(obj=car)
    if form.validate_on_submit():
        car.problem = form.problem.data
        db.session.commit()
        flash('You have successfully updated your car\'s issue!', 'success')
        return redirect(url_for('profile'))
    return render_template('edit_issue.html', form=form, car=car)


@app.route('/delete_car/<int:car_id>', methods=['GET', 'POST'])
@login_required
def delete_car(car_id):
    if current_user:
        car = Car.query.get_or_404(car_id)
        db.session.delete(car)
        db.session.commit()
        flash('You have successfully deleted your car!', 'success')
        return redirect(url_for('profile'))
    return render_template('logout.html')


# for admin to fill service collection
@app.route('/add_service', methods=['POST'])
def add_service_to_db():
    if request.method == 'POST':
        service = request.form.get('service')
        price = request.form.get('price')
        desc = request.form.get('desc')
        new_service = Repairs(
            service=service,
            price=float(price),
            desc=desc,
        )
        db.session.add(new_service)
        db.session.commit()
        return redirect(url_for('profile'))


@app.route('/services', methods=['GET'])
def services():
    disp_services = Repairs.query.all()
    print("test print")
    print(disp_services)
    return render_template("services.html", disp_services=disp_services)


@app.route('/view_service/<int:repair_id>', methods=['GET'])
@login_required
def view_service(repair_id):
    user = current_user
    repair = Repairs.query.filter_by(user_id=user.id, id=repair_id).first_or_404()
    car_for_service = Car.query.filter_by(id=repair.car_id, user_id=user.id).first_or_404()

    return render_template("profile.html", user=user, car=car_for_service, service=repair)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

