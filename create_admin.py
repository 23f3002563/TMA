from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():

    admin = User.query.filter_by(email="admin@gmail.com").first()

    if not admin:
        admin = User(
            name="Admin",
            email="admin@gmail.com",
            password="admin123",
            role="Admin",
            is_active=True
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin created successfully!")

    else:
        print("Admin already exists!")