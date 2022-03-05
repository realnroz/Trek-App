from crypt import methods
from doctest import FAIL_FAST
from pickle import FALSE
from sqlite3 import Cursor
from flask import Flask,render_template, request,redirect,flash,jsonify, session
from forms import RegistrationForm

# for database
from flask_mysqldb import MySQL

#for sessions
# from flask_sessions import Session

app = Flask(__name__)
app.secret_key="b'\xee\x7f\x15O\x0f\xee\x0b\xd7\xa4ixK\xc9#\x17_'"

# Database Config 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'db_user'
app.config['MYSQL_PASSWORD'] = '1230'
app.config['MYSQL_DB'] = 'db_trekapp'

mysql = MySQL(app)

# Session Config 
# app.config['SESSION_PERMANENET'] = False
# app.config['SESSION_TYPE'] = 'filesystem'
# Session(app)

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
        print(user)
        session['email'] = email
        flash("You are successfully signed in.","success")       
        return redirect("/")
    else:
        flash("Invalid Credentials. Please try again.","danger")
        return redirect("/")

@app.route("/logout",methods=['POST'])
def logout():
    session.pop('email',default=None)
    flash("You are successfully signed out.","success")
    return redirect('/')


@app.route("/treks")
def allTreks():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT td.id as 'SNO',td.title as 'Title',td.days as 'Days',td.difficulty as 'Difficulty',td.total_cost as 'Total Cost',td.upvotes as 'Upvotes',u.first_name as 'First Name',u.last_name as 'Last Name' FROM `trek_destinations` as td JOIN `users` as u ON td.user_id=u.id''')
    treks = cursor.fetchall()
    cursor.close()
    return render_template("treks.html",resp = treks)

@app.route("/trek/<int:pk>")
def getTrekById(pk):
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT td.id as 'SNO',td.title as 'Title',td.days as 'Days',td.difficulty as 'Difficulty',td.total_cost as 'Total Cost',td.upvotes as 'Upvotes',u.first_name as 'First Name',u.last_name as 'Last Name' FROM `trek_destinations` as td JOIN `users` as u ON td.user_id=u.id where td.id=%s''',(pk,))
    trek = cursor.fetchone()
    cursor.close()


    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM `iternaries` WHERE `trek_destination_id` = %s;''',(pk,))
    iternaries = cursor.fetchall()
    cursor.close()  

    return render_template('trek_detail.html',trek=trek,iternaries=iternaries)

@app.route('/addTrek',methods=["POST"])
def addTrek():
    title = request.form['title']
    days = request.form['days']
    difficulty = request.form['difficulty']
    total_cost = request.form['total_cost']
    upvotes = 0

    # Gets User ID of logged in user 
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT id FROM `users` WHERE  email = %s''',(session['email'],))
    resp = cursor.fetchone()
    cursor.close()

    user_id = resp[0]
 
    # Finally inserts values into trek_destinatio table 
    cursor = mysql.connection.cursor()
    cursor.execute('''INSERT INTO trek_destinations values(NUll,%s,%s,%s,%s,%s,%s)''',(title,days,difficulty,total_cost,upvotes,user_id))
    mysql.connection.commit()
    cursor.close()

    flash("Trek Destination successfully added.","success")

    return redirect('/treks')

    

if __name__ == '__main__':
    app.run(debug=True)
