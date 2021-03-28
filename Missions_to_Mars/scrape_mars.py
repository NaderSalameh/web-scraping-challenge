# importing dependencies 
import pandas as pd 
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time


# creating function to scrape all data needed for site then inserting the data into MongoDB
def scrape():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    # creating HTML as an object
    html = browser.html

    # parsing the HMTL 
    soup = BeautifulSoup(html, 'html.parser')

    # capturing the news title
    title = soup.find_all('div', class_='content_title')
    news_title = title[1].text
    
    # capturing the news paragraph
    news_paragraph = soup.find('div', class_='article_teaser_body').text

    # capturing the url for the site's latest featured image 
    featured_url ='https://www.jpl.nasa.gov/images?search=&category=Mars'
    browser.visit(featured_url)

    # clicking the mars checkbox
    target = 'input[class="text-theme-red focus:ring-2 focus:ring-jpl-red flex-shrink-0 w-5 h-5 mt-px mr-1 align-middle border rounded-none"]'
    browser.find_by_tag(target).click()

    # clicking the mars picture
    target = 'a[class="group  cursor-pointer block"]'
    browser.find_by_tag(target).click()

    # taking a second rest an giving page time to load before continuing the scrape 
    time.sleep(2)

    # grabbing the url for the jpeg imgae url
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    # capturing the image url
    featured_image_url = soup.find_all('a', class_="BaseButton")[0]['href']

    #capturing site url to scrape mars data, using pandas
    mars_facts_url_for_pandas = 'https://space-facts.com/mars/'

    #creating the data 
    tables = pd.read_html(mars_facts_url_for_pandas)

    # converting table into a dataframe, then using pandas to output and capture the HTNL to build the table 
    mars_df = tables[0]
    mars_df.columns = ['attribute', 'value']
    html_table_string = mars_df.to_html()

    #removing line breaks
    html_table_string = html_table_string.replace('\n', '')

    #adding html file
    mars_df.to_html('mars_facts.html')
    #!open mars_facts.html

    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)

    # creating the soup 
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    # capturing the hemisphere html
    hem_html = soup.find_all('div', class_="description")

    # creating a list of dictionaries
    hemisphere_image_urls = []
    for info in range(len(hem_html)):
        #creating a dictionary
        img_dict = {}
    
        #doing a click through 
        ref = hem_html[info].h3.text
        browser.find_by_text(ref).click()
    
        #setting up the soup
        html = browser.html
        soup = BeautifulSoup(html,'html.parser')
    
        #appending the title to the dictionary 
        title = soup.find_all('h2', class_="title")[0].text
        img_dict['title'] = title
    
        #appending the image url to the dictionary 
        img_url = soup.find_all('div', class_='downloads')[0].li.a['href']
        img_dict['img_url'] = img_url
    
        # printing for validation 
        print(f"title: {title}")
        print(f"img_url: {img_url}")
        print("*******************************************************************************************************************")
        print("*******************************************************************************************************************")
        
        #appending the dictionary to the list
        hemisphere_image_urls.append(img_dict)
    
        #click back
        browser.back()


    # creating dictionary
    mars_information = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "html_table_string": html_table_string,
        "featured_image_url": featured_image_url,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    browser.quit()

    return mars_information
















    

