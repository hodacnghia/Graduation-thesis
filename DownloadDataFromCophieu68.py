import sys, time, os, csv
from selenium import webdriver

def get_driver(save_to_folder):
    save_path = os.path.join(current_director, save_to_folder)
    
    prefs = {'download.default_directory' : save_path}
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome("D:/chromedriver_win32/chromedriver.exe", chrome_options=options)
    
    return driver

def login_to_web(driver, username = 'vttqhuy@gmail.com', password = 'Sinhvien1'):
    driver.get("http://www.cophieu68.vn")
    
    loginElem = driver.find_element_by_link_text('Đăng nhập')
    loginElem.click()
    time.sleep(1)
    
    usernameElem = driver.find_element_by_name("username")
    passwordElem = driver.find_element_by_name("tpassword")
    usernameElem.send_keys(username)
    passwordElem.send_keys(password)
    passwordElem.submit()

def download_stockIDs_from_netfonds(driver, market_name):
    driver.get('http://www.netfonds.no/quotes/exchange.php?exchange=' + market_name)
    time.sleep(1)
    
    list_stockID = []
    
    links = driver.find_elements_by_class_name('left')
    links = links[1:]
    
    for l in links:
        tag_a = l.find_element_by_css_selector('a')
        list_stockID.append(tag_a.text)
    
    save_list_stockID_to_file(list_stockID, "stockID_nyse.txt")

def download_vnindex_stockIDs(driver):
    driver.get('http://www.cophieu68.vn/calculating_market_index.php?id=^vnindex')
    time.sleep(1)
    
    login_to_web(driver)
    time.sleep(1)
    
    list_stockID = []
    pageCurrent = 1
    total_pages = 15
    
    while True:
        # TODO: Go to stock list
        tableElem = driver.find_element_by_id('fred')
        rowElem = tableElem.find_elements_by_css_selector('tr')
        
        # TODO: Delete Header
        rowElem = rowElem[1:]
        
        for r in rowElem:
            columnElems = r.find_elements_by_css_selector('td')
            
            #TODO get link stock in second column
            link = columnElems[1].find_element_by_css_selector('a')
            list_stockID.append(link.text)
            
        pageCurrent += 1
        
        if (pageCurrent > total_pages):
            break
        driver.get("http://www.cophieu68.vn/calculating_market_index.php?currentPage=" + str(pageCurrent) + "&id=^vnindex")
        time.sleep(1)
    
    save_list_stockID_to_file(list_stockID, "stockID_vnindex.txt")

def download_hnxindex_stockIDs(driver):
    driver.get('http://www.cophieu68.vn/calculating_market_index.php?id=^hastc')
    time.sleep(1)
    
    login_to_web(driver)
    time.sleep(1)
    
    list_stockID = []
    pageCurrent = 1
    total_pages = 16
    
    while True:
        # TODO: Go to stock list
        tableElem = driver.find_element_by_id('fred')
        rowElem = tableElem.find_elements_by_css_selector('tr')
        
        # TODO: Delete Header
        rowElem = rowElem[1:]
        
        for r in rowElem:
            columnElems = r.find_elements_by_css_selector('td')
            
            #TODO get link stock in second column
            link = columnElems[1].find_element_by_css_selector('a')
            list_stockID.append(link.text)
            
        pageCurrent += 1
        
        if (pageCurrent > total_pages):
            break
        driver.get("http://www.cophieu68.vn/calculating_market_index.php?currentPage=" + str(pageCurrent) + "&id=^hastc")
        time.sleep(1)
    
    save_list_stockID_to_file(list_stockID, "stockID_hnxindex.txt")

def save_list_stockID_to_file(listStockID, fileName):
    theFile = open(fileName, 'w')
    theFile.write('\n'.join(listStockID))
    theFile.close()
    
def read_list_stockID_from_file(filePath):
    theFile = open(filePath, 'r')
    listStockID = theFile.read().split('\n')
    return listStockID

def download_history_price(stockID):
    driver.get("http://www.cophieu68.vn/export/excel.php?id=" + stockID + "&df=&dt=")
    
def crawl_data_from_netfond(driver, ticker):
    driver.get('https://www.netfonds.no/quotes/paperhistory.php?paper=' + ticker + '.N&csv_format=csv')
    
    data = [['<Ticker>', '<DTYYYYMMDD>', '<Open>', '<High>', '<Low>', '<Close>', '<Volume>']]
    content = driver.find_element_by_css_selector('pre')
    
    rows = content.text.split('\n')
    rows = rows[1:]
    
    for r in rows:
        r_data = r.split(',')
        data.append([r_data[1], r_data[0], r_data[3], r_data[4], r_data[5], r_data[6], r_data[7]])
    
    folder_to_save = os.path.join(os.getcwd(), 'dulieunyse')
    file = open(os.path.join(folder_to_save, ticker + '.csv'), 'w', newline='')
    with file:
        writer = csv.writer(file)
        writer.writerows(data)
    
current_director = os.getcwd()   
os.makedirs('dulieuvnindex', exist_ok=True)
os.makedirs('dulieuhnxindex', exist_ok=True)
#savePath = os.path.join(current_director, "dulieuvnindex")
'''
# TODO: Open Chrome
prefs = {'download.default_directory' : savePath}
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome("D:/chromedriver_win32/chromedriver.exe", chrome_options=options)

list_id = get_all_stockIDs('http://www.cophieu68.vn/calculating_market_index.php?id=^vnindex', 'vttqhuy@gmail.com', 'Sinhvien1', 15)
        
save_list_stockID_to_file(list_id, "stockID_vnindex.txt")

listStockID = read_list_stockID_from_file('stockID_vnindex.txt')
'''


driver = get_driver('dulieuvnindex')
login_to_web(driver)
#download_vnindex_stockIDs(driver)
vnindex_stockIDs = read_list_stockID_from_file('stockID_vnindex.txt')

for id in vnindex_stockIDs:
    download_history_price(id)


driver = get_driver('dulieuhnxindex')
login_to_web(driver)
#download_hnxindex_stockIDs(driver)
hnx_stockIDs = read_list_stockID_from_file('stockID_hnxindex.txt')

for id in hnx_stockIDs:
    download_history_price(id)


'''
os.makedirs('dulieunyse', exist_ok=True)
driver = get_driver('dulieunyse')
#download_stockIDs_from_netfonds(driver, 'N')
nyse_stockIDs = read_list_stockID_from_file('stockID_nyse.txt')

for ticker in nyse_stockIDs:
    crawl_data_from_netfond(driver, ticker)
'''