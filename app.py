from flask import Flask, render_template, request, redirect, url_for, session
import pickle
import pandas as pd

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'your_secret_key'  # Change this to a secure random key in production

# Dummy username and password for demonstration purposes
correct_username = 'admin'
correct_password = 'password'

# Dictionary to store user information
users = {'admin': 'password'}

# Load the machine learning model
pipe = pickle.load(open('ipl prediction\pipe.pkl', 'rb'))

# List of IPL teams and cities
teams = ['Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore', 'Kolkata Knight Riders', 'Kings XI Punjab', 'Chennai Super Kings', 'Rajasthan Royals', 'Delhi Capitals']

cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi', 'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth', 'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley', 'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala', 'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi', 'Sharjah', 'Mohali', 'Bengaluru']

@app.route('/')
def home():
         if 'username' in session:
          return render_template('index.html', teams=teams, cities=cities)
         else:
          return redirect(url_for('login'))
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username 
        password = request.form['password']
        return redirect(url_for('home'))
    else:
        if 'username' in session:
          return redirect(url_for('home'))
        
        return render_template('login.html')

     

@app.route('/username')
def username():
    if "username" in session:
        username= session["username"]
        return f"<h1>{home}</h1> "
    else:
        return redirect(url_for('login'))    


@app.route('/signup', methods=['GET', 'POST'])
def signup():
     if request.method == 'POST':
        username = request.form['username']
        session['username'] = username 
        password = request.form['password']
    
        return redirect(url_for(''))
     else:   
        if 'username' in session:
          return redirect(url_for('login'))
         
        return render_template('signup.html')

@app.route('/username')
def usernames():
    if "username" in session:
        username= session["username"]
        return f"<h1>{login}</h1> "
    else:
        return redirect(url_for('signup'))  

@app.route('/predict', methods=['POST'])
def predict():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    # Retrieve form data and perform prediction
    batting_team = request.form['batting_team']
    bowling_team = request.form['bowling_team']
    city = request.form['selected_city']  # Update to match the expected column name
    target = int(request.form['target'])
    score = int(request.form['score'])
    overs = int(request.form['overs'])
    wickets = int(request.form['wickets'])
    crr = float(request.form['crr'])
    runs_left = int(request.form['runs_left'])
    rrr = float(request.form['rrr'])
    total_runs_x = int(request.form['total_runs_x'])
    balls_left = int(request.form['balls_left'])

    # Create a DataFrame with the input data
    input_data = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'city': [city],  # Update to match the expected column name
        'target': [target],
        'score': [score],
        'overs': [overs],
        'wickets': [wickets],
        'crr': [crr],
        'runs_left': [runs_left],
        'rrr': [rrr],
        'total_runs_x': [total_runs_x],
        'balls_left': [balls_left],
    })

    # Use the machine learning model to make predictions
    win_probability = pipe.predict_proba(input_data)[:, 1] * 100  # Assuming the second column is the probability of winning
    loss_probability = 100 - win_probability

    return render_template('result.html', batting_team=batting_team, win_probability=win_probability[0], bowling_team=bowling_team, loss_probability=loss_probability[0])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)