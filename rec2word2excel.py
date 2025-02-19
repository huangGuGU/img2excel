import os
import pandas as pd
from PIL import Image
from pytesseract import pytesseract
import re

file_path = '/Users/hzh/Desktop/img'
img_list = os.listdir(file_path)
try:
    img_list.remove('.DS_Store')
except:
    pass
project_list, year_list, month_list = [], [], []
img_list = sorted(img_list, key=lambda x: (int(x.split('_')[0]), x.split('_')[1]))
for i in range(0, len(img_list), 3):  # 年
    img_year_path = os.path.join(file_path, img_list[i])
    text = pytesseract.image_to_string(Image.open(img_year_path))
    cleaned_text = re.sub(r'[^0-9.,]', '', text)
    year_list.append(cleaned_text)
df_year = pd.DataFrame(year_list, columns=['本年累计金额'])

for j in range(1, len(img_list), 3):  # 月
    img_month_path = os.path.join(file_path, img_list[j])
    text = pytesseract.image_to_string(Image.open(img_month_path))
    cleaned_text = re.sub(r'[^0-9.,]', '', text)
    month_list.append(cleaned_text)
df_month = pd.DataFrame(month_list, columns=['本月金额'])

for k in range(2, len(img_list), 3):  # 项目
    img_project_path = os.path.join(file_path, img_list[k])
    text = pytesseract.image_to_string(Image.open(img_project_path), lang='chi_sim')
    cleaned_text = re.sub(r'[^\u4e00-\u9fa5:、：“”]', '', text)

    project_list.append(cleaned_text)

df_project = pd.DataFrame(project_list)
df_combined = pd.concat([df_project, df_year, df_month], axis=1)

# 将合并后的 DataFrame 写入 Excel
df_combined.to_excel('merged_output.xlsx', index=False)
