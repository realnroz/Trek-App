from crypt import methods
from sqlite3 import Cursor
from flask import Flask,render_template, request,redirect,flash
from forms import RegistrationForm

# for database
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key="b'\xee\x7f\x15O\x0f\xee\x0b\xd7\xa4ixK\xc9#\x17_'"

# Database Config 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'db_user'
app.config['MYSQL_PASSWORD'] = '1230'
app.config['MYSQL_DB'] = 'db_trekapp'

mysql = MySQL(app)

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/registration",methods=["GET","POST"])
def registration():
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.form)
        print(form.phone_number.data)

        cursor = mysql.connection.cursor()
        if form.validate_on_submit():
            resp = cursor.execute('''SELECT * FROM users where email LIKE %s''',[form.email.data])
            if resp == 0:
                cursor.execute('''INSERT INTO users values(NUll,%s,%s,%s,%s,%s,%s)''',(form.first_name.data,form.last_name.data,form.address.data,form.phone_number.data,form.email.data,form.password1.data))
                mysql.connection.commit()
                cursor.close()
                flash("User successfully registered.","success")
                return redirect("/registration")
            else:
                flash("Email already exists.","danger")

    return render_template("registration.html",form=form)

@app.route("/login",methods=["POST"])
def login():
    email = request.form['email']
    password=request.form['password']

    cursor = mysql.connection.cursor()
    resp = cursor.execute('''SELECT * FROM users where email = %s and password = %s''',(email,password))
    user = cursor.fetchone()
    cursor.close()
    if resp == 1:
        flash("You are successfully logged in.","success")       
        return redirect("/")
    else:
        flash("Invalid Credentials. Please try again.","danger")
        return redirect("/")


@app.route("/treks")
def allTreks():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT td.id as 'SNO',td.title as 'Title',td.days as 'Days',td.difficulty as 'Difficulty',td.total_cost as 'Total Cost',td.upvotes as 'Upvotes',u.first_name as 'First Name',u.last_name as 'Last Name' FROM `trek_destinations` as td JOIN `users` as u ON td.user_id=u.id''')
    treks = cursor.fetchall()
    cursor.close()
    return render_template("treks.html",resp = treks)




if __name__ == '__main__':
    app.run(debug=True)
