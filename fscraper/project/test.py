from operator import index
import requests
from flask import send_file, send_from_directory, safe_join, abort

BASE = 'http://127.0.0.1:5000/'

#files= {'file': open(".csv","rb")}

#r = requests.post(BASE + 'account' , files= files)
response = requests.post(BASE + 'account' , {'url' : "https://www.facebook.com/permalink.php?story_fbid=100266906010361&id=100266766010375&comment_id=7321086184629608"} )

print(response.text)
#print(r.text)