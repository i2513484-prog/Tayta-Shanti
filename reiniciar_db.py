from app import create_app
from app.extensions import db

db.create_all()
app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    print("Base reiniciada correctamente ✅")