import re 
import pandas as pd 


str1 = "q20 = 234.0 при P = 50"
str2 ="q20 = 1                   при P = 20"
str3 = "q20 = 12y                      при P = 10"
str4 = "q20 = 1.0                  при P = 5"
str5 = "q20 = 1101.0                    при P = 2"
str6 = "q20 = 91.0                    при P = 1"

        
list_str = [str1, str2,str3,str4,str5,str6]

def rain_parse_q20(result_str):
    for i in result_str[6:10]:
        if not i.isdigit() and not i in [' ', '.']: 
            print(f'fail in parse string q20 - \n {result_str}')
            print('not digit')
            return 0

        print(float(result_str[6:10]))
        return float(result_str[6:10])


a = float(str1[6:10])

for i in list_str:
    rain_parse_q20(i)





