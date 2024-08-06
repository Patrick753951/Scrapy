import requests
from bs4 import BeautifulSoup
import xlwt

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'}
link_list = []
for start_number in range(0, 550, 25):
    response = requests.get(f'https://product.pconline.com.cn/mobile/{start_number}s1.shtml', headers=header).text
    soup = BeautifulSoup(response, 'html.parser')
    item_list = soup.find_all('li', attrs={"class": "item"})
    for item in item_list:
        link = item.find('a', attrs={"target": "_blank"})
        if link is not None:
            url = link.attrs['href']
            link_list.append(url)

# print(link_list)
print(len(link_list))

device_list = []
for link in link_list:
    response_1 = requests.get("https://" + link[2:-5] + "_detail.html")
    param = BeautifulSoup(response_1.text, "html.parser").find_all("tbody")
    total = {}
    for item in param:
        if item != '\n':
            for tr in item.find_all("tr"):
                if tr.find("th") is not None:
                    try:
                        key = tr.find("th").text
                        val = tr.find("td").text.strip()
                        if '•' in val:
                            val = val.split('•')[0]
                        if key == 'CPU' and tr.find("td").find('a', attrs={"class": "poptxt"}) is not None:
                            val = tr.find("td").find('a', attrs={"class": "poptxt"}).text.strip()
                        total[key] = val
                    except AttributeError as e:
                        print(tr)

    device_list.append(total)
print(device_list)
print(len(device_list))

workbook = xlwt.Workbook(encoding='utf-8')  # 创建一个新的 Excel 文件
worksheet = workbook.add_sheet('phonesheet')  # 在 Excel 文件中创建一个名为 'phonesheet' 的表格
title = list(device_list[0])  # 获取 device_list 中第一个元素的键，作为表格的标题行

# 写入表格的标题行
for i in range(len(title)):
    worksheet.write(0, i, title[i])

# 逐行逐列写入数据
for i in range(len(device_list)):
    for j in range(len(title)):
        # 检查当前列的标题是否存在于当前行的数据字典中
        if title[j] not in device_list[i]:
            worksheet.write(i + 1, j, "None")  # 如果不存在，则写入 "None"
        else:
            worksheet.write(i + 1, j, device_list[i][title[j]])  # 如果存在，则写入对应的值

workbook.save("phone.xls")  # 保存 Excel 文件为 "phone.xls"
