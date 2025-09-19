from database import get_db
from repository import DocumentRepository

def main():
    # Получаем сессию базы данных
    db = next(get_db())
    
    # Создаем репозиторий с внедрением зависимости
    repo = DocumentRepository(db)
    
    # Добавление документа
    doc = repo.add_document(
        title='СНиП 2.03.01-84',
        number='2.03.01-84',
        date_str='1984-01-01',
        doc_type='СНиП',
        status='действующий',
        version='1.0'
    )
    
    # Добавление пунктов
    repo.add_point(doc.id, '1.1', 'Пункт 1.1: Общие положения')
    repo.add_point(doc.id, '1.2', 'Пункт 1.2: Требования к материалам')
    
    # Закрываем сессию
    db.close()

if __name__ == "__main__":
    main()
