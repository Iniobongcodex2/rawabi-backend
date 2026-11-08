from database import engine, Base
import models

# This tells SQLAlchemy to create all the tables defined in models.py
models.Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")