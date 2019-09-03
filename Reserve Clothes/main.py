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
user = None
################################################################# pokusavanje
@app.route('/login-store', methods=["GET","POST"])
def prijavaStore():
	if request.method == "POST":
		store_code = request.form.get("store_code")
		lozinka = request.form.get("password")
		# If a field wasn't sent, go back to login screen
		if store_code is None or lozinka is None:
			return render_template("login-store.html")
		
		storecode = db.execute("select id from Ducan where store_code=:store_code AND password_store=:password_store",{"store_code":store_code,"password_store":lozinka}).fetchone()

		if not storecode:
			print("Wrong username or password!")
			return render_template("login-store.html")
		else:
			cur.execute("SELECT * FROM Artikal WHERE trgovina=:trgovina",{"trgovina":store_code})
			dataa = cur.fetchall()
			return render_template("pregled_artikla.html",data=dataa)
	return render_template("login-store.html")
#####################################################################################


@app.route("/")      # ruta    
def home():			# metoda
    return render_template('pocetna.html')


@app.route('/login-korisnik', methods=["GET","POST"])
def prijava(): 
	global user
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
					user = cur.execute("SELECT username FROM Korisnik WHERE email=:email",{"email":email}).fetchone()
					print(user[0])
					print("test=========")
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
	global user
	print(user[0])
	return render_template('odjecaHM.html')


@app.route('/odjecaNY', methods=["GET","POST"])
def ny():
	return render_template('odjecaNY.html')


@app.route('/majiceeNY', methods=["GET","POST"])
def majiceeNY():
	global user
	if request.method=="POST":
		
		naziv = request.form.get("majica")
		velicina = request.form.get("velicina")
		cijena = request.form.get("cijena")
		raspolozivost = request.form.get("raspolozivost")
		raspolozivost = "on"
		trgovina = request.form.get("NY")
		print("========================")
		print(naziv)
		print(velicina)
		print(cijena)
		print(raspolozivost)

		if raspolozivost == "on" and (velicina=="s" or velicina=="l" or velicina =="xl" or velicina=="m" or velicina =="xs"):
			db.execute("INSERT INTO Artikal(naziv, cijena, velicina, raspolozivost, trgovina, user) VALUES (:naziv, :cijena, :velicina, :raspolozivost, :trgovina, :user)", {"naziv":naziv, "cijena":cijena, "velicina":velicina, "raspolozivost":raspolozivost,"trgovina":trgovina, "user":user[0]})
			db.commit()
		
	return render_template('majiceNY.html')


@app.route('/haljineNY', methods=["GET","POST"])
def haljineNY():
	global user
	if request.method=="POST":
		
		naziv = request.form.get("haljina")
		velicina = request.form.get("velicina")
		cijena = request.form.get("cijena")
		raspolozivost = request.form.get("raspolozivost")
		raspolozivost = "on"
		trgovina = request.form.get("NY")
		print("========================")
		print(naziv)
		print(velicina)
		print(cijena)
		print(raspolozivost)

		if raspolozivost == "on" and (velicina=="s" or velicina=="l" or velicina =="xl" or velicina=="m" or velicina =="xs"):
			db.execute("INSERT INTO Artikal(naziv, cijena, velicina, raspolozivost, trgovina, user) VALUES (:naziv, :cijena, :velicina, :raspolozivost, :trgovina, :user)", {"naziv":naziv, "cijena":cijena, "velicina":velicina, "raspolozivost":raspolozivost, "trgovina":trgovina, "user":user[0]})
			db.commit()
	return render_template('haljineNY.html')
	

@app.route('/hlaceNY', methods=["GET","POST"])
def hlaceNY():
	global user
	if request.method=="POST":
		
		naziv = request.form.get("hlace")
		velicina = request.form.get("velicina")
		cijena = request.form.get("cijena")
		raspolozivost = request.form.get("raspolozivost")
		raspolozivost = "on"
		trgovina = request.form.get("NY")
		print("========================")
		print(naziv)
		print(velicina)
		print(cijena)
		print(raspolozivost)

		if raspolozivost == "on" and (velicina=="s" or velicina=="l" or velicina =="xl" or velicina=="m" or velicina =="xs"):
			db.execute("INSERT INTO Artikal(naziv, cijena, velicina, raspolozivost, trgovina, user) VALUES (:naziv, :cijena, :velicina, :raspolozivost, :trgovina, :user)", {"naziv":naziv, "cijena":cijena, "velicina":velicina, "raspolozivost":raspolozivost, "trgovina":trgovina, "user":user[0]})
			db.commit()
	return render_template('hlaceNY.html')


@app.route('/majiceHM', methods=["GET","POST"])
def majiceHM():
	global user
	if request.method=="POST":
		
		naziv = request.form.get("majica")
		velicina = request.form.get("velicina")
		cijena = request.form.get("cijena")
		raspolozivost = request.form.get("raspolozivost")
		raspolozivost = "on"
		trgovina = request.form.get("HM")
		print("========================")
		print(naziv)
		print(velicina)
		print(cijena)
		print(raspolozivost)

		if raspolozivost == "on" and (velicina=="s" or velicina=="l" or velicina =="xl" or velicina=="m" or velicina =="xs"):
			db.execute("INSERT INTO Artikal(naziv, cijena, velicina, raspolozivost, trgovina, user) VALUES (:naziv, :cijena, :velicina, :raspolozivost, :trgovina, :user)", {"naziv":naziv, "cijena":cijena, "velicina":velicina, "raspolozivost":raspolozivost, "trgovina":trgovina, "user":user[0]})
			db.commit()
		
	return render_template('majiceHM.html')


@app.route('/haljineHM', methods=["GET","POST"])
def haljineHM():
	global user
	if request.method=="POST":
		
		naziv = request.form.get("haljine")
		velicina = request.form.get("velicina")
		cijena = request.form.get("cijena")
		trgovina = request.form.get("HM")
		raspolozivost = request.form.get("raspolozivost")
		raspolozivost = "on"
		
		print("========================")
		print(naziv)
		print(velicina)
		print(cijena)
		print(raspolozivost)

		if raspolozivost == "on" and (velicina=="s" or velicina=="l" or velicina =="xl" or velicina=="m" or velicina =="xs"):
			db.execute("INSERT INTO Artikal(naziv, cijena, velicina, raspolozivost, trgovina, user) VALUES (:naziv, :cijena, :velicina, :raspolozivost, :trgovina, :user)", {"naziv":naziv, "cijena":cijena, "velicina":velicina, "raspolozivost":raspolozivost, "trgovina":trgovina, "user":user[0]})
			db.commit()
		
	return render_template('haljineHM.html')


@app.route('/hlaceHM', methods=["GET","POST"])
def hlaceHM():
	global user
	if request.method=="POST":
		
		naziv = request.form.get("hlace")
		velicina = request.form.get("velicina")
		cijena = request.form.get("cijena")
		raspolozivost = request.form.get("raspolozivost")
		raspolozivost = "on"
		trgovina = request.form.get("HM")
		print("========================")
		print(naziv)
		print(velicina)
		print(cijena)
		print(raspolozivost)

		if raspolozivost == "on" and (velicina=="s" or velicina=="l" or velicina =="xl" or velicina=="m" or velicina =="xs"):
			db.execute("INSERT INTO Artikal(naziv, cijena, velicina, raspolozivost, trgovina, user) VALUES (:naziv, :cijena, :velicina, :raspolozivost, :trgovina, :user)", {"naziv":naziv, "cijena":cijena, "velicina":velicina, "raspolozivost":raspolozivost, "trgovina":trgovina, "user":user[0]})
			db.commit()
		
	return render_template('hlaceHM.html')

@app.route("/login-store")     
def loginStore():			
    return render_template('login-store.html')


@app.route("/pregled_artikla")     
def pregled():
    return render_template('pregled_artikla.html')


if __name__=="__main__": 
    app.secret_key=os.urandom(12)
    app.run(debug=True,host='0.0.0.0',port=5000)



	