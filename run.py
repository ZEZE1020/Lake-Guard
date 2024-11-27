from app import app, db

with app.app_context():
    db.create_all()  # Create database tables

if __name__ == '__main__':
    app.run(debug=True)
