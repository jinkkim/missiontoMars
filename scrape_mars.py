#!/usr/bin/env python
# coding: utf-8


# Dependencies
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import pandas as pd

def scrape():

    # query urls
    url_news = "https://mars.nasa.gov/news"
    url_featured_image = "https://www.jpl.nasa.gov/spaceimages"
    url_weather = "https://twitter.com/marswxreport"
    url_facts = "https://space-facts.com/mars/"  
    url_hemispheres = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

  
    # selenium webdriver setup
    driver = webdriver.Chrome("./chromedriver.exe")
    driver.implicitly_wait(3)


    # Retrieve mars news

    driver.get(url_news)
    response = driver.page_source
    soup = bs(response,'html.parser')
    news_title = soup.body.find_all("div",class_="content_title")[0].text
    news_p = soup.body.find_all("div", class_="article_teaser_body")[0].text


    # Retrieve mars image
    driver.get(url_featured_image)
    response = driver.page_source
    soup = bs(response,'html.parser')

    temp_url = soup.body.find_all("article", class_="carousel_item")[0]["style"].split("'")[1].split("/")[-1].split("-")[0]
    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/images/largesize/" + temp_url  + "_hires.jpg"


    # Retreive mars weather
    driver.get(url_weather)
    response = driver.page_source
    soup = bs(response,'html.parser')
    temp_p = soup.body.find_all("p",class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")[0]
    temp_p.a.decompose()
    mars_weather = temp_p.text


    # Retrieve mars fact
    driver.get(url_facts)
    response = driver.page_source
    soup = bs(response,'html.parser')
    table_html = soup.body.find_all("table")[0]

    # Retreive Mars hemispheres
    driver.get(url_hemispheres)
    response = driver.page_source
    soup = bs(response,'html.parser')

    hemispheres_image_urls = []
    temp_dict = {}

    temp_image_list = soup.body.find_all("div", class_="description")

    for item in temp_image_list:
        temp_dict["title"] = item.a.h3.text.rsplit(" ",1)[0]
        temp_dict["img_url"] = "http://astropedia.astrogeology.usgs.gov/download/" + item.a["href"].split("/",3)[-1] + ".tif/full.jpg" 
        hemispheres_image_urls.append(temp_dict.copy())


    information = {}
    information["news_title"] = news_title
    information["news_p"] = news_p
    information["featured_image_url"] = featured_image_url
    information["table_html"] = table_html
    information["mars_weather"] = mars_weather
    information["hemispheres_image_urls"] = hemispheres_image_urls

    return information
    
    
    
    


