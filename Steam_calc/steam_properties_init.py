import pandas as pd 


def init_steam_properties_df():
    return pd.read_csv('calculations\Steam_calc\Свойства насыщенного водяного пара.csv')