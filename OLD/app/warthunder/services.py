from sqlalchemy.orm import Session
from warthunder import models
from sqlalchemy import func, or_
from datetime import datetime, timedelta
import json

class SquadronService:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_recently_active_squadrons1(self):
        thirty_minutes_ago = datetime.utcnow() - timedelta(minutes=30)
        
        # Consulta para obter esquadrões ativos baseada em mudanças nos campos de interesse
        active_squadrons = self.db.query(models.SquadronLeaderboard).join(
            models.SquadronLeaderboardHistory,
            models.SquadronLeaderboard.id == models.SquadronLeaderboardHistory.squadronleaderboard_id
        ).filter(
            models.SquadronLeaderboardHistory.timestamp >= thirty_minutes_ago,
            or_(
                models.SquadronLeaderboardHistory.duel_ratio != models.SquadronLeaderboard.duel_ratio,
                models.SquadronLeaderboardHistory.air_targets_destroyed != models.SquadronLeaderboard.air_targets_destroyed,
                models.SquadronLeaderboardHistory.ground_targets_destroyed != models.SquadronLeaderboard.ground_targets_destroyed,
                models.SquadronLeaderboardHistory.deaths != models.SquadronLeaderboard.deaths,
                models.SquadronLeaderboardHistory.flight_time != models.SquadronLeaderboard.flight_time
            )
        ).group_by(models.SquadronLeaderboard.id).all()
        
        return active_squadrons
    
    def get_recently_inserted_squadrons2(self):
        thirty_minutes_ago = datetime.utcnow() - timedelta(minutes=30)
        
        # Consulta para obter esquadrões inseridos nos últimos 30 minutos
        recently_inserted_squadrons = self.db.query(models.SquadronLeaderboard).filter(
            models.SquadronLeaderboard.insert_datetime >= thirty_minutes_ago
        ).all()
    
        return recently_inserted_squadrons
    
    from sqlalchemy import func

    from sqlalchemy import func
    from sqlalchemy.sql import text

    def get_recently_inserted_squadrons(self):
        thirty_minutes_ago = datetime.utcnow() - timedelta(minutes=30)
        
        # Subconsulta para contar o número de registros por esquadrão
        count_subquery = self.db.query(
            models.SquadronLeaderboard.name,
            func.count(models.SquadronLeaderboard.id).label('count')
        ).group_by(models.SquadronLeaderboard.name).subquery()

        # CTE ou Subconsulta para atribuir números de linha com base em insert_datetime para cada esquadrão
        row_number_subquery = self.db.query(
            models.SquadronLeaderboard.id,
            models.SquadronLeaderboard.name,
            models.SquadronLeaderboard.insert_datetime,
            func.row_number().over(
                partition_by=models.SquadronLeaderboard.name,
                order_by=models.SquadronLeaderboard.insert_datetime.desc()
            ).label('row_num')
        ).filter(
            models.SquadronLeaderboard.insert_datetime >= thirty_minutes_ago
        ).subquery()

        # Consulta principal para obter apenas o registro mais recente para cada esquadrão
        # que foi inserido nos últimos 30 minutos e que tem mais de um registro
        recently_inserted_squadrons = self.db.query(models.SquadronLeaderboard).join(
            count_subquery, models.SquadronLeaderboard.name == count_subquery.c.name
        ).join(
            row_number_subquery, models.SquadronLeaderboard.id == row_number_subquery.c.id
        ).filter(
            count_subquery.c.count > 1,
            row_number_subquery.c.row_num == 1  # Apenas o registro mais recente
        ).all()

        return recently_inserted_squadrons


# Continuação do seu código existente...

if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    with open('../db_config.json', 'r') as f:
                config = json.load(f)

    DATABASE_URI = f"mysql+mysqlconnector://{config['user']}:{config['password']}@{config['host']}/{config['database']}"

    engine = create_engine(DATABASE_URI)
    SessionLocal = sessionmaker(bind=engine)

    # Criação da sessão do banco de dados
    db_session = SessionLocal()

    # Instância do serviço
    service = SquadronService(db_session)

    # Chamada do método para obter esquadrões ativos
    active_squadrons = service.get_recently_inserted_squadrons()

    # Imprimir os resultados para verificação
    for squadron in active_squadrons:
        print(f"Squadron ID: {squadron.id}, Name: {squadron.name}")  # Ajuste os atributos conforme seu modelo
    
    if active_squadrons:
        print(f"Total active squadrons: {len(active_squadrons)}")
    else:    
        print("No active squadrons found")

    # Fechamento da sessão do banco de dados
    db_session.close()
