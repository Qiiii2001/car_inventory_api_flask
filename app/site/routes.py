from flask import Blueprint, render_template, flash
from models import db, Car, car_schema, cars_schema
from forms import CarForm
from flask import request, jsonify, redirect, url_for

site = Blueprint('site',__name__,template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
def profile():
    return render_template('profile.html')

@site.route('/contact')
def contact():
    return render_template('contact.html')



@site.route('/car', methods=['POST'])
def create_car():
    # create a new car instance
    form = CarForm(request.form)
    if form.validate_on_submit():
        new_car = Car(
            make=form.make.data,
            model=form.model.data,
            year=form.year.data
        )
        db.session.add(new_car)
        db.session.commit()
        # For API
        # return car_schema.jsonify(new_car)
        
        return redirect(url_for('site.get_cars'))

@site.route('/cars', methods=['GET'])
def get_cars():
    # retrieve all cars
    cars = Car.query.all()
    
    return render_template('car_list.html', cars=cars)
    
@site.route('/add_car', methods=['GET', 'POST'])
def add_car():
    form = CarForm()
    if form.validate_on_submit():
        new_car = Car(make=form.make.data, model=form.model.data, year=form.year.data)
        db.session.add(new_car)
        db.session.commit()
        return redirect(url_for('site.get_cars'))
    return render_template('car_form.html', form=form)



@site.route('/car/<string:id>', methods=['GET'])
def get_car(id):
    # retrieve a single car
    car = Car.query.get_or_404(id)
    return render_template('car_detail.html', car=car)
    
    
@site.route('/update_car/<string:id>', methods=['GET', 'POST'])
def update_car(id):
    car = Car.query.get_or_404(id)
    if request.method == 'POST':
        form = CarForm(request.form)
        if form.validate_on_submit():
            car.make = form.make.data
            car.model = form.model.data
            car.year = form.year.data
            db.session.commit()
            flash('Car updated successfully!', 'success')
            return redirect(url_for('site.get_cars'))
        else:
            # If form did not validate, show form again with errors
            flash('Error updating the car.', 'danger')
            return render_template('car_form.html', form=form, car=car)
    # If a GET request, show existing car data in form
    form = CarForm(obj=car)
    return render_template('car_form.html', form=form, car=car)

@site.route('/delete_car/<string:id>', methods=['POST'])
def delete_car(id):
    car = Car.query.get_or_404(id)
    db.session.delete(car)
    db.session.commit()
    flash('Car deleted successfully!', 'success')
    return redirect(url_for('site.get_cars'))

@site.route('/search')
def search():
    query = request.args.get('query')
    if query:
        # Search by 'make' and 'model' fields 
        results = Car.query.filter(
            (Car.make.ilike('%' + query + '%')) | 
            (Car.model.ilike('%' + query + '%'))
        ).all()
    else:
        results = []
    return render_template('search_results.html', query=query, results=results)

@site.route('/contact_submit', methods=['POST'])
def contact_submit():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    
    flash('Thank you for your message, we will get back to you shortly.')
    
    return redirect(url_for('site.home'))