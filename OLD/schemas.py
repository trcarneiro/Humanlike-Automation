from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SquadronInfoBase(BaseModel):
    name: str
    number_of_players: int
    creation_date: datetime

class SquadronInfoSchema(SquadronInfoBase):
    id: int
    class Config:
        orm_mode = True

class SquadronPlayersSchema(BaseModel):
    squadron_name: str
    number: str
    player_name: str
    player_link: Optional[str] = None
    personal_clan_rating: int
    activity: int
    role: str
    date_of_entry: datetime

class SquadronPlayers(SquadronPlayersSchema):
    id: int
    class Config:
        orm_mode = True

class SquadronLeaderboardSchema(BaseModel):
    link: str
    place: int
    name: str
    duel_ratio: str
    members: int
    air_targets_destroyed: str
    ground_targets_destroyed: str
    deaths: str
    flight_time: str

class SquadronLeaderboard(SquadronLeaderboardSchema):
    id: int
    class Config:
        orm_mode = True
