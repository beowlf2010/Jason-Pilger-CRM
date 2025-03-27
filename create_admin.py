from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@example.com', role='admin')
        admin.set_password('password123')
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin created: admin / password123")
    else:
        print("⚠️ Admin already exists.")
