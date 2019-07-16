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
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1024,768')

def download(sex = '男性', age = '30', ppp = '60歳満了'):
    s = time.time()
    output = Path(f'results/{sex}-{age}-{ppp}.csv')
    if (output.exists()):
        print(f'result already exists for {output}')
        return

    try:
        driver = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver", options=options);

        url="https://asbox.irrc.co.jp/"
        driver.get(url)

        wait = WebDriverWait(driver, 30)

        # login
        wait.until(EC.element_to_be_clickable((By.ID, 'UserID')))
        driver.find_element_by_id('UserID').send_keys('demo00601')
        driver.find_element_by_id('Password').send_keys('1234568b')
        driver.find_element_by_id('LoginButton').click()

        # 既にログインしている場合は確認のポップアップが出るので'はい'を押す
        try:
            element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.ID, 'PopupUtils_PopupButton1'))).click()
        except:
            pass

        wait.until(EC.element_to_be_clickable((By.ID, 'OpeningScreen_StartButton'))).click()  # clickできても反応しない時がある。

        wait.until(EC.element_to_be_clickable((By.ID, 'StartMenu_FirstVisitorKojinButton'))).click()

        wait.until(EC.element_to_be_clickable((By.ID, 'FamilyBasicInfoEdit_gender_0'))).click()
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT , '男性'))).click()

        wait.until(EC.element_to_be_clickable((By.ID , 'FamilyBasicInfoEdit_age_0'))).send_keys(age)
        wait.until(EC.element_to_be_clickable((By.ID , 'FamilyBasicInfoEdit_SearchProduct'))).click()

        wait.until(EC.element_to_be_clickable((By.LINK_TEXT , '収入保障保険'))).click()
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT , ppp))).click()

        # 払込期間を選択する。保険期間を選んだ後でないと出てこない。
        time.sleep(1)
        if driver.find_elements_by_link_text(ppp)[1].get_attribute('class') != 'on':  # 50歳満了の場合は最初からonになっている。
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
        table = table.replace('<span class="icon-menjyo"></span>', 'P免')
        df = pd.read_html(table)
        output.parent.mkdir(parents=True, exist_ok=True)

        df[1]['特　徴'] = df[1]['特　徴'].str.replace('---', '\n') 
        df[1]['保険期間---払込期間'] = df[1]['保険期間---払込期間'].str.replace('---', '\n') 
        df[1].drop(columns=['処理---対象'], inplace=True)
        df[1].to_csv(output, encoding='utf-8-sig', index=False)
        e = time.time()
        print(f'result created for {output}', f': {e-s} sec')
    finally:
        driver.close()

if __name__ == "__main__":
    sexs = ['男性', '女性']
    issue_ages = list(map(str, range(30, 51)))
    pay_fin_ages = ['50', '55', '60', '65', '70']
    for sex in sexs:
        for issue_age in issue_ages:
            for pay_fin_age in pay_fin_ages:
                if (int(pay_fin_age) - int(issue_age)<10): continue
                try:
                    download(sex, str(issue_age), f'{pay_fin_age}歳満了')
                except:
                    print('failed', sex, str(issue_age), pay_fin_age)
