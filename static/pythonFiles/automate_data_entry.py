from merchant.models import *
import pandas as pd
import os
import json

def excel_to_json():
    # with open(os.path.join(path, 'rooms.json'), 'r') as json_file:
    #     data = json.load(json_file)
    
    # for room_number, room_data in data.items():
    #     if not Room.objects.filter(room_number=room_number).exists():
    #         Room.objects.create(
    #             room_number=room_number,
    #             room_name=room_data['room_name'],
    #             rent_amount=Decimal(room_data['rent_amount']),
    #             available=room_data['available']
    #         )
    return

def enter_user(path):
    dataframe1 = pd.read_excel(os.path.join(path, 'user.xlsx'))
    dataframe1 = dataframe1.astype(str)
    for x in range(len(dataframe1)):
        first_name = dataframe1[x]['first_name']
        last_name = dataframe1[x]['last_name']
        email = dataframe1[x]['email']
        username = dataframe1[x]['username']
        password = dataframe1[x]['password']
        is_superuser = dataframe1[x]['is_superuser']
        is_staff = dataframe1[x]['is_staff']
        is_active = dataframe1[x]['is_active']
        User.objects.create(
            
            first_name = first_name, last_name = last_name,
            username = username, password = password,
            email = email, is_active = is_active,
            is_staff = is_staff, is_superuser = is_superuser
            )

def enter_tags(path):
    dataframe1 = pd.read_excel(os.path.join(path, 'tags.xlsx'))
    dataframe1 = dataframe1.astype(str)
    for x in range(len(dataframe1)):
        title = dataframe1.iloc[x]['title']
        Tag.objects.create(
            title = title
        )

def enter_category(path):
    dataframe1 = pd.read_excel(os.path.join(path, 'category.xlsx'))
    dataframe1 = dataframe1.astype(str)
    return

def enter_store(path):
    dataframe1 = pd.read_excel(os.path.join(path, 'tags.xlsx'))
    dataframe1 = dataframe1.astype(str)
    return

def enter_products(path):
    dataframe1 = pd.read_excel(os.path.join(path, 'tags.xlsx'))
    dataframe1 = dataframe1.astype(str)
    return 

def enter_review(path):
    dataframe1 = pd.read_excel(os.path.join(path, 'tags.xlsx'))
    dataframe1 = dataframe1.astype(str)
    return

def automate_data_entry():
    path = "static/pythonFiles"
    # enter_user()
    enter_store()
    # enter_category()
    # enter_tags(path) #done
    # enter_products()
    # enter_review()
    print('Function called')
    