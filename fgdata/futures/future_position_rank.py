# -*- coding: utf-8 -*-
import requests
from lxml import html
import pandas as pd

# 示例url
url = f'https://vip.stock.finance.sina.com.cn/q/view/vFutures_Positions_cjcc.php?t_breed=FU2505&t_date=2024-12-25'

def futures_position_rank_sina(futures_code='FU2505', t_date='2024-12-25'):
    # 根据期货品种代码和日期构建URL
    url = f'https://vip.stock.finance.sina.com.cn/q/view/vFutures_Positions_cjcc.php?t_breed={futures_code}&t_date={t_date}'
    
    try:
        # 使用requests库发送GET请求，获取网页内容
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        response.encoding = response.apparent_encoding  # 设置正确的编码

        # 解析网页内容
        doc = html.fromstring(response.text)
        # print(response.text)

        # 初始化数据列表
        data = []

        # 遍历表格中的每一行，提取数据
        # rows = doc.xpath('/html/body/div[3]/table/tbody/tr/td[1]/table/tbody/tr')
        # rows = doc.xpath('/html/body/div[3]/table/tbody/tr/td[1]/table/tbody')  # 移除 tbody
        rows = doc.xpath('/html/body/div[3]/table/tr/td[1]/table/tr')
        # print("rows",rows)
        for row in rows[1:]:  # 跳过表头
            rank = row.xpath('./td[1]/text()')[0] # 名次字段
            member_name = row.xpath('./td[2]/a/text()')  # 会员简称字段
            volume = row.xpath('./td[3]/text()')[0] # 成交量字段
            change = row.xpath('./td[4]/text()')[0]  # 增减字段
            print('member_name',type(member_name),'volume',type(volume),'change',type(change) )

            # 将提取的数据添加到列表中
            data.append([rank, member_name, volume, change])

        # 创建DataFrame
        df = pd.DataFrame(data, columns=['名次', '会员简称', '成交量', '增减'])

        df['futures_code'] = futures_code
        df['t_date'] = t_date

        return df

    except requests.exceptions.RequestException as e:
        print(f"请求网页时发生错误：{e}")
        return None
    
if __name__ == '__main__':
    futures_code = 'FU2505'
    t_date = '2025-01-27'
    df = futures_position_rank_sina(futures_code, t_date)
    print(df)