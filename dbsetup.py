from app import initialize_app
from app.models import db

app = initialize_app()

with app.app_context():
    db.create_all()
    print("✅ Tables created.")
