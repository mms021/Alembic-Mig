from sqlalchemy import  ARRAY, BigInteger, Boolean, Column, Date, DateTime, ForeignKey, Index, Integer, JSON, Numeric, String, Table, Text, UniqueConstraint, text ,create_engine , ForeignKeyConstraint  , PrimaryKeyConstraint , UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, OID, UUID , TIMESTAMP
from sqlalchemy.orm import create_session, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
import uuid

from ..models_Abstract import Entity, SystemInfoEntity, CodeNameEntity, VersioningEntity
from ..LifeCycles.models_lifeCycle import LifeCycle , Status , StepLifeCycle


Base = declarative_base()

class Domain(Entity, Base):
    __tablename__ = 'domains'
    __tableargs__ = {'comment': 'Домен' }
    __table_args__ = (
        UniqueConstraint('participant_id', 'parent_participant_id', 'start_date'),
        {'schema': 'base'})
    participant_id = Column(UUID, nullable=False, comment='ИД организации')
    parent_participant_id = Column(UUID ,nullable=False,  comment='ИД вышестоящей организации')
    start_date = Column(TIMESTAMP(timezone=False),nullable=False ) 
    
    object_setting = relationship('ObjectSetting')
    participant = relationship('Participant')
    components = relationship('Component')
    ref_books = relationship('RefBook')
    type_values = relationship('TypeValue')


class Enum(Entity, Base):
    __tablename__ = 'enums'
    __tableargs__ = {'comment': 'Заголовки системных справочников' }
    __table_args__ = {'schema': 'base'}
    code = Column(String(32), comment='Код справочника' , nullable=False, unique=True, )
    name = Column(String(255),nullable=False, comment='Наименование справочника')
    description = Column(String(255) , comment='Описание справочника') 


class EnumItem(Entity, Base):
    __tablename__ = 'enum_items'
    __table_args__ = (
        UniqueConstraint('code', 'enum_id'),
        { 'comment': 'Элементы справочников относящиеся к base.enums' , 'schema': 'base'},
    )
    enum_id = Column(UUID, ForeignKey("base.enums.id", ondelete='RESTRICT' ),nullable=False, index=True, comment='Ссылка на base.enums')
    code = Column(String(32) , comment='Код элемента справочника', nullable=False ) 
    name = Column(String(255) , comment='Наименование элемента справочника', nullable=False) 
    description = Column(String(255) , comment='Описание элемента справочника') 
    
    enum = relationship(u'Enum')


class Object(Entity, Base):
    __tablename__ = 'objects'
    __tableargs__ = {'comment': 'Сущность предназначена для хранения списка бизнес-объектов системы' }
    __table_args__ = {'schema': 'base'}
    code = Column(String(40), nullable=False, unique=True, server_default=text("''::character varying"), comment='Код') 
    name = Column(String(255) , comment='Полное наименование') 
    name_list = Column(String(255) , comment='Наименование формы со списком') 
    name_detail = Column(String(255) , comment='Наименование формы редактирования') 
  

class ObjectSetting(Entity, SystemInfoEntity, Base):
    __tablename__ = 'object_settings'
    __tableargs__ = {'comment': 'Сущность предназначена для ведения настроек поведения бизнес-объектов' }
    __table_args__ = {'schema': 'base'}
    life_cycle_id = Column(ForeignKey('conf_lc.life_cycles.id', ondelete='RESTRICT'), nullable=False, index=True, comment='Ссылка на жизненный цикл')
    object_id = Column(ForeignKey('base.objects.id') ,nullable=False, index=True, comment='Ссылка на бизнес-объект')
    begin_date = Column(TIMESTAMP(timezone=False) , comment='Дата начала применяемости настроек') 
    end_date = Column(TIMESTAMP(timezone=False) , comment='Дата окончания применяемости настроек') 
    type_setting_id = Column(ForeignKey(u'base.enum_items.id', ondelete=u'RESTRICT'),nullable=False, index=True,  comment='Тип применимости настроек по дате')
    iterated = Column(Boolean,nullable=False, comment='Признак итерирования объектов', default=False)
    
    domain = relationship('Domain')
    life_cycles = relationship("LifeCycle", secondary='conf_lc.life_cycles', back_populates="life_cycle_log")
    object = relationship('Object')
    owner = relationship('Participant')
    type_setting = relationship('EnumItem')


class FunctionalRole(Entity, Base):
    __tablename__ = 'functional_roles'
    __tableargs__ = {'comment': 'Функциональные роли' }
    __table_args__ = {'schema': 'base'}


class FunctionalGroup(Entity, Base):
    __tablename__ = 'functional_groups'
    __tableargs__ = {'comment': 'Функциональные группы' }
    __table_args__ = {'schema': 'base'}
    functional_role_id = Column(ARRAY(Text()) ,  comment='Массив функциональных ролей') 


class LifeCycleLog(Entity, Base):
    __tablename__ = 'life_cycle_log'
    __tableargs__ = {'comment': 'Аудит переходов статусов ЖЦ' }
    __table_args__ = {'schema': 'base'}
    object_id = Column(UUID, nullable=False, comment='Ссылка на бизнес-объект')
    life_cycle_id = Column(ForeignKey('conf_lc.life_cycles.id', ondelete='RESTRICT'), nullable=False, index=True, comment='Ссылка на ЖЦ"')
    status_id = Column(ForeignKey('conf_lc.statuses.id', ondelete=u'RESTRICT'), nullable=False, index=True , comment='Ссылка на статус')
    life_cycle_id = Column(UUID, nullable=False, comment='Ссылка на ЖЦ"')
    status_id = Column(UUID, nullable=False, comment='Ссылка на статус')
    changed_date = Column(TIMESTAMP(timezone=False ,precision=0), nullable=False, server_default=text("now()"), comment='Дата смены статуса')
    changed_id = Column(String,server_default=text("\"current_user\"()"), comment='Кто сменил статус')
    comment = Column(Text, comment='Комментарий')

    life_cycles = relationship("LifeCycle", secondary='conf_lc.life_cycles', back_populates="life_cycle_log")
    status = relationship('Status')


class LinkSolutionObject(Entity, Base):
    __tablename__ = 'link_solution_object'
    __tableargs__ = {'comment': 'LinkSolutionObject' }
    __table_args__ = {'schema': 'base'}
    solution_id = Column(UUID , ForeignKey('base.solution.id'))
    object_type_id = Column(UUID )
    classifier_id = Column(UUID, nullable=False)


class Participant(Entity, SystemInfoEntity, CodeNameEntity, VersioningEntity, Base):
    __tablename__ = 'participants'
    __tableargs__ = {'comment': 'Участник информационного взаимодействия. Сокращенно - УИВ.'}
    __table_args__ = {'schema': 'base'}
    inn  = Column(String(12), comment='ИНН')
    kpp = Column(String(9), comment='КПП')
    okpo = Column(String(12), comment='ОКПО')
    actual_address = Column(String(255), comment='Фактический адрес')
    legal_address = Column(String(255), comment='Юридический адрес')
    latitude = Column(Numeric(20, 15), comment='Широта',  server_default=text("0.0"))
    longitude = Column(Numeric(20, 15), comment='Долгота',  server_default=text("0.0"))

    domain = relationship('Domain')
    owner = relationship('Participant', remote_side=[id])
    components = relationship('Component')
    ref_books = relationship('RefBook')
    type_values = relationship('TypeValue')


class PersonFunctionalGroup(Entity, Base):
    __tablename__ = 'person_functional_groups'
    __tableargs__ = {'comment': 'Связь пользователей и функциональных групп' }
    __table_args__ = {'schema': 'base'}
    functional_group_id = Column(ARRAY(Text()), comment='Массив функциональных групп') 


class PersonSetting(Entity, Base):
    __tablename__ = 'person_settings'
    __tableargs__ = {'comment': 'Персональные настройки меню' }
    __table_args__ = {'schema': 'base'}
    person_id = Column(Text, nullable=False, unique=True, server_default=text("\"current_user\"()")) 
    action_id = Column(ARRAY(UUID()), comment='Ссылка на core.actions')


class SettingCounter(Entity, Base):
    __tablename__ = 'setting_counter'
    __tableargs__ = {'comment': 'SettingCounter' }
    __table_args__ = {'schema': 'base'}
    entity = Column(String(255) ) 
    cycle_id = Column(UUID, ForeignKey(StepLifeCycle.id) )
    mask = Column(String(255) ) 
    begin_date = Column(TIMESTAMP(timezone=False)) 


class Counter(Entity, Base):
    __tablename__ = 'counter'
    __tableargs__ = {'comment': 'Counter' }
    __table_args__ = {'schema': 'base'}
    setting_counter_id = Column(UUID , ForeignKey('base.setting_counter.id'))
    code = Column(String(255)) 
    value = Column(Integer)  


class Solution(Entity, Base):
    __tablename__ = 'solution'
    __tableargs__ = {'comment': 'Solution' }
    __table_args__ = {'schema': 'base'}
    code = Column(String(255)) 
    name = Column(String(255))  

