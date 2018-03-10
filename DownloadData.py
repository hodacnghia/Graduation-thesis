import sys, time, os
from selenium import webdriver


def login_to_web(username, password):
	usernameElem = driver.find_element_by_name("username")
	passwordElem = driver.find_element_by_name("tpassword")
	usernameElem.send_keys(username)
	passwordElem.send_keys(password)
	passwordElem.submit()	

def get_all_stockIDs(totalPages):
	pageCurrent = 1
	totalPages = 59
	listStockID = []
	
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
			
			listStockID.append(link.text)
			
		pageCurrent += 1
		
		if (pageCurrent > totalPages):
			break
		driver.get("http://www.cophieu68.vn/companylist.php?currentPage=" + str(pageCurrent) + "&o=s&ud=a")
		time.sleep(1)
	
	return listStockID
	
def save_list_stockID_to_file(listStockID):
	theFile = open('listStockID.txt', 'w')
	theFile.write('\n'.join(listStockID))
	theFile.close()
	
def read_list_stockID_from_file(fileName):
	theFile = open(fileName, 'r')
	listStockID = theFile.read().split('\n')
	return listStockID
	
def download_history_price(stockID):
	# comment
	if False:
		stockIDElem = driver.find_element_by_name("id")
		stockIDElem.send_keys(stockID)
		stockIDElem.submit()
		
		# TODO: Click Lich Su Gia
		driver.get('http://www.cophieu68.vn/historyprice.php?id=' + stockID)
		historyPriceElem = driver.find_element_by_link_text('Lịch Sử Giá')
		historyPriceElem.click()
		
		# TODO: Download
		downloadExcelElem = driver.find_element_by_link_text('Export Excel')
		downloadExcelElem.click()
	#comment
	
	driver.get("http://www.cophieu68.vn/export/excel.php?id=" + stockID + "&df=&dt=")

	
	
	
current_director = os.getcwd()
os.makedirs('dulieucophieu', exist_ok=True)
savePath = os.path.join(current_director, "dulieucophieu")

if len(sys.argv) > 2:
	username = sys.argv[1]
	password = sys.argv[2]
	
	# TODO: Open Chrome
	prefs = {'download.default_directory' : savePath}
	options = webdriver.ChromeOptions()
	options.add_experimental_option('prefs', prefs)
	driver = webdriver.Chrome("D:/chromedriver_win32/chromedriver.exe", chrome_options=options)
	
	# TODO: Open firefox and go to all stock in cophieu68.vn
	driver.get('http://www.cophieu68.vn/companylist.php')
	time.sleep(1)
	
	# TODO: Login into cophieu68
	loginElem = driver.find_element_by_link_text('Đăng nhập')
	loginElem.click();
	time.sleep(1)
	
	login_to_web(username, password)
	time.sleep(1)
	
	listStockID = read_list_stockID_from_file('listStockID.txt')
	
	for id in listStockID:
		download_history_price(id)
		
	
	