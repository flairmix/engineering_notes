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