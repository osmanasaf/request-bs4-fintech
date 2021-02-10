from os import write
from bs4.element import ResultSet
import requests
from bs4 import BeautifulSoup as bs
import base64
import json

dataDict={
            "Link":"ilan_link",
            "Fiyat":"ilan_fiyat",
            "Resim Link":"ilan_resim_link",
            "ResimBase64":"ilan_resim_base64"
}

user_login ={
    'UserName': 'kazimhas96',
    'Password': 'hXbtvxUNVOs',
    'csrf_token': '86d9e876ebe194e5d3fdbc095e24c004',
    'form_id':'loginForm'
}

headers={
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.344'
}

with requests.Session() as session:
    getUrl='https://www.itemsatis.com/'
    sendUrl='https://www.itemsatis.com/api/Login'
    favUrl='https://www.itemsatis.com/favori-ilanlarim.html'
    req=session.get(getUrl,headers=headers)
    soup=bs(req.content,'html5lib')
    user_login['csrf_token']=(soup.find('input',attrs={'name':'csrf_token'})['value'])
    login=session.post(sendUrl,headers=headers,data=user_login)

    reqFav=session.get(favUrl,headers=headers)
    soupFav=bs(reqFav.content)

    offers=soupFav.find_all('div',attrs={'class':'col-md-4 col-sm-12 col-xs-12 AdvertBox-1'})

    
    forCounter=0
    for offer in offers:
        forCounter=forCounter+1
        offerUrl=offer.a.get('href')
        dataDict["Link"]=getUrl+offerUrl
        
        price=offer.find('div',attrs={'class':'AdvertBox-Price'}).text
        dataDict["Fiyat"]=price
        
        offerImg=offer.img.get('data-src')
        dataDict["Resim Link"]= offerImg
                

        imgDoc=requests.get(offerImg).content  # download data-src img
        with open(str(forCounter),'wb') as handler:
            handler.write(imgDoc)

        with open("1", "rb") as img_file:      # to base64
            my_string = base64.b64encode(img_file.read())
            dataDict["ResimBase64"]= my_string.decode('utf-8')
    
        with open("data.json","a") as jsonFile:
            json.dump(dataDict,jsonFile,indent=2)
            jsonFile.write ('\n')
            
    