
import csv 
import mojimoji
from selenium import webdriver
from bs4 import BeautifulSoup

# ブラウザを初期化
def browser_init():
	browser = webdriver.Chrome(executable_path='./chromedriver')
	return browser

# 詳細条件を開く
def click_open_btn(browser):
	browser.find_elements_by_xpath("//input[@id='ID_allOpen1']")[0].click()

# 検索ボタンを押す
def click_search_btn(browser):
	browser.find_elements_by_xpath("//input[@id='ID_commonSearch']")[0].click()

# 事業者名テキストフォームに事業者名を入力
def input_text(browser, office_name):
	search_form = browser.find_element_by_id('ID_jigyoshomei')
	# 初期化
	search_form.clear()
	search_form.send_keys(office_name)

# 千葉県の検索ページに遷移する
def access_chiba_page(browser):
	url = 'https://www.hellowork.go.jp/servicef/130020.do?action=initDisp&screenId=130020'
	browser.get(url)
	browser.find_elements_by_xpath("//input[@value='千葉県']")[0].click()


if __name__ == '__main__':

	browser = browser_init()			
	access_chiba_page(browser)
	click_open_btn(browser)

	with open('chiba_sheet.csv', 'r') as ori_f, open('chiba_hello_work.csv', 'w', encoding='utf-8') as new_f:
		reader = csv.reader(ori_f)
		writer = csv.writer(new_f, lineterminator='\n')

		header = ['source', 'company', 'tel', 'url']
		writer.writerow(header)
		for row in reader:

			src = row[0]
			office_name = mojimoji.han_to_zen(row[1])
			tel = row[3]

			if src == 'ハロワ':
				input_text(browser, office_name)
				click_search_btn(browser)

				is_exist_table = browser.find_elements_by_xpath("//div[@class='d-sole']")
				
				# 検索結果
				if is_exist_table:
					url =  browser.page_source.encode('utf-8')
					html = BeautifulSoup(url, 'lxml')

					rows = html.find(class_='d-sole').find_all('tr')
					offer_num = len(rows) - 1

					# URL
					basic_url = 'https://www.hellowork.go.jp/servicef/'
					page_url = rows[1].a.get('href')[2:]
					detail_page_url = basic_url + page_url
					print(office_name, offer_num, tel, detail_page_url)
					print('-' * 10)

					writer.writerow(['ハロワ', office_name, tel, detail_page_url])




			