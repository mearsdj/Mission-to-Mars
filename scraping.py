
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
        "facts": mars_facts(browser),
        "last_modified": dt.datetime.now(),
        "hemisphere_images":mars_hemispheres(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):
    #send browser to mars news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'

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
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
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
        img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

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
    return  df.to_html(classes="table table-hover table-striped")
def mars_hemispheres(browser):
    url = 'https://marshemispheres.com/'
    # url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    html = browser.html
    soup_hemispheres = soup(html, 'html.parser')
    listitems = soup_hemispheres.find_all('div', class_='description')
    for item in listitems:
        # browser.links.find_by_partial_href('.html').click
        img_url_rel = item.find('a', class_='itemLink product-item')['href']
        img_url = f'{url}{img_url_rel}'
        browser.visit(img_url)
        html_item = browser.html
        soup_item = soup(html_item, 'html.parser')
        target_img_url_rel = soup_item.find('img', class_='wide-image').get('src')
        target_img_url = f'{url}{target_img_url_rel}'
        title = item.find('h3').text
        hemisphere_image_urls.append({'img_url': target_img_url, 'title': title})
        # print(item.find('h3').text, target_img_url)
        browser.back

    # 5. Quit the browser
    browser.quit()

    return hemisphere_image_urls

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())