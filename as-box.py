import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path

options = Options()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1024,768')

def download( sex = '男性', age = '30', ppp = '60歳満了'):
    output = Path(f'results/{sex}-{age}-{ppp}.csv')
    if (output.exists()):
        print(f'result already exists for {output}')
        return

    driver = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver", options=options);
    driver.implicitly_wait(15)
    url="https://asbox.irrc.co.jp/"
    driver.get(url)
    # login
    time.sleep(3)
    driver.find_element_by_id('UserID').send_keys('demo00601')
    driver.find_element_by_id('Password').send_keys('1234568b')
    driver.find_element_by_id('LoginButton').click()

    time.sleep(3)
    # 既にログインしている場合は確認のポップアップが出るので'はい'を押す
    try:
        driver.find_element_by_id('PopupUtils_PopupButton1').click()
    except:
        pass

    # click start
    time.sleep(5)
    driver.find_element_by_id('OpeningScreen_StartButton').click()

    time.sleep(5)
    driver.find_element_by_id('StartMenu_FirstVisitorKojinButton').click()

    time.sleep(5)

    driver.find_element_by_id('FamilyBasicInfoEdit_gender_0').click()
    time.sleep(2)
    driver.find_element_by_link_text("男性").click()

    driver.find_element_by_id('FamilyBasicInfoEdit_age_0').send_keys(age)
    driver.find_element_by_id('FamilyBasicInfoEdit_SearchProduct').click()

    time.sleep(8)
    driver.find_element_by_link_text("収入保障保険").click();

    time.sleep(2)
    driver.find_element_by_link_text(ppp).click()
    # 払込期間を選択する。保険期間を選んだ後でないと出てこない。
    time.sleep(2)
    driver.find_elements_by_link_text(ppp)[1].click()
        
    face_amount = driver.find_element_by_xpath("//input[@type='number' and @min=3]")
    face_amount.send_keys('10')

    driver.find_element_by_link_text('2年').click()
    driver.find_element_by_link_text('標準体').click()
    driver.find_element_by_link_text('非喫煙者標準体').click()
    driver.find_element_by_link_text('非喫煙者優良体').click()
    driver.find_element_by_id('InsuranceItemChoice_SearchButton').click()

    time.sleep(10)  # TODO:ちゃんと待ったほうがよい。

    # resultsの結果の取得と保存
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = str(soup.findAll('table', {'class':'tableFull dataTable no-footer'}))
    table = table.replace('<br/>', '---')  # pd.read_htmlで改行がうまくとれないので'---'に変換しておく。
    # table = table.replace('<br/>', '<br>')
    table = table.replace('<span class="icon-menjyo"></span>', 'P免')
    df = pd.read_html(table)
    output.parent.mkdir(parents=True, exist_ok=True)

    df[1]['特　徴'] = df[1]['特　徴'].str.replace('---', '\n') 
    df[1]['保険期間---払込期間'] = df[1]['保険期間---払込期間'].str.replace('---', '\n') 
    df[1].to_csv(output, encoding='utf-8-sig')
    print(f'result created for {output}')

if __name__ == "__main__":
    download('男性', '30', '60歳満了')
    download('男性', '30', '65歳満了')
    download('女性', '30', '60歳満了')
    download('女性', '30', '65歳満了')
    download('男性', '31', '60歳満了')
    download('男性', '31', '65歳満了')
    download('女性', '31', '60歳満了')
    download('女性', '31', '65歳満了')
    download('男性', '32', '60歳満了')
    download('男性', '32', '65歳満了')
    download('女性', '32', '60歳満了')
    download('女性', '32', '65歳満了')