from re import U
from flask import Flask, config, render_template, session, request, redirect, url_for, json
import pyrebase
import urllib.request

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234' 

config = {
    "apiKey": "AIzaSyDa4DBbtXI2dnDHUn-Uh-x9muNKa4skZxo",
    "authDomain": "verk6-106e9.firebaseapp.com",
    "databaseURL": "https://verk6-106e9-default-rtdb.firebaseio.com",
    "projectId": "verk6-106e9",
    "storageBucket": "verk6-106e9.appspot.com",
    "messagingSenderId": "798615754573",
    "appId": "1:798615754573:web:b7ba8b229e60d437e2c904",
    "measurementId": "G-GQF28H5198"
}

fb = pyrebase.initialize_app(config)
db = fb.database()

@app.route('/')
def index():
    g = db.child("Comp").get().val()
    Complst = list(g.items())
    session.pop('login', None)
    return render_template('secret.html', upplys=Complst)

@app.route('/admin')
def admin():
    if session:
        g = db.child("Comp").get().val()
        Complst = list(g.items())
        return render_template('change.html', upplys=Complst)
    else:
        return render_template('login.html', msg="Þú þarft aðgang til að sjá upplýsingarnar")

@app.route('/login', methods=['GET','POST'])
def login():
    if session:
        g = db.child("Comp").get().val()
        Complst = list(g.items())
        return render_template('change.html', upplys=Complst)
    elif request.method == 'POST':
        u = request.form['luser']
        p = request.form['lpwd']
        
        c = db.child("User").get().val()
        lst = list(c.items())
        print(lst, u, p)
        for i in lst:
            if u == i[1]['usr'] and p == str(i[1]['pwd']):
                session['login'] = True
                g = db.child("Comp").get().val()
                Complst = list(g.items())
                return render_template('change.html', upplys=Complst)
        else:
            return render_template('login.html', msg="Rangt lykilorð eða aðgangsorð", u=u, p=p)
    else:
        return render_template('login.html', msg="Það þarf að skrá sig inn til að sjá upplísingar")


@app.route('/logout')
def logout():
    session.pop('login', None)
    g = db.child("Comp").get().val()
    Complst = list(g.items())
    return render_template("secret.html", upplys=Complst)

@app.route('/remove')
def remove():
    g = db.child("Comp").get().val()
    Complst = list(g.items())
    nafn = request.args['nafn']
    date = request.args['date']
    g = db.child("Comp").get().val()
    Complst = list(g.items())
    l=0
    for x in Complst:
        l=l+1
        if x[1]['nafn'] == nafn and x[1]['date'] == date:
            vm="Comp"+str(l)
            db.child("Comp").child(vm).remove()
    return render_template("change.html", upplys=Complst)

@app.route('/adding')
def adding():
    g = db.child("Comp").get().val()
    Complst = list(g.items())
    if session:
        return render_template("adding.html")
    else:
        return render_template("secret.html", upplys=Complst)

@app.route('/add', methods=['GET','POST'])
def add():
    g = db.child("Comp").get().val()
    Complst = list(g.items())
    n = request.form['nuser']
    m = request.form['npwd']
        
    e=1
    for b in Complst:
        e+=1
    fs="Comp"+str(e)
    db.child("Comp").child(fs).set({'nafn': n, 'date': m})
    return render_template('change.html', upplys=Complst)

@app.errorhandler(404)
def villa(error):
    return render_template('error.html')

if __name__ == "__main__":
    app.run(debug=True)