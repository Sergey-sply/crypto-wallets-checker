from PySide6.QtCore import QThread
from Utils.headers import *

from bs4 import BeautifulSoup as bs
import time
import requests


class Thread_pars(QThread):

    def __init__(self, mainwindow, parent = None):
        super(Thread_pars, self).__init__(parent)
        self.mainwindow = mainwindow


    def run(self):
        self.start_check()

    def start_check(self):
        if self.mainwindow.label_file_name != "None":         #TODO Fix the Workaround
            path_to_file = self.mainwindow.label_file_name.text()
            file_address = open(path_to_file, "r")
            all_address = file_address.readlines()
            for address in all_address:
                self.debank(address.strip())
            file_address.close()

    def debank(self, id, retry = 5):
        try:
            s = requests.Session()
            url = f"https://api.debank.com/user/addr?addr={id}"
            req = s.get(url, headers=headers_debank)
        except Exception as ex:
            if req.status_code == 429:
                if retry:
                    time.sleep(10)
                    return self.debank(id, retry = (retry-1))
                else:
                    #TODO 429
                    result = f"{req.status_code} | DeBank | Too many requests | ------- | {id}"
                    self.mainwindow.list_widget.addItem(result)
                    self.save_results(result)
                    s.close()
                    self.aptos(id)
            else:
                s.close()
                self.aptos(id)
        else:
            if req.status_code == 200:
                src = req.text
                error_code = src.split('"error_code":', 1)[1][0]
                if error_code == "0":
                    balance = src.split('"usd_value":', 1)[1].split(',"user"',1)[0]
                    result = f"{req.status_code} | DeBank | Success | {balance} | {id}"
                    self.mainwindow.list_widget.addItem(result)
                    self.save_results(result)
                    s.close()
                else:
                    s.close()
                    self.aptos(id)
            else:
                if retry:
                    return self.debank(id, retry=(retry - 1))
                else:
                    self.aptos(id)


    def aptos(self, id, retry=5):
        try:
            s = requests.Session()
            url = f"https://aptoscan.com/address/{id}"
            req = s.get(url=url, headers=headers_aptos)
        except Exception as ex:
            if retry:
                time.sleep(15)
                return self.aptos(id, retry = (retry-1))
            else:
                if req.status_code == 429:
                    result = f"{req.status_code} | AptoScan | Too many requests | -------- | {id}"
                    self.mainwindow.list_widget.addItem(result)
                    self.save_results(result)
                    s.close()
                    self.bscscan(id)
                else:
                    result = f"{req.status_code} | AptoScan | ERROR | -------- | {id}"
                    self.mainwindow.list_widget.addItem(result)
                    self.save_results(result)
                    s.close()
                    self.bscscan(id)


        else:
            check_acc_url = f"https://api.aptoscan.com/api?module=account&action=balance&address={id}"
            check_acc_req = requests.get(url=check_acc_url)
            check_acc_src = check_acc_req.text
            status = check_acc_src.split('"status":"')[1].split('","')[0]
            if status == "1":
                src = req.text
                balance = src.split('alt="Aptos">\n')[2].split('<span')[0]
                result = f"{req.status_code} | AptoScan | Success | {balance} APT | {id}"
                self.mainwindow.list_widget.addItem(result)
                self.save_results(result)
            else:
                self.bscscan(id)


    def bscscan(self, id, retry=5):
        try:
            s = requests.Session()
            url = f"https://bscscan.com/address/{id}"
            req = s.get(url=url, headers=headers_bscscan)
        except Exception as ex:
            if retry:
                time.sleep(15)
                return self.bscscan(id, retry=(retry-1))

            else:
                if req.status_code == 429:
                    result = f"{req.status_code} | BscScan | Too many requests | -------- | {id}"
                    self.mainwindow.list_widget.addItem(result)
                    self.save_results(result)
                    s.close()
                    self.solscan(id)
                else:
                    result = f"{req.status_code} | BscScan | ERROR | -------- | {id}"
                    self.mainwindow.list_widget.addItem(result)
                    self.save_results(result)
                    s.close()
                    self.solscan(id)

        else:
            src = bs(req.content, features='lxml')
            if "Binance Account (Invalid Address)" in src:
                s.close()
                self.solscan(id)
            else:
                src = bs(req.content, features='lxml')
                balance = str(src.select('.col-md-8')[1]).split('<div class="col-md-8">')[1].split('<')[0]
                if balance != '$0.00':
                    result = f"{req.status_code} | BscScan | Success | {balance} | {id}"
                    self.mainwindow.list_widget.addItem(result)
                    self.save_results(result)
                else:
                    s.close()
                    self.solscan(id)




    def solscan(self, id, retry=5):
        try:
            s = requests.Session()
            url = f"https://api.solscan.io/account?address={id}"

            req = s.get(url=url, headers=headers_solscan)

        except Exception as ex:
            if retry:
                time.sleep(15)
                return self.solscan(id, retry = (retry-1))
            else:
                if req.status_code == 429:
                    result = f"{req.status_code} | SolScan | Too many requests | -------- | {id}"
                    self.mainwindow.list_widget.addItem(result)
                    self.save_results(result)
                    s.close()
                else:
                    result = f"{req.status_code} | SolScan | ERROR | -------- | {id}"
                    self.mainwindow.list_widget.addItem(result)
                    self.save_results(result)
                    s.close()
        else:
            src = req.text
            try:
                balance = src.split('"lamports":')[1].split(",")[0]
                result = f"{req.status_code} | SolScan | Success | {balance} SOL | {id}"
                self.mainwindow.list_widget.addItem(result)
                self.save_results(result)

            except:
                result = f"{req.status_code} | SolScan | Wallet not found | ????????? | {id}"
                self.mainwindow.list_widget.addItem(result)
                self.save_results(result)
                s.close()


    def save_results(self, result):                         # Creates file with checked addresses
        with open('results/results.txt', 'a') as f:         # You can add the date-time for the file name if you need
            f.write(result + '\n')





        
