from urllib import request
from bs4 import BeautifulSoup as bs
import pandas as pd 
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException as e
import time

def add_first(top, bottom):
    data["Rank"].append(top.find('div', class_='c-chart__table--rank').get_text())
    data["Title"].append(top.find('div', class_='c-chart__table--title').find('p').get_text())
    data["Artists"].append(top.find('div', class_='c-chart__table--caption').get_text())
    data["Song_Units"].append(top.find('span', class_='c-chart__table--song-units-songs').get_text().strip())        
    data["Weeks_on_Chart"].append(bottom.find('div', class_=['c-chart__table--weeks-present','c_chart__table--stats-base']).find('span').get_text())
    data["Song_Streams"].append(bottom.find('div', class_=['c_chart__table--stats-base', 'c-chart__table--song-streams']).find('span').get_text())
    data["Record_Label"].append(bottom.find('span', class_='c-chart__table--label-text').get_text())

    city_list = [i.get_text().split(',')[0] for i in bottom.find('ol') if i != '\n']
    data["Top_Cities"].append(city_list)


if __name__ == '__main__':    
    url = "https://www.rollingstone.com/charts/songs/"

    driver = webdriver.Firefox(executable_path=r"/home/thedarkcoder/geckodriver/geckodriver")
    driver.get(url)
    counter = 15
    while counter < 100:
        string = '[data-counter="' + str(counter)  + '"]'
        link = driver.find_elements_by_css_selector(string)
        print(link)
        link[0].click()
        time.sleep(1)
        counter += 15

    url = driver.page_source
    data = {"Rank": [], "Title": [], "Artists": [], "Weeks_on_Chart": [], "Song_Streams": [], 'Song_Units': [], "Record_Label": [], "Top_Cities": []}
    soup = bs(url, 'html.parser')
    city_list = []
    top = soup.find_all('div', attrs={'class':'c-chart__table--top'})
    container = soup.find_all('div', attrs={'class':'c-chart__table--container'})
    bottom = soup.find('div', class_='c-chart__table--bottom')

    if len(top) == len(container) + 1:
        add_first(top[0], bottom)
        for songs1, songs2 in zip(top[1:], container):
            data["Rank"].append(songs1.find('div', class_='c-chart__table--rank').get_text())
            data["Title"].append(songs1.find('div', class_='c-chart__table--title').find('p').get_text())
            data["Artists"].append(songs1.find('div', class_='c-chart__table--caption').get_text())
            data["Weeks_on_Chart"].append(songs2.find('div', class_=['c-chart__table--weeks-present','c_chart__table--stats-base']).find('span').get_text())
            data["Song_Streams"].append(songs2.find('div', class_=['c-chart__table--song-streams','c_chart__table--stats-base']).find('span').get_text())
            data["Song_Units"].append(songs1.find('span', class_='c-chart__table--song-units-songs').get_text().strip())
            data["Record_Label"].append(songs2.find('span', class_='c-chart__table--label-text').get_text())

            city_list = [i.get_text().split(',')[0] for i in songs2.find('ol') if i != '\n']
            data["Top_Cities"].append(city_list)
        data = pd.DataFrame.from_dict(data) 
    data.to_csv('output_file.csv', index=False)       
    print(data)
