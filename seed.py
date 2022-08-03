from models import User, db
from app import app

db.drop_all()
db.create_all()

# could also do User.query.delete()

alex = User(first_name = 'Alex', last_name = 'Kim')
jordan = User(first_name = 'Jordan', last_name = 'Wong')
random = User(first_name = 'Ash', last_name = 'Ketchum')

db.session.add(alex)
db.session.add(jordan)
db.session.add(random)

db.sesion.commit()