
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from .database import Base
from datetime import datetime

class SquadronInfo(Base):
    __tablename__ = 'squadroninfo'
    id = Column(Integer, primary_key=True)
    insert_datetime = Column(DateTime)
    name = Column(String(255))
    number_of_players = Column(Integer)
    creation_date = Column(DateTime)

class SquadronPlayers(Base):
    __tablename__ = 'squadronplayers'
    id = Column(Integer, primary_key=True)
    insert_datetime = Column(DateTime)
    squadron_name = Column(String(255))
    number = Column(String(255))
    player_name = Column(String(255))
    player_link = Column(String(255))
    personal_clan_rating = Column(Integer)
    activity = Column(Integer)
    role = Column(String(255))
    date_of_entry = Column(DateTime)

class SquadronLeaderboard(Base):
    __tablename__ = 'squadronleaderboard'
    id = Column(Integer, primary_key=True)
    insert_datetime = Column(DateTime)
    link = Column(String(255))
    place = Column(Integer)
    name = Column(String(255))
    duel_ratio = Column(String(255))
    members = Column(Integer)
    air_targets_destroyed = Column(String(255))
    ground_targets_destroyed = Column(String(255))
    deaths = Column(String(255))
    flight_time = Column(String(255))
    
class SquadronLeaderboardHistory(Base):
    __tablename__ = 'squadronleaderboardhistory'
    id = Column(Integer, primary_key=True)
    squadronleaderboard_id = Column(Integer, ForeignKey('squadronleaderboard.id'))
    duel_ratio = Column(String(255))
    timestamp = Column(DateTime, default=datetime.utcnow)