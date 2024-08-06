import os
from pathlib import Path
import pandas as pd
from bs4 import BeautifulSoup
import requests

import re
import urllib.request, urllib.parse


# 获取页面内容

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


def gen_url(base_url, pages):
    for i in range(pages):
        url = base_url + f"{i * 25}s1.shtml"
        yield url
def get_page_content(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        response_encoding=response.apparent_encoding
        return response.text
    else:
        print('请求失败:', response.status_code)
        return None


# 解析内容
def parse_page_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    tv_list = soup.find_all('div', class_='item-detail')
    tv_href_list = []
    for tv in tv_list:
        a_tag = tv.select_one('a.item-title-name')
        if a_tag:
            href = a_tag.get("href")
            tv_href_list.append("https:" + href)
    return tv_href_list


def extract_tv_detail(html, sep = "：") -> dict:
    info = {}
    soup = BeautifulSoup(html, 'html.parser')
    tv_info_tables = soup.find_all('table', class_='dtparams-table')

    for tv_info_table in tv_info_tables:
        for tr in tv_info_table.select("tbody>tr"):
            key = tr.select_one("th").text.strip()
            if key == "型号":
                value = soup.select_one('#Jwrap>div.pro-info>div>h1').text.strip()
            else:
                value = tr.select_one("td").text.strip()
            split_key = "• "

            if split_key not in value:
                pass
            else:
                value_new = ""
                value_list = value.split(",")
                for value_temp in value_list:
                    value_new = value_new + value_temp.split("• ")[0] + " "
                value = value_new
            info[key] = value
    return info


# 获取某一页全部电视信息
def extract_one_page(url, sep="："):
    response = get_page_content(url)
    details = []
    if not response:
        return details
    href_list = parse_page_content(response)
    for href in href_list:
        href_new = href.replace(".html", "_detail.html")
        detail_content = get_page_content(href_new)
        if detail_content:
            detail = extract_tv_detail(detail_content, sep=sep)
            details.append(detail)
    return details

def write_to_csv(df, file_path, write_header=False):
    if not df.empty:
        # 将字符串路径转换为 Path 对象
        path = Path(file_path)

        # 如果文件不存在，则先写入表头
        if not path.exists() or write_header:
     #     df.to_csv(file_path, mode='a', header=True, index=False, encoding='GB18030')
        # else:
        #     df.to_csv(file_path, mode='a', header=False, index=False,encoding='GB18030')
            with open("tv0.csv","a",encoding="GB2312", newline="") as fp:
                df.to_csv(fp)

def main():
    base_url = 'https://product.pconline.com.cn/lcd_tv/'
    pages = 87
    for url in gen_url(base_url, pages=pages):
        info = extract_one_page(url)
        print(info)
        df = pd.DataFrame(info)
        file_path = 'tv0.csv'
        # 检查文件是否存在
        if not os.path.exists(file_path):
            # 如果文件不存在，写入第一个 DataFrame 并添加表头
            write_to_csv(df, file_path, write_header=True)
        else:
            # 如果文件已存在，直接追加数据
            write_to_csv(df, file_path, write_header=False)


if __name__ == '__main__':
    main()
