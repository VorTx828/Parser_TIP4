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
from tkinter import messagebox

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


    if price and title:
    
        ar=price.split('<')[0].replace(" ", "")

        price=int(ar)


        info = {"Айди товара": url[0], "Цена товара": price, "Название товара": title, "Дата": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "Директория сайта": url[4]}

        result["https://neptun66.ru"].append(info)  

def GroheSearch(url):

    #Ванна акриловая Tira 1700х700мм


    SelConnect(url[5])


    price = driver.find_element(By.CSS_SELECTOR, "span.price.product.product-price__price").get_attribute("innerHTML")
    title = driver.find_element(By.CSS_SELECTOR, "h1.product-card__title.js-name").get_attribute("innerHTML")


    if price and title:
    
        ar=price.replace("&nbsp;","").split("<")[0]

        price=int(ar)


        info = {"Айди товара": url[0], "Цена товара": price, "Название товара": title, "Дата": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "Директория сайта": url[5]}

        result["https://grohe-russia.shop"].append(info) 

def DomotSearch(url):
    SelConnect(url[6])

    price = driver.find_element(By.CSS_SELECTOR, "span.price_value").get_attribute("innerHTML")
    title = driver.find_element(By.CSS_SELECTOR, "h1#pagetitle").get_attribute("innerHTML")

    if price and title:
    
        ar=price.replace("&nbsp;","").split("<")[0]

        price=int(ar)


        info = {"Айди товара": url[0], "Цена товара": price, "Название товара": title, "Дата": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "Директория сайта": url[5]}

        result["https://www.domotex.ru/"].append(info) 

def ParseFromShops():

    global result

    result = {"https://gipermarketdom.ru/":[], "https://www.vodoparad.ru/":[], "https://neptun66.ru":[], "https://grohe-russia.shop": [], "https://www.domotex.ru/":[]}

    cursor.execute("SELECT * FROM Good")
    goods=cursor.fetchall()


    for g in goods:
        DomSearch(g)
    for g in goods:
        VodSearch(g)
    for g in goods:
        NeptunSearch(g)
    for g in goods:
        GroheSearch(g)
    for g in goods:
        DomotSearch(g)

       
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
INSERT INTO Shops (ShopID, Name, Url) VALUES (?, ?, ?) ON CONFLICT(ShopID) DO NOTHING;
''', (5, "domotex", "https://www.domotex.ru/"))

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Good (
    GoodID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    DomUrl TEXT NOT NULL,
    VodUrl TEXT NOT NULL,
    NepUrl TEXT NOT NULL,
    GroUrl TEXT NOT NULL,
    DomoUrl TEXT NOT NULL
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
        product_name = entry_productName.get().strip()
        link_dom = entry_linkDom.get().strip()
        link_vod = entry_linkVod.get().strip()
        link_nep = entry_linkNep.get().strip()
        link_grohe = entry_linkGrohe.get().strip()
        link_domotex = entry_linkDomotex.get().strip()
        
        if not product_name or not link_dom or not link_vod or not link_nep or not link_grohe or not link_domotex:
            messagebox.showwarning("Парсер сайта", "Заполните все поля.")
            return
        
        cursor.execute('''
            INSERT INTO Good (Name, DomUrl, VodUrl, NepUrl, GroUrl, DomoUrl) VALUES (?, ?, ?, ?, ?, ?)
            ''', (product_name, link_dom, link_vod, link_nep, link_grohe, link_domotex))
        
        entry_productName.delete(0, tk.END)
        entry_linkDom.delete(0, tk.END)
        entry_linkVod.delete(0, tk.END)
        entry_linkNep.delete(0, tk.END)
        entry_linkGrohe.delete(0, tk.END)
        entry_linkDomotex.delete(0, tk.END)

        conn.commit()

        # messagebox.showinfo("Ввод", f"Вы ввели: {user_input}")  # Показываем введенные данные в 

    def MakeNewWindow(title="Результаты парсинга"):
        def display(i):

            #{"Айди товара": url[0], "Цена товара": price, "Название товара": title, "Дата": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "Директория сайта": url[5]}

            r1 = result["https://gipermarketdom.ru/"][i]["Цена товара"]
            r2 = result["https://grohe-russia.shop"][i]["Цена товара"]
            r3 = result["https://neptun66.ru"][i]["Цена товара"]
            r4 = result["https://www.vodoparad.ru/"][i]["Цена товара"]
            r5 = result["https://www.domotex.ru/"][i]["Цена товара"]

            # match min(r1, r2, r3, r4):
            #     case r1:
            #         s=result["https://gipermarketdom.ru/"][i]
            #         return f"GoodID: {str(s["Айди товара"])}, Price: {str(s["Цена товара"])}, Title: {str(s["Название товара"])}, Time: {str(s["Дата"])}, Url: {str(s["Директория сайта"])}"
            #     case r2:
            #         s=result["https://grohe-russia.shop"][i]
            #         return f"GoodID: {str(s["Айди товара"])}, Price: {str(s["Цена товара"])}, Title: {str(s["Название товара"])}, Time: {str(s["Дата"])}, Url: {str(s["Директория сайта"])}"
            #     case r3:
            #         s=result["https://neptun66.ru"][i]
            #         return f"GoodID: {str(s["Айди товара"])}, Price: {str(s["Цена товара"])}, Title: {str(s["Название товара"])}, Time: {str(s["Дата"])}, Url: {str(s["Директория сайта"])}"
            #     case r4:
            #         s=result["https://www.vodoparad.ru/"][i]
            #         return f"GoodID: {str(s["Айди товара"])}, Price: {str(s["Цена товара"])}, Title: {str(s["Название товара"])}, Time: {str(s["Дата"])}, Url: {str(s["Директория сайта"])}"
        
            min_price = min(r1, r2, r3, r4, r5)

            if min_price == r1:
                s = result["https://gipermarketdom.ru/"][i]
            elif min_price == r2:
                s = result["https://grohe-russia.shop"][i]
            elif min_price == r3:
                s = result["https://neptun66.ru"][i]
            elif min_price == r4:
                s = result["https://www.vodoparad.ru/"][i]
            elif min_price == r5:
                s = result["https://www.domotex.ru/"][i]

            return f"GoodID: {str(s['Айди товара'])}, Price: {str(s['Цена товара'])}, Title: {str(s['Название товара'])}, Time: {str(s['Дата'])}, Url: {str(s['Директория сайта'])}"

        def on_click():
            selected_index = listbox.curselection()
            if selected_index: 
                selected_value = listbox.get(selected_index)
                r = selected_value.split("Url: ")[-1]
                SelConnect(r)

        def display_array(mylistbox):
            mylistbox.delete(0, tk.END)
            for i in range(result["https://gipermarketdom.ru/"].__len__()):
                mylistbox.insert(tk.END, display(i))

                
                


        window = tk.Tk()

        frame_header = tk.Frame(window, bg = "#2A2927")
        frame_header.pack(anchor=tk.N,fill=tk.X)

        window.title(title)

        label_header1 = tk.Label(frame_header, text="Полученные результаты парсинга", bg="#2A2927", fg="#CECBC6", font=("Montserrat", 24, "bold"))
        label_header1.pack(anchor=tk.W, padx=40, pady=(20,0))

        label_header2 = tk.Label(frame_header, text="С минимальными ценами", bg="#2A2927", fg="#CECBC6", font=("Montserrat", 12))
        label_header2.pack(anchor=tk.W, padx=40, pady=(0,20))
        
        frame_main = tk.Frame(window, bg="#CECBC6")
        frame_main.pack(fill=tk.BOTH, expand=True)

        listbox = tk.Listbox(frame_main, width=200, height=10)
        listbox.pack(pady=20)

        display_array(listbox)

        button_go = tk.Button(frame_main, text="Перейти к выбранному элементу", command=on_click, width=35, bd=0, bg="#2A2927", fg="#CECBC6")
        button_go.pack(anchor=tk.S, pady=40)

        window.mainloop()

    def Button():

        ParseFromShops()

        th=td.Thread(target=MakeNewWindow)

        th.start()

        # MakeNewWindow()

        ResultToDB()

    root = tk.Tk()
    root.title("Парсер сайта")
    root.geometry("900x560")
    root.resizable(width=False, height=False)

    frame_header = tk.Frame(root, bg = "#2A2927")
    frame_header.pack(anchor=tk.N,fill=tk.X)

    label_header1 = tk.Label(frame_header, text="Выберите опцию", bg="#2A2927", fg="#CECBC6", font=("Montserrat", 24, "bold"))
    label_header1.pack(anchor=tk.W, padx=40, pady=(20,0))

    label_header2 = tk.Label(frame_header, text="Введите данные", bg="#2A2927", fg="#CECBC6", font=("Montserrat", 12))
    label_header2.pack(anchor=tk.W, padx=40, pady=(0,20))

    frame_main = tk.Frame(root, bg="#CECBC6")
    frame_main.pack(fill=tk.BOTH, ipady=50)

    labelFrame_productName = tk.LabelFrame(frame_main, text="Название товара", font=("Montserrat",8), bg="#CECBC6", bd="0")
    labelFrame_productName.pack(anchor=tk.W, padx=40, pady=(40,5))
    entry_productName = tk.Entry(labelFrame_productName, width=70)
    entry_productName.pack()

    labelFrame_linkDom = tk.LabelFrame(frame_main, text="Ссылка на товар на сайте Dom", font=("Montserrat",8), bg="#CECBC6", bd="0")
    labelFrame_linkDom.pack(anchor=tk.W, padx=40, pady=5)
    entry_linkDom = tk.Entry(labelFrame_linkDom, width=70)
    entry_linkDom.pack()

    labelFrame_linkVod = tk.LabelFrame(frame_main, text="Ссылка на товар на сайте Vod", font=("Montserrat",8), bg="#CECBC6", bd="0")
    labelFrame_linkVod.pack(anchor=tk.W, padx=40, pady=5)
    entry_linkVod = tk.Entry(labelFrame_linkVod, width=70)
    entry_linkVod.pack()

    labelFrame_linkNep = tk.LabelFrame(frame_main, text="Ссылка на товар на сайте Nep", font=("Montserrat",8), bg="#CECBC6", bd="0")
    labelFrame_linkNep.pack(anchor=tk.W, padx=40, pady=5)
    entry_linkNep = tk.Entry(labelFrame_linkNep, width=70)
    entry_linkNep.pack()

    labelFrame_linkGrohe = tk.LabelFrame(frame_main, text="Ссылка на товар на сайте Grohe", font=("Montserrat",8), bg="#CECBC6", bd="0")
    labelFrame_linkGrohe.pack(anchor=tk.W, padx=40, pady=5)
    entry_linkGrohe = tk.Entry(labelFrame_linkGrohe, width=70)
    entry_linkGrohe.pack()

    labelFrame_linkDomotex = tk.LabelFrame(frame_main, text="Ссылка на товар на сайте Domotex", font=("Montserrat",8), bg="#CECBC6", bd="0")
    labelFrame_linkDomotex.pack(anchor=tk.W, padx=40, pady=5)
    entry_linkDomotex = tk.Entry(labelFrame_linkDomotex, width=70)
    entry_linkDomotex.pack()
    
    
    button_get = tk.Button(frame_main, text="Добавить название товара и ссылку", command=get_input, width=35, bd=0)
    button_get.pack(anchor=tk.E, padx=40, pady=(50,5))

    button_run = tk.Button(frame_main, text="Перейти к результатам", command=Button, width=35, bd=0, bg="#2A2927", fg="#CECBC6")
    button_run.pack(anchor=tk.E, padx=40, pady=(5,10))

    root.mainloop()

def MinPrice(i):
    r1 = result["https://gipermarketdom.ru/"][i]["Цена товара"]
    r2 = result["https://grohe-russia.shop"][i]["Цена товара"]
    r3 = result["https://neptun66.ru"][i]["Цена товара"]
    r4 = result["https://www.vodoparad.ru/"][i]["Цена товара"]
    r5 = result["https://www.domotex.ru/"][i]["Цена товара"]

    return min(r1, r2, r3, r4, r5)

def ResultToDB():

    

    i=0
    
    for el in result["https://gipermarketdom.ru/"]:
        cursor.execute('''
    INSERT INTO Prices (GoodID, ShopID, Name, Price, CardUrl, DateTime) VALUES (?, ?, ?, ?, ?, ?);
    ''', (el["Айди товара"], 1, el["Название товара"], el["Цена товара"], el["Директория сайта"], el["Дата"]))

        if el["Цена товара"] <= MinPrice(i):

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


        if el["Цена товара"] <= MinPrice(i):

            cursor.execute('''
        INSERT INTO Results (GoodID, ShopID, Name, Price, CardUrl) VALUES (?, ?, ?, ?, ?) ON CONFLICT(GoodID, ShopID) DO UPDATE SET Name = excluded.Name, Price = excluded.Price, CardUrl = excluded.CardUrl;
        ''', (el["Айди товара"], 2, el["Название товара"], el["Цена товара"], el["Директория сайта"]))

        i+=1

        conn.commit()


    i=0

    for el in result["https://neptun66.ru"]:
        cursor.execute('''
    INSERT INTO Prices (GoodID, ShopID, Name, Price, CardUrl, DateTime) VALUES (?, ?, ?, ?, ?, ?);
    ''', (el["Айди товара"], 3, el["Название товара"], el["Цена товара"], el["Директория сайта"], el["Дата"]))


        if el["Цена товара"] <= MinPrice(i):

            cursor.execute('''
        INSERT INTO Results (GoodID, ShopID, Name, Price, CardUrl) VALUES (?, ?, ?, ?, ?) ON CONFLICT(GoodID, ShopID) DO UPDATE SET Name = excluded.Name, Price = excluded.Price, CardUrl = excluded.CardUrl;
        ''', (el["Айди товара"], 3, el["Название товара"], el["Цена товара"], el["Директория сайта"]))

        i+=1

        conn.commit()

    i=0


    for el in result["https://grohe-russia.shop"]:
        cursor.execute('''
    INSERT INTO Prices (GoodID, ShopID, Name, Price, CardUrl, DateTime) VALUES (?, ?, ?, ?, ?, ?);
    ''', (el["Айди товара"], 4, el["Название товара"], el["Цена товара"], el["Директория сайта"], el["Дата"]))


        if el["Цена товара"] <= MinPrice(i):

            cursor.execute('''
        INSERT INTO Results (GoodID, ShopID, Name, Price, CardUrl) VALUES (?, ?, ?, ?, ?) ON CONFLICT(GoodID, ShopID) DO UPDATE SET Name = excluded.Name, Price = excluded.Price, CardUrl = excluded.CardUrl;
        ''', (el["Айди товара"], 4, el["Название товара"], el["Цена товара"], el["Директория сайта"]))

        i+=1

        conn.commit()
    
    i=0

    for el in result["https://www.domotex.ru/"]:
        cursor.execute('''
    INSERT INTO Prices (GoodID, ShopID, Name, Price, CardUrl, DateTime) VALUES (?, ?, ?, ?, ?, ?);
    ''', (el["Айди товара"], 5, el["Название товара"], el["Цена товара"], el["Директория сайта"], el["Дата"]))


        if el["Цена товара"] <= MinPrice(i):

            cursor.execute('''
        INSERT INTO Results (GoodID, ShopID, Name, Price, CardUrl) VALUES (?, ?, ?, ?, ?) ON CONFLICT(GoodID, ShopID) DO UPDATE SET Name = excluded.Name, Price = excluded.Price, CardUrl = excluded.CardUrl;
        ''', (el["Айди товара"], 5, el["Название товара"], el["Цена товара"], el["Директория сайта"]))

        i+=1

        conn.commit()
    
    conn.commit()



# url = "https://gipermarketdom.ru/"
# url2="https://www.vodoparad.ru/"
# result = {"https://gipermarketdom.ru/":[], "https://www.vodoparad.ru/":[], "https://neptun66.ru":[], "https://grohe-russia.shop": []}


# Слава
if os.path.exists('chromedriver-win64\\chromedriver.exe'):
    # Set up Selenium with Chrome
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-extensions")
    chrome_service = Service('chromedriver-win64\\chromedriver.exe')  # Update with your path to chromedriver
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

