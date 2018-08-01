import webbrowser
import requests
import time
from bs4 import BeautifulSoup
import re
import os


#   请求数据
def get_data(url, num_retries = 3):
    print(url)
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"}

    # 异常处理
    try:
        data_1 = requests.get(url, headers=headers)
        print(data_1.status_code)
    except requests.exceptions.ConnectionError as e:
        print("请求错误")
        data_1 = None

    if (data_1 != None) and (500 <= data_1.status_code < 600):
        if (num_retries > 0):
            print("服务器错误，正在重试……")
            time.sleep(1)
            num_retries -= 1
            get_data(url, num_retries)

    return data_1

# 解析数据
def parse_data(data):
    if(data != None):
        soup = BeautifulSoup(data.text, 'lxml')
    else:
        print("无法访问")
        exit()
    # print(soup)
    # if(soup.find('ul',{'class':'messages'}).find_all('li')[0].get_text() == 'No items found.'):
    #    print("No items found.")
    #   exit()
    # else:
    try:
        if (soup.find('ul', {'class', 'inline_list left display_settings'}).find_all('li')[0].get_text() == 'Summary'):
            first_result = soup.find('div', {'class': 'rprt'})
            key_num = first_result.find_all('a')[0].get('href')
            print("key_num:", key_num)
        elif ((soup.find('ul', {'class', 'inline_list left display_settings'}).find_all('li')[0].get_text() == 'Full')):
            if (data.text.find('<p>See Also:</p>') > 0):
                # t=data_2.text.find('<p>See Also:</p>')
                # print(t)
                Entry = re.findall(r'<p>Entry Terms:</p><ul><li>.*</li></ul><p>See Also:</p>', data.text)
            elif (data.text.find('<p>Previous Indexing:</p>') > 0):
                Entry = re.findall(r'<p>Entry Terms:</p><ul><li>.*</li></ul><p>Previous Indexing:</p>', data.text)
            else:
                # print('2')
                Entry = re.findall(r'<p>Entry Terms:</p><ul><li>.*</li></ul>', data.text)
            soup_3 = BeautifulSoup(''.join(Entry), 'lxml')
            # print(soup_2)
            Entry_Termses = soup_3.find_all('li')

            # 修改对解析结果格式
            datas = []
            for Entry_Termse in Entry_Termses:
                data = Entry_Termse.get_text()
                datas.append(data)

            Entrys = '(' + ')or('.join(datas) + ')'

            return Entrys
    except:
        print("No items found.")
        exit()

    # print(key_num)
    print("请求数据2……")
    url_2 = "https://www.ncbi.nlm.nih.gov" + key_num
    data_2 = get_data(url_2)
    # print(data_2.text)

    #soup_2 = BeautifulSoup(data_2.text, 'lxml')
    # print(soup_2)

    # Entry_Terms = soup_2.find_all('ul',{'class':None} and {'id':None})
    # Entry_Terms = Entry_Terms.find_all('li')
    print("解析数据……")
    if (data_2.text.find('<p>See Also:</p>') > 0):
        # t=data_2.text.find('<p>See Also:</p>')
        # print(t)
        Entry = re.findall(r'<p>Entry Terms:</p><ul><li>.*</li></ul><p>See Also:</p>', data_2.text)
    elif (data_2.text.find('<p>Previous Indexing:</p>') > 0):
        Entry = re.findall(r'<p>Entry Terms:</p><ul><li>.*</li></ul><p>Previous Indexing:</p>', data_2.text)
    else:
        # print('2')
        Entry = re.findall(r'<p>Entry Terms:</p><ul><li>.*</li></ul>', data_2.text)
    soup_2 = BeautifulSoup(''.join(Entry), 'lxml')
    # print(soup_2)
    Entry_Termses = soup_2.find_all('li')

    print("调整格式……")
    # 修改对解析结果格式
    datas = []
    for Entry_Termse in Entry_Termses:
        data = Entry_Termse.get_text()
        datas.append(data)

    Entrys = '(' + ')or('.join(datas) + ')'

    return Entrys


# 输入多个关键词
def input_keywords():
    key_words = []
    # 向列表中连续输入字符串
    while True:
        key_word = input('请输入要查找的关键词:')
        if key_word == 'quit':
            break
        key_words.append(key_word)
        print(key_words)

    return key_words


def run():
    key_values = input_keywords()
    # key_word = input('请输入要查找的关键词:')
    PubMed_words = []
    for key_value in key_values:
        print('*************************************')
        print("开始……")
        url_1 = "https://www.ncbi.nlm.nih.gov/mesh/?term=" + key_value
        data_result1 = get_data(url_1)
        data_result2 = parse_data(data_result1)
        PubMed_words.append(data_result2)
        reuslts = key_value + ':' + data_result2
        print(reuslts)

    # 打开浏览器，并显示结果
    print('*************************************')
    address = 'https://www.ncbi.nlm.nih.gov/pubmed?term=' + 'AND'.join(PubMed_words)
    print(address)
    webbrowser.open(address)
    #os.system('"C:/Program Files/Internet Explorer/iexplore.exe" ' + address)


if __name__=='__main__':
    run()
