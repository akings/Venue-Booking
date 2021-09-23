from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_bcrypt import check_password_hash, generate_password_hash
from databases import Users
from databases import Booking


app = Flask(__name__)
app.secret_key = "akkkjddkshbjhyu"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form["x"]
        password = request.form["y"]

        try:
            user = Users.get(Users.email == email)
            hashed_password = user.password
            if check_password_hash(hashed_password, password):
                flash("Login Successful")
                session["name"] = user.name
                session["email"] = user.email
                session["id"] = user.id
                session["logged_in"] = True
                if email == "admin@gmail.com" and password == "1234":
                    return redirect(url_for("admin_home"))
                else:
                    return redirect(url_for("client_home"))
        except Users.DoesNotExist:
            flash("Wrong username or password")
    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        name = request.form["x"]
        email = request.form["y"]
        password = request.form["z"]
        password = generate_password_hash(password)
        try:
            Users.create(name=name, email=email, password=password)
            flash("Account created successfully")
        except Exception:
            flash("That email is already used")
    return render_template('register.html')

@app.route('/logout')
def logout():
    if not session.get("logged_in"):
        return redirect(url_for("index"))
    session.pop("logged_in", None)
    return redirect(url_for("index"))

@app.route('/admin')
def admin_home():
    if not session.get("logged_in"):
        return redirect(url_for("index"))
    return render_template("admin.html")

@app.route('/client')
def client_home():
    if not session.get("logged_in"):
        return redirect(url_for("index"))
    return render_template("clients.html")

@app.route('/view_users')
def admin():
    users = Users.select()
    return render_template("admin.html", users=users)

@app.route('/delete_users/<int:id>')
def delete_users(id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    Users.delete().where(Users.id == id).execute()
    return redirect(url_for("admin"))

@app.route('/update_user/<int:id>', methods=['GET','POST'])
def update_user(id):
    user = Users.get(Users.id == id)
    if request.method == 'POST':
        updated_name = request.form["x"]
        updated_email = request.form["y"]
        updated_password = request.form["z"]
        hashed_password = generate_password_hash(updated_password)
        user.name = updated_name
        user.email = updated_email
        user.password = hashed_password
        user.save()
        flash("User Updated Successfully")
        return redirect(url_for("admin"))
    return render_template("update_User.html", user = user)



@app.route('/update_profile/<int:id>', methods=['GET','POST'])
def update_profile(id):
    user = Users.get(Users.id == id)
    if request.method == 'POST':
        updated_name = request.form["x"]
        updated_email = request.form["y"]
        updated_password = request.form["z"]
        hashed_password = generate_password_hash(updated_password)
        user.name = updated_name
        user.email = updated_email
        user.password = hashed_password
        user.save()
        flash("User Updated Successfully")
        return redirect(url_for("client_home"))
    return render_template("update_Profile.html", user = user)

@app.route('/profile')
def clients():
    user = Users.select()
    return render_template("clients.html", user=user)

@app.route('/add_users', methods=['GET', 'POST'])
def add_users():
    if request.method == "POST":
        name = request.form["x"]
        email = request.form["y"]
        password = request.form["z"]
        password = generate_password_hash(password)
        try:
            Users.create(name=name, email=email, password=password)
            flash("User Added successfully")
        except Exception:
            flash("User product Failed")
    return render_template('add_user.html')

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == "POST":
        name = request.form["n"]
        nationality = request.form["ny"]
        current_residence = request.form["cr"]
        county = request.form["c"]
        constituency = request.form["cy"]
        address = request.form["add"]
        phone_no = request.form["pn"]
        email = request.form["e"]
        service_needed = request.form["sn"]
        venue = request.form["v"]
        date = request.form["d"]
        time = request.form["t"]
        capacity = request.form["cap"]
        description = request.form["dn"]
        try:
            Booking.create(name=name, nationality=nationality, current_residence=current_residence, county=county,
                           constituency=constituency, address=address, phone_no=phone_no, email=email, service_needed=service_needed,
                            venue=venue, date=date, time=time, capacity=capacity, description=description)
            flash("Booking successful")
        except Exception:
            flash("Error Booking")
    return render_template('book.html')



@app.route('/delete_request/<int:id>')
def delete_request(id):
    if not session.get("booked"):
        return redirect(url_for("bookings"))
    Booking.delete().where(id == Booking.id).execute()
    return redirect(url_for("admin"))

@app.route('/bookings')
def bookings():
    bookings = Booking.select()
    return render_template("admin.html", bookings=bookings)

@app.route('/booking_status')
def booking_status():
    bookings = Booking.select()
    return render_template("clients.html", bookings=bookings)

@app.route('/blog')
def blog():
    return render_template("blog.html")

@app.route('/blog_details')
def blog_details():
    return render_template("blog_details.html")

@app.route('/gallery')
def gallery():
    return render_template("gallery.html")

if __name__ == '__main__':
    app.run()
