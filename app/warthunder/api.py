from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from warthunder.database import SessionLocal, engine
#from warthunder.services import SquadronService
from warthunder import models, schemas, services
from fastapi import APIRouter

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
router = APIRouter()

# Dependency to get the database session.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
async def root():
    return {"message": "Hello War Thunder"}

# Read Squadron Info
@router.get("/squadron-info/", response_model=List[schemas.SquadronInfoSchema])
def read_squadron_info(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    squadron_info = db.query(models.SquadronInfo).offset(skip).limit(limit).all()
    return squadron_info

# Read Squadron Players
@router.get("/squadron-players/", response_model=List[schemas.SquadronPlayersSchema])
def read_squadron_players(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    squadron_players = db.query(models.SquadronPlayers).offset(skip).limit(limit).all()
    return squadron_players

# Read Squadron Leaderboard
@router.get("/squadron-leaderboard/", response_model=List[schemas.SquadronLeaderboardSchema])
def read_squadron_leaderboard(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    squadron_leaderboard = db.query(models.SquadronLeaderboard).offset(skip).limit(limit).all()
    return squadron_leaderboard

# Dependency to get the service instance
def get_squadron_service(db: Session = Depends(get_db)):
    return services.SquadronService(db)

@router.get("/active-squadrons/", response_model=List[schemas.SquadronLeaderboardSchema])
def read_active_squadrons(service: services.SquadronService = Depends(get_squadron_service)):
    active_squadrons = service.get_recently_active_squadrons()
    return active_squadrons


