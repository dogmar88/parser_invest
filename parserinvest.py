import requests
import re
dict={} # сам словарик
porog=.2 # минимальное значение по прибыли в год
sum=0 # сумма уже отстуканных фондов
page=1 # текущая страница
maxsum=10 # максимум пифов для оценки

def parse(a,b): # парсим страницу a регуляркой b
    regex_num = re.compile(b)  
    return regex_num.findall(a)

while sum<maxsum:
    page=page+1
    response = requests.get('https://investfunds.ru/funds/?qual=on&showID=99&sort=delta_pay_5y&order=desc&scroll_to_table=1&cstm=0-3c96ag&sortId=99&limit=10&page='+str(page))
#     response = requests.get('https://investfunds.ru/funds/?qual=on&showID=99&sort=coeff_srtn&order=desc&scroll_to_table=1&cstm=0-3cesk8&limit=10&page='+str(page))
    a=(response.content).decode('utf-8')
    y5=parse(a,'<td data-show_71="" class="field_delta_pay_5y text_right hidden js_swtch_cntrl_visible">\n +<div class="js_td_width">\n +(.+)%')
    y1=parse(a,'<td data-show_71="" class="field_delta_pay_1y text_right hidden js_swtch_cntrl_visible">\n +<div class="js_td_width">\n +(.+)%')
    adresses=parse(a,'/funds/\d+/')  
    print(adresses)
    for i in range(len(y5)):
        if float(y1[i])>porog*100:
#         if float(y1[i])>porog*100 and float(y5[i])>((1+porog)*(1+porog)*(1+porog)*(1+porog)*(1+porog))*100:
            if sum>=maxsum: break
            print('https://investfunds.ru'+adresses[i]+' '+y1[i]+' '+y5[i],end='\n')
            response1 = requests.get('https://investfunds.ru'+adresses[i])
            b=(response1.content).decode('utf-8')
            kek=(b,'\d+\/">(.+)\. ')  
            if kek!=[]:
                sum=sum+1
                for j in range(5):
                    if kek[j] not in dict: dict[kek[j]]=0
                    dict[kek[j]]=dict[kek[j]]+5-j
                    print(kek[j])
dict = {k: dict[k] for k in sorted(dict, key=dict.get, reverse=True)}
for k, v in dict.items(): 
    print(k, v)
