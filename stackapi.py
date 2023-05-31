# import requests
# import csv


# urls = " https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow"
# response = requests.get(urls)

# # print(response.json()['items'])
# for data in response.json()['items']:
#     datatitle =data['title']
#     print(datatitle)
   

# with open('abc.csv', 'w', newline='')as pdf:
#     writer = csv.writer(pdf)
#     writer.writerow(['Data'])
#     writer.writerow([data]for data in datatitle)





import requests
import csv

url = "https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow"
response = requests.get(url)

data_list = []
for data in response.json()['items']:
    datatitle = data['title']
    print(datatitle)
    data_list.append(datatitle)

with open('abc.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Data'])
    writer.writerows([[data] for data in data_list])
