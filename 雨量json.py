import json
import datetime
import matplotlib.pyplot as plt

file = '日累積雨量(每月更新).json'

with open (file,'r',encoding='utf-8') as file_json:
    rain_record = json.load(file_json)

'''
{'siteid': '85', 'sitename': '大城', 'rainfall24hr': '3', 'datasourceagency': '環境部',
 'monitordate': '2024-10-31', 'itemunit': 'mm'}]
'''

star_date = datetime.date(2024,9,1)
end_date = datetime.date(2024,9,30)

select = ['28','29','30']
    
site_id_28 = []
site_id_29 = []
site_id_30 = []

rain_28 = []
rain_29 = []
rain_30 = []

for i in rain_record:
    if star_date <= datetime.date.fromisoformat(i['monitordate'])<=end_date:
        if i['siteid'] =='28':
            site_id_28.append(i)
        elif i['siteid'] =='29':   
            site_id_29.append(i)
        elif i['siteid'] =='30':
            site_id_30.append(i)
            
for j in site_id_28:
    rain_28.append(eval(j['rainfall24hr']))
for j in site_id_29:
    rain_29.append(eval(j['rainfall24hr']))
for j in site_id_30:
    rain_30.append(eval(j['rainfall24hr']))


rain = [sum(rain_28),sum(rain_29),sum(rain_30)]
area = ['豐原','沙鹿','大里']
plt.rcParams ['font.family']=['Microsoft JhengHei']

plt.bar(area,rain,color = 'skyblue',edgecolor = 'black')
plt.xlabel('雨量',fontsize = 15)
plt.ylabel('地區',fontsize = 15,rotation = 0)
plt.xticks(fontsize = 20)
plt.title('台中區雨量觀測',fontsize= 30)
plt.grid()
plt.show





