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

def DomSearch(name):
    SelConnect("https://gipermarketdom.ru/")

    search_box = driver.find_element(By.ID, 'title-search-input')

    search_box.send_keys(name)

    search_box.send_keys(Keys.RETURN)

    time.sleep(5)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    results = driver.find_elements(By.CLASS_NAME, 'digi-product__main')

    return results

def VodSearch(name):
    SelConnect("https://www.vodoparad.ru/")

    # search_box = driver.find_element(By.ID, 'art-search-input')
    # print(driver.page_source)
    with open("test.txt", "w") as file:
        file.write(driver.page_source)
    search_box = WebDriverWait(driver, 50).until(
        EC.visibility_of_element_located((By.ID, 'art-search-input'))
    )

    results=[]

    search_box.send_keys(name)

    search_box.send_keys(Keys.RETURN)

    time.sleep(5)

    navbar = driver.find_element(By.CSS_SELECTOR, "ul")

    if navbar:
        lt = navbar.find_elements(By.CSS_SELECTOR, "li") # массив элементова поиска
        max = int(lt[-2].find_element(By.CSS_SELECTOR, "a").get_attribute("innerHTML"))

        # elements = driver.find_elements(By.CLASS_NAME, "product-item__content")

        # for el in elements:
        #     results.append(el)
    
        for i in range(max-1):
            elements = driver.find_elements(By.CLASS_NAME, "product-item__content")

            for el in elements:
                results.append(el)

            els = driver.find_element(By.CSS_SELECTOR, "ul").find_elements(By.CSS_SELECTOR, "li")[-1].find_element(By.CSS_SELECTOR, "a").get_attribute("href") #следующая ссылка
            SelConnect(els)
            

    return results

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

                CollectDataFromGipermarketdom(site+postfix)
        else:
            CollectDataFromGipermarketdom(site)

    ToDatabase(result)

    

    driver.quit()

def ParseFromShops():
    # shops_url=[]
    # goods_url=[]
    # cursor.execute("SELECT * FROM Shops")
    # shops=cursor.fetchall()

    

    # for el in shops:
    #     shops_url.append(el[2]) #в urls помещаем ссылки на сайты из базы данных



    cursor.execute("SELECT * FROM Good")
    goods=cursor.fetchall()


    for g in goods:

        fd = DomSearch(g[1])



        for el in fd:

            soup= BeautifulSoup(el.get_attribute("innerHTML"), "lxml")
            print(soup)

        
            # soup= BeautifulSoup(el.text, "lxml")
            
            # price = soup.find("span", class_="digi-product-price-variant digi-product-price-variant_actual").contents
            # title = soup.find("a", class_="digi-product__label").text
            # url = soup.find("a", class_="digi-product__button").get("href")

            price = el.find_element(By.CLASS_NAME, "digi-product-price-variant").get_attribute("innerHTML")
            title = el.find_element(By.CLASS_NAME, "digi-product__label").get_attribute("innerHTML")
            url = el.find_element(By.CLASS_NAME, "digi-product__button").get_attribute("href")


            if price and title and url:
            
                info = {"Цена товара": price, "Название товара": title, "Директория сайта": url}

                result["https://gipermarketdom.ru/"].append(info)

        fv = VodSearch(g[1])
        
        for el in fv:
            # soup= BeautifulSoup(el.text, "lxml")
            
            # price = soup.find("p", class_="product-item__price-new").find("span").contents[0]
            # title = soup.find("a", class_="product-item__name").text
            # url = soup.find("a", class_="product-item__name").get("href")


            price = el.find_element(By.CLASS_NAME, "product-item__price-new").find_element(By.CSS_SELECTOR, "span").get_attribute("innerHTML")
            title = el.find_element(By.CLASS_NAME, "product-item__name").get_attribute("innerHTML")
            url = el.find_element(By.CLASS_NAME, "product-item__name").get_attribute("href")

            if price and title and url:
            
                info = {"Цена товара": price, "Название товара": title, "Директория сайта": url}

                result["https://gipermarketdom.ru/"].append(info)

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
                result["https://gipermarketdom.ru/"].append(info)
       
def CreateDB(name="Goods.db"):
    global conn
    global cursor

    conn = sqlite3.connect(name)
    cursor = conn.cursor()




    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Shops (
    ShopID SERIAL PRIMARY KEY AUTOINCREMENT,
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
    GoodID SERIAL PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Url TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Prices (
    ID SERIAL PRIMARY KEY AUTOINCREMENT,
    GoodCategoryID INT NOT NULL,
    ShopID INT NOT NULL,
    Name TEXT NOT NULL,
    Price INT NOT NULL,
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


        if entry1.get():
            cursor.execute('''
    INSERT INTO Good (Name, Url) VALUES (?, ?)
    ''', (entry1.get(), entry2.get()))


            entry1.delete(0, tk.END)
            entry2.delete(0, tk.END)

            conn.commit()


        # messagebox.showinfo("Ввод", f"Вы ввели: {user_input}")  # Показываем введенные данные в 

    def MakeNewWindow(title="Результаты парсинга"):
        result="Подождите, производится парсинг"

        window = tk.Tk()

        window.title(title)

        label = tk.Label(window, text=result)
        label.pack()

        window.mainloop()

    def result():

        thread = td.Thread(target=MakeNewWindow)

        thread.start()

        ParseFromShops()

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

def ResultToDB():

    # cursor.execute("SELECT * FROM Good")
    # g=cursor.fetchall()

    # r={}

    # for i in g:
    #     r[i[1]]=i[2]
    
    for el in result["https://gipermarketdom.ru/"]:
        cursor.execute('''
    INSERT INTO Prices (GoodCategoryID, ShopID, Name, Price, CardUrl) VALUES (?, ?, ?, ?, ?) ON CONFLICT(GoodCategoryIDD) DO NOTHING;
    ''', (1, 1, el["Название товара"], el["Цена товара"], el["Директория сайта"]))
        conn.commit()

    for el in result["https://www.vodoparad.ru/"]:
        cursor.execute('''
    INSERT INTO Prices (GoodCategoryID, ShopID, Name, Price, CardUrl) VALUES (?, ?, ?, ?, ?) ON CONFLICT(GoodCategoryID) DO NOTHING;
    ''', (1, 2, el["Название товара"], el["Цена товара"], el["Директория сайта"]))
        conn.commit()



# url = "https://gipermarketdom.ru/"
# url2="https://www.vodoparad.ru/"
result = {"https://gipermarketdom.ru/":[], "https://www.vodoparad.ru/":[]}

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

