from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .database import SessionLocal, engine
from . import models, schemas, services

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get the database session.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Read Squadron Info
@app.get("/squadron-info/", response_model=List[schemas.SquadronInfoSchema])
def read_squadron_info(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    squadron_info = db.query(models.SquadronInfo).offset(skip).limit(limit).all()
    return squadron_info

# Read Squadron Players
@app.get("/squadron-players/", response_model=List[schemas.SquadronPlayersSchema])
def read_squadron_players(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    squadron_players = db.query(models.SquadronPlayers).offset(skip).limit(limit).all()
    return squadron_players

# Read Squadron Leaderboard
@app.get("/squadron-leaderboard/", response_model=List[schemas.SquadronLeaderboardSchema])
def read_squadron_leaderboard(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    squadron_leaderboard = db.query(models.SquadronLeaderboard).offset(skip).limit(limit).all()
    return squadron_leaderboard

@app.get("/active-squadron-leaderboard/", response_model=List[schemas.SquadronLeaderboardSchema])
def read_active_squadron_leaderboard(db: Session = Depends(get_db)):
    active_squadrons = services.get_active_squadrons(db)
    return active_squadrons


