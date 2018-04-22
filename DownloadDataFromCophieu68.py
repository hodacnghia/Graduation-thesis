import sys, time, os
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

'''
for id in listStockID:
    download_history_price(id)
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
