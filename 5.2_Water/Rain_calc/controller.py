from litestar import Controller, get
from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
import pandas as pd
from pydantic import Field, ValidationError, validate_call
from typing_extensions import Annotated
from typing import Optional, Literal

from difflib import get_close_matches

df_rain_coeff_c = pd.read_csv("calculations\Rain_calc\source_files\df_coeff_c.csv") 
df_rain_layer_h_a = pd.read_csv("calculations\Rain_calc\source_files\layer_h_a.csv") 
df_rain_q20 = pd.read_csv("calculations\Rain_calc\source_files\\rain_q20.csv") 
df_rain_type = pd.read_csv("calculations\Rain_calc\source_files\\rain_type.csv") 

class RainController(Controller):
    path = "/rain_calc"
    tags=["rain_calc"]

    @get("/city_rain_parameters")
    @validate_call
    async def rain_parameters(self,
                        city_input: Annotated[str, Field(min_length=1)] = "Москва",
                        ) -> dict[str, float]:
        try:
            #finding city
            city = get_close_matches(city_input.lower(), df_rain_coeff_c["city"].to_list(), n=1 )[0]
            
            if city:
                #coeff_c
                output_city_info = df_rain_coeff_c.loc[df_rain_coeff_c["city"] == city].to_dict(orient='records')[0]

                #layer_h_a
                layer_h_a = df_rain_layer_h_a.loc[df_rain_layer_h_a["city"] == city].values[0]
                output_city_info['layer_h_a'] = layer_h_a[1]
                
                #rain_q20
                rain_q20 = df_rain_q20.loc[df_rain_q20["city"] == city].values[0]
                for i in range (1, len(df_rain_q20.columns)):
                    output_city_info[df_rain_q20.columns[i]] = rain_q20[i]

                #rain_type
                rain_type = df_rain_type.loc[df_rain_type["city"] == city].values[0]
                for i in range (1, len(df_rain_type.columns)):
                    output_city_info[df_rain_type.columns[i]] = rain_type[i]

            return output_city_info

        except ValidationError as exc:
            return {"ValidationError": -1}
        

        

