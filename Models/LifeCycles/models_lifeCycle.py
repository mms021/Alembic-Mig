from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime, ForeignKey, Index, Integer, JSON, Numeric, String, Table, Text, UniqueConstraint, text ,create_engine
from sqlalchemy.dialects.postgresql import JSONB, OID, UUID
from sqlalchemy.orm import create_session, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
import uuid
from ..models_Abstract import Entity, SystemInfoEntity , CodeNameEntity , VersioningEntity

Base = declarative_base()

class LifeCycle(Entity, SystemInfoEntity ,CodeNameEntity, Base):
    __tablename__ = 'life_cycles'
    __tableargs__ = {'comment': 'Сущность предназначена для ведения основных данных справочника жизненные циклы' }
    __table_args__ = {'schema': 'conf_lc'}
    

class Status(Entity, SystemInfoEntity ,CodeNameEntity, Base):
    __tablename__ = 'statuses'
    __tableargs__ = {'comment': 'Статусы жизненого цикла' }
    __table_args__ = {'schema': 'conf_lc'}
    phase_id = Column(UUID, comment='Ссылка на фазу жизненного цикла')
    
    phase = relationship(u'EnumItem')


class StepLifeCycle(Entity, SystemInfoEntity,Base):
    __tablename__ = 'step_life_cycles'
    __tableargs__ = {'comment': 'Сущность предназначена для ведения списка переходов статусов жизненных циклов объектов' }
    __table_args__ = (
        Index('ix_step_life_cycles_owner_id_life_cycle_id_status_id_next_stat', 'owner_id', 'life_cycle_id', 'status_id', 'next_status_id', unique=True),
        {'schema': 'conf_lc'}
    )
    life_cycle_id = Column(UUID, nullable=False,  comment='Этапы жизненного цикла_УИД')
    status_id = Column(ForeignKey('conf_lc.statuses.id', ondelete='RESTRICT'), index=True, comment='Текущий статус')
    next_status_id = Column(ForeignKey('conf_lc.statuses.id', ondelete='RESTRICT'), nullable=False, index=True, comment='Разрешенный статус перехода')
    
    next_status = relationship(u'Status', primaryjoin='StepLifeCycle.next_status_id == Status.id')
    status = relationship(u'Status', primaryjoin='StepLifeCycle.status_id == Status.id')
