#!/usr/bin/python
# -*- coding: utf-8 -*-


class PDA(object):

    # Product Variables
    IDs = []
    types = []
    products = []
    quantities = []
    volumes = []
    cost_benefit_factors = []
    prices = []

    # Class Variables
    store_id = "501"
    option = "0"

    def __init__(self):
        # It doesn't initialize anything LOL
        pass

    def set_store(self):
        # Will set the Class Variable "store_id" to your desired store
        import os
        import time

        stores = {
            501: "Loja Online",
            81: "Rua Clodomiro Amazonas 955 - (Itaim Bibi)",
            141: "Av. Washington Luís 3919 - (Vila Mascote)",
            10: "Rua Teodoro Sampaio 1933 - (Pinheiros)",
            122: "Av. Magalhães de Castro 6118 - (Real Parque)",
            361: "Rua Joaquim Floriano 24 - (Joaquim Floriano)",
            261: "Rua Bairi 435 - (Cerro Cora)",
            461: "Rua Prof. Serafim Orlandi 299 - (Ricardo Jafet)",
            641: "Av. Eng Armando 2022 - (Jabaquara)",
            5: "Av. Professor Francisco Morato 2385 - (Morumbi)",
            941: "Al. Ministro Rocha Azevedo 1136 - (Oscar Freire)",
            841: "Praça Panamericana 217 - (Panamericana)",
            101: "Al. Gabriel Monteiro Da Silva 1351 - (Gabriel Monteiro)",
            1061: "Av. Reg Feijo 1425 - (Analia Franco)",
            1161: "Rua Domingos De Morais 486 - (Ana Rosa)",
        }
        os.system("cls")
        print("These are the stores in SP!\n")
        for key in stores:
            print("ID: {} - Address: {}".format(key, stores[key]))
        print("")
        x = input("Type you requeried store ID: ")
        if int(x) in stores:
            self.store_id = x
        else:
            os.system("cls")
            print("Invalid ID!\nTry it again")
            time.sleep(2)
            self.set_store()

    def set_option(self):
        import time
        import os

        print("What kind of liquor do you want?\n")
        print("1 - Standard Beers")
        print("2 - Special Beers")
        print("3 - Vines")
        print("4 - Vodkas, Cachaças And Sakes")
        print("A - All kinds :)")
        x = input("\nPlease Input your option: ")
        if x in ["1", "2", "3", "4", "A", "a"]:
            self.option = x.upper()
        else:
            os.system("cls")
            print("Invalid Option!\nTry it again")
            time.sleep(2)
            self.set_option()

    def get_infos(self, option):
        import requests
        import json

        urls = {
            "1": r"https://api.gpa.digital/pa/products/list/secoes/C4215/cervejas?storeId=1161&qt=12&s=&ftr=facetSubShelf_ss%3A4215_Cervejas&p=1&rm=&gt=list&isClienteMais=true",
            "2": r"https://api.gpa.digital/pa/products/list/secoes/C4215/cervejas-especiais?storeId=1161&qt=12&s=&ftr=facetSubShelf_ss%3A4215_Cervejas%20Especiais&p=1&rm=&gt=list&isClienteMais=true",
            "3": r"https://api.gpa.digital/pa/products/list/secoes/C4215/?storeId=1161&qt=12&s=&ftr=facetSubShelf_ss:4215_Vinhos%20e%20Espumantes&p=1&rm=&gt=grid&isClienteMais=true",
            "4": r"https://api.gpa.digital/pa/products/list/secoes/C4215/vodka-cachacas-e-saques?storeId=1161&qt=12&s=&ftr=facetSubShelf_ss%3A4215_Vodka%2C%20Cacha%C3%A7as%20e%20Saqu%C3%AAs&p=1&rm=&gt=list&isClienteMais=true",
        }

        x = urls[option].replace("storeId=1161", "storeId=" + self.store_id)
        new_urls = []
        for i in range(1, 501):
            new_urls.append(x.replace("&p=1", "&p=" + str(i)))
        for i in new_urls:
            HTML_page = requests.get(i).text
            number_elements = json.loads(
                HTML_page)["content"]["numberOfElements"]
            if number_elements == 0:
                break
            else:
                for x in range(0, number_elements):
                    self.IDs.append(json.loads(HTML_page)[
                                    "content"]["products"][x]["id"])
                    product_type = json.loads(
                        HTML_page)["content"]["products"][x]["shelfList"][0]["name"]
                    if product_type == "Bebidas":
                        self.types.append(
                            json.loads(HTML_page)["content"]["products"][x]["shelfList"][1]["name"])
                    else:
                        self.types.append(product_type)
                    self.products.append(
                        str(json.loads(HTML_page)["content"]["products"][x]["name"]).strip())
                    quantity = json.loads(HTML_page)[
                        "content"]["products"][x]["totalQuantity"]
                    if quantity == 0:
                        self.quantities.append(1)
                    else:
                        self.quantities.append(quantity)
                    self.prices.append(
                        round(
                            json.loads(HTML_page)["content"]["products"][x]["currentPrice"],
                            2))

    def get_volume(self, Product):
        import re

        volumeRegex = re.compile(
            "(\d+)([ ]*)(ml|litro|litros)+", re.IGNORECASE)
        result = volumeRegex.findall(Product)
        if len(result) > 0:
            volume = result[0][0]
            volume = int(volume)
            if "litro" in (item.lower() for item in result[0]):
                volume *= 1000
        else:
            volume = "Unavailable"
        return volume

    def export_xlsx(self):
        # import Workbook object from Openpyxl
        from openpyxl import Workbook

        wb = Workbook()
        ws = wb.active
        self.spreed_sheet_name = input("Export Excel file name: ")

        ws.append(["IDs", "Types", "Products",
                   "Quantities", "Volumes", "prices"])

        for i in range(0, len(self.IDs)):
            ws.append([self.IDs[i],
                       self.types[i],
                       self.products[i],
                       self.quantities[i],
                       self.get_volume(self.products[i]),
                       self.prices[i]])
        wb.save(self.spreed_sheet_name + ".xlsx")

    def make_cost_benefit(self):
        # makes an array of quantity * volume / price
        for i in range(0, len(self.IDs)):
            try:
                self.cost_benefit_factors.append(
                    self.quantities[i] * self.volumes[i] / self.prices[i])
            except BaseException:
                self.cost_benefit_factors("Unavailable")

    def run(self):
        import os
        import threading

        if self.option == "1":
            os.system("cls")
            print("Getting the information.....")
            print("Please wait for it!")
            self.get_infos(self.option)
        elif self.option == "2":
            os.system("cls")
            print("Getting the information.....")
            print("Please wait for it!")
            self.get_infos(self.option)
        elif self.option == "3":
            os.system("cls")
            print("Getting the information.....")
            print("Please wait for it!")
            self.get_infos(self.option)
        elif self.option == "4":
            os.system("cls")
            print("Getting the information.....")
            print("Please wait for it!")
            self.get_infos(self.option)
        elif self.option == "a" or self.option == "A":
            os.system("cls")
            print("Getting the information.....")
            print("Please wait for it!")
            self.get_infos("1")
            self.get_infos("2")
            self.get_infos("3")
            self.get_infos("4")
            # It actually doesn't work because it append out of order :(

            #t1 = threading.Thread(target=self.get_infos, args=("1"))
            #t2 = threading.Thread(target=self.get_infos, args=("2"))
            #t3 = threading.Thread(target=self.get_infos, args=("3"))
            #t4 = threading.Thread(target=self.get_infos, args=("4"))
            # t1.start()
            # t2.start()
            # t3.start()
            # t4.start()
            # t1.join()
            # t2.join()
            # t3.join()
            # t4.join()
