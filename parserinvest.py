import requests
import re
dict={} # the dictionary
porog=.20 # minimal requirements of income per year
sum=0 # current sum of checked funds
page=0 # current page of rating
maxsum=20 # maximum funds for the rating

def parse(a,b): # parsing page A with regexp B
    regex_num = re.compile(b)
    return regex_num.findall(a)

while sum<maxsum:
    page=page+1
    response = requests.get('https://investfunds.ru/funds/?qual=on&showID=99&sort=delta_pay_5y&order=desc&scroll_to_table=1&cstm=0-3c96ag&sortId=99&limit=10&page='+str(page))
    a=(response.content).decode('utf-8')
    y5=parse(a,'5y text_right hidden js_swtch_cntrl_visible">\n +<div class="js_td_width">\n +(.+)%')
    y1=parse(a,'1y text_right hidden js_swtch_cntrl_visible">\n +<div class="js_td_width">\n +(.+)%')
    adresses=parse(a,'/funds/\d+/')  
#     print(adresses)
    for i in range(len(y5)):
#         if float(y1[i])>porog*100:
        if float(y1[i])>porog*100 and float(y5[i])>((1+porog)*(1+porog)*(1+porog)*(1+porog)*(1+porog))*100-100:
            if sum>=maxsum: break
            response1 = requests.get('https://investfunds.ru'+adresses[i])
            b=(response1.content).decode('utf-8')
            fundslist=parse(b,'\/">(.+?)[,|\[]')  
            if fundslist!=[]:
                sum=sum+1
                print(parse(b,'itle>(.+) ??????')[0]+' https://investfunds.ru'+adresses[i]+' '+y1[i]+' '+y5[i],end='\n')
                for j in range(5):
                    if fundslist[j] not in dict: dict[fundslist[j]]=0
                    dict[fundslist[j]]=dict[fundslist[j]]+5-j
#                     print(fundslist[j])
dict = {k: dict[k] for k in sorted(dict, key=dict.get, reverse=True)}
print ('-----------------------')
for k, v in dict.items(): 
    print(k, v)