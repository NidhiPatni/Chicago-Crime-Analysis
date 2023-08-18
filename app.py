"""
Name: Nidhi Jitendra Patni
Date: 17-July-2023
Course Number: ITMD 513
Final Project: Chicago Crime Analysis
"""

# Importing necessary libraries
from flask import Flask, render_template, request, redirect, session, url_for
import module
import sqlite3
import time

app = Flask(__name__)
app.secret_key = 'secret_key'

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS users (User_ID INTEGER PRIMARY KEY NOT NULL,username TEXT,password TEXT)")
        conn.commit()
        conn.close()

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()

        return redirect('/login')
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT username,password FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchall()

        for i in user:
            if username == i[0] and password == i[1]:
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('dashboard'))

        return redirect('/login?error=true')
    else:
        return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        home_latitude = request.form.get('home_latitude')
        home_longitude = request.form.get('home_longitude')
        destination_latitude = request.form.get('destination_latitude')
        destination_longitude = request.form.get('destination_longitude')
        year = request.form.get('year')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        chart_type = request.form.get('chart_type')
        column_name = request.form.get('column_name')

        session['chart_type_session']=request.form.get('chart_type')
        session['column_name_session'] = request.form.get('column_name')

        module.createURL(chart_type, column_name, year, start_date, end_date, home_latitude,
                        home_longitude, destination_latitude, destination_longitude)

        return redirect(url_for('chart'))
    else:
        return render_template('dashboard.html')

@app.route('/chart')
def chart():
    chart_type_session = session.get('chart_type_session')
    column_name_session = session.get('column_name_session')

    if chart_type_session == 'barChart':
        chart_type_name = 'Bar Chart For'
    elif chart_type_session == 'sideBySideBarChart':
        chart_type_name = 'Side by Side Bar Chart For Arrest and '
    elif chart_type_session == 'lineChart':
        chart_type_name = 'Line Chart For'
    elif chart_type_session == 'scatterPlot':
        chart_type_name = 'Scatter Plot For Latitude and Longitude categorized by '
    elif chart_type_session == 'pieChart':
        chart_type_name = 'Pie Chart For'
    elif chart_type_session == 'heatMap':
        chart_type_name = 'Correlation Heat Map'
    elif chart_type_session == 'statistics':
        chart_type_name = 'Statistics'
    else:
        chart_type_name = 'Chart Type not selected'

    if column_name_session == 'primary_type' and chart_type_session != 'heatMap' and chart_type_session != 'statistics':
        column_name_name = 'Primary type vs Number of Incidents'
    elif column_name_session == 'arrest' and chart_type_session != 'heatMap' and chart_type_session != 'statistics':
        column_name_name = 'Arrest vs Number of Incidents'
    elif column_name_session == 'block' and chart_type_session != 'heatMap' and chart_type_session != 'statistics':
        column_name_name = 'Block vs Number of Incidents'
    elif column_name_session == 'location_description' and chart_type_session != 'heatMap' and chart_type_session != 'statistics':
        column_name_name = 'Location Description vs Number of Incidents'
    elif column_name_session == 'Month' and chart_type_session != 'heatMap' and chart_type_session != 'statistics':
        column_name_name = 'Month vs Number of Incidents'
    elif column_name_session == 'Day' and chart_type_session != 'heatMap' and chart_type_session != 'statistics':
        column_name_name = 'Day vs Number of Incidents'
    elif column_name_session == 'latitude' and chart_type_session != 'heatMap' and chart_type_session != 'statistics':
        column_name_name = 'Latitude vs Number of Incidents'
    elif column_name_session == 'longitude' and chart_type_session != 'heatMap' and chart_type_session != 'statistics':
        column_name_name = 'Longitude vs Number of Incidents'
    elif column_name_session != '' and chart_type_session == 'heatMap':
        column_name_name = ''
    elif column_name_session != '' and chart_type_session == 'statistics':
        column_name_name = ''
    else:
        column_name_name = 'Please select correct column name'

    timestamp = int(time.time())
    return render_template('chart.html', timestamp=timestamp,chart_type_name=chart_type_name,column_name_name=column_name_name)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
