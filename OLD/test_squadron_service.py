from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
#import models
import json
from services import SquadronService  # Adjust the import based on your project structure

# Adjust these to match your test database configuration
with open('../db_config.json', 'r') as f:
                config = json.load(f)

DATABASE_URI = f"mysql+mysqlconnector://{config['user']}:{config['password']}@{config['host']}/{config['database']}"
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_get_active_squadrons():
    # Setup: create a session and insert test data
    db = SessionLocal()
    # Assuming you have a method to add test data or you can add it manually
    
    # Test
    squadron_service = SquadronService(db_session=db)
    active_squadrons = squadron_service.get_active_squadrons()
    
    # Assert: Replace the following line with your actual test conditions
    assert len(active_squadrons) > 0  # Example assertion

    # Teardown: Close the session and remove test data if necessary
    db.close()
