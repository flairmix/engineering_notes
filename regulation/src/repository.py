from sqlalchemy.orm import Session
from sqlalchemy import inspect

from models import Document, Point
from datetime import date

class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_document(
        self, 
        number: str, 
        version: str, 
        title: str, 
        date_str: str, 
        doc_type: str, 
        status: str
    ) -> Document:
        date_obj = date.fromisoformat(date_str)
        new_doc = Document(
            number=number,
            version=version,
            title=title,
            date=date_obj,
            type=doc_type,
            status=status
        )
        self.db.add(new_doc)
        self.db.commit()
        self.db.refresh(new_doc)
        return new_doc

    def add_point(
        self, 
        doc_id: int, 
        number: str, 
        text: str, 
        comments: str = ''
    ) -> Point:
        new_point = Point(
            document_id=doc_id,
            number=number,
            text=text,
            comments=comments
        )
        self.db.add(new_point)
        self.db.commit()
        self.db.refresh(new_point)
        return new_point
    
    def get_all_documents(self):
        return self.db.query(Document).all()

    def get_document_by_id(self, document_id: int):
        return self.db.query(Document).filter(Document.id == document_id).first()

    def get_document_by_number(self, document_number: int):
        return self.db.query(Document).filter(Document.number == document_number).first()

    def get_points_by_document(self, document_id: int):
        return self.db.query(Point).filter(Point.document_id == document_id).all()

    def get_documents_sorted_by_date(self):
        return self.db.query(Document).order_by(Document.date.desc()).all()

    def get_points_sorted_by_number(self, document_id: int):
        return self.db.query(Point).filter(Point.document_id == document_id).order_by(Point.number).all()
