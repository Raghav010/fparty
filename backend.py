from flask import Flask,render_template,request,redirect,url_for,session
import sqlite3 as dbm
import os

app=Flask(__name__)
db=dbm.connect('party.db')
dbc=db.cursor()
dbc.execute("CREATE TABLE UserData (phone_number varchar(20) primary key,name varchar(200))")
dbc.execute("create table foodata (partyid integer primary key,food varchar(150),place varchar(150), userphn varchar(20), price_req integer)")

#redirecting is done by flask itself and not js in html

# login page accepts the name and phone number
@app.route('/',methods=["GET","POST"])
def login():
    if(session.get('logged',-1)!=True):
        if(request.method=='GET'):
            # if request is get , renders the login html page
            return render_template('login.html')
        if(request.method=='POST'):
            # if its post then we need to recieve user data
            name=request.form['name']
            phnum=request.form['number']
            dbc.execute("insert into UserData values (?,?)",[phnum,name])

            # storing user specific data
            session['name']=name
            session['phnum']=phnum
            session['logged']=True
            return redirect(url_for('food'))
    else:
        return redirect(url_for('food'))


# this route is the search for food page
@app.route('/food',methods=["POST","GET"])
def readFood():
    if(session.get('logged',-1)!=True):
        return redirect(url_for('/'))
    else:
        if(request.method=='GET'):
            # if request is get , then render the search page
            return render_template('searchfood.html')
        if(request.method=='POST'):
            # needs to recieve a food item and display all parties under that food
            fooditem=request.form['food']
            dbc.execute("select partyid,place,userphn from foodata group by food where food=(?)",[fooditem])
            parties=dbc.fetchall()
            if(parties==[]):
                return redirect(url_for('foodcreate'))
            else:
                return redirect(url_for('showparties'))
            #tuples of data of each row get returned
            #render the tuples in html somehow

@app.route('/foodcreate',methods=["POST","GET"])
def createFood():
    if(session.get('logged',-1)!=True):
        return redirect(url_for('/'))
    else:
        if(request.method=='GET'):
            return render_template('foodcreate.html')
        if(request.method=='POST'):
            newfood=request.form['newfood']
            session['food']=newfood
            return redirect(url_for('createparty'))






if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)



    
