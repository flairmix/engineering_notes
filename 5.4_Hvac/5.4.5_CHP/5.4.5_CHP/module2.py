from typing import Dict, List, Type, Any
import pandas as pd
import re

pd.set_option('display.max_columns', None)  # None = все колонки
pd.set_option('display.width', 200)    

class ModuleMeta(type):
    """Метакласс для автоматической регистрации экземпляров"""
    _registry: Dict[str, List['Module']] = {}

    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)
        if name != 'Module':
            cls._registry[new_class.__name__] = []
        return new_class

class Module(metaclass=ModuleMeta):
    """Базовый класс для всех модулей"""
    columns: List[str] = []
    dtypes: Dict[str, type] = {}
    index_col: str = 'u_id'

    def __init__(self, **kwargs):
        self._data = self._normalize_and_validate(kwargs)
        self.__class__._registry[self.__class__.__name__].append(self)

    def _normalize_key(self, key: str) -> str:
        """Нормализация имени ключа"""
        return re.sub(r'[^a-zA-Z0-9_]', '', key).lower()

    def _normalize_and_validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Нормализация и валидация данных"""
        normalized_data = {}
        
        # Нормализация ключей
        for key, value in data.items():
            normalized_key = self._normalize_key(key)
            normalized_data[normalized_key] = value

        # Валидация обязательных полей
        validated = {}
        for col in self.columns:
            normalized_col = self._normalize_key(col)
            if normalized_col not in normalized_data:
                raise ValueError(f"Отсутствует обязательное поле: {col}")
            
            try:
                validated[col] = self.dtypes[col](normalized_data[normalized_col])
            except (TypeError, ValueError) as e:
                raise TypeError(f"Ошибка в поле {col}: {e}") from e

        return validated

    @property
    def data(self) -> Dict[str, Any]:
        return self._data.copy()

    @classmethod
    def get_all_instances(cls, module_type: str = None) -> List['Module']:
        if module_type:
            return cls._registry.get(module_type, [])
        return [inst for instances in cls._registry.values() for inst in instances]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self._data[self.index_col]}>"

    def get_module_by_u_id(self, u_id: int) -> Dict[str, Any]:
        """Поиск по u_id"""
        try:
            for row in self.data:
                    if row['u_id'] == u_id:
                        return row.copy()
            
            return "Модуль u_id {u_id} не найден"
                    
        except (ValueError, TypeError):
                raise ValueError("Модуль u_id {u_id} не найден")
    
    @classmethod
    def get_all_instances(cls) -> List['Module']:
        """Возвращает все инстансы данного типа."""
        return cls._registry.get(cls.__name__, [])

    @classmethod
    def to_dataframe(cls) -> pd.DataFrame:
        """Создает DataFrame для всех инстансов данного типа."""
        data = [inst.data for inst in cls.get_all_instances()]
        return pd.DataFrame(data).astype(cls.dtypes).set_index(cls.index_col)
    



class HeatInputModule(Module):
    """Модуль теплового ввода с унифицированными именами"""
    columns = [
        'u_id', 
        'diameter', 
        'g_min_t_h', 
        'g_max_t_h', 
        'dt',
        'q_min_gcal_h', 
        'q_max_gcal_h',
        'system_volume_m3_h',
        'makeup_flow_t_h', 
        'fill_flow_t_h'
    ]
    
    dtypes = {
        'u_id': str,
        'diameter': int,
        'g_min_t_h': float,
        'g_max_t_h': float,
        'dt': int,
        'q_min_gcal_h': float,
        'q_max_gcal_h': float,
        'system_volume_m3_h': float,
        'makeup_flow_t_h': float,
        'fill_flow_t_h': float
    }
    
    @classmethod
    def get_all_instances(cls) -> List['HeatInputModule']:
        """Переопределяем метод для возврата инстансов конкретного типа."""
        return super().get_all_instances()

    @classmethod
    def to_dataframe(cls) -> pd.DataFrame:
        """Создает DataFrame для всех инстансов HeatInputModule."""
        return super().to_dataframe()

