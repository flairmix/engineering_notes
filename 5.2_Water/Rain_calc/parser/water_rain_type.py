
from  water_parser import * 


def main():

    time_start = time.time()
    
    url = 'https://www.vo-da.ru/tool/rain-type'
    input_field_city = "input__control"
    drop_down_menu = '//*[@id="rain_type_tool"]/div[2]/div/div/div/div[2]/div/ul/li[1]'

    #create df
    data_city_100 = pd.read_csv('city_100.csv')
    columns_rain_type = ['city', 'district', 'n_P>1', 'n_P<1', 'mr', 'y']
    df_rain_type = pd.DataFrame(columns=columns_rain_type)

    #selenium parameters and init 
    browser = start_browser(headless_on=True)
    driver_rain_type = browser.get(url)

    #start parse 
    for city in data_city_100['city']:

        write_field_by_class_name(browser=browser, class_name=input_field_city, input=city)
        time.sleep(1)
        click_button_by_xpath(browser=browser, xpath=drop_down_menu)

        soup_page = get_bs4_page(browser, parser='html.parser')
        soup_find = soup_page.find_all(attrs={"class":{"rain-param", "rain-type-params"}})

        str_district = str(soup_find[0].text)
        stop_str_0 = str_district.find('Значения')
        district = str_district[:stop_str_0]
        list_str = [str(soup_find[i].text) for i in range(1, 5)]

        df_city_one = pd.DataFrame([[city] + [district] + list_str], columns=columns_rain_type)
        df_rain_type = df_rain_type.append(df_city_one)

        print(df_rain_type.tail(1))


    #edit df to final form 
    df_layer = df_rain_type.set_index('city')
    df_layer.to_csv('rain_type.csv')
    
    
    print(f"--- {round((time.time() - time_start), 5)} seconds ---" )


if __name__ == "__main__":
    main()


