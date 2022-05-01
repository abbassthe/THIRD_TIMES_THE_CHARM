
from flask import Flask, render_template, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
import datetime
from logging import exception
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import json
import time
import pandas as pa
import random
import time
import os
import csv

#https://www.facebook.com/jumpstarttesting/posts/117961834176064?comment_id=117964500842464s
datarow = []
app = Flask(__name__)
api = Api(app)

def __repr__(self):
    pass
#		return f"Video(name = {name}, views = {views}, likes = {likes})"

account_put_args = reqparse.RequestParser()
account_put_args.add_argument("url", type=str, help="url of the account is required", required=True)

resource_fields = {
	'url': fields.String
}

accounts = {}

class account(Resource):

    @marshal_with(resource_fields)
    def get(self):
        pass

    @marshal_with(resource_fields)
    def post(self):
        with open(r'C:\Users\homsi\OneDrive\Desktop\New folder\input\settings.txt', 'r') as f:
            chromedriverpath = f.readline().replace('\n', '')
            maincsv = f.readline().replace('\n', '')
            max_threads = f.readline().replace('\n', '')
        def random_float(low, high):
            return random.random()*(high-low) + low
        def setup_driver():
            chrome_options = webdriver.ChromeOptions()
            prefs = {"profile.default_content_setting_values.notifications" : 2}
            chrome_options.add_experimental_option("prefs",prefs)
            driver = webdriver.Chrome(executable_path=chromedriverpath,chrome_options=chrome_options)
            return driver
        driver = setup_driver()
        def doscrape(driver):
            try:
                args = account_put_args.parse_args()
            except Exception as e:
                print('error: ',e)
            with open("work.txt", "w") as f:
                f.write(f"{args}")

            #try:
            #    driver.get("https://www.facebook.com")
            #    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
            #    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))
            #    time.sleep(random_float(0.5,2))
            #    username.clear()
            #    username.send_keys("majholmeme@gmail.com")
            #    time.sleep(random_float(0.5,2))
            #    password.clear() 
            #    password.send_keys("mhmdashek445")
            #    time.sleep(random_float(0.5,2))
            #    button = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
            #    time.sleep(random_float(0.5,2))
            #except Exception as e:
            #    print('error: ', e)
            datas = []
            try:
                with open("work.txt", "r") as f:
                    pls_work= f.readline()
                url= pls_work[9:-2]
                time.sleep(random_float(0.5,2))
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
                selectAllComment = driver.find_elements(By.CSS_SELECTOR, '._54ni')[2]
                selectAllComment.click()

                # WAIT
                driver.implicitly_wait(20)

                # EXPAND ALL REMAINING COMMENT
                remainingComment = driver.find_element(By.CSS_SELECTOR, '._7a94._7a9d ._4sxc._42ft')
                remainingComment.click()

                # # WAIT
                # driver.implicitly_wait(20)
                time.sleep(2)

                # SCROLL TO BOTTOM OF PAGE
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                time.sleep(2)

                commentList = driver.find_elements(By.CSS_SELECTOR, 'ul._7a9a > li')


                counterId = 0

                for cList in commentList:
                
                  comment = {}

                  soup = BeautifulSoup(cList.get_attribute('innerHTML'), 'html.parser')

                  authorComment = soup.find(class_="_6qw4")
                  textComment = soup.select_one("._3l3x > span")
                  attachmentComment = soup.select_one("._2txe img")
                  commentReplyLink = soup.select_one("._4sxc._42ft")
                  commentDate = soup.select_one("a._6qw7 abbr")
                  acc= soup.select_one("a._3mf5._3mg0")['href']
                  pic = soup.select_one("img._3me-._3mf1.img")['src']
                  # print("Author: " + authorComment.text)
                  # print("Date: " + commentDate.get("data-utime"))

                  comment['id'] = counterId
                  comment['author'] = authorComment.text
                  comment['date'] = commentDate.get("data-utime")
                  comment['account_url'] = acc
                  comment['pic']= pic
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

                    replyCommentList = cList.find_elements(By.CSS_SELECTOR, "._7a9h > ul > li")

                    for replyC in replyCommentList:
                    
                      replyDict = {}

                      replySoup = BeautifulSoup(replyC.get_attribute('innerHTML'), 'html.parser')

                      authorReplyComment = replySoup.find(class_="_6qw4")
                      attachmentReplyComment = replySoup.select_one("._2txe img")
                      commentReplyDate = replySoup.select_one("a._6qw7 abbr")

                      # print('\tAuthor : ' + authorReplyComment.text)
                      # print("\tDate: " + commentReplyDate.get("data-utime"))

                      replyDict['id'] = counterId
                      replyDict['author'] = authorReplyComment.text
                      replyDict['date'] = commentReplyDate.get("data-utime")

                      if attachmentReplyComment is not None:
                        # print("\attachment : " + attachmentReplyComment.get('src'))
                        replyDict['attachment'] = attachmentReplyComment.get('src')
                      else:
                        replyDict['attachment'] = ''

                      readMoreLink = replySoup.select_one("._5v47.fss")
                      if readMoreLink is not None:
                        replyC.find_element(By.CSS_SELECTOR, "._5v47.fss").click()
                        driver.implicitly_wait(10)
                        readMoreHtml = replyC.find_element(By.CSS_SELECTOR, "._3l3x")
                        readMoreSoup = BeautifulSoup(readMoreHtml.get_attribute('innerHTML'), 'html.parser')
                        # print("\tComment Reply Text: " + readMoreSoup.text)
                        replyDict['comment'] = readMoreSoup.text
                      else:
                        textReplyComment = replySoup.select_one("._3l3x > span")
                        if textReplyComment is not None:
                          # print("\tComment Reply Text: " + textReplyComment.text)
                          replyDict['comment'] = textReplyComment.text

                      comment['replies'].append(replyDict)
                      counterId += 1

                  datas.append(comment)
                with open('data.json', 'w') as outfile:
                  json.dump(datas, outfile)
            except:
                pass
            #driver.close()
            #driver.quit()
            return "stay_positive"
        return doscrape(driver)

api.add_resource(account, "/account")

if __name__ == "__main__":
    app.run(debug=True)
