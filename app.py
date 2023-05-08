from flask import Flask, render_template, request, url_for, flash, redirect
import reservations as spot

app = Flask(__name__)
app.config["DEBUG"] = True

app.config['SECRET_KEY'] = 'your secret key'

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == "POST":
        choice = request.form['pages']
        if choice == '':
            flash("You have to choose an option. ")
        elif choice == "reservation":
            return redirect(url_for('reservations'))
        elif choice == "admin":
            return redirect(url_for('admin'))   
    return render_template('index.html')

def logadmin(loguser, logpassword):
    with open("passcodes.txt", "r") as f:
        user_list = [line.strip().split(", ") for line in f.readlines()]

    for user, password in user_list:
        if loguser == user and logpassword == password:
            f.close()
            return True

    f.close()
    return False

def get_cost_matrix():
    cost_matrix = [[100, 75, 50, 100] for row in range(12)]
    return cost_matrix

def calcsales(chart):
    cost_matrix = get_cost_matrix()
    total_sales = 0
    for row in range(len(chart)):
        for seat in range(len(chart[row])):
            if chart[row][seat] == 'X':
                total_sales += cost_matrix[row][seat]
    salesstr = f"${total_sales}"
    return salesstr

@app.route("/reservations", methods=('GET', 'POST'))
def reservations():
    if request.method == "GET":
        try:
            seating = spot.get_seating()
        except:
            seating = None
        return render_template('reservations.html', seating=seating)
    
    if request.method == "POST":
        try:
            seating = spot.get_seating()
            row = request.form.get("row")
            seat = request.form.get("seat")
            first_name = request.form.get("first_name")
            last_name = request.form.get("last_name")

            ticket_number = spot.get_ticket(first_name)

            with open('reservations.txt', 'a') as seatf:
                entry = f"{first_name}, {row}, {seat}, {ticket_number}\n"
                seatf.write(entry)
            conf_text = f"{first_name}. Row: {int(row)+1} Seat: {int(seat)+1} is now reserved for you. Enjoy your trip! Your confirmation number is: {ticket_number}"

            return render_template('reservations.html', seating=seating, conf_text=conf_text)
        except:
            flash("Something went wrong.")
            return render_template('reservations.html')
        

        
@app.route("/admin", methods=('GET', 'POST'))
def admin():
    if request.method == "GET":
        return render_template('admin.html')

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        veradmin = logadmin(username, password)
        if username == ' ':
            flash("Username required.")
            return render_template('admin.html')
        elif password == '':
            flash("Password required.")
            return render_template('admin.html')
        elif veradmin == False:
            flash("Invalid credentials.")
            return render_template('admin.html')
        
        seating = spot.get_seating()
        sales = calcsales(seating)

        return render_template('admin.html', sales=sales, seating=seating)

app.run()