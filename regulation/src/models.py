from sqlalchemy import (
    create_engine, 
    Column, 
    Integer, 
    String, 
    Date, 
    ForeignKey, 
    Index
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import date
from sqlalchemy.schema import UniqueConstraint

Base = declarative_base()

class Document(Base):
    __tablename__ = 'documents'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(String(255), nullable=False, index=True, unique=True)
    version = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False, unique=True)
    date = Column(Date, index=True)
    type = Column(String(100))
    status = Column(String(50))
    
    # Уникальное ограничение для номера и версии
    __table_args__ = (
        UniqueConstraint('number', 'version', name='uix_number_version'),
    )
    
    points = relationship(
        "Point", 
        back_populates="document",
        cascade="all, delete-orphan"
    )

class Point(Base):
    __tablename__ = 'points'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(
        Integer, 
        ForeignKey('documents.id', ondelete='CASCADE'),
        nullable=False
    )
    number = Column(String(50), index=True)
    text = Column(String, nullable=False)
    comments = Column(String)
    
    document = relationship(
        "Document", 
        back_populates="points"
    )
    
    # Индекс для быстрого поиска по номеру пункта
    __table_args__ = (
        Index('idx_document_point_number', 'document_id', 'number'),
    )
