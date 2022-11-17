#!/usr/bin/python3

import csv
import json
import time
from pprint import pprint

import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN', None)


def check_if_present(store_name, title, asin):
    headers = {"Content-Type": "application/json",
               "X-Shopify-Access-Token": API_TOKEN}

    api_url = "https://{}.myshopify.com/admin/api/2022-04/products.json".format(
        store_name
    )

    params = {"title": title}

    resp = requests.get(api_url, headers=headers, params=params, timeout=10)

    json_dict = resp.json()

    if json_dict.get("products") is None or len(json_dict.get("products")) == 0:
        return False

    for prod_dict in json_dict.get("products"):
        variant = prod_dict.get("variants")[0]
        if variant.get("sku") == asin:
            return True

    return False


def import_product(store_name, product):
    headers = {"Content-Type": "application/json",
               "X-Shopify-Access-Token": API_TOKEN}

    api_url = "https://{}.myshopify.com/admin/api/2022-04/products.json".format(
        store_name
    )

    payload = {
        "product": {
            "title": product.get("title"),
            "body_html": product.get("product_details"),
            "vendor": product.get("brand", "")
            .replace("Visit the ", "")
            .replace(" Store", ""),
            "tags": product.get("breadcrumbs", "").split("/"),
            "published": True,
            "options": [
                {"name": "Size"},
            ],
            "product_type": "Shoes",
            "images": [],
            "variants": [
                {
                    "sku": product.get("asin"),
                    "price": product.get("price").split(" - ")[-1].replace("£", ""),
                    "requires_shipping": True,
                }
            ],
        }
    }

    i = 1

    for img_url in json.loads(product.get("images_list")):
        payload["product"]["images"].append(
            {
                "src": img_url,
                "position": i,
            }
        )

        i += 1

    pprint(payload)

    resp = requests.post(api_url, headers=headers, json=payload, timeout=10)

    if resp.status_code != 201:
        print("Error: Import to shopify failed!")
        print(resp.text)


def main():
    global API_TOKEN

    # store_name = input(
    #     "Enter store name (part of subdomain before .myshopify.com): ")
    store_name = os.getenv('store_name', None)

    # t_f = open("api_token.txt", "r")
    # API_TOKEN = t_f.read()
    # t_f.close()
    file_name = input(
        "Enter 1 for IPAD LCD, Enter 2 for IPAD HOUSING, Enter 3 for IPHONE LCD, Enter 4 for IPHONE HOUSING, Enter 5 for SAMSUNG LCD, Enter 6 for SAMSUNG BATTERIES")

    if file_name == 1:
        in_f = open("IPAD LCD.csv", "r")
        csv_reader = csv.DictReader(in_f)
        model = None
        qty = None

        for row in csv_reader:
            model = row.get("MODEL")
            qty = row.get('QTY')

    elif file_name == 2:
        in_f = open("IPAD HOUSING.csv", "r")
        csv_reader = csv.DictReader(in_f)
        model = None
        qty = None
        color = None
        for row in csv_reader:
            model = row.get("MODEL")
            qty = row.get('QTY')
            color = row.get('COLOR')

    elif file_name == 3:
        in_f = open("IPHONE LCD.csv", "r")
        csv_reader = csv.DictReader(in_f)
        model = None
        qty = None

        for row in csv_reader:
            model = row.get("MODEL")
            qty = row.get('QTY')

    elif file_name == 4:
        in_f = open("IPHONE HOUSING.csv", "r")
        csv_reader = csv.DictReader(in_f)
        model = None
        qty = None
        color = None

        for row in csv_reader:
            model = row.get("MODEL")
            qty = row.get('QTY')
            color = row.get('COLOR')

    elif file_name == 5:
        in_f = open("SAMSUNG LCD.csv", "r")
        csv_reader = csv.DictReader(in_f)
        model = None
        qty = None

        for row in csv_reader:
            model = row.get("MODEL")
            qty = row.get('QTY')

    elif file_name == 6:
        in_f = open("SAMSUNG BATTERIES.csv", "r")
        csv_reader = csv.DictReader(in_f)
        model = None
        qty = None

        for row in csv_reader:
            model = row.get("MODEL")
            qty = row.get('QTY')

    in_f.close()

    # for row in csv_reader:
    #     if row.get("price") == "":
    #         continue

    #     if not check_if_present(store_name, row.get("title"), row.get("asin")):
    #         import_product(store_name, row)
    #     else:
    #         print(
    #             "{} ({}) already present - skipping...".format(
    #                 row.get("title"), row.get("asin")
    #             )
    #         )

    #     time.sleep(0.5)


if __name__ == "__main__":
    main()
