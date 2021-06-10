####################################################
# # mission_to_mars
# ----
# 
# Written in the Python 3.7.9 Environment
# 
# By Nicole Lund 
# 
# This Python script scrapes Mars space data from various 
# locations for storage in a Pymongo DB and display on a webpage.
####################################################

# Import Dependencies
import pandas as pd 
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

def nasa_news(browser):
    ####################################################
    # NASA Mars News
    ####################################################
  
    # Access NASA news site
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    nasa_html = browser.html
    nasa_soup = BeautifulSoup(nasa_html, 'html.parser')

    # Collect the latest news headline and paragraph
    latest_container = nasa_soup.find('div', class_='image_and_description_container')
    
    # Final Nasa Result
    news_headline = latest_container.find('div', class_='content_title').find('a').text
    news_teaser = latest_container.find('div', class_='article_teaser_body').text
    nasa_news_headline = {'headline':news_headline,'teaser':news_teaser}

    # print('')
    # print('-------- NASA News Top Headline --------')
    # print(nasa_news_headline)

    return nasa_news_headline

def jpl_feature(browser):
    ####################################################
    # JPL Mars Space Images - Featured Image
    ####################################################

    # Access JPL image site
    jpl_base_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'
    jpl_url = jpl_base_url + 'index.html'
    browser.visit(jpl_url)
    jpl_html = browser.html
    jpl_soup = BeautifulSoup(jpl_html, 'html.parser')

    # Collect the full url path for the full size featured image
    featured = jpl_soup.find('div', class_='floating_text_area')
    jpl_relative_url = featured.find('a')['href']

    # Final JPL Result
    featured_image_url = jpl_base_url + jpl_relative_url
    
    # print('')
    # print('-------- JPL Featured Image --------')
    # print(featured_image_url)

    return featured_image_url

def mars_facts(browser):
    ####################################################
    # Mars Facts
    ####################################################

    # Collect Mars Facts Table
    facts_url = 'https://space-facts.com/mars/'
    facts_df = pd.read_html(facts_url)[0]

    # Clean up table
    facts_df = facts_df.rename(columns={0:'Description',1:'Value'})
    facts_df = facts_df.set_index('Description')
    # print('')
    # print('-------- Mars Facts Table --------')
    # print(facts_df)
    # print('')

    # Final Mars Facts Result - Convert facts table to html string
    facts_html = facts_df.to_html()
    return facts_html

def mars_hemispheres(browser):
    ####################################################
    # Mars Hemispheres
    ####################################################

    # Access Astrogeology site
    astropedia_base_url = 'https://astrogeology.usgs.gov'
    astropedia_relative_url = '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    astropedia_url = astropedia_base_url + astropedia_relative_url
    browser.visit(astropedia_url)
    astropedia_html = browser.html
    astropedia_soup = BeautifulSoup(astropedia_html, 'html.parser')

    # Collect hemisphere titles
    hemisphere_titles = []
    hemisphere_containers = astropedia_soup.find_all('div', class_='description')

    for image_num in range(0,5):
        try:
            hemisphere_found = hemisphere_containers[image_num].h3.text
            hemisphere_titles.append(hemisphere_found)
            print(f'Found Hemisphere: {hemisphere_found}')
        except IndexError:
            print('All Hemispheres Found')

    # Navigate to each hemisphere link and collect image link and title in a dictionary
    hemisphere_image_urls = []

    for hemisphere in hemisphere_titles:
        # Navigate to each hemisphere link
        browser.links.find_by_partial_text(hemisphere).click()

        # Collect URL for full size image
        hemisphere_html = browser.html
        hemisphere_soup = BeautifulSoup(hemisphere_html, 'html.parser')

        hemisphere_image = hemisphere_soup.find('img', class_='wide-image')['src']
        image_link = astropedia_base_url + hemisphere_image
        hemisphere_image_urls.append(\
            {"title":hemisphere,"img_url":image_link})

        # Return to main page
        browser.visit(astropedia_url)

    # print('')
    # print('-------- Mars Hemisphere Images --------')
    # print(hemisphere_image_urls)
    # print('')

    return hemisphere_image_urls

def scrape():
    ####################################################
    # Scrape Mars Related Data
    ####################################################

    # Initialize browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Retrieve NASA news
    nasa_headline_teaser = nasa_news(browser)
    
    # Retrieve JPL Featured Image
    jpl_image = jpl_feature(browser)

    # Retrieve Mars Facts Table
    facts_table = mars_facts(browser)

    # Retrieve Mars Hemisphere Images
    hemisphere_image_links = mars_hemispheres(browser)
    
    # Store all retrieved data within a single dictionary
    mars_data = {\
        'nasa_top_story':nasa_headline_teaser,\
        'jpl_featured_img':jpl_image,\
        'facts_table_html':facts_table,\
        'hemisphere_images':hemisphere_image_links\
        }

    # print('')
    # print('-------- Combined Mars Data --------')
    # print(mars_data)

    return(mars_data)

    # Close splinter browser
    browser.quit()

if __name__ == "__main__":
   scrape() 