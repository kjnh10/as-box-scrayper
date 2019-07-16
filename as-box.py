import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

    url="https://asbox.irrc.co.jp/"
    driver.get(url)

    wait = WebDriverWait(driver, 15)

    # login
    wait.until(EC.element_to_be_clickable((By.ID, 'UserID')))
    driver.find_element_by_id('UserID').send_keys('demo00601')
    driver.find_element_by_id('Password').send_keys('1234568b')
    driver.find_element_by_id('LoginButton').click()

    # 既にログインしている場合は確認のポップアップが出るので'はい'を押す
    try:
        elemnt = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.ID, 'PopupUtils_PopupButton1')))
        driver.find_element_by_id('PopupUtils_PopupButton1').click()
        element.click()
    except:
        pass

    # click start
    element = wait.until(EC.element_to_be_clickable((By.ID, 'OpeningScreen_StartButton')))
    element.click()

    element = wait.until(EC.element_to_be_clickable((By.ID, 'StartMenu_FirstVisitorKojinButton')))
    element.click()


    wait.until(EC.element_to_be_clickable((By.ID, 'FamilyBasicInfoEdit_gender_0'))).click()
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT , '男性'))).click()

    wait.until(EC.element_to_be_clickable((By.ID , 'FamilyBasicInfoEdit_age_0'))).send_keys(age)
    # driver.find_element_by_id('FamilyBasicInfoEdit_age_0').send_keys(age)
    wait.until(EC.element_to_be_clickable((By.ID , 'FamilyBasicInfoEdit_SearchProduct'))).click()

    wait.until(EC.element_to_be_clickable((By.LINK_TEXT , '収入保障保険'))).click()

    wait.until(EC.element_to_be_clickable((By.LINK_TEXT , ppp))).click()

    # 払込期間を選択する。保険期間を選んだ後でないと出てこない。
    time.sleep(1)
    driver.find_elements_by_link_text(ppp)[1].click()
        
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='number' and @min=3]"))).send_keys('10')
    driver.find_element_by_link_text('2年').click()
    driver.find_element_by_link_text('標準体').click()
    driver.find_element_by_link_text('非喫煙者標準体').click()
    driver.find_element_by_link_text('非喫煙者優良体').click()
    driver.find_element_by_id('InsuranceItemChoice_SearchButton').click()

    # resultsの結果の取得と保存
    wait.until(EC.element_to_be_clickable((By.ID, "InsuranceItemList_AllCheckedButton")))  # tableのloadが終わると'全選択'bottunが見えるようになるのでそれまで待つ。

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