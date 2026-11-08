from database import SessionLocal
import models

# Open a session to talk to the database
db = SessionLocal()

# Check if the user already exists
existing_user = db.query(models.User).filter(models.User.email == "admin@rawabi.ae").first()

if existing_user:
    print("User already exists!")
else:
    # Create a new user
    new_user = models.User(
        email="admin@rawabi.ae",
        password="password123",
        full_name="Iniobong Okon"
    )
    db.add(new_user)
    db.commit()
    print("User created successfully!")
    print("Email: admin@rawabi.ae")
    print("Password: password123")

db.close()