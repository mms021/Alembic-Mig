#from typing_extensions import Required
from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime, ForeignKey, Index, Integer, JSON, Numeric, String, Table, Text, UniqueConstraint, text , TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB, OID, UUID
import uuid
from sqlalchemy.orm import create_session, relationship
from sqlalchemy.sql.sqltypes import BOOLEAN
from sqlalchemy.ext.declarative import declarative_base
#from .LifeCycles.models_lifeCycle import LifeCycle as Lc , Status  as St
from sqlalchemy.ext.declarative import as_declarative ,declared_attr

Base_ABS = declarative_base()

class Entity(Base_ABS):
    __abstract__ = True
    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
   
class SystemInfoEntity(Base_ABS):
    __abstract__ = True
    code_db = Column(String(2),nullable=False, comment='Значение уникального идентификатора развернутой системы') 
    @declared_attr
    def owner_id(cls):
        return Column(ForeignKey('base.participants.id', ondelete='RESTRICT'), nullable=False, index=True,  comment='Ссылка на организацию владельца данных')
    
    @declared_attr
    def owner(cls):
        return relationship("Participant" )
        
    @declared_attr
    def domain_id(cls):
        return Column(ForeignKey('base.domains.id', ondelete='RESTRICT'), index=True, comment='Домен владельца записи')
    
    @declared_attr
    def domain(cls):
        return relationship('Domain')
    #owner_id = Column(String, nullable=False, index=True,  comment='Ссылка на организацию владельца данных')
    #domain_id = Column(String, index=True, comment='Домен владельца записи')
    creator_id = Column(String , nullable=False, server_default=text("\"current_user\"()") , comment='Пользователь, создавший объект' )
    create_date = Column(TIMESTAMP(timezone=False), nullable=False, server_default=text("now()"), comment='Дата создания записи' )
    editor_id = Column(String, nullable=False, server_default=text("\"current_user\"()"), comment='Пользователь, отредактировавший объект. При первичном создании совпадает с создателем.')
    edit_date = Column(TIMESTAMP(timezone=False),nullable=False, server_default=text("now()"), comment='Дата последнего редактирования' )
    removed = Column(Boolean,nullable=False, default=False, server_default=text("false") ,  comment='Признак удаленной записи')
    released = Column(Boolean, nullable=False, default=False, server_default=text("false") ,  comment='Признак опубликованной записи')
    

class CodeNameEntity(Base_ABS):
    __abstract__ = True

    code = Column(String(32), nullable=False, comment='Код' )
    name = Column(String(255), nullable=False, comment='Полное наименование') 
    name_short = Column(String(255), comment='Сокращенное наименование')
    name_abbr = Column(String(255), comment='Абрревиатура наименования') 
    description = Column(Text, comment=u'\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435')


class VersioningEntity(Base_ABS):  
    __abstract__ = True

    master_id = Column(UUID, comment='Уникальный идентицикатор, Мастер_УИД')
    is_master = Column(Boolean, comment='Тип записи')
    release_id = Column(UUID, comment='Ссылка на последнюю опубликованную запись')
    work_id = Column(UUID,server_default=text("'00000000-0000-0000-0000-000000000000'::uuid"), comment='Ссылка на рабочую версию записи')
    status_id = Column(UUID,  comment='Статус записи')
    life_cycle_id = Column(UUID, comment='Жизненный цикл записи')
    version = Column(Numeric, comment='Номер версии записи',nullable=False,  default= 0)
    iteration = Column(Numeric, comment='Номер итерации записи в пределах версии',nullable=False,  default= 0)
    

if __name__ == "__main__":
    Entity()
    CodeNameEntity()
    VersioningEntity()
    SystemInfoEntity()












