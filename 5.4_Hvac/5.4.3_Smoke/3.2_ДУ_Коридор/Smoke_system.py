from typing import Literal

smoke_system_type = Literal(
    'Противодымная вытяжная из помещения',
    'Противодымная вытяжная из смежного помещения',
    'Противодымная приточная - компенсация',
    'Противодымная приточная - подпор',
) 

class Smoke_system():
    def __init__(self):
        pass