#### активация venv

env\Scripts\activate.bat

или 

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
env\Scripts\Activate.ps1

<br>

#### alembic
```
alembic init alembic
```

в alembic.ini
```
sqlalchemy.url = sqlite:///normative_docs.db
```

в alembic/env.py
```
from models import Base

target_metadata = Base.metadata
```

```
alembic revision --autogenerate -m "Initial migration"
```

```
alembic upgrade head
```

#### внесение изменений 

```
alembic revision --autogenerate -m "add_unique_constraint_to_number"
alembic upgrade head
```

<br>