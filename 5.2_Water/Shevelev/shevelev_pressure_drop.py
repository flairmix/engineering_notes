# from litestar import Controller, get
# from litestar.exceptions import HTTPException
# from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
# from pydantic import Field, ValidationError, validate_call
# from typing_extensions import Annotated
# from typing import Optional, Literal


# https://prostobuild.ru/onlainraschet/244-gidravlicheskiy-raschet-truboprovoda-onlayn.html

g = 9.81

class ShevelevController(Controller):
    path = "/shevelev_tables"
    tags=["shevelev_tables"]

    @get("/")
    @validate_call
    async def shevelev_pressure_drop(self, 
                                  pipe_type: Literal["steel_new", "cast_iron_new", "steel_used", "cast_iron_used"] = "steel_new",
                                  diameter: Annotated[int, Field(gt=0)] = 50,
                                  Flow_l_s: Annotated[float, Field(gt=0)] = 1,
                                  ) -> dict[str, float]:

        try:
            velocity = round(10**6 *((Flow_l_s*3.6) / (diameter**2) / 2826), 2)
            if (pipe_type in ("steel_new", "cast_iron_new") and pipe_type is not None):
                if (velocity >= 1.2):
                    # formula #6 - Shevelev book
                    i_1000 = round(1000 * 0.00107 * (velocity**2 / (diameter/1000) ** 1.3), 3)
                else:
                    # formula #7 - Shevelev book
                    i_1000 = round(1000 * 0.000912 * ((velocity**2) / ((diameter/1000) ** 1.3)) * pow(1+(0.867/velocity), 0.3), 3)

            elif (pipe_type in ("steel_used", "cast_iron_used")  and pipe_type is not None): 
                # formula #5a - Shevelev book
                _lambda = (0.0179/(pow(diameter/1000, 0.3))) * (pow(1+(0.867/velocity), 0.3))
                # formula #1 - Shevelev book
                i_1000 = round(1000 * _lambda * (1/(diameter/1000)) * (velocity**2 / (2*g)), 3)

            else:
                return {"velocity m/s": -1, 
                    "1000*i_mm/m": -1}

            return {"velocity m/s": velocity, 
                    "1000*i_mm/m": i_1000}
        
        except ValidationError as exc:
            return {"ValidationError": -1}
        