from pony import orm
import os
import datetime as dt

db =orm.Database()
db.bind(provider='sqlite',filename='baza.sqlite',create_db=True)


class Korisnik(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    username = orm.Required(str)
    email = orm.Required(str)
    ime_korisnika = orm.Required(str)
    prezime = orm.Required(str)
    password = orm.Required(str)
    phone_numb = orm.Required(int)

class Rezervacija(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    #datum = orm.Required(datetime.date)


class Artikal(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    naziv = orm.Required(str)
    cijena = orm.Required(int)
    velicina = orm.Required(str)
    raspolozivost = orm.Required(str)


class Ducan(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    store_code = orm.Required(str)
    password_store = orm.Required(int)



db.generate_mapping(check_tables=True,create_tables=True)
