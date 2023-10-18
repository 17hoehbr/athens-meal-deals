import os
from flask import Flask, render_template, redirect, request, send_file, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:////{os.getcwd()}/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# form
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
ADMIN_USERNAME =  os.getenv('ADMIN_USERNAME')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

# Creating an SQLAlchemy instance
db = SQLAlchemy(app)

# Define the model representing the 'deals' table
class deals(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    place = db.Column(db.Text, nullable=False)
    category = db.Column(db.Text, nullable=False)
    dates = db.Column(db.Text, nullable=False)
    start_time = db.Column(db.Text)
    end_time = db.Column(db.Text)
    title = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text)
    last_verified = db.Column(db.Text)

class pending_deals(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    place = db.Column(db.Text, nullable=False)
    category = db.Column(db.Text, nullable=False)
    dates = db.Column(db.Text, nullable=False)
    start_time = db.Column(db.Text)
    end_time = db.Column(db.Text)
    title = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text)
    last_verified = db.Column(db.Text)

# Create a decorator for authentication
def authenticate(username, password):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            auth = request.authorization
            if not auth or not (auth.username == username and auth.password == password):
                return 'Authentication required!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'}
            return func(*args, **kwargs)
        return wrapper
    return decorator

@app.route("/", methods=['GET', 'POST'])
def index():
    db.create_all()
    all_deals = deals.query.all()
    days = []
    places = []

    weekday_order = {
        'Daily': 0,
        'Monday': 1,
        'Tuesday': 2,
        'Wednesday': 3,
        'Thursday': 4,
        'Friday': 5,
        'Saturday': 6,
        'Sunday': 7
    }

    # Used for days and places filter on sidebar
    for deal in all_deals:
        d = deal.dates.split(',')
        for day in d:
            if day not in days:
                days.append(day)

            if deal.place not in places:
                places.append(deal.place)

    # Sort the remaining dates
    days.sort(key=lambda date: weekday_order[date.split(',')[0]])

    filtered_deals = all_deals  # Initialize with all deals

    if request.method == 'POST':
        # Get filter criteria from the form
        filtered_categories = request.form.getlist('category')
        filtered_days = request.form.getlist('days')
        filtered_places = request.form.getlist('places')

        # Filter the deals based on the selected criteria
        filtered_deals = [deal for deal in filtered_deals if
                          deal.category in filtered_categories and
                          deal.dates in filtered_days and
                          deal.place in filtered_places]
    else:
        # If it's a GET request, you can initialize the filter values here.
        filtered_categories = ['food', 'drink']  # Default values
        filtered_days = days  # All days selected by default
        filtered_places = places  # All places selected by default

    return render_template('index.html', deals=filtered_deals, days=days, places=places,
                           filtered_categories=filtered_categories, filtered_days=filtered_days,
                           filtered_places=filtered_places)


@app.route("/form", methods=('GET', 'POST'))
def form():
    all_deals = deals.query.all()
    places = []

    for deal in all_deals:
        if deal.place not in places:
            places.append(deal.place)

    if request.method == 'POST':
        # Check if the 'new_location' input field has a value
        new_location = request.form.get('new_location')
        
        if new_location:
            # If 'new_location' has a value, use it as the 'location' response
            location = new_location
        else:
            # If 'new_location' is empty, use the 'location' selected from the dropdown
            location = request.form.get('location')
        category = request.form['category']

        dlist = request.form.getlist('days[]')
        if len(dlist) == 6:
            days = 'Daily'
        else:
            days = ','.join(dlist)

        starttime = request.form['starttime']
        endtime = request.form['endtime']
        title = request.form['title']
        description = request.form['description']
        lastverified = request.form['last-verified']

        if not location:
            flash('Location is required!')
        else:
            response = pending_deals(
                place=location,
                category=category,
                dates=days,
                start_time=starttime,
                end_time=endtime,
                title=title,
                notes=description,
                last_verified=lastverified
            )

            db.session.add(response)
            db.session.commit()

            return redirect(url_for('index'))

    return render_template('form.html', places=places)


@app.route("/bryce", methods=('GET', 'POST'))
@authenticate(ADMIN_USERNAME, ADMIN_PASSWORD)
def admin():
    if request.method == 'POST':
        if 'approve' in request.form:
            rowid = request.form['approve']
            approved = pending_deals.query.filter_by(id=rowid).all()[0]
            new_row = deals(
                # later: make it automatically fetch the keys
                # for key in deals
                #   key = approved['key']?
                place = approved.place,
                category = approved.category,
                dates = approved.dates,
                start_time = approved.start_time,
                end_time = approved.end_time,
                title = approved.title,
                notes = approved.notes,
                last_verified = approved.last_verified
            )

            db.session.add(new_row)
            pending_deals.query.filter_by(id=rowid).delete()
            db.session.commit()
            return redirect('/bryce')
        elif 'edit' in request.form:
            pass
        elif 'delete' in request.form:
            table = request.form['table']
            rowid = request.form['delete']
            if table == 'pending_deals':
                pending_deals.query.filter_by(id=rowid).delete()
            elif table == 'deals':
                deals.query.filter_by(id=rowid).delete()

            db.session.commit()
            return redirect('/bryce')


    # Convert each row to a dictionary
    def row2dict(table):
        table_data = []
        for row in table:
            row_data = {}
            for column in pending_deals.__table__.columns:
                # Use column.name to access column names
                row_data[column.name] = getattr(row, column.name)
            table_data.append(row_data)
        return table_data

    pending_deals_data = row2dict(pending_deals.query.all())
    
    deals_data = row2dict(deals.query.all())

    col_names = pending_deals.__table__.columns.keys()

    return render_template('admin.html', col_names=col_names, pending_deals=pending_deals_data, deals=deals_data)


@app.route('/manifest.json')
def serve_manifest():
    return send_file('manifest.json', mimetype='application/manifest+json')

@app.route('/sw.js')
def serve_sw():
    return send_file('sw.js', mimetype='application/javascript')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=5007, host="0.0.0.0")