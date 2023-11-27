import pandas as pd
import numpy as np
import os

main_path = os.getcwd()
area_dataset_dir = os.path.join(main_path, 'dataset/crime_by_area')
office_dataset_dir = os.path.join(main_path, 'dataset/crime_by_office')

area_file_list = [os.path.join(area_dataset_dir, file)
                  for file in os.listdir(area_dataset_dir)]
office_file_list = [os.path.join(office_dataset_dir, file)
                    for file in os.listdir(office_dataset_dir)]


def get_area_file(year):
    return f'{area_dataset_dir}/경찰청_서울특별시지방경찰청_범죄발생 장소별 현황_{year}.csv'


def get_office_file(year):
    return f'{office_dataset_dir}/경찰청_서울특별시지방경찰청_관서별 5대범죄 발생 및 검거 현황_{year}.csv'


year_options = [2016, 2017, 2018, 2019, 2020, 2021]
guilty_options = ['살인', '강도', '강간', '절도', '폭력']
