
import requests
import json
from bs4 import BeautifulSoup
response = requests.get('https://docs.aws.amazon.com/service-authorization/latest/reference/reference_policies_actions-resources-contextkeys.html')
soup = BeautifulSoup(response.content, "html.parser")
#To get the text out of it

div_highlight =  soup.find_all(name = 'div',class_ = "highlights",recursive=True)
urls= []
for li in div_highlight:
    hrefs = li.find_all("a",href=True)
    for href in hrefs:
        #print(href['href'])
        urls.append(href['href'][1:])
for url in urls:
    url = "https://docs.aws.amazon.com/service-authorization/latest/reference"+url
    response = requests.get(url)
    soup = BeautifulSoup(response.content,"html.parser")
    title = soup.find("title")
    title = title.text.split("-")[0]
    if "Amazon" in title:
        title = title.split("Amazon")[-1]
    else:
        title= title.split("AWS")[-1]

    #print(title)
    tags = soup.find("div" , class_="table-container")
    trs = tags.find_all("tr")
    data = []
    tempMap = dict()
    for tr_tag in trs:
        tds = tr_tag.find_all("td")
        keys = ["action","desc","access","resources","conditionKeys","dependentActions"]
        createMap = dict()
        if len(tds)>3:
            i=0
            for td in tds: 
                createMap[keys[i]] = [t.text for t in td if t.text!="\n"]
                if i<3:
                    tempMap[keys[i]] = [t.text for t in td if t.text!="\n" ]
                i=i+1
        else:
            i=3
            for td in tds:
                createMap[keys[i]] = [t.text for t in td if t.text!="\n" ]
                i=i+1
            for key in tempMap.keys():
                createMap[key] = tempMap[key]
        data.append(createMap)

    for da in data[1:]:
        da["action"] = "".join(da["action"])
        da["desc"] = "".join(da["desc"])
        da["access"] = "".join(da["access"])
        da["resources"] = [t.strip("\n") for t in da["resources"]]
        

    finalMap = dict()
    finalMap["prefix"] = title
    finalMap["link"] = url
    finalMap["actions"] =data[1:]
    print(finalMap)
    print("---------------------"*3)
with open("output.json", "w") as outfile:
    json.dump(finalMap, outfile)
    

#for li in div_highlight:
 #   lis = li.find_all("li",recursive=True)
  #  for al in lis:
   #     als=al.find_all("a",href=True)
    #    print(als[0]['href'])
 
# to get the div tags
#divs = soup.find_all('div')
#div_highlights = soup.find("div",class_="highlights")


