from typing import Literal, Optional

class PipeAccessory:
    PipeAccessoryType = Literal[
        'ball_valve',       
        'butterfly_valve',   
        'gate_valve',        
        'control_valve',     
        'two_way_valve',     
        'three_way_valve',   
        'safety_valve',      
        'check_valve',       
        'flexible inserts (vibration compensators)',
        'air vents',
    ]

    def __init__(
            self,
            pipeAccessoryType: PipeAccessoryType,
            diameter: Literal[15, 20, 25, 32, 40, 50, 65, 80, 100, 125, 150, 200, 250, 300],
            pressure_rating_bar: float,
            Kvs: Optional[int] = None,
            material: Literal['стальной', 'латунный', 'чугунный'] = 'стальной',
            joining: Literal['фланцевый', 'муфтовый'] = 'фланцевый',
            handling: Literal['рукоятка', 'с голым штоком', 'редуктор'] = 'рукоятка',
            manufacturer: Optional[str] = None
        ):
        self.pipeAccessoryType = pipeAccessoryType
        self.diameter = diameter
        self.pressure_rating_bar = pressure_rating_bar
        self.Kvs = Kvs
        self.material = material
        self.joining = joining
        self.handling = handling
        self.manufacturer = manufacturer

    def __str__(self):
        return (self.get_name_and_parameters())

    def get_type_description_base(self) -> str:
        descriptions = {
            'ball_valve': "Шаровой кран",       
            'butterfly_valve': "Дисковый затвор",   
            'gate_valve': "Задвижка клиновая",        
            'control_valve': "Клапан регулирующий",     
            'two_way_valve': "Клапан регулирующий двухходовой",     
            'three_way_valve': "Клапан трехходовой",   
            'solenoid_valve': "Клапан соленоидный",   
            'safety_valve': "Клапан предохранительный",      
            'check_valve': "Клапан обратный",       
            'flexible inserts (vibration compensators)': "Гибкая вставка (виброкомпенсатор)",
            'air vents': "Воздухоотводчик",
        }
        return descriptions.get(self.pipeAccessoryType, 'Тип не определен')
    
    def get_name_and_parameters(self) -> str:
        base = f"{self.get_type_description_base()} " 
        joining = f"{self.material} {self.joining}, "
        dn_pn = f"DN{self.diameter}, PN{self.pressure_rating_bar}, "
        handling = f"{self.handling}"
        setting = ""
        addition_info = ""
        
        return (base + joining + dn_pn + handling + setting + addition_info)
    

