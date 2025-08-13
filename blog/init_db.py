from database import Base, engine
# import models

# This creates all tables in the SQLite DB file
Base.metadata.create_all(bind=engine)
print("Database and tables created!")
