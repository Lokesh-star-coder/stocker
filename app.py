from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Change this to a secure secret key

# In-memory data structures
users = []
bookings = []
booking_counter = 1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'success',
        'message': 'Book Exchange API is running'
    })

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Find user in users list
        user = next((u for u in users if u['email'] == email), None)
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['name'] = user['name']
            print(f"User logged in: {user['name']} ({email})")
            return redirect(url_for('home1'))
        else:
            flash('Invalid email or password')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if email already exists
        if any(u['email'] == email for u in users):
            flash('Email already registered')
            return redirect(url_for('signup'))

        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('signup'))

        # Create new user
        new_user = {
            'id': len(users) + 1,
            'name': name,
            'email': email,
            'password': generate_password_hash(password)
        }
        users.append(new_user)
        print(f"New user registered: {name} ({email})")
        print(f"Current users: {users}")
        
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/home1')
def home1():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Get user's bookings
    user_bookings = [b for b in bookings if b['user_id'] == session['user_id']]
    return render_template('home1.html', name=session['name'], bookings=user_bookings)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

@app.route('/b1')
def booking_form():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    movie = request.args.get('movie')
    return render_template('b1.html', movie=movie)

@app.route('/tickets', methods=['POST'])
def book_tickets():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    movie = request.form['movie']
    seats = int(request.form['seats'])
    date = request.form['date']
    time = request.form['time']
    
    # Create new booking
    new_booking = {
        'id': booking_counter,
        'user_id': session['user_id'],
        'movie': movie,
        'seats': seats,
        'date': date,
        'time': time,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    bookings.append(new_booking)
    booking_counter += 1
    
    print(f"New booking created: {new_booking}")
    print(f"Current bookings: {bookings}")
    
    return render_template('tickets.html', booking=new_booking)

@app.route('/tickets')
def tickets():
    return render_template('tickets.html')

if __name__ == '__main__':
    app.run(debug=True)
