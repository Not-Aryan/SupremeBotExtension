import requests
import bs4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import flask
from flask import *
import json

app = Flask("QuickCop Bot")

@app.route('/', methods=['GET', 'POST'])
def start():
    # INFO = {
    #     "product": "Supreme®/Schott® Fringe Suede Coat",
    #     "color": "Red",
    #     "size": "Large",
    #     "category": "jackets",
    #     "name": "first last",
    #     "email": "example@example.com",
    #     "phone": "1111111111",
    #     "address": "example road",
    #     "city": "example",
    #     "state" : "CA",
    #     "zip": "94588",
    #     "credit_card_number": "1234123412341234",
    #     "cc_month": "09",
    #     "cc_year": "2020",
    #     "cvv": "123"
    # }
    print("HI")
    return '',200

@app.route('/sum', methods=['GET', 'POST', "OPTIONS"])
def summ():
    # if request.method == "POST":
    rf = request.form
    print(rf)
    for x in rf.keys():
        print(x)
        data_dic = json.loads(x)
        print(data_dic.keys())

    INFO = data_dic
    bot = SupremeBot(**INFO)
    bot.run()
    resp = Response("Data received")
    resp.headers['Access-Control-Allow-Origin']='*'
    return resp


class SupremeBot:
    def __init__(self, **info):
        self.base = "https://www.supremenewyork.com/"
        self.shop = "shop/all/"
        self.checkout = "checkout/"
        self.info = info 

    def init_browser(self):
        self.wd = webdriver.Firefox()

    def find_product(self):
        r = requests.get("{}{}{}".format(self.base,self.shop,self.info['category'])).text
        soup = bs4.BeautifulSoup(r, 'lxml')
        temp_tuple = []
        temp_link = []

        # print(soup)

        # print("{}{}{}".format(self.base,self.shop,self.info['category']))

        for link in soup.findAll('a', href=True):
            temp_tuple.append((link["href"], link.text))

        # print(temp_link)

        for i in temp_tuple:
            if i[1] == self.info['product'] or i[1] == self.info['color']:
                temp_link.append(i[0])

        self.final_link = list(set([x for x in temp_link if temp_link.count(x) == 2]))[0]
        
        print(self.final_link)

    def visit_site(self):
        self.wd.get("{}{}".format(self.base, str(self.final_link)))
        size = self.wd.find_element_by_id('s')
        for option in size.find_elements_by_tag_name('option'):
            if option.text == self.info['size']:
                option.click()
                break
        self.wd.find_element_by_xpath("//input[@value='add to cart']").click()
        # self.wd.find_element_by_id('s').click()
        
    def checkoutFunc(self):
        self.wd.get("{}{}".format(self.base, self.checkout))
        self.wd.find_element_by_id('order_billing_name').send_keys(self.info['name'])
        self.wd.find_element_by_id('order_email').send_keys(self.info['email'])
        self.wd.find_element_by_id('order_tel').send_keys(self.info['phone'])
        self.wd.find_element_by_name('order[billing_address]').send_keys(self.info['address'])
        self.wd.find_element_by_id('order_billing_zip').send_keys(self.info['zip'])
        # self.wd.find_element_by_id('order_billing_city').send_keys(self.info['city'])
        self.wd.find_element_by_id('rnsnckrn').send_keys(self.info['credit_card_number'])
        self.wd.find_element_by_id('orcer').send_keys(self.info['cvv'])
        # self.wd.find_element_by_id('order_terms').click()

        #All text areas should be filled, moving onto select tags
        state = self.wd.find_element_by_id('state_label')
        for option in state.find_elements_by_tag_name('option'):
            if option.text == self.info['state']:
                option.click()
                break
        # country = self.wd.find_element_by_id('order_billing_country')
        # for option in country.find_elements_by_tag_name('option'):
        #     if option.text == self.info['country']:
        #         option.click()
        #         break
        month = self.wd.find_element_by_id('credit_card_month')
        for option in month.find_elements_by_tag_name('option'):
            if option.text == self.info['cc_month']:
                option.click()
                break
        year = self.wd.find_element_by_id('credit_card_year')
        for option in year.find_elements_by_tag_name('option'):
            if option.text == self.info['cc_year']:
                option.click()
                break

    def run(self):
        self.find_product()
        self.init_browser()
        self.visit_site()
        self.checkoutFunc()

app.run(debug=False)