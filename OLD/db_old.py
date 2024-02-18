from sqlalchemy import create_engine, Column, Integer, String, DateTime, Time, ForeignKey, Float, BigInteger , func, case, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import json
from datetime import datetime

Base = declarative_base()

class AppConfig(Base):
    __tablename__ = 'app_config'

    key = Column(String(255), primary_key=True)
    value = Column(String(255), nullable=False)
    description = Column(String(255))

    def __repr__(self):
        return f"<AppConfig(key='{self.key}', value='{self.value}')>"


class ProcessedTransaction(Base):
    __tablename__ = 'processed_transactions'
    
    id = Column(String(255), primary_key=True)
    description = Column(String(255), nullable=False)
    value = Column(String(255), nullable=False)
    date = Column(DateTime, nullable=False)
    name = Column(String(255), nullable=False)
    
class ScheduledTaskLog(Base):
    __tablename__ = 'scheduled_task_logs'
    
    id = Column(Integer, primary_key=True)
    scheduled_message_id = Column(Integer, ForeignKey('scheduled_messages.id'), nullable=False)
    execution_datetime = Column(DateTime, default=datetime.utcnow)
    status = Column(String(255), nullable=False)  # ex: 'success', 'failure'
    error_message = Column(String(255), nullable=True)

class ScheduledMessage(Base):
    __tablename__ = 'scheduled_messages'
    
    id = Column(Integer, primary_key=True)
    channel_id = Column(String(255), nullable=False)
    message_text = Column(String(255), nullable=True)
    command = Column(String(255), nullable=True)
    schedule_time = Column(Time, nullable=False)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)

class MessageLog(Base):
    __tablename__ = 'message_logs'
    
    id = Column(Integer, primary_key=True)
    channel_id = Column(String(255), nullable=False)
    message_text = Column(String(255), nullable=True)
    command = Column(String(255), nullable=True)
    
class Giveaway(Base):
    __tablename__ = 'giveaways'
    
    id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    xp_needed = Column(Integer, default=0, nullable=False)
    max_winners = Column(Integer, nullable=False)  # Número máximo de ganhadores
    max_tickets_per_user = Column(Integer, nullable=False)  # Máximo de tickets por usuário
    message_id = Column(BigInteger, nullable=True)  # ID da mensagem do sorteio
    status = Column(String(255), nullable=False)  # Status do sorteio

    entries = relationship("GiveawayEntry", back_populates="giveaway")


class GiveawayEntry(Base):
    __tablename__ = 'giveaway_entries'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    giveaway_id = Column(Integer, ForeignKey('giveaways.id'), nullable=False)
    tickets = Column(Integer, nullable=False, default=0)
    entry_date = Column(DateTime, default=datetime.utcnow)  
    xp_invested = Column(Integer, default=0, nullable=False)# Nova coluna para data de inscrição

    # Relacionamento com a tabela Giveaway
    giveaway = relationship("Giveaway", back_populates="entries")
 
class GiveawayWinner(Base):
    __tablename__ = 'giveaway_winners'

    id = Column(Integer, primary_key=True)
    giveaway_id = Column(Integer, ForeignKey('giveaways.id'), nullable=False)
    user_id = Column(BigInteger, nullable=False)
    win_date = Column(DateTime, default=datetime.utcnow)

    # Relacionamento com a tabela Giveaway (opcional)
    giveaway = relationship("Giveaway")
 
     
class WTPlayerSquadData(Base):
    __tablename__ = 'WTPlayerSquadData'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    clan = Column(String(100), nullable=False)
    activity = Column(Integer, nullable=False)
    personal_clan_rating = Column(Integer, nullable=False)
    player_link = Column(String(255))
    role = Column(String(100))
    date_of_entry = Column(DateTime)
    insert_datetime = Column(DateTime, default=datetime.utcnow)
    date_of_exit = Column(DateTime, nullable=True)  # Nova coluna para data de saída
    
class UserXP(Base):
    __tablename__ = 'user_xp'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, unique=True, nullable=False)  # Altere para BigInteger
    xp = Column(Integer, default=0, nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow)
    
    # Adicionar relacionamento com XPUpdateLog
    xp_update_logs = relationship("XPUpdateLog", back_populates="user")
    
class UserActivity(Base):
    __tablename__ = 'user_activities'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    activity_type = Column(String(255), nullable=False)  # Ex: 'message', 'voice'
    xp_gained = Column(Integer, nullable=False)
    activity_timestamp = Column(DateTime, default=datetime.utcnow)
    channel_id = Column(String(255), nullable=True)  # ID do canal
    message_content = Column(String(2000), nullable=True)  # Conteúdo da mensagem, se aplicável

    def __init__(self, user_id, activity_type, xp_gained, channel_id=None, message_content=None):
        self.user_id = user_id
        self.activity_type = activity_type
        self.xp_gained = xp_gained
        self.channel_id = channel_id
        self.message_content = message_content
        
class KeywordResponse(Base):
    __tablename__ = 'keyword_responses'

    id = Column(Integer, primary_key=True)
    keyword = Column(String(255), unique=True, nullable=False)
    response = Column(String(255), nullable=False)

class WarThunderData(Base):
    __tablename__ = 'war_thunder_data'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    ab_battles = Column(Float)
    ab_win_rate = Column(Float)
    ab_air_frags_per_battle = Column(Float)
    ab_air_frags_per_death = Column(Float)
    ab_ground_frags_per_battle = Column(Float)
    ab_ground_frags_per_death = Column(Float)
    rb_battles = Column(Float)
    rb_win_rate = Column(Float)
    rb_air_frags_per_battle = Column(Float)
    rb_air_frags_per_death = Column(Float)
    rb_ground_frags_per_battle = Column(Float)
    rb_ground_frags_per_death = Column(Float)
    sb_battles = Column(Float)
    sb_win_rate = Column(Float)
    sb_air_frags_per_battle = Column(Float)
    sb_air_frags_per_death = Column(Float)
    sb_ground_frags_per_battle = Column(Float)
    sb_ground_frags_per_death = Column(Float)
    alt_name = Column(String(255))
    wk_name = Column(String(255))
    nation = Column(String(255))
    cls = Column(String(255))
    ab_br = Column(Float)
    rb_br = Column(Float)
    sb_br = Column(Float)
    ab_repair = Column(Float)
    rb_repair = Column(Float)
    sb_repair = Column(Float)
    is_premium = Column(String(255))  # Pode ser alterado para Boolean ou Integer se os valores forem binários
    ab_rp_rate = Column(Float)
    ab_sl_rate = Column(Float)
    rb_rp_rate = Column(Float)
    rb_sl_rate = Column(Float)
    sb_rp_rate = Column(Float)
    sb_sl_rate = Column(Float)
    date_of_exit = Column(DateTime, nullable=True)  # Nova coluna para data de saída


    def update_data(self, data):
        # Atualize os campos com base no dicionário de dados fornecido
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

class XPUpdateLog(Base):
    __tablename__ = 'xp_update_logs'

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('user_xp.user_id'), nullable=False)
    category = Column(String(255), nullable=False)  # Exemplo: 'role', 'clan_activity', 'cb_activity'
    last_update = Column(DateTime, nullable=False)

    # Relacionamento com a tabela UserXP
    user = relationship("UserXP", back_populates="xp_update_logs")
    

class Suggestion(Base):
    __tablename__ = 'suggestions'

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False)
    suggestion_text = Column(String(1000), nullable=False)
    status = Column(String(255), default='pending')  # Exemplos: 'pending', 'reviewing', 'approved', 'denied'
    response = Column(String(1000), nullable=True)  # Resposta da equipe, se aplicável
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    

class SuggestionVote(Base):
    __tablename__ = 'suggestion_votes'

    id = Column(Integer, primary_key=True)
    suggestion_id = Column(Integer, ForeignKey('suggestions.id'), nullable=False)
    user_id = Column(BigInteger, nullable=False)  # ID do usuário que votou
    voted_at = Column(DateTime, default=datetime.utcnow)


class Database:
    def __init__(self):
        # Load database config from a json file
        with open('db_config.json', 'r') as f:
            config = json.load(f)
        
        DATABASE_URI = f"mysql+mysqlconnector://{config['user']}:{config['password']}@{config['host']}/{config['database']}"
        self.engine = create_engine(DATABASE_URI)
        self.Session = sessionmaker(bind=self.engine)

        Base.metadata.create_all(self.engine)
    
        
    async def log_scheduled_task_execution(self, scheduled_message_id, status, error_message=None):
        session = self.Session()
        try:
            log_entry = ScheduledTaskLog(
                scheduled_message_id=scheduled_message_id,
                status=status,
                error_message=error_message
            )
            session.add(log_entry)
            session.commit()
        except Exception as e:
            print(f"Erro ao registrar execução da tarefa agendada: {e}")
        finally:
            session.close()

# Na classe Database

    def update_player_exit_date(self, player_name):
        session = self.Session()
        try:
            player = session.query(WTPlayerSquadData).filter_by(name=player_name).first()
            if player:
                player.date_of_exit = datetime.utcnow()
                session.commit()
        except Exception as e:
            print(f"Erro ao atualizar a data de saída do jogador {player_name}: {e}")
        finally:
            session.close()

   
    async def add_player_squad_data(self, player_info):
        session = self.Session()
        try:
            # Verifica se já existe um registro para este jogador
            existing_player = session.query(WTPlayerSquadData).filter_by(name=player_info['player']).order_by(WTPlayerSquadData.insert_datetime.desc()).first()

            # Se existe e não tem data de saída, atualiza o registro
            if existing_player and not existing_player.date_of_exit:
                existing_player.activity = int(player_info['activity'])
                existing_player.personal_clan_rating = int(player_info['personal_clan_rating'])
                existing_player.player_link = player_info.get('player_link', '')
                existing_player.role = player_info.get('role', '')
                # Não atualize a data de entrada aqui
            else:
                # Se não existe ou tem data de saída, cria um novo registro
                new_player = WTPlayerSquadData(
                    name=player_info['player'],
                    clan=player_info['clan'],
                    activity=int(player_info['activity']),
                    personal_clan_rating=int(player_info['personal_clan_rating']),
                    player_link=player_info.get('player_link', ''),
                    role=player_info.get('role', ''),
                    date_of_entry=datetime.strptime(player_info['date_of_entry'], '%d.%m.%Y') if player_info['date_of_entry'] else None,
                    insert_datetime=datetime.utcnow()
                )
                session.add(new_player)

            session.commit()
        except Exception as e:
            print(f"Erro ao adicionar ou atualizar jogador: {e}")
        finally:
            session.close()

        
    def add_player_squad_data1(self, player_info):
        session = self.Session()
        try:
            player = WTPlayerSquadData(
                name=player_info['player'],
                clan=player_info['clan'],
                activity=int(player_info['activity']),
                personal_clan_rating=int(player_info['personal_clan_rating']),
                player_link=player_info.get('player_link', ''),
                role=player_info.get('role', ''),
                date_of_entry=datetime.strptime(player_info['date_of_entry'], '%d.%m.%Y') if player_info['date_of_entry'] else None,
                insert_datetime=datetime.utcnow()
            )
            session.add(player)
            session.commit()
        except Exception as e:
            print(f"Erro ao adicionar jogador: {e}")
        finally:
            session.close()    
          
    def is_processed(self, transaction_id):
        session = self.Session()
        result = session.query(ProcessedTransaction).filter_by(id=transaction_id).first()
        session.close()
        return result is not None

    def mark_as_processed(self, transaction):
        session = self.Session()
        new_transaction = ProcessedTransaction(**transaction)
        session.add(new_transaction)
        session.commit()
        session.close()

    async def fetch_scheduled_messages(self):
        current_datetime = datetime.now()
        session = self.Session()
        messages = session.query(ScheduledMessage).filter(
            ScheduledMessage.schedule_time <= current_datetime.time(),
            ScheduledMessage.start_date <= current_datetime,
            (ScheduledMessage.end_date == None) | (ScheduledMessage.end_date >= current_datetime)
        ).all()
        session.close()
        return [(msg.id, msg.channel_id, msg.message_text, msg.command, msg.schedule_time , msg.start_date, msg.end_date) for msg in messages]

    async def log_action(self, channel_id, message_text, command):
        session = self.Session()
        log = MessageLog(channel_id=channel_id, message_text=message_text, command=command)
        session.add(log)
        session.commit()
        session.close()
        
        
    async def add_giveaway(self, description, start_date, end_date, xp_needed, max_winners, max_tickets_per_user, status='active'):
        session = self.Session()
        new_giveaway = Giveaway(description=description, start_date=start_date, end_date=end_date, xp_needed=xp_needed, max_winners=max_winners, max_tickets_per_user=max_tickets_per_user, status=status)
        session.add(new_giveaway)
        session.commit()
        giveaway_id = new_giveaway.id
        session.close()
        return giveaway_id

    async def add_giveaway_entry(self, user_id, giveaway_id, tickets):
        session = self.Session()
        entry = GiveawayEntry(user_id=user_id, giveaway_id=giveaway_id, tickets=tickets)
        session.add(entry)
        session.commit()
        session.close()

    async def get_active_giveaways(self):
        session = self.Session()
        active_giveaways = session.query(Giveaway).filter_by(status='active').all()
        session.close()
        return active_giveaways
    
    async def get_giveaway(self, giveaway_id):
        session = self.Session()
        try:
            # Busca as informações do sorteio com base no ID fornecido
            giveaway = session.query(Giveaway).filter_by(id=giveaway_id).first()
        except Exception as e:
            print(f"Erro ao buscar informações do sorteio: {e}")
            giveaway = None
        finally:
            session.close()

        return giveaway
    

    async def get_giveaway_by_message_id(self, message_id):
        session = self.Session()  # Garanta que esta linha está correta
        try:
            print(f"Procurando sorteio com message_id: {message_id}")
            
            # Busca as informações do sorteio com base no ID fornecido
            giveaway = session.query(Giveaway).filter_by(message_id=message_id).first()

            if giveaway:
                print(f"Sorteio encontrado: {giveaway}")
                print(f"Descrição do sorteio: {giveaway.description}")
                print(f"ID do sorteio: {giveaway.id}")
            else:
                print(f"Nenhum sorteio encontrado com message_id: {message_id}")

        except Exception as e:
            print(f"Erro ao buscar informações do sorteio: {e}")
            giveaway = None
        finally:
            session.close()

        return giveaway

    async def update_giveaway_entry(self, giveaway_entry):
        session = self.Session()
        try:
            # Buscar a entrada existente no banco de dados
            existing_entry = session.query(GiveawayEntry).get(giveaway_entry.id)
            if existing_entry:
                # Atualizar a entrada com as novas informações
                existing_entry.tickets = giveaway_entry.tickets
                session.commit()
        except Exception as e:
            print(f"Erro ao atualizar a entrada do sorteio: {e}")
            session.rollback()
        finally:
            session.close()

    async def update_giveaway_status(self, giveaway_id, new_status):
        session = self.Session()
        giveaway = session.query(Giveaway).filter_by(id=giveaway_id).first()
        if giveaway:
            giveaway.status = new_status
            session.commit()
        session.close()
        
    async def get_giveaway_entries(self, giveaway_id):
        """Retorna as entradas para um sorteio específico."""
        session = self.Session()
        try:
            entries = session.query(GiveawayEntry).filter_by(giveaway_id=giveaway_id).all()
            return [{'user_id': entry.user_id, 'tickets': entry.tickets} for entry in entries]
        except Exception as e:
            print(f"Erro ao buscar entradas do sorteio: {e}")
            return []
        finally:
            session.close()
            
    async def get_giveaway_entry(self, user_id, giveaway_id):
        """
        Busca uma entrada específica de um usuário em um sorteio.
        """
        session = self.Session()
        try:
            # Cria a consulta
            query = session.query(GiveawayEntry).filter_by(user_id=user_id, giveaway_id=giveaway_id)

            # Para ver a consulta SQL gerada
            sql_query = str(query.statement.compile(compile_kwargs={"literal_binds": True}))
            print(sql_query)

            # Executa a consulta
            entry = query.first()
            return entry
        except Exception as e:
            print(f"Erro ao buscar entrada do sorteio para o usuário {user_id}: {e}")
            return None
        finally:
            session.close()
            
    async def get_latest_giveaway_id(self):
        """Retorna o ID do último sorteio criado."""
        session = self.Session()
        try:
            latest_giveaway = session.query(Giveaway).order_by(Giveaway.id.desc()).first()
            return latest_giveaway.id if latest_giveaway else None
        except Exception as e:
            print(f"Erro ao buscar o último ID de sorteio: {e}")
            return None
        finally:
            session.close()

    async def get_user_giveaway_entries(self, user_id):
        session = self.Session()
        try:
            entries = session.query(GiveawayEntry).filter_by(user_id=user_id).all()
            return [{'giveaway_id': entry.giveaway_id, 'tickets': entry.tickets} for entry in entries]
        except Exception as e:
            print(f"Erro ao buscar entradas do sorteio para o usuário {user_id}: {e}")
            return []
        finally:
            session.close()

    async def get_all_players(self, name=None, clan=None, min_activity=None, max_activity=None, min_personal_clan_rating=None, max_personal_clan_rating=None, role=None, date_of_entry=None, most_recent_only=False):
        """Retorna todos os jogadores registrados na tabela WTPlayerSquadData, com opções de filtro."""
        session = self.Session()
        try:
            # Iniciar a consulta
            query = session.query(WTPlayerSquadData)

            # Aplicar filtros condicionais
            if name is not None:
                query = query.filter(WTPlayerSquadData.name == name)
            if clan is not None:
                query = query.filter(WTPlayerSquadData.clan == clan)
            if min_activity is not None:
                query = query.filter(WTPlayerSquadData.activity >= min_activity)
            if max_activity is not None:
                query = query.filter(WTPlayerSquadData.activity <= max_activity)
            if min_personal_clan_rating is not None:
                query = query.filter(WTPlayerSquadData.personal_clan_rating >= min_personal_clan_rating)
            if max_personal_clan_rating is not None:
                query = query.filter(WTPlayerSquadData.personal_clan_rating <= max_personal_clan_rating)
            if role is not None:
                query = query.filter(WTPlayerSquadData.role == role)
            if date_of_entry is not None:
                query = query.filter(WTPlayerSquadData.date_of_entry == date_of_entry)
                
            if most_recent_only:
                query = query.order_by(WTPlayerSquadData.insert_datetime.desc()).limit(1)


            # Executar a consulta
            players = query.all()

            # Converter os resultados para um formato de dicionário
            return [
                {
                    'id': player.id,
                    'name': player.name,
                    'clan': player.clan,
                    'activity': player.activity,
                    'personal_clan_rating': player.personal_clan_rating,
                    'player_link': player.player_link,
                    'role': player.role,
                    'date_of_entry': player.date_of_entry,
                    'insert_datetime': player.insert_datetime
                }
                for player in players
            ]
        except Exception as e:
            print(f"Erro ao buscar jogadores: {e}")
            return []
        finally:
            session.close()

    async def add_or_update_user_xp(self, user_id, xp_amount):
        session = self.Session()
        user_xp = session.query(UserXP).filter_by(user_id=user_id).first()
        
        if user_xp:
            user_xp.xp += xp_amount
            user_xp.last_updated = datetime.utcnow()
        else:
            new_user_xp = UserXP(user_id=user_id, xp=xp_amount)
            session.add(new_user_xp)
        
        session.commit()
        session.close()

    async def get_user_xp(self, user_id):
        session = self.Session()
        user_xp = session.query(UserXP).filter_by(user_id=user_id).first()
        session.close()
        return user_xp

    async def convert_xp_to_tickets(self, user_id, xp_to_ticket_rate):
        session = self.Session()
        user_xp = session.query(UserXP).filter_by(user_id=user_id).first()
        tickets = 0

        if user_xp and user_xp.xp >= xp_to_ticket_rate:
            tickets = user_xp.xp // xp_to_ticket_rate
            user_xp.xp -= tickets * xp_to_ticket_rate
            session.commit()

        session.close()
        return tickets

    async def record_user_activity(self, user_id, activity_type, xp_gained, channel_id=None, message_content=None):
        session = self.Session()
        new_activity = UserActivity(user_id=user_id, activity_type=activity_type, xp_gained=xp_gained, channel_id=channel_id, message_content=message_content)
        session.add(new_activity)
        session.commit()
        session.close()

    async def get_keyword_response(self, keyword):
        session = self.Session()
        keyword_response = session.query(KeywordResponse).filter_by(keyword=keyword).first()
        session.close()
        return keyword_response
    
    async def update_war_thunder_data(self, data):
        session = self.Session()
        try:
            # Preparar os dados para inserção/atualização em lote
            new_entries = []
            all_current_player_names = set(row['name'] for row in data)

            for row in data:
                entry = session.query(WarThunderData).filter_by(name=row['name']).first()
                if entry:
                    entry.update_data(row)
                    entry.date_of_exit = None  # Resetar a data de saída, pois o jogador ainda está no clã
                else:
                    new_entries.append(WarThunderData(**row))

            # Atualizar a data de saída para jogadores que não estão mais no arquivo
            all_players_in_db = session.query(WarThunderData).all()
            for player in all_players_in_db:
                if player.name not in all_current_player_names:
                    player.date_of_exit = datetime.utcnow()  # Definir a data de saída

            # Executar inserções em lote
            if new_entries:
                session.bulk_save_objects(new_entries)

            session.commit()
        except Exception as e:
            print(f"Erro ao atualizar dados do War Thunder: {e}")
            session.rollback()
        finally:
            session.close()
            
    async def get_vehicle_data(self, name=None, nation=None, cls=None, min_br=None, max_br=None):
        """Retorna os dados dos veículos registrados na tabela WarThunderData, com opções de filtro."""
        session = self.Session()
        try:
            # Iniciar a consulta
            query = session.query(WarThunderData)

            # Aplicar filtros condicionais
            if name is not None:
                query = query.filter(WarThunderData.name == name)
            if nation is not None:
                query = query.filter(WarThunderData.nation == nation)
            if cls is not None:
                query = query.filter(WarThunderData.cls == cls)
            if min_br is not None:
                query = query.filter(WarThunderData.br >= min_br)
            if max_br is not None:
                query = query.filter(WarThunderData.br <= max_br)

            # Executar a consulta
            vehicles = query.all()

            # Converter os resultados para um formato de dicionário
            return [
                {
                    'id': vehicle.id,
                    'name': vehicle.name,
                    'nation': vehicle.nation,
                    'cls': vehicle.cls,
                    'br': vehicle.br,
                    # Adicione outros campos conforme necessário
                }
                for vehicle in vehicles
            ]
        except Exception as e:
            print(f"Erro ao buscar dados dos veículos: {e}")
            return []
        finally:
            session.close()
            
    async def get_top_xp_users_detailed(self, number_of_users):
        session = self.Session()
        try:
            # Supondo que a tabela UserXP armazena o total de XP
            top_users = session.query(UserXP.user_id, UserXP.xp.label('total_xp'),
                                      func.sum(UserActivity.xp_gained).label('activity_xp'),
                                      func.sum(case((UserActivity.activity_type == 'message', UserActivity.xp_gained), else_=0)).label('message_xp'),
                                      func.sum(case((UserActivity.activity_type == 'voice', UserActivity.xp_gained), else_=0)).label('voice_xp'),
                                      # Adicione outras categorias de XP conforme necessário
                                      ).join(UserActivity, UserActivity.user_id == UserXP.user_id
                                      ).group_by(UserXP.user_id
                                      ).order_by(desc(UserXP.xp)
                                      ).limit(number_of_users
                                      ).all()

            return [{'user_id': user.user_id, 'total_xp': user.total_xp, 'message_xp': user.message_xp, 'voice_xp': user.voice_xp} for user in top_users]
        except Exception as e:
            print(f"Erro ao buscar top usuários XP: {e}")
            return []
        finally:
            session.close()
            
    async def get_user_xp_details(self, user_id):
        session = self.Session()
        try:
            # Obter detalhes do XP para um usuário específico
            user_xp_details = session.query(
                UserXP.user_id, 
                UserXP.xp.label('total_xp'),
                func.sum(UserActivity.xp_gained).label('activity_xp'),
                func.sum(case((UserActivity.activity_type == 'message', UserActivity.xp_gained), else_=0)).label('message_xp'),
                func.sum(case((UserActivity.activity_type == 'voice', UserActivity.xp_gained), else_=0)).label('voice_xp'),
                func.sum(case((UserActivity.activity_type == 'squadactivity', UserActivity.xp_gained), else_=0)).label('squadactivity_xp'),
                func.sum(case((UserActivity.activity_type == 'cb_activity', UserActivity.xp_gained), else_=0)).label('squadcb_xp'),
                func.sum(case((UserActivity.activity_type == 'role', UserActivity.xp_gained), else_=0)).label('role_xp'),
                func.sum(case((UserActivity.activity_type == 'event', UserActivity.xp_gained), else_=0)).label('event_xp'),
                func.sum(case((UserActivity.activity_type == 'other', UserActivity.xp_gained), else_=0)).label('other_xp'),
                # Adicione outras categorias de XP conforme necessário
            ).join(UserActivity, UserActivity.user_id == UserXP.user_id
            ).filter(UserXP.user_id == user_id
            ).group_by(UserXP.user_id
            ).first()

            if user_xp_details:
                return {
                    'user_id': user_xp_details.user_id, 
                    'total_xp': user_xp_details.total_xp, 
                    'message_xp': user_xp_details.message_xp, 
                    'voice_xp': user_xp_details.voice_xp, 
                    'squadactivity_xp': user_xp_details.squadactivity_xp,
                    'squadcb_xp': user_xp_details.squadcb_xp, 
                    'role_xp': user_xp_details.role_xp, 
                    'event_xp': user_xp_details.event_xp, 
                    'other_xp': user_xp_details.other_xp
                    # Adicione outras categorias de XP se implementadas
                }
            else:
                return None
        except Exception as e:
            print(f"Erro ao buscar detalhes de XP do usuário: {e}")
            return None
        finally:
            session.close()

    async def get_last_xp_update(self, user_id, category):
        session = self.Session()
        try:
            last_update_entry = session.query(XPUpdateLog).filter_by(user_id=user_id, category=category).order_by(XPUpdateLog.last_update.desc()).first()
            return last_update_entry.last_update if last_update_entry else None
        except Exception as e:
            print(f"Erro ao buscar a última atualização do XP: {e}")
            return None
        finally:
            session.close()

    async def set_last_xp_update(self, user_id, category, update_time):
        session = self.Session()
        try:
            # Verificar se o usuário existe em user_xp
            user_xp = session.query(UserXP).filter_by(user_id=user_id).first()
            if not user_xp:
                # Se o usuário não existir, crie um novo registro em user_xp
                new_user_xp = UserXP(user_id=user_id, xp=0)
                session.add(new_user_xp)
                session.flush()  # Garante que new_user_xp seja persistido antes de prosseguir

            # Agora podemos inserir com segurança o registro em xp_update_logs
            new_update_log = XPUpdateLog(user_id=user_id, category=category, last_update=update_time)
            session.add(new_update_log)
            session.commit()
        except Exception as e:
            print(f"Erro ao registrar a última atualização do XP: {e}")
            session.rollback()
        finally:
            session.close()

    async def check_xp_consistency(self, user_id):
        session = self.Session()
        try:
            # Obtenha o total de XP do usuário
            user_xp = session.query(UserXP).filter_by(user_id=user_id).first()
            total_xp = user_xp.xp if user_xp else 0

            # Calcule a soma do XP registrado em user_activity
            soma_xp_activities = session.query(func.sum(UserActivity.xp_gained))\
                                        .filter(UserActivity.user_id == user_id)\
                                        .scalar()

            # Verifique a consistência
            if soma_xp_activities != total_xp:
                print(f"Inconsistência detectada para o usuário {user_id}: Total XP ({total_xp}) != Soma XP Atividades ({soma_xp_activities})")
                # Aqui você pode decidir o que fazer em caso de inconsistência
                # Por exemplo, você pode ajustar o total de XP para corresponder à soma das atividades
                if user_xp:
                    user_xp.xp = soma_xp_activities
                    session.commit()

        except Exception as e:
            print(f"Erro ao verificar consistência do XP para o usuário {user_id}: {e}")
        finally:
            session.close()
            
    async def record_or_update_user_activity(self, user_id, activity_type, xp_gained, channel_id, message_content, current_season_start):
        session = self.Session()
        try:
            # Verificar se existe uma atividade anterior na temporada atual
            existing_activity = session.query(UserActivity)\
                                       .filter(UserActivity.user_id == user_id,
                                               UserActivity.activity_type == activity_type,
                                               UserActivity.activity_timestamp >= current_season_start)\
                                       .first()

            if existing_activity:
                # Atualizar a atividade existente se necessário
                existing_activity.xp_gained = xp_gained
            else:
                # Criar uma nova atividade se não existir
                new_activity = UserActivity(user_id=user_id, 
                                            activity_type=activity_type, 
                                            xp_gained=xp_gained, 
                                            channel_id=channel_id, 
                                            message_content=message_content)
                session.add(new_activity)

            # Atualizar a última data de atividade
            self.set_last_xp_update(user_id, activity_type, datetime.utcnow())

            session.commit()
        except Exception as e:
            print(f"Erro ao registrar ou atualizar a atividade do usuário: {e}")
            session.rollback()
        finally:
            session.close()
            
    async def set_config(self, key, value, description=None):
        session = self.Session()
        config_entry = session.query(AppConfig).get(key)
        if config_entry:
            config_entry.value = value
            if description is not None:
                config_entry.description = description
        else:
            new_config = AppConfig(key=key, value=value, description=description)
            session.add(new_config)
        session.commit()
        session.close()

    async def get_config(self, key):
        session = self.Session()
        config_entry = session.query(AppConfig).get(key)
        session.close()
        return config_entry.value if config_entry else None

    async def remove_config(self, key):
        session = self.Session()
        config_entry = session.query(AppConfig).get(key)
        if config_entry:
            session.delete(config_entry)
            session.commit()
        session.close()
        
    async def subtract_user_xp(self, user_id, xp_amount):
        session = self.Session()
        user_xp = session.query(UserXP).filter_by(user_id=user_id).first()

        if user_xp:
            if user_xp.xp >= xp_amount:
                user_xp.xp -= xp_amount  # Subtrai o XP
                user_xp.last_updated = datetime.utcnow()

                # Registrar a atividade de subtração de XP
                subtraction_activity = UserActivity(
                    user_id=user_id, 
                    activity_type='ticket_purchase', 
                    xp_gained=-xp_amount  # Negativo, pois é uma subtração
                )
                session.add(subtraction_activity)

                session.commit()
                return True  # Sucesso
            else:
                return False  # Falha, XP insuficiente
        else:
            return False  # Falha, usuário não encontrado

        session.close()
        
    async def get_total_invested_xp(self, user_id):
        session = self.Session()
        try:
            total_xp = session.query(func.sum(GiveawayEntry.tickets * Giveaway.xp_per_ticket))\
                            .join(Giveaway, Giveaway.id == GiveawayEntry.giveaway_id)\
                            .filter(GiveawayEntry.user_id == user_id, Giveaway.status == 'active')\
                            .scalar()
            return total_xp if total_xp else 0
        except Exception as e:
            print(f"Erro ao calcular o total de XP investido: {e}")
            return 0
        finally:
            session.close()

    async def get_all_giveaway_ids(self):
        session = self.Session()
        try:
            giveaways = session.query(Giveaway.id).filter(Giveaway.status == 'active').all()
            #print(f"IDs dos sorteios: {giveaways}")
            return [giveaway.id for giveaway in giveaways]
        except Exception as e:
            print(f"Erro ao buscar IDs dos sorteios: {e}")
            return []
        finally:
            session.close()
            
    async def get_all_giveaway_ids_all_columns(self):
        session = self.Session()
        try:
            giveaways = session.query(Giveaway).all()
            return [giveaway for giveaway in giveaways]
        except Exception as e:
            print(f"Erro ao buscar IDs dos sorteios: {e}")
            return []
        finally:
            session.close()
            
    async def get_user_xp_balance(self, user_id):
        session = self.Session()
        try:
            # Obter o total de XP do usuário
            user_xp = session.query(UserXP).filter_by(user_id=user_id).first()
            if user_xp:
                total_xp = user_xp.xp

                # Calcular o total de XP gasto em entradas de sorteio
                total_spent_xp = session.query(func.sum(GiveawayEntry.tickets * Giveaway.xp_needed))\
                                        .join(Giveaway, GiveawayEntry.giveaway_id == Giveaway.id)\
                                        .filter(GiveawayEntry.user_id == user_id)\
                                        .scalar() or 0

                # Calcular o saldo de XP
                xp_balance = total_xp - total_spent_xp
                return xp_balance
            else:
                return 0
        except Exception as e:
            print(f"Erro ao buscar saldo de XP do usuário: {e}")
            return 0
        finally:
            session.close()
            
    # Dentro da classe Database

    async def get_war_thunder_data(self, keyword):
        session = self.Session()
        try:
            vehicle = session.query(WarThunderData).filter(
                (
                    WarThunderData.alt_name.ilike(f"%{keyword}%"),
                    WarThunderData.wk_name.ilike(f"%{keyword}%"),
                    WarThunderData.name.ilike(f"%{keyword}%")
                )
            ).first()
            return vehicle
        except Exception as e:
            print(f"Erro ao buscar dados do War Thunder: {e}")
            return None
        finally:
            session.close()
            
    async def load_war_thunder_data(self):
        session = self.Session()
        try:
            data = session.query(WarThunderData).all()
            return data
        except Exception as e:
            print(f"Erro ao carregar dados do War Thunder: {e}")
            return []
        finally:
            session.close()

    async def get_number_of_participants(self, giveaway_id):
        """
        Retorna o número de participantes únicos em um sorteio.
        """
        session = self.Session()
        try:
            number_of_participants = session.query(GiveawayEntry).filter_by(giveaway_id=giveaway_id).distinct(GiveawayEntry.user_id).count()
            return number_of_participants
        except Exception as e:
            print(f"Erro ao obter número de participantes: {e}")
            return 0
        finally:
            session.close()

    async def get_tickets_sold(self, giveaway_id):
        """
        Retorna o número total de tickets vendidos para um sorteio.
        """
        session = self.Session()
        try:
            tickets_sold = session.query(func.sum(GiveawayEntry.tickets)).filter_by(giveaway_id=giveaway_id).scalar()
            return tickets_sold or 0
        except Exception as e:
            print(f"Erro ao obter tickets vendidos: {e}")
            return 0
        finally:
            session.close()         

    async def update_giveaway_with_message_id(self, giveaway_id, message_id):
        session = self.Session()
        try:
            # Busca o sorteio pelo ID
            giveaway = session.query(Giveaway).filter_by(id=giveaway_id).first()
            if giveaway:
                # Atualiza o ID da mensagem
                giveaway.message_id = message_id
                session.commit()
            else:
                print(f"Sorteio com ID {giveaway_id} não encontrado.")
        except Exception as e:
            print(f"Erro ao atualizar o ID da mensagem para o sorteio: {e}")
            session.rollback()
        finally:
            session.close()
            
    async def add_giveaway_winner(self, giveaway_id, user_id):
        session = self.Session()
        try:
            winner = GiveawayWinner(giveaway_id=giveaway_id, user_id=user_id)
            session.add(winner)
            session.commit()
        except Exception as e:
            print(f"Erro ao adicionar ganhador do sorteio: {e}")
            session.rollback()
        finally:
            session.close()
            
    async def update_giveaway_message_id(self, giveaway_id, message_id):
        session = self.Session()
        try:
            giveaway = session.query(Giveaway).filter_by(id=giveaway_id).first()
            if giveaway:
                giveaway.message_id = message_id
                session.commit()
        except Exception as e:
            print(f"Erro ao atualizar o ID da mensagem do sorteio: {e}")
            session.rollback()
        finally:
            session.close()
            
    async def get_all_giveaways(self):
        session = self.Session()
        try:
            all_giveaways = session.query(Giveaway).all()
            return all_giveaways
        except Exception as e:
            print(f"Erro ao buscar todos os sorteios: {e}")
            return []
        finally:
            session.close()
            
    async def get_giveaway_message_id(self, giveaway_id):
        session = self.Session()
        try:
            
            query =  session.query(Giveaway).filter_by(id=giveaway_id)#.first()
            
            # Para ver a consulta SQL gerada
            sql_query = str(query.statement.compile(compile_kwargs={"literal_binds": True}))
            print(sql_query)

            # Executa a consulta
            giveaway = query.first()
            
            return giveaway.message_id if giveaway else None
        except Exception as e:
            print(f"Erro ao buscar o ID da mensagem do sorteio: {e}")
            return None
        finally:
            session.close()
            
    
            
    async def remove_giveaway_entry(self, giveaway_entry_id):
        session = self.Session()
        try:
            # Localizar a entrada do sorteio no banco de dados usando o ID
            entry = session.query(GiveawayEntry).filter_by(id=giveaway_entry_id).first()
            if entry:
                # Remover a entrada do sorteio
                session.delete(entry)
                session.commit()
            else:
                print(f"Entrada de sorteio com ID {giveaway_entry_id} não encontrada.")
        except Exception as e:
            print(f"Erro ao remover a entrada do sorteio: {e}")
            session.rollback()
        finally:
            session.close()
            
            
    async def add_suggestion(self, user_id, suggestion_text):
        session = self.Session()
        try:
            new_suggestion = Suggestion(user_id=user_id, suggestion_text=suggestion_text, status='pending')
            session.add(new_suggestion)
            session.commit()
        except Exception as e:
            print(f"Erro ao adicionar sugestão: {e}")
            session.rollback()
        finally:
            session.close()

    async def add_suggestion_vote(self, suggestion_id, user_id):
        session = self.Session()
        try:
            vote = SuggestionVote(suggestion_id=suggestion_id, user_id=user_id)
            session.add(vote)
            session.commit()
        except Exception as e:
            print(f"Erro ao adicionar voto: {e}")
        finally:
            session.close()

    async def count_suggestion_votes(self, suggestion_id):
        session = self.Session()
        try:
            count = session.query(SuggestionVote).filter_by(suggestion_id=suggestion_id).count()
            return count
        except Exception as e:
            print(f"Erro ao contar votos: {e}")
        finally:
            session.close()


        
        