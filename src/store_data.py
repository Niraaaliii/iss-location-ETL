from sqlalchemy import create_engine, Column, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

Base = declarative_base()

class ISSLocation(Base):
    __tablename__ = 'iss_locations'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    latitude = Column(Float)
    longitude = Column(Float)

def setup_database():
    # Step 1: Create a database engine and initialize the database schema
    engine = create_engine('sqlite:///data/iss_location.db')
    Base.metadata.create_all(engine)
    return engine

def store_iss_data(engine, df):
    # Step 2: Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Step 3: Iterate over the data and create instances of the ORM class
    for _, row in df.iterrows():
        location = ISSLocation(
            timestamp=row['timestamp'],
            latitude=row['latitude'],
            longitude=row['longitude']
        )
        session.add(location)
    
    # Step 4: Commit the session to save the data to the database
    session.commit()
    session.close()

def read_iss_data(engine):
    """Read all ISS location data from the database"""
    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Query all records
    locations = session.query(ISSLocation).all()
    
    # Convert to list of dictionaries
    data = [
        {
            'timestamp': loc.timestamp,
            'latitude': loc.latitude,
            'longitude': loc.longitude
        }
        for loc in locations
    ]
    
    session.close()
    return pd.DataFrame(data)
