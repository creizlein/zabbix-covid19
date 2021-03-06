#!/usr/bin/env python
#===============================================================================
# IDENTIFICATION DIVISION
#        ID SVN:   $Id$
#          FILE:  covid9_status.py
#         USAGE:  $0
#   DESCRIPTION:  Get Worldometers Coronavirus / Covid9 data and print to JSON
#  REQUIREMENTS:  pandas (pip install pandas)
#                 lxml (pip install lxml)
#          BUGS:  ---
#         NOTES:  ---
#          TODO:  ---
#        AUTHOR:  Ricardo Barbosa, rickkbarbosa@live.com
#       COMPANY:  ---
#       VERSION:  1.1
#       CREATED:  2020-Mar-10 21:47 BRT
#      REVISION:  2020-Nov-01 By creizlein
#===============================================================================

import re
import pandas as pd
import requests

url = 'https://www.worldometers.info/coronavirus/#countries'
header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36","X-Requested-With": "XMLHttpRequest"}

r = requests.get(url, headers=header).text
r = re.sub(r'.*(<table id="main_table_countries_today".*?>.*?<\/table>).*', r'\1', r, flags=re.DOTALL)
r = re.sub(r'<tbody class="body_continents">.*?<\/tbody>', '', r, flags=re.DOTALL)
r = re.sub(r'<.*?>', lambda g: g.group(0).upper(), str(r))

df = pd.read_html(r, index_col=1, thousands=r',', flavor="bs4")[0]
df = df.replace(regex=[r'\+', r'\,'], value='')

df = df.fillna('0')
df = df.to_json(orient='index')

print(df)

