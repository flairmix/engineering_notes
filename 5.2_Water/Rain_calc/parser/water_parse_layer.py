from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import re
from bs4 import BeautifulSoup


def click_button_by_xpath(browser, xpath):
    try:
        elem = browser.find_element(By.XPATH, xpath)
        elem.click()
    except:
        print(f"fail with button {xpath}")


def get_page_layer(browser, city):
    delay = 1
    try:
        # browser.find_element(By.XPATH, '//*[@id="title_region"]'.click()) #tab "choose city"
        browser.find_element(By.CLASS_NAME,  'input__control' ).clear()
        browser.find_element(By.CLASS_NAME,  'input__control' ).send_keys(city)
        time.sleep(delay)
        elem = browser.find_element(By.XPATH, '//*[@id="layer-place-search"]/div/ul/li[1]') #choose city 
        elem.click()
        browser.find_element(By.CLASS_NAME, 'layer_button__text').click()
        time.sleep(delay)
        elem = browser.find_element(By.ID, 'button_result') #tab "results"
        elem.click()
        time.sleep(delay)

    except: 
        print(f'{browser.current_url} not access - city {city}')

    return BeautifulSoup(browser.page_source, 'html.parser')


def parse_result_str(result_str):
    start_str = result_str.find('/sub>') + 8
    end_str = start_str + 5

    return float(result_str[start_str:end_str])


def main():
    
    time_start = time.time()

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.page_load_strategy = 'normal'
    browser = webdriver.Chrome('/Applications/Google Chrome', chrome_options=options)
    
    # tools from site
    url_layer = 'https://www.vo-da.ru/tool/layer'

    #water_layer
    driver_layer = browser.get(url_layer)

    data_city_100 = pd.read_csv('city_100.csv')

    columns_layer = ['city', 'ha']
    df_layer = pd.DataFrame(columns=columns_layer)


    for city in data_city_100['city']:
        result_str =  str(get_page_layer(browser, city).find_all('b'))
        ha = parse_result_str(result_str)

        df_city_one = pd.DataFrame([[city] + [ha]], columns=columns_layer)

        df_layer = df_layer.append(df_city_one)

        print(df_layer.tail(1))

        elem = browser.find_element(By.ID, 'title_region') #tab "change region"
        elem.click()


    df_layer = df_layer.set_index('city')
    # df_layer = df_layer.drop(["Unnamed: 0"], axis=1)
    df_layer.to_csv('layer_h_a.csv')
 
    print(f"--- {round((time.time() - time_start), 5)} seconds ---" )


if __name__ == "__main__":
    main()