import sqlite3
import datetime
import os
from datetime import datetime
from flask import Flask, render_template, redirect, request, send_file
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape

app = Flask(__name__)

# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:////{os.getcwd()}/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creating an SQLAlchemy instance
db = SQLAlchemy(app)

# Define the model representing the 'deals' table
class deal_table(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    place = db.Column(db.Text, nullable=False)
    category = db.Column(db.Text, nullable=False)
    dates = db.Column(db.Text, nullable=False)
    start_time = db.Column(db.Text)
    end_time = db.Column(db.Text)
    title = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text)
    last_verified = db.Column(db.Text)

@app.route("/", methods=['GET', 'POST'])
def index():
    db.create_all()
    deals = deal_table.query.all()
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

    # used for places filter on sidebar
    for deal in deals:
        if deal.dates not in days:
            days.append(deal.dates)

        if deal.place not in places:
            places.append(deal.place)

    # makes days appear in chronological order
    days.sort(key=lambda date: weekday_order[date.split(',')[0]])

    filtered_categories = request.form.get('category')

    filtered_days = request.form.get('days')

    filtered_places = request.form.get('places')


    # conn.execute('SELECT * FROM deals WHERE category = ? AND dates = ? AND place = ?', (filtered_categories, filtered_days, filtered_places))

    return render_template('index.html', deals=deals, days=days, places=places)


@app.route("/form")
def form():
    return redirect("https://docs.google.com/forms/d/e/1FAIpQLScTx580IQvS-rVmIdm3eev65QMcF91zMtd68pJSx3DSutXFJg/viewform?usp=sf_link")

@app.route('/manifest.json')
def serve_manifest():
    return send_file('manifest.json', mimetype='application/manifest+json')

@app.route('/sw.js')
def serve_sw():
    return send_file('sw.js', mimetype='application/javascript')

if __name__ == '__main__': 
   app.run()