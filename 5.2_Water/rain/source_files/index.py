import pandas as pd 

_path = 'source_files\\'

df_rain_coeff_c = pd.read_csv(f"{_path}df_coeff_c.csv", index_col='city') 
df_rain_layer_h_a = pd.read_csv(f"{_path}layer_h_a.csv", index_col='city') 
df_rain_q20 = pd.read_csv(f"{_path}rain_q20.csv", index_col='city') 
df_rain_type = pd.read_csv(f"{_path}rain_type.csv", index_col='city') 

dict_rain_coeff_c = df_rain_coeff_c.to_dict()
dict_rain_layer_h_a = df_rain_layer_h_a.to_dict()
dict_rain_q20 = df_rain_q20.to_dict()
dict_rain_type = df_rain_type.to_dict()
