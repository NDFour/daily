#
#   Description: ---
#        Author: Lynn
#         Email: lgang219@gmail.com
#        Create: 2018-04-25 21:14:12
# Last Modified: 2018-04-25 22:09:18
#

import requests 
import re

def getHtml(url):
    html_text=''
    try:
        r=requests.get(url,timeout=10)
        html_text=r.text
    except:
        html_text=''
    return html_text

def shortUrl(url):
    baseurl='https://urlc.cn/api/add?longurl='
    geturl=baseurl+url 
    html_text=getHtml(geturl)
    # get shortid":"RJy7Uia"
    reShortId=re.compile(r'shortid":".*?"')
    rawShortId=reShortId.findall(html_text)[0]
    shortId=rawShortId.replace('shortid":','').replace('"','')
    return shortId

def genUrl(title,url):
    url='https://urlc.cn/'+url
    relUrl='<a href="'+url+'">'+title+'</a>'
    return relUrl

def main():
    while(1):
        title=input("Title:")
        url=input("URL:")
        todaytops=genUrl(title,shortUrl(url))
        with open('todayTop','a') as f:
            f.write(todaytops)
            f.write("\n")

main()
