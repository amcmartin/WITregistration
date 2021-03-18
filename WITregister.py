from configparser import ConfigParser
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import smtplib
import time

parser = ConfigParser()
parser.read("config.ini")
user = parser.get('auth', 'user')
pas = parser.get('auth', 'pas')
browser = webdriver.Chrome(parser.get('auth', 'drivepath'))

def sign_in (user,pas):
    '''
    :param user: username
    :param pas: password
    :return: nothing
    This signs into Leopard Web using user name and password provided in the config
    '''

    url = 'https://cas.wit.edu/cas/login?service=https%3A%2F%2Fselfservice.wit.edu%3A443%2Fssomanager%2Fc%2FSSB'
    browser.get(url)
    username = browser.find_element_by_id('username')
    password = browser.find_element_by_id('password')
    username.send_keys(user)
    password.send_keys(pas)
    password.send_keys(Keys.ENTER)


def register():
    '''
    Navigates to the registration page on Leopard web
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    only works when the registration period is open
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    '''
    browser.get('https://selfservice.wit.edu/SSBPROD/bwskfreg.P_AddDropCrse')
    # search = browser.find_element_by_xpath('//*[@id="keyword_in_id"]')
    # search.send_keys('registration')
    # search.send_keys(Keys.ENTER)
    # selectTerm = browser.find_element_by_xpath('/html/body/div[3]/table[1]/tbody/tr[1]/td[2]/a')
    # selectTerm.click()
    browser.find_element_by_xpath('/html/body/div[3]/form/input').click()#click submit
    # #clicks add or drop
    # browser.find_element_by_xpath('/html/body/div[5]/span/map/p[2]/a[2]').click()


def submit_class(schedule):
    '''

    :param schedule: choeses a schedule from the config file
    Will enter the crn codes for the classes neccesary enter the code in the config.
    :return:
    '''
    # enters codes
    browser.find_element_by_xpath('//*[@id="crn_id1"]').send_keys(parser.get(schedule, 'class1'))
    browser.find_element_by_xpath('//*[@id="crn_id2"]').send_keys(parser.get(schedule, 'class2'))
    browser.find_element_by_xpath('//*[@id="crn_id3"]').send_keys(parser.get(schedule, 'class3'))
    browser.find_element_by_xpath('//*[@id="crn_id4"]').send_keys(parser.get(schedule, 'class4'))
    browser.find_element_by_xpath('//*[@id="crn_id5"]').send_keys(parser.get(schedule, 'class5'))
    browser.find_element_by_xpath('//*[@id="crn_id6"]').send_keys(parser.get(schedule, 'class6'))
    browser.find_element_by_xpath('//*[@id="crn_id7"]').send_keys(parser.get(schedule, 'class7'))
    browser.find_element_by_xpath('//*[@id="crn_id8"]').send_keys(parser.get(schedule, 'class8'))
    browser.find_element_by_xpath('//*[@id="crn_id9"]').send_keys(parser.get(schedule, 'class9'))
    browser.find_element_by_xpath('//*[@id="crn_id10"]').send_keys(parser.get(schedule, 'class10'))

    #clicks submit
    browser.find_element_by_xpath('/html/body/div[3]/form/input[19]').click()  # clicks submit


def backup_check():
    '''
    Checks if all classes were successfully registered

    if not runs your back up schedule from the config
    :return:
    '''
    try:
        error1 = browser.find_element_by_xpath('/html/body/div[3]/form/table[4]/tbody/tr[2]/td[1]').text
        #error2 = browser.find_element_by_xpath('/html/body/div[3]/form/table[4]/tbody/tr[3]/td[1]').text
        #error3 = browser.find_element_by_xpath('/html/body/div[3]/form/table[4]/tbody/tr[4]/td[1]').text
        #error4 = browser.find_element_by_xpath('/html/body/div[3]/form/table[4]/tbody/tr[5]/td[1]').text
        #error5 = browser.find_element_by_xpath('/html/body/div[3]/form/table[4]/tbody/tr[6]/td[1]').text
        #error6 = browser.find_element_by_xpath('/html/body/div[3]/form/table[4]/tbody/tr[7]/td[1]').text
        if 'ERROR' in error1: #or 'ERROR' in error2:
            print('True')
            submit_class('backup')

        else:
            browser.quit()
    except:
        browser.quit()





start = time.time()
sign_in(user,pas)
register()
try:
    submit_class('main')
except NoSuchElementException:
    print('not open')
backup_check()
print(f'time %fs'%(time.time()-start))

#3.933089
