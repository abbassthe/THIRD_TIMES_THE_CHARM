import os
import threading
from flask import Flask
from flask import request
from flask_restful import Api, Resource, reqparse,  fields
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import random
import time

from sqlalchemy import true


app = Flask(__name__)
api = Api(app)
data = {}
html_data = {}

def __repr__(self):
    pass
#		return f"Video(name = {name}, views = {views}, likes = {likes})"

account_put_args = reqparse.RequestParser()
account_put_args.add_argument("list", action="append", help="list url of the account is required", required=True)

resource_fields = {
	'url': fields.String
}
dirname = os.path.dirname(__file__)
with open(f'{dirname}/settings.txt', 'r') as f:
    chromedriverpath = f.readline().replace('\n', '')
    max_threads = f.readline().replace('\n', '')
def random_float(low, high):
    return random.random()*(high-low) + low
def setup_driver():
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(executable_path=chromedriverpath,chrome_options=chrome_options)
    return driver
def doscrape(url,driver,driver_pool,datakey):
    datas= []
    try:
        driver.get(url)
        # REMOVE POPUP
        container = driver.find_element_by_class_name(u"_5hn6")
        driver.execute_script("arguments[0].style.display = 'none';", container)
        # CLICK SHOW COMMENT
        link = driver.find_element(By.CSS_SELECTOR, '.userContentWrapper ._3hg-')
        link.click()
        # WAIT TO FETCH THE COMMENT
        driver.implicitly_wait(20)
        # CLICK COMMENT FILTER SELECTION
        commentFilter = driver.find_element(By.CSS_SELECTOR, '._7a99._21q1._p')
        commentFilter.click()
        # WAIT
        driver.implicitly_wait(20)
        # SELECT ALL COMMENT
        selectAllComment = driver.find_elements(By.CSS_SELECTOR, '._54ni')[1]
        selectAllComment.click()
        # WAIT
        driver.implicitly_wait(40)
        # EXPAND ALL REMAINING COMMENT
        remainingComment = driver.find_element(By.CSS_SELECTOR, '._7a94._7a9d ._4sxc._42ft')
        remainingComment.click()
        # # WAIT
        driver.implicitly_wait(20)
        # SCROLL TO BOTTOM OF PAGE
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.implicitly_wait(20)
        commentList = driver.find_elements(By.CSS_SELECTOR, 'ul._7a9a > li')
        counterId = 0
        comment = {}
        cList = commentList[0]
        soup = BeautifulSoup(cList.get_attribute('innerHTML'), 'html.parser')
        authorComment = soup.find(class_="_6qw4")
        textComment = soup.select_one("._3l3x > span")
        attachmentComment = soup.select_one("._2txe img")
        commentReplyLink = soup.select_one("._4sxc._42ft")
        commentDate = soup.select_one("a._6qw7 abbr")
        acc= "https://facebook.com" + soup.select_one("a._3mf5._3mg0")['href']
        acc2 = soup.select_one("a._3mf5._3mg0")['data-hovercard']
        pic = soup.select_one("img._3me-._3mf1.img")['src']
        comment['id'] = counterId
        comment['author'] = authorComment.text
        comment['date'] = commentDate.get("data-utime")
        comment['account_url'] = acc
        comment['pic']= pic
        comment['acoount_id'] = acc2[25:-1]
        if textComment is not None:
          # print("Comment Text: " + textComment.text)
          comment['comment'] = textComment.text
        else:
          comment['comment'] = ''
        if attachmentComment is not None:
          # print("Attachment : " + attachmentComment.get('src'))
          comment['attachment'] = attachmentComment.get('src')
        else:
          comment['attachment'] = ''
        comment['replies'] = []
        counterId += 1
        if commentReplyLink is not None:
          cList.find_element(By.CSS_SELECTOR, "._4sxc._42ft").click()
          driver.implicitly_wait(10)
        datas.append(comment)
    except:
        pass
    #driver.close()
    #driver.quit()
    driver_pool.append(driver)
    data[datakey].append(datas)
    return
def scrape_html(url,driver,driver_pool,datakey):
  try:
      driver.get(url)
      # REMOVE POPUP
      container = driver.find_element_by_class_name(u"_5hn6")
      driver.execute_script("arguments[0].style.display = 'none';", container)
      # CLICK SHOW COMMENT
      link = driver.find_element(By.CSS_SELECTOR, '.userContentWrapper ._3hg-')
      link.click()
      # WAIT TO FETCH THE COMMENT
      driver.implicitly_wait(20)
      # CLICK COMMENT FILTER SELECTION
      commentFilter = driver.find_element(By.CSS_SELECTOR, '._7a99._21q1._p')
      commentFilter.click()
      # WAIT
      driver.implicitly_wait(20)
      # SELECT ALL COMMENT
      selectAllComment = driver.find_elements(By.CSS_SELECTOR, '._54ni')[1]
      selectAllComment.click()
      # WAIT
      driver.implicitly_wait(40)
      # EXPAND ALL REMAINING COMMENT
      remainingComment = driver.find_element(By.CSS_SELECTOR, '._7a94._7a9d ._4sxc._42ft')
      remainingComment.click()
      # # WAIT
      driver.implicitly_wait(20)
      # SCROLL TO BOTTOM OF PAGE
      driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      driver.implicitly_wait(20)
      commentList = driver.find_elements(By.CSS_SELECTOR, 'ul._7a9a > li')
      cList = commentList[0]
      soup = BeautifulSoup(cList.get_attribute('innerHTML'), 'html.parser')
      driver_pool.append(driver)
      html_data[datakey].append(soup.__str__())
      return
  except:
      pass
accounts = {}
driver_pool = []
for i in range(int(max_threads)):
  driver_pool.append(setup_driver())
class account(Resource):
    requestkey = 0
    def get(self):
        pass
    def post(self):
      requestkey = self.requestkey
      self.requestkey += 1
      list = request.json["list"]
      data[requestkey] = []
      for url in list : 
       while len(driver_pool) == 0:
           time.sleep(0.2)
       this_driver = driver_pool[0]
       del driver_pool[0]
       threading.Thread(target=doscrape, args=[url,this_driver,driver_pool,requestkey]).start()
      while len(driver_pool) != int(max_threads):
        time.sleep(0.2)
      data_to_return = data[requestkey].copy()
      del data[requestkey]
      return data_to_return
class html(Resource):
  requestkey = 0
  def get(self):
      pass
  def post(self):
    requestkey = self.requestkey
    self.requestkey += 1
    list = request.json["list"]
    html_data[requestkey] = []
    for url in list : 
     while len(driver_pool) == 0:
         time.sleep(0.2)
     this_driver = driver_pool[0]
     del driver_pool[0]
     threading.Thread(target=scrape_html, args=[url,this_driver,driver_pool,requestkey]).start()
    while len(driver_pool) != int(max_threads):
      time.sleep(0.2)
    data_to_return = html_data[requestkey]
    del html_data[requestkey]
    return data_to_return
api.add_resource(account, "/account")
api.add_resource(html, "/html")
if __name__ == '__main__':
    app.run(use_debugger=False, use_reloader=False, passthrough_errors=True)
