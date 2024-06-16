import pandas as pd
import numpy as np
from tqdm import tqdm
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import time
from time import sleep
from time import strftime
from time import gmtime
from selenium.common.exceptions import NoSuchElementException

""""""
""""""
""""""
""""""
"""

    ==== DO NOT RUN UNTIL FURTHER NOTICE ====
    As of June 12, 2024 (time website was checked), HOTHtools backlink checker
    REQUIRES a LinkedIn login. With this login, they will be able to enforce their ToS
    on their publicly available tool. This means that AUTOMATION ON THEIR TOOL IS A NO-GO, unless
    we want our LinkedIn accounts flagged for misuse and breach of ToS. Only workaround, as of now,
    is to manually get and input the number of backlinks for each link in our dataset (which sucks).
    
"""
""""""
""""""
""""""
""""""

"""


def execute(df, mode):
    backlinks = {}
    url_list = []
    index = 0

    if mode == 'video':
        cols = ['video_id', 'backlinks']
        for col in cols:
            backlinks[col] = {}

        video_id_list = df['video_id'].tolist()
        for i in range(len(video_id_list)):
            backlinks['video_id'][i] = video_id_list[i]

        cols = [cols[1]]

        for i in range(df.shape[0]):
            url_list.append("https://www.youtube.com/watch?v=" + df.iloc[i]['video_id'])

    elif mode == 'external':
        cols = ['channel_id', 'channel_name', 'LinkedIn', 'Wiki', 'Website', 'Twitter', 'Facebook']
        for col in cols:
            backlinks[col] = {}

        channel_id_list = df['channel_id'].tolist()
        channel_name_list = df['channel_name'].tolist()
        for i in range(len(channel_id_list)):
            backlinks['channel_id'][i] = channel_id_list[i]
            backlinks['channel_name'][i] = channel_name_list[i]

        cols = cols[2:7]

        for col in cols:
            for i in range(df.shape[0]):
                url_list.append(df.iloc[i][col])

    print("Launching Selenium Firefox webdriver...")
    driver = webdriver.Firefox()
    driver.get("https://www.thehoth.com/backlinks-checker/")

    captcha_passed = False

    pbar = tqdm(total=len(url_list))
    pbar.set_description("Getting backlinks...")
    start_time = time()

    for col in cols:
        for i in range(df.shape[0]):
            if url_list[index] is np.nan:
                backlinks[col][i] = 0
                # print(f"--------------------- INDEX {index} COMPLETE ({col}: {i}: No link) ---------------------")
                index += 1
                pbar.update(1)
                sleep(1)
                continue
            else:
                # Wait for page to load and locate textbox
                # print("Waiting for frame")
                cont = True
                while cont:
                    try:
                        WebDriverWait(driver, 300).until(
                            EC.frame_to_be_available_and_switch_to_it((By.ID, "hothtools"))
                        )
                        cont = False
                    except:
                        driver.refresh()
                        sleep(10)

                sleep(1)

                WebDriverWait(driver, 200).until_not(
                    EC.visibility_of_element_located((By.CLASS_NAME, "hoth-loader__container"))
                )

                # Input link
                # print("Inputting link")
                notFound = False
                while not notFound:
                    try:
                        targeturl = driver.find_element(By.ID, "targeturl")
                        notFound = True
                    except:
                        sleep(10)
                        pass

                targeturl.click()
                targeturl.send_keys(Keys.CONTROL + "A")
                targeturl.send_keys(Keys.BACKSPACE)
                targeturl.send_keys(url_list[index])

                # Select 'This Exact URL'
                dropdown = driver.find_element(By.ID, "mode")
                dropdown.click()
                option = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/form/div[2]/select/option[3]")
                option.click()

                # Submit
                submit = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/form/div[2]/button")
                submit.click()

                sleep(5)

                if not captcha_passed:
                    try:
                        # In case of Captcha page
                        # print("Solving CAPTCHA")
                        iframes = driver.find_elements(By.TAG_NAME, "iframe")
                        cont = False
                        for iframe in iframes:
                            try:
                                driver.switch_to.frame(iframe)
                                checkbox = driver.find_element(By.ID, "recaptcha-anchor")
                                checkbox.click()
                                cont = True
                                break
                            except:
                                # print("Not Found")
                                driver.switch_to.default_content()

                        if not cont:
                            raise Exception("No CAPTCHA iframe found.")

                        # Giving enough time to manually solve CAPTCHA puzzle
                        sleep(15)

                        driver.switch_to.default_content()
                        driver.switch_to.frame("hothtools")
                        submit = driver.find_element(
                            By.XPATH, "//*[@id='submit']"
                        )
                        submit.click()
                        captcha_passed = True
                        sleep(3)
                    except:
                        pass

                # Get external backlinks
                # print("Getting results")
                driver.switch_to.default_content()
                driver.switch_to.frame("hothtools")
                try:
                    # print("Waiting for result frame")
                    WebDriverWait(driver, 200).until(
                        EC.element_to_be_clickable((By.ID, "targeturl"))
                    )

                    result = driver.find_element(
                        By.XPATH, "/html/body/div[2]/div/div/div[2]/div[2]/div/div/div[1]/div[2]"
                    ).text
                except NoSuchElementException:
                    result = '0'
                finally:
                    backlinks[col][i] = int(result.replace(',', ''))
                    # print(f"--------------------- INDEX {index} COMPLETE ({col}: {i}: {result}) ---------------------")
                    index += 1
                    pbar.update(1)
                    driver.switch_to.default_content()

    pbar.close()
    elapsed_time = time() - start_time
    print('Execution time:', strftime("%H:%M:%S", gmtime(elapsed_time)))
    print("Closing Selenium Firefox webdriver...")
    driver.close()

    return backlinks


def get_backlinks(video_df, source_links):
    video_backlinks = execute(video_df, mode='video')
    source_backlinks = execute(source_links, mode='external')

    vbl_df = pd.DataFrame.from_dict(video_backlinks)
    print("Saving as video backlinks as video_backlinks.csv...")
    vbl_df.to_csv("video_backlinks.csv")

    sbl_df = pd.DataFrame.from_dict(source_backlinks)
    print("Saving as external source backlinks as source_backlinks.csv...")
    sbl_df.to_csv("source_backlinks.csv")

    print("Backlinks acquired.")


if __name__ == '__main__':
    filename = input("Filename (w/o .csv): ")
    path = os.getcwd() + "/datasets/" + filename
    os.chdir(path)

    video_df = pd.read_csv("videos.csv", index_col=0)
    source_links = pd.read_csv("source_links.csv", index_col=0)

    get_backlinks(video_df, source_links)

    os.chdir("..")
    os.chdir("..")
    print("Back @ " + os.getcwd())
    
    
# """
