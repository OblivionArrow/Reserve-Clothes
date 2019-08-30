from flask import Flask, Response, jsonify, request, flash, render_template, current_app, redirect
from modell import Korisnik,Rezervacija,Ducan
import sqlite3 
import os 
import secrets
from passlib.hash import sha256_crypt

db = sqlite3.connect("baza.sqlite",check_same_thread=False)
app = Flask(__name__) 

cur = db.cursor()
global dataa

@app.route("/")      # ruta    
def home():			# metoda
    return render_template('pocetna.html')

@app.route('/login-korisnik', methods=["GET","POST"])
def prijava(): 
	if request.method == "POST":
		email = request.form.get("email")
		lozinka = request.form.get("password")
		
		e_mail = db.execute("SELECT email FROM Korisnik WHERE email=:email",{"email":email}).fetchone()
		passw = db.execute("SELECT password FROM Korisnik WHERE email=:email",{"email":email}).fetchone()
		
		cur.execute("SELECT username,password FROM Korisnik WHERE email=:email",{"email":email})
		dataa= cur.fetchall()
		
		if e_mail is None:
			return render_template("login-korisnik.html")
		else: 
			for data in passw: 
				if sha256_crypt.verify(lozinka,data):
					return render_template("izbor-trgovine.html",data=dataa)
		
	return render_template("login-korisnik.html")

@app.route('/registracija',methods=["GET","POST"])
def registracija(): 
    if request.method == "POST":
	    ime_korisnika = request.form.get("ime")
	    name = request.form.get("name")
	    username = request.form.get("username")
	    email = request.form.get("email")
	    lozinka = request.form.get("psw")
	    broj = request.form.get("phonenumb")
	    sig_lozinka = sha256_crypt.encrypt(str(lozinka))
		
	    if ime_korisnika != "" and name != "" and email != "" and lozinka != "":
        
	       db.execute("INSERT INTO Korisnik(username, email, ime_korisnika, prezime, password, phone_numb) VALUES (:username, :email, :ime_korisnika, :prezime, :password, :phone_numb)", {"username":username,"email":email,"ime_korisnika":ime_korisnika,"prezime":name,"password":sig_lozinka,"phone_numb":broj})
	       db.commit()
	       return render_template('izbor-trgovine.html')
    return render_template('create_novi-korisnik.html')
	
@app.route('/odjecaHM', methods=["GET","POST"])
def hm():
	return render_template('odjecaHM.html')
	
@app.route('/odjecaNY', methods=["GET","POST"])
def ny():
	return render_template('odjecaNY.html')

@app.route('/majiceeNY', methods=["GET","POST"])
def majiceeNY():
	if request.method=="POST":
		
		naziv = request.form.get("majica")
		velicina = request.form.get("velicina")
		cijena = request.form.get("cijena")
		raspolozivost = request.form.get("raspolozivost")
		raspolozivost = "on"
		print("========================")
		print(naziv)
		print(velicina)
		print(cijena)
		print(raspolozivost)

		if raspolozivost == "on" and (velicina=="s" or velicina=="l" or velicina =="xl" or velicina=="m" or velicina =="xs"):
			db.execute("INSERT INTO Artikal(naziv, cijena, velicina, raspolozivost) VALUES (:naziv, :cijena, :velicina, :raspolozivost)", {"naziv":naziv, "cijena":cijena, "velicina":velicina, "raspolozivost":raspolozivost})
			db.commit()
		
	return render_template('majiceNY.html')

@app.route('/haljineNY', methods=["GET","POST"])
def haljineNY():
	return render_template('haljineNY.html')
	
@app.route('/hlaceNY', methods=["GET","POST"])
def hlaceNY():
	return render_template('hlaceNY.html')
	

	
if __name__=="__main__": 
    app.secret_key=os.urandom(12)
    app.run(debug=True,host='0.0.0.0',port=5000)