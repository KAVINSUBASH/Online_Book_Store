from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'firsttime'

mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['data']

def create_table():
    pass

def validate_login(username, password):
    user = db.login.find_one({'Email': username, 'password': password})
    return bool(user)
def register_user(username, password):
    db.login.insert_one({'Email': username, 'password': password})
    return redirect(url_for('index'))
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/loginpage', methods=['GET', 'POST'])
def loginpage():
    if request.method == 'POST':
        action = request.form['action']
        if action == 'login':
            username = request.form['uname']
            password = request.form['psw']
            if validate_login(username, password):
                return redirect(url_for('home'))
            else:
                session['message'] = 'Invalid login credentials. Please try again.'
                print(f"Session message set: {session['message']}") 
                return redirect(url_for('loginpage'))
        elif action == 'signup':
            return redirect(url_for('register'))
    message = session.get('message', '')
    print(f"Session message set: {session['message']}")
    print(f"Session message retrieved: {message}")
    return render_template('index.html',message=message)
@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        action = request.form['action']
        if action == 'signup':
            username = request.form['email']
            password = request.form['password']
            if register_user(username, password):
                return redirect(url_for('index'))
        elif action == 'login':
            return redirect(url_for('index'))
    return render_template('register.html')
@app.route('/scific', methods=['GET', 'POST'])
def scific():
    return render_template('scific.html')
@app.route('/shortstories', methods=['GET', 'POST'])
def shortstories():
    return render_template('shortstories.html')
@app.route('/cart', methods=['GET', 'POST'])
def cart():
    return render_template('cart.html')
@app.route('/payment', methods=['GET', 'POST'])
def payment():
    return render_template('payment.html')
if __name__ == '__main__':
    create_table()
    app.run(debug=True)