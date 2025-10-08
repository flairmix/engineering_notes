from typing import Literal, Optional, List
from Room import Room
from Corridor import Corridor


class Smoke_system():
    def __init__(self, name, number,
               smoke_system_type = Literal[
                'Противодымная вытяжная из помещения',
                'Противодымная вытяжная из смежного помещения',
                'Противодымная приточная - компенсация',
                'Противодымная приточная - подпор',
                ],  
                room = Optional(Room, None),
                room_list = Optional(List[Room], None),
                corridor = Optional(Corridor, None),
                 ):
        
        self.number = number
        self.name = name
        self.smoke_system_type = smoke_system_type
        self.served_room = room
        self.served_list_of_room = room_list
        self.served_corridor = corridor

   