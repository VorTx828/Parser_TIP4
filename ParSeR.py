from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os

# Кажется, у Славы работает только с этим импортом. У Тихона работает без него
# if os.path.exists('C:\\Program Files\\ChromeDriver\\chromedriver-win64\\chromedriver.exe'):
#     from seleniumwire import webdriver

import time
import sqlite3
import tkinter as tk
import threading as td



def interceptor(request):
    del request.headers["User-Agent"]
    del request.headers["Sec-Ch-Ua"]
    del request.headers["Sec-Fetch-Site"]
    del request.headers["Accept-Encoding"]



    request.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 YaBrowser/24.7.0.0 Safari/537.36"
    # request.headers["Sec-Ch-Ua"] = "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Google Chrome\";v=\"122\""
    request.headers["Sec-Fetch-Site"] = "cross-site"
    request.headers["Accept-Encoding"] = "gzip, deflate, br, zstd"

def DomSearch(url):
    SelConnect(url[2])



    res = driver.find_element(By.CLASS_NAME, "content")

    title = res.find_element(By.CSS_SELECTOR, "h1").get_attribute("innerHTML")
    price = res.find_element(By.CSS_SELECTOR, "div.item_current_price").get_attribute("innerHTML")


    if price and title:
    
        info = {"Айди товара": url[0], "Цена товара": int(price), "Название товара": title, "Директория сайта": url[2]}

        result["https://gipermarketdom.ru/"].append(info)
    
def VodSearch(url):
    SelConnect(url[3])



    card = driver.find_element(By.CSS_SELECTOR, "div.product-card__actions")

    price = card.find_element(By.CSS_SELECTOR, "p.product-item__price-new").get_attribute("innerHTML")
    title = card.find_element(By.CSS_SELECTOR, "h1.block-title").get_attribute("innerHTML")


    if price and title and url:
    
        ar=price.split()

        price=int("".join(ar[:2]))


        info = {"Айди товара": url[0], "Цена товара": price, "Название товара": title, "Директория сайта": url[3]}

        result["https://www.vodoparad.ru/"].append(info)    

def ParseFromShops():

    cursor.execute("SELECT * FROM Good")
    goods=cursor.fetchall()


    for g in goods:

        DomSearch(g)

        VodSearch(g)

    global IsDone

    IsDone=True
       
def CreateDB(name="Goods.db"):
    global conn
    global cursor

    conn = sqlite3.connect(name)
    cursor = conn.cursor()




    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Shops (
    ShopID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Url TEXT NOT NULL
    )
    ''')

    cursor.execute('''
INSERT INTO Shops (ShopID, Name, Url) VALUES (?, ?, ?) ON CONFLICT(ShopID) DO NOTHING;
''', (1,"gipermarketdom", "https://gipermarketdom.ru/"))



    cursor.execute('''
INSERT INTO Shops (ShopID, Name, Url) VALUES (?, ?, ?) ON CONFLICT(ShopID) DO NOTHING;
''', (2, "vodoparad", "https://www.vodoparad.ru/"))
    


    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Good (
    GoodID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    DomUrl TEXT NOT NULL,
    VodUrl TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Prices (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    GoodID INTEGER NOT NULL,
    ShopID INTEGER NOT NULL,
    Name TEXT NOT NULL,
    Price INTEGER NOT NULL,
    CardUrl TEXT NOT NULL
    )
    ''')

    conn.commit()

def SelConnect(site):
    while True:
        try:
            driver.get(site)
            time.sleep(0.1)  # Wait for the page to load
            break
        except Exception as e:
            print(f"Error occurred: {e}, trying again after 5 seconds")
            time.sleep(5)

def ResultToDB():
    
    for el in result["https://gipermarketdom.ru/"]:
        cursor.execute('''
    INSERT INTO Prices (GoodCategoryID, ShopID, Name, Price, CardUrl) VALUES (?, ?, ?, ?, ?);
    ''', (el["Айди товара"], 1, el["Название товара"], el["Цена товара"], el["Директория сайта"]))
        conn.commit()

    for el in result["https://www.vodoparad.ru/"]:
        cursor.execute('''
    INSERT INTO Prices (GoodCategoryID, ShopID, Name, Price, CardUrl) VALUES (?, ?, ?, ?, ?);
    ''', (el["Айди товара"], 2, el["Название товара"], el["Цена товара"], el["Директория сайта"]))
        conn.commit()

def Interface():
    

    def get_input():
        # Получаем данные из поля ввода


        if entry1.get():
            cursor.execute('''
    INSERT INTO Good (Name, DomUrl, VodUrl) VALUES (?, ?, ?)
    ''', (entry1.get(), entry2.get(), entry3.get()))


            entry1.delete(0, tk.END)
            entry2.delete(0, tk.END)
            entry3.delete(0, tk.END)

            conn.commit()


        # messagebox.showinfo("Ввод", f"Вы ввели: {user_input}")  # Показываем введенные данные в 

    def MakeNewWindow(title="Результаты парсинга"):
        result="Подождите, производится парсинг"

        window = tk.Tk()

        window.title(title)

        label = tk.Label(window, text=result)
        label.pack()

        if IsDone:

            result= "Полученные результаты парсинга"


            def display_array(array, listbox):
                # Очищаем Listbox перед добавлением новых данных
                listbox.delete(0, tk.END)
                
                for dic in array:
                    for key in dic:
                    # Преобразуем каждую строку массива в строку текста и добавляем в Listbox
                        listbox.insert(tk.END, ' '.join(map(str, dic[key])))
            
            listbox = tk.Listbox(root, width=30, height=10)
            listbox.pack(pady=20)

            display_array(result["https://gipermarketdom.ru/"], listbox)

            listbox1 = tk.Listbox(root, width=30, height=10)
            listbox1.pack(pady=20)

            display_array(result["https://www.vodoparad.ru/"], listbox1)

        window.mainloop()

    def result():

        thread = td.Thread(target=MakeNewWindow)

        thread.start()

        ParseFromShops()

        ResultToDB()

    root = tk.Tk()
    root.title("Парсер сайта")

    label = tk.Label(root, text="Выберите опцию")
    label.pack()


    labe2 = tk.Label(root, text="Введите данные (1 строка - название товара, 2 строка - ссылка на товар на сайте Dom, 3 строка - ссылка на товар на сайте Vod)")
    labe2.pack()


    entry1 = tk.Entry(root)
    entry1.pack(pady=10)

    entry2 = tk.Entry(root)
    entry2.pack(pady=10)

    entry3 = tk.Entry(root)
    entry3.pack(pady=10)


    
    button = tk.Button(root, text="Добавить название товара и ссылку", command=get_input)
    button.pack(pady=10)

    button = tk.Button(root, text="Перейти к результатам", command=result)
    button.pack(pady=10)



    root.mainloop()

def ResultToDB():

    # cursor.execute("SELECT * FROM Good")
    # g=cursor.fetchall()

    # r={}

    # for i in g:
    #     r[i[1]]=i[2]
    
    for el in result["https://gipermarketdom.ru/"]:
        cursor.execute('''
    INSERT INTO Prices (GoodID, ShopID, Name, Price, CardUrl) VALUES (?, ?, ?, ?, ?);
    ''', (el["Айди товара"], 1, el["Название товара"], el["Цена товара"], el["Директория сайта"]))
        conn.commit()

    for el in result["https://www.vodoparad.ru/"]:
        cursor.execute('''
    INSERT INTO Prices (GoodID, ShopID, Name, Price, CardUrl) VALUES (?, ?, ?, ?, ?);
    ''', (el["Айди товара"], 2, el["Название товара"], el["Цена товара"], el["Директория сайта"]))
        conn.commit()



# url = "https://gipermarketdom.ru/"
# url2="https://www.vodoparad.ru/"
result = {"https://gipermarketdom.ru/":[], "https://www.vodoparad.ru/":[]}

IsDone=False

# Слава
if os.path.exists('C:\\Program Files\\ChromeDriver\\chromedriver-win64\\chromedriver.exe'):
    # Set up Selenium with Chrome
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-extensions")
    chrome_service = Service('C:\\Program Files\\ChromeDriver\\chromedriver-win64\\chromedriver.exe')  # Update with your path to chromedriver
    chrome_options.binary_location = "C:\\Program Files\\ChromeDriver\\chrome-win64\\chrome.exe"
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
# Тихон
elif os.path.exists('C:\\Program Files (x86)\\Microsoft\\WebDriver\\msedgedriver.exe'):
    edge_options = webdriver.EdgeOptions()
    edge_service = webdriver.EdgeService('C:\\Program Files (x86)\\Microsoft\\WebDriver\\msedgedriver.exe')  # Update with your path to chromedriver
    edge_options.binary_location = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
    driver = webdriver.Edge(service=edge_service, options=edge_options)
else:
    print("Для вас не было настроено открывание браузера :(")

driver.request_interceptor = interceptor
driver.maximize_window()


CreateDB()

Interface()

