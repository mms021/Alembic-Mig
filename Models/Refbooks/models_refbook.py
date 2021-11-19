from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime, ForeignKey, Index, Integer, JSON, Numeric, String, Table, Text, UniqueConstraint, text ,create_engine
from sqlalchemy.dialects.postgresql import JSONB, OID, UUID
from sqlalchemy.orm import create_session, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
import uuid

from ..models_Abstract import Entity, SystemInfoEntity , CodeNameEntity , VersioningEntity
from ..LifeCycles.models_lifeCycle import LifeCycle , Status , StepLifeCycle
from ..Core.models_core import Person , ObjectType , Action
#metadata = MetaData(schema="refbook")
Base = declarative_base()


class Component(Entity, SystemInfoEntity ,CodeNameEntity, Base):
    __tablename__ = 'components'
    __tableargs__ = {'comment': 'Состовляющие производственного потенциала' }
    __table_args__ = {'schema': 'refbook'}
    

class RefBook(Entity, SystemInfoEntity ,CodeNameEntity, Base):
    __tablename__ = 'ref_books'
    __tableargs__ = {'comment': 'Справочник' }
    __table_args__ = {'schema': 'refbook'}
    code = Column(String(32), comment='Код справочника. Уникальный')
    name = Column(String(32), comment='Наименование справочника')


class TypeValue(Entity, SystemInfoEntity, Base):
    __tablename__ = 'type_values'
    __tableargs__ = {'comment': 'Хранение основных данных справочника типов значений' }
    __table_args__ = {'schema': 'refbook'}
   


