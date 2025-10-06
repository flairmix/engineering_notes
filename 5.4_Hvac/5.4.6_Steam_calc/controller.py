
from litestar import Controller, get
from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
from pydantic import Field, ValidationError, validate_call
from typing_extensions import Annotated
from typing import Optional, Literal

from calculations.Steam_calc.steam_properties_init import init_steam_properties_df

df_steam_properties = init_steam_properties_df()

class SteamPipeController(Controller):
    path = "/steam_pipe_calc"
    tags=["steam_pipe_calc"]

    @get("/steam_parameters")
    @validate_call
    async def steam_parameters_by_pressure(self, 
                                  steam_pressure_bar: Annotated[float, Field(gt=0, lt=105)] = 1.0,
                                  ) -> dict[str, float]:
        try:
            #TODO find andselect by minimum difference 
            df = df_steam_properties.loc[df_steam_properties["Давление насыщенного пара (абс) бар"] == round(steam_pressure_bar, 2)]

            return df.to_dict(orient='records')

        except ValidationError as exc:
            return {"ValidationError": -1}
        

    @get("/steam_pipe")
    @validate_call
    async def steam_pipe_calc_dn(self, 
                                  steam_pressure_bar: Annotated[float, Field(gt=0, lt=105)] = 1.0,
                                  steam_flow_t_h: Annotated[float, Field(gt=0)] = 10.0,
                                  ) -> dict[str, int]:
        try:
            # СП60 - 
            # 10.1.6 Диаметры трубопроводов следует принимать исходя из максимальных часовых расчетных расходов теплоносителя и допускаемых потерь давления.
            # При этом скорость пара следует принимать не более:

            # для перегретого пара при диаметре труб, мм:
            # - до 200 - 40 м/с;
            # - свыше 200 - 70 м/с;

            # для насыщенного пара при диаметре труб, мм:
            # - до 200 - 30 м/с;
            # - свыше 200 - 60 м/с.

            #TODO find andselect by minimum difference 
            df = df_steam_properties.loc[df_steam_properties["Давление насыщенного пара (абс) бар"] == round(steam_pressure_bar, 2)]
            density = df["Плотность (пара) кг/м3"].values[0]
            dn_30 =  int(1000 * pow( (steam_flow_t_h * 4) / (density * 3.1415 * 3.6 * 30) , 0.5))
            dn_60 =  int(1000 * pow( (steam_flow_t_h * 4) / (density * 3.1415 * 3.6 * 60) , 0.5))
            
            return {
                "Плотность (пара) кг/м3" : density,
                "dn_мм" : dn_30 if dn_30 <200 else dn_60,
                "velocity_m_s" : 30 if dn_30 <200 else 60,
                }

        except ValidationError as exc:
            return {"ValidationError": -1}
        


