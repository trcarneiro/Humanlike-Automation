from sqlalchemy.orm import Session
import models
from sqlalchemy import func
from datetime import datetime, timedelta

class SquadronService:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_active_squadrons(self):
        thirty_minutes_ago = datetime.utcnow() - timedelta(minutes=30)
        active_squadrons = self.db.query(models.SquadronLeaderboard).join(
            models.SquadronLeaderboardHistory,
            models.SquadronLeaderboard.id == models.SquadronLeaderboardHistory.squadronleaderboard_id
        ).filter(
            models.SquadronLeaderboardHistory.timestamp >= thirty_minutes_ago
            # Implementar lógica adicional conforme necessário
        ).group_by(
            models.SquadronLeaderboard.id
        ).having(
            func.count(models.SquadronLeaderboard.id) > 1
        ).all()
        
        return active_squadrons
