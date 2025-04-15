from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import requests
import json
# 初始化 WebDriver
driver = webdriver.Chrome()






try:
    
    #driver = webdriver.Chrome()
   

    # 定义API的URL
    url = "https://care-rc.wisleep-eck.org/ota/login"

    # 定义请求的Payload
    payload = {
        "username": "admin",
        "password": "123456"
    }
        
        
    # 使用 requests.post 发送 POST 请求
    response = requests.post(url, json=payload)

    # 检查响应状态
    if response.status_code == 200:
        # 解析返回的 JSON 数据
        data = response.json()
        # 获取嵌套在 'data' 字段中的 token
        token = data.get("data", {}).get("token")
        print("token:",token)
        if token:
            print(f"登录成功，token: {token}")
        else:
            print("登录失败，未返回token")
    else:
        print(f"请求失败，状态码: {response.status_code}, 内容: {response.text}")
        
    
     
    '''    
    #upload                                                                                 #20250414
    # 网址
    url = 'https://care-rc.wisleep-eck.org/ota/upload/files'

    # 你的 Token
    #token = 'your_token_here'

    # 打开并读取 JSON 文件
    #with open('andarX_upload.json', 'r',encoding='utf-8') as file:
    #    data = json.load(file)

    # 设置请求头
    headers = {
        'Authorization': f'Bearer {token}',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryRoNgWgkzIESS5ZEz'
    }

    # 发起 POST 请求
    response = requests.post(url, headers=headers, json=data)

    # 检查响应状态
    if response.status_code == 200:
        print('上传成功')
    else:
        print(f'上传失败, 状态码: {response.status_code}')
        print('响应内容:', response.text)
    '''










    
    
    
    # 打開新的登錄頁面
    driver.get('https://care-rc.wisleep-eck.org/login.html')
    
    time.sleep(10)
    
    # 找到用户名输入框，并输入用户名
    # 找到用户名输入框，并输入用户名
    username_box = driver.find_element(By.ID, 'userName')  # 使用ID来定位用户名输入框
    username_box.send_keys('admin')

    # 找到密码输入框，并输入密码
    password_box = driver.find_element(By.ID, 'password')  # 或使用其他定位方法
    password_box.send_keys('123456')

    # 找到登录按钮并点击
    login_button = driver.find_element(By.CLASS_NAME, 'login-form-button')
    login_button.click()
        
    
    #driver.get('https://care-rc.wisleep-eck.org/list.html')
    #url = 'https://care-rc.wisleep-eck.org/ota/upload/files'
    driver.get('https://care-rc.wisleep-eck.org/list.html')
    
    time.sleep(10)
    
    switch_button = driver.find_element(By.XPATH, '//button[contains(@i18n, "switchToOta")]')
    switch_button.click()
    print("test1")
    time.sleep(5)
    
    # 使用 XPath 找到下拉選單元素
    # 使用 XPath 找到下拉選單元素
    dropdown = driver.find_element("xpath", "//select")

    # 使用 Select 來操作下拉選單
    select = Select(dropdown)

    
    
    
    # 選擇值為 "076f03" 的選項
    select.select_by_value("07a205")
    print("test2")
    time.sleep(3)
    

    switch_button = driver.find_element(By.XPATH, '//button[contains(@i18n, "searchUpdateX")]')
    switch_button.click()
    print("test3")
    time.sleep(3)
    
    
    driver.get('https://care-rc.wisleep-eck.org/upload.html')
    
    file_input = driver.find_element(By.ID, 'fileInput')  # 通过ID定位文件输入框    # 设置要上传的文件路径
    #file_path = 'D:\\andarX_upload.json'# 替换为你要上传的文件的实际路径
    #file_path = 'D:\\andarX_upload.json'# 替换为你要上传的文件的实际路径
    file_path = 'D://tools//auto_update_FD_raw_data//andarX_upload.json'# 替换为你要上传的文件的实际路径

    # 输入文件路径到文件输入框以选择文件
    file_input.send_keys(file_path)

    # 等待几秒观察效果
    time.sleep(5)

    # 可选：点击上传按钮
    upload_button = driver.find_element(By.ID, 'fileBtn')
    upload_button.click()

    #upload_json('andarX_upload.json', 'https://care-rc.wisleep-eck.org/ota/upload/files',token)

finally:
    # 關閉瀏覽器
    #driver.quit()
    print("Quit loop")

