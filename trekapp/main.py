from crypt import methods
from flask import Flask,render_template, request,url_for,redirect
from flask_mysqldb import MySQL

# for database
app = Flask(__name__)

# Database Config 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1230'
app.config['MYSQL_DB'] = 'db_trekapp'

mysql = MySQL(app)

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/registration")
def registration():
    return render_template("registration.html")

@app.route("/login",methods=["POST"])
def login():
    email = request.form['email']
    password=request.form['password']

    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM users where email = %s and password = %s''',(email,password))
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)
