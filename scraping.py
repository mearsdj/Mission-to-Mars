
#import splinter, beautiful soup, and pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt
import pandas as pd

def scrape_all():
    # Initiate headless driver for deployment
    # visit mars nasa news site

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):
    #send browser to mars news site
    url = 'https://redplanetscience.com'

    browser.visit(url)
    browser.is_element_present_by_css('div.list_text',wait_time=1)

    #convert browser html to soup html object and quit browser

    html = browser.html
    news_soup = soup(html,'html.parser')

    try:

        slide_elem = news_soup.select_one('div.list_text',)

        slide_elem.find('div',class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

    except AttributeError:

        return None, None

    #use parent element news_title to find teaser text
    news_p = slide_elem.find('div',class_='article_teaser_body').get_text()


    return news_title, news_p

def featured_image(browser):
    # ## JPL Space Images featured image
    #visit url
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    #find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    #parse the resulting html
    html = browser.html
    img_soup = soup(html,'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        img_url_rel

        # Use the base URL to create an absolute URL
        img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    except AttributeError:
        return None

    return img_url

def mars_facts(browser):
# ##  Mars Facts
#download mars data table using pandas
    try:
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

#assign col names and index
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    #add bootstrap styling to tble
    return  df.to_html(classes="table table-striped")



if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())