from flask import Flask,render_template,request,redirect
import sqlite3 as dbm

app=Flask(__name__)
db=dbm.connect('party.db')
dbc=db.cursor()
dbc.execute("CREATE TABLE UserData (phone_number varchar(20) primary key,name varchar(200))")
dbc.execute("create table foodata (partyid integer primary key,food varchar(150),place varchar(150), userphn varchar(20), price_req integer)")

#redirecting is done by flask itself and not js in html

# login page accepts the name and phone number
@app.route('/',methods=["GET","POST"])
def login():
    if(request.method=='GET'):
        # if request is get , renders the login html page
        return render_template('login.html')
    if(request.method=='POST'):
        # if its post then we need to recieve user data
        name=request.form['name']
        phnum=request.form['number']
        dbc.execute("insert into UserData values (?,?)",[phnum,name])
        return redirect('/food')


# this route is the search for food page
@app.route('/food',methods=["POST","GET"])
def readFood():
    if(request.method=='GET'):
        # if request is get , then render the search page
        return render_template('searchfood.html')
    if(request.method=='POST'):
        # needs to recieve a food item and display all parties under that food
        fooditem=request.form['food']
        dbc.execute("select partyid,place,userphn from foodata group by food where food=(?)",[fooditem])
        parties=dbc.fetchall()
        #tuples of data of each row get returned
        #render the tuples in html somehow





    
