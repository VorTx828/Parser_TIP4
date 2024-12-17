from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import sqlite3
import tkinter as tk
import threading as td

def ParseAllDataGipermarketdom():
    
    url = "https://gipermarketdom.ru/"
    SelConnect(url)

    soup = BeautifulSoup(driver.page_source, "lxml")

    urlget = []

    init=soup.find("ul", class_="menu-items-2")

    categories = init.find_all("li", recursive=False)  # Use BeautifulSoup to find categories

    for el in categories:
        list1=el.find("ul")
        options = list1.find_all("li", recursive=False)
        for i in options:
            list2=i.find("ul")
            if list2:
                var = list2.find_all("li", recursive=False)
                for e in var:
                    urlget.append(url + e.find("a").get("href")[1:])
            else:
                urlget.append(url + i.find("a").get("href"))

    for site in urlget:
        SelConnect(site)

        soup = BeautifulSoup(driver.page_source, "lxml")
        


        navbar = soup.find("div", class_="tb_block")

        if navbar:
            pages=navbar.find_all("a", recursive=False)[1:-1]
            
            for page in pages:
                num=page.contents
                postfix=f"?page={num}&ff&sort_price=&in_stock=0&price_from=&price_to="

                CollectData(site+postfix)
        else:
            CollectData(site)

    ToDatabase(result)

    driver.quit()

def ParseFromShops():
    shops_url=[]
    goods_url=[]
    cursor.execute("SELECT * FROM Shops")
    shops=cursor.fetchall()

    

    for el in shops:
        shops_url.append(el[2]) #в urls помещаем ссылки на сайты из базы данных



    cursor.execute("SELECT * FROM Good")
    goods=cursor.fetchall()


    for el in goods:
        goods_url.append(el[2])


    # for el in data:



    for site in shops_url:
        if site == "https://gipermarketdom.ru/":


            CollectDataFromGipermarketdom() #НА вход метода передается юрл категории с требуемым товаром

            pass
        elif site == "https://www.vodoparad.ru/":
            CollectDataFromVodoparad()

            pass
        else:
            pass


    # print(data)


def CollectDataFromVodoparad():
    pass


def CollectDataFromGipermarketdom(url):
    # url="https://gipermarketdom.ru/"
    SelConnect(url)
    soup = BeautifulSoup(driver.page_source, "lxml")
    data = soup.find_all("div", class_="card-previwe")

    if data:
        for el in data:
            price = el.find("a", class_="gtm_link_to_card").get("data-price")
            title = el.find("a", class_="gtm_link_to_card").get("data-name")
            url = el.find("a", class_="gtm_link_to_card").get("href")

            if price and title and url:
                info = {"Цена товара": price, "Название товара": title, "Директория сайта": url}
                result[url].append(info)
       
def CreateDB(name="Goods.db"):
    global conn
    global cursor

    conn = sqlite3.connect(name)
    cursor = conn.cursor()




    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Shops (
    ShopID SERIAL PRIMARY KEY,
    Name TEXT NOT NULL,
    Url TEXT NOT NULL
    )
    ''')

    cursor.execute('''
INSERT INTO Shops (Name, Url) VALUES (?, ?) ON CONFLICT(ShopID) DO NOTHING;
''', ("gipermarketdom", "https://gipermarketdom.ru/"))



    cursor.execute('''
INSERT INTO Shops (Name, Url) VALUES (?, ?) ON CONFLICT(ShopID) DO NOTHING;
''', ("vodoparad", "https://www.vodoparad.ru/"))
    


    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Good (
    GoodID SERIAL PRIMARY KEY,
    Name TEXT NOT NULL,
    Url TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Prices (
    id SERIAL PRIMARY KEY,
    GoodID INT NOT NULL,
    ShopID INT NOT NULL,
    Price INT NOT NULL
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

def ToDatabase(data, name = 'GoodsFromSite.db'):
    conn = sqlite3.connect(name)
    cursor = conn.cursor()

    cursor.execute('''
CREATE TABLE IF NOT EXISTS Goods (
    id SERIAL PRIMARY KEY,
    Title TEXT NOT NULL,
    Price INTEGER,
    Url TEXT NOT NULL
)
''')

    conn.commit()


    for element in data:
        cursor.execute('''
INSERT INTO Goods (Title, Price, Url) VALUES (%s, %s, %s)
''', (element["Название товара"], element["Цена товара"],  element["Директория сайта"]))

        conn.commit()

def Interface():
    def on_button_click():
        label.config(text="Парсер запущен!")
        thread1=td.Thread(target=ParseAllDataGipermarketdom)
        thread1.start()


    def get_input():
        # Получаем данные из поля ввода


        if entry1.get() and entry2.get():
            cursor.execute('''
    INSERT INTO Good (Name, Url) VALUES (?, ?)
    ''', (entry1.get(), entry2.get()))


            entry1.delete(0, tk.END)
            entry2.delete(0, tk.END)

            conn.commit()


        # messagebox.showinfo("Ввод", f"Вы ввели: {user_input}")  # Показываем введенные данные в 



    def result():


        ParseFromShops()


        window = tk.Tk()

        window.title("Результаты парсинга")


        result=""

        label = tk.Label(window, text=result)
        label.pack()



        


        



    root = tk.Tk()
    root.title("Парсер сайта")

    label = tk.Label(root, text="Выберите опцию")
    label.pack()

    button = tk.Button(root, text="Собрать все товары с сайта и выгрузить в базу данных (занимает много времени)", command=on_button_click)
    button.pack()

    labe2 = tk.Label(root, text="Введите данные (1 строка - название товара, 2 строка - ссылка на товар)")
    labe2.pack()


    entry1 = tk.Entry(root)
    entry1.pack(pady=10)

    entry2 = tk.Entry(root)
    entry2.pack(pady=10)


    
    button = tk.Button(root, text="Добавить название товара и ссылку", command=get_input)
    button.pack(pady=10)

    button = tk.Button(root, text="Перейти к результатам", command=result)
    button.pack(pady=10)



    root.mainloop()





# url = "https://gipermarketdom.ru/"
# url2="https://www.vodoparad.ru/"
result = {"https://gipermarketdom.ru/":[], "https://www.vodoparad.ru/":[]}

# Set up Selenium with Chrome
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-extensions")
chrome_service = Service('C:\\Program Files\\ChromeDriver\\chromedriver-win64\\chromedriver.exe')  # Update with your path to chromedriver
chrome_options.binary_location = "C:\\Program Files\\ChromeDriver\\chrome-win64\\chrome.exe"
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)




CreateDB()

Interface()

