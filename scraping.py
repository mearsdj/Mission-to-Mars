
#import splinter, beautiful soup, and pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

#set up splinter
executable_path = {'executable_path':ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

#visit mars nasa news site
url = 'https://redplanetscience.com'

#send browser to mars news site
browser.visit(url)
browser.is_element_present_by_css('div.list_text',wait_time=1)

#convert browser html to soup html object and quit browser

html = browser.html
news_soup = soup(html,'html.parser')
slide_elem = news_soup.select_one('div.list_text',)

slide_elem.find('div',class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

#use parent element news_title to find teaser text
news_p = slide_elem.find('div',class_='article_teaser_body').get_text()
news_p


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

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# ##  Mars Facts
#download mars data table using pandas
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()

df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

df.to_html()

browser.quit()