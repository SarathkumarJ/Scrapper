# -*- coding: utf-8 -*-
#EXTRACT the rank of perticular brand From amazon.in
#python version 2.7


from bs4 import BeautifulSoup as BS
from urllib2 import Request, urlopen
import re
import requests
from lxml import etree
import re 
import json
import datetime
brands =['Tresemme','Loreal']  



result= {}
url = "http://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords="
keywords = ['Conditioner','Hair fall shampoo','Hair oil']

for words in keywords :
    result.update({words:{}})
    search = words.replace(' ','+')
    search_url ="%s%s"%(url,search)
    response = requests.get(search_url, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'})
    soup = BS(response.content, "lxml")
    tags = {}
    response_set  = soup.select('li.s-result-item')
    result_set={}
    for product,rank in zip(response_set,range(1,len(response_set)+1)):         
       if product.select('h2') and product.select('h2')[0] :
           data = product.select('h2')[0].text.lower().replace("'",'')
           for brand in brands :
               if len(result_set) == len(brands) :  #Reduce runtime by avioding unwanted  traversals
                   break

               if re.match(brand.lower(), data):
                   if brand.lower() in result_set :
                       pass 
                   else  :
                       result_set.update({brand.lower() : rank
})
        
    result[words] = {'position':result_set}



results=[]
for output in result :
    results.append({
            "keyword": output.lower(),
            "position" : result.get(output,{}).get('position',{})
            })

output ={'result':results}
print json.dumps(output)

