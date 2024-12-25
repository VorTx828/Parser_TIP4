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

import time


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
    
        info = {"Айди товара": url[0], "Цена товара": int(price), "Название товара": title, "Дата": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"Директория сайта": url[2]}

        result["https://gipermarketdom.ru/"].append(info)
    
def VodSearch(url):
    SelConnect(url[3])



    card = driver.find_element(By.CSS_SELECTOR, "div.product-card__actions")

    price = card.find_element(By.CSS_SELECTOR, "p.product-item__price-new").get_attribute("innerHTML")
    title = card.find_element(By.CSS_SELECTOR, "h1.block-title").get_attribute("innerHTML")


    if price and title and url:
    
        ar=price.split()

        price=int("".join(ar[:2]))


        info = {"Айди товара": url[0], "Цена товара": price, "Название товара": title, "Дата": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "Директория сайта": url[3]}

        result["https://www.vodoparad.ru/"].append(info)    

def NeptunSearch(url):
    SelConnect(url[4])



    card = driver.find_element(By.CSS_SELECTOR, "div.product-main-col.flex-row-item")

    price = card.find_element(By.CSS_SELECTOR, "div.product-price").get_attribute("innerHTML")
    title = card.find_element(By.CSS_SELECTOR, "h1.page-title.section-title.product-title.js-title").get_attribute("innerHTML")


    if price and title and url:
    
        ar=price.split('"')

        price=int("".join(ar[0][:-1]))


        info = {"Айди товара": url[0], "Цена товара": price, "Название товара": title, "Дата": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "Директория сайта": url[4]}

        result["https://neptun66.ru"].append(info)  

def GroheSearch(url):

    #Ванна акриловая Tira 1700х700мм


    SelConnect(url[5])


    price = driver.find_element(By.CSS_SELECTOR, "span.price product.product-price__price").get_attribute("#text")
    title = driver.find_element(By.CSS_SELECTOR, "h1.product-card__title.js-name").get_attribute("innerHTML")


    if price and title and url:
    
        ar=price.replace("&nbsp;","").replace('"', "")

        price=int("".join(ar))


        info = {"Айди товара": url[0], "Цена товара": price, "Название товара": title, "Дата": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "Директория сайта": url[5]}

        result["https://grohe-russia.shop"].append(info) 



def ParseFromShops():

    cursor.execute("SELECT * FROM Good")
    goods=cursor.fetchall()


    for g in goods:

        DomSearch(g)

        VodSearch(g)

        NeptunSearch(g)

        GroheSearch(g)

       
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
INSERT INTO Shops (ShopID, Name, Url) VALUES (?, ?, ?) ON CONFLICT(ShopID) DO NOTHING;
''', (3, "neptun66", "https://neptun66.ru/"))

    cursor.execute('''
INSERT INTO Shops (ShopID, Name, Url) VALUES (?, ?, ?) ON CONFLICT(ShopID) DO NOTHING;
''', (4, "grohe", "https://grohe-russia.shop/"))
    


    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Good (
    GoodID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    DomUrl TEXT NOT NULL,
    VodUrl TEXT NOT NULL,
    NepUrl TEXT NOT NULL,
    GroUrl TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Prices (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    GoodID INTEGER NOT NULL,
    ShopID INTEGER NOT NULL,
    Name TEXT NOT NULL,
    Price INTEGER NOT NULL,
    CardUrl TEXT NOT NULL,
    DateTime TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Results (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    GoodID INTEGER NOT NULL,
    ShopID INTEGER NOT NULL,
    Name TEXT NOT NULL,
    Price INTEGER NOT NULL,
    CardUrl TEXT NOT NULL,
    UNIQUE (GoodID, ShopID)
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

def Interface():
    

    def get_input():
        # Получаем данные из поля ввода


        if entry1.get():
            cursor.execute('''
    INSERT INTO Good (Name, DomUrl, VodUrl, NepUrl, GroUrl) VALUES (?, ?, ?, ?, ?)
    ''', (entry1.get(), entry2.get(), entry3.get(), entry4.get(), entry5.get()))


            entry1.delete(0, tk.END)
            entry2.delete(0, tk.END)
            entry3.delete(0, tk.END)

            conn.commit()


        # messagebox.showinfo("Ввод", f"Вы ввели: {user_input}")  # Показываем введенные данные в 

    def MakeNewWindow(title="Результаты парсинга"):
        def display(arr):
            return f"GoodID: {str(arr[0])}, Price: {str(arr[1])}, Title: {str(arr[2])}, Time: {str(arr[3])}, Url: {str(arr[4])}"

        def on_click():
                selected_index = listbox.curselection()
                if selected_index: 
                    selected_value = listbox.get(selected_index)
                    r = selected_value.split("Url: ")[-1]
                    SelConnect(r)

        def display_array(mylistbox):
            # Очищаем Listbox перед добавлением новых данных  res[""]=[{},{}]    s=[ [ [],[],[] ],[ [],[] ] ]
            mylistbox.delete(0, tk.END)
            s=[[],[]]
            for dic in result["https://gipermarketdom.ru/"]:
                r=[]
                for key in dic:
                    r.append(dic[key])
                s[0].append(r)
            for dic in result["https://www.vodoparad.ru/"]:
                r=[]
                for key in dic:
                    r.append(dic[key])
                s[1].append(r)

            for i in range(s[0].__len__()):
                m1=display(s[0][i])
                m2=display(s[1][i])
                mylistbox.insert(tk.END,(m1, m2)[s[0][i][1]<=s[1][i][1]])


        window = tk.Tk()

        r = "Полученные результаты парсинга (с минимальными ценами)"

        window.title(title)

        label = tk.Label(window, text=r)
        label.pack()

        
        listbox = tk.Listbox(window, width=200, height=10)
        listbox.pack(pady=20)

        display_array(listbox)


        button = tk.Button(window, text="Перейти к выбранному элементу", command=on_click)
        button.pack(pady=20)

        window.mainloop()

    def Button():

        ParseFromShops()

        th=td.Thread(target=MakeNewWindow)

        th.start()

        # MakeNewWindow()

        ResultToDB()

    root = tk.Tk()
    root.title("Парсер сайта")

    label = tk.Label(root, text="Выберите опцию")
    label.pack()


    labe2 = tk.Label(root, text="Введите данные (1 строка - название товара, 2 строка - ссылка на товар на сайте Dom, 3 строка - ссылка на товар на сайте Vod)")
    labe2.pack()

    labe3 = tk.Label(root, text="Название товара")
    labe3.pack()
    
    entry1 = tk.Entry(root)
    entry1.pack(pady=10)

    labe4 = tk.Label(root, text="Ссылка на товар на сайте Dom")
    labe4.pack()

    entry2 = tk.Entry(root)
    entry2.pack(pady=10)

    labe5 = tk.Label(root, text="Ссылка на товар на сайте Vod")
    labe5.pack()

    entry3 = tk.Entry(root)
    entry3.pack(pady=10)

    labe6 = tk.Label(root, text="Ссылка на товар на сайте Nep")
    labe6.pack()

    entry4 = tk.Entry(root)
    entry4.pack(pady=10)


    labe7 = tk.Label(root, text="Ссылка на товар на сайте Grohe")
    labe7.pack()

    entry5 = tk.Entry(root)
    entry5.pack(pady=10)


    
    button = tk.Button(root, text="Добавить название товара и ссылку", command=get_input)
    button.pack(pady=10)

    button = tk.Button(root, text="Перейти к результатам", command=Button)
    button.pack(pady=10)



    root.mainloop()

def ResultToDB():

    # cursor.execute("SELECT * FROM Good")
    # g=cursor.fetchall()

    # r={}

    # for i in g:
    #     r[i[1]]=i[2]

    i=0
    
    for el in result["https://gipermarketdom.ru/"]:
        cursor.execute('''
    INSERT INTO Prices (GoodID, ShopID, Name, Price, CardUrl, DateTime) VALUES (?, ?, ?, ?, ?, ?);
    ''', (el["Айди товара"], 1, el["Название товара"], el["Цена товара"], el["Директория сайта"], el["Дата"]))

        if el["Цена товара"] <= result["https://www.vodoparad.ru/"][i]["Цена товара"]:

            cursor.execute('''
        INSERT INTO Results (GoodID, ShopID, Name, Price, CardUrl) VALUES (?, ?, ?, ?, ?) ON CONFLICT(GoodID, ShopID) DO UPDATE SET Name = excluded.Name, Price = excluded.Price, CardUrl = excluded.CardUrl;
        ''', (el["Айди товара"], 1, el["Название товара"], el["Цена товара"], el["Директория сайта"]))

        i+=1
        
        conn.commit()

    i=0

    for el in result["https://www.vodoparad.ru/"]:
        cursor.execute('''
    INSERT INTO Prices (GoodID, ShopID, Name, Price, CardUrl, DateTime) VALUES (?, ?, ?, ?, ?, ?);
    ''', (el["Айди товара"], 2, el["Название товара"], el["Цена товара"], el["Директория сайта"], el["Дата"]))


        if el["Цена товара"] <= result["https://gipermarketdom.ru/"][i]["Цена товара"]:

            cursor.execute('''
        INSERT INTO Results (GoodID, ShopID, Name, Price, CardUrl) VALUES (?, ?, ?, ?, ?) ON CONFLICT(GoodID, ShopID) DO UPDATE SET Name = excluded.Name, Price = excluded.Price, CardUrl = excluded.CardUrl;
        ''', (el["Айди товара"], 1, el["Название товара"], el["Цена товара"], el["Директория сайта"]))

        i+=1

        conn.commit()
    

    
    conn.commit()



# url = "https://gipermarketdom.ru/"
# url2="https://www.vodoparad.ru/"
result = {"https://gipermarketdom.ru/":[], "https://www.vodoparad.ru/":[], "https://neptun66.ru":[], "https://grohe-russia.shop": []}


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

