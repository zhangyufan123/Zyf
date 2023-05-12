import requests
import json


def sin():
    url = "http://192.168.43.227:8080/Payment_nnr/signin/"

    payload = {"username": "testman", "password": "111111"}
    res = requests.post(url, json=payload)
    data = res.json()
    print(data)


def cin():
    url = "http://192.168.43.227:8080/Payment_nnr/Payment_information/"

    payload = {"order_id": "-1", "seat_price": 100, "air_name": "test_airline", "payer_id": "tair"}
    res = requests.post(url, json=payload)
    data = res.json()
    print(data)


def tran():
    url = "http://192.168.43.227:8080/Payment_nnr/transfer/"

    payload = {"uid": 1, "password": "111111", "u2": "testman1", "u3": "testman1", "money": 50}
    res = requests.post(url, json=payload)
    data = res.json()
    print(data)


def depos():
    url = "http://192.168.43.227:8080/Payment_nnr/deposit/"

    payload = {"uid": 1}
    res = requests.post(url, json=payload)
    data = res.json()
    print(data)


def ere():
    url = "http://192.168.43.227:8080/Payment_nnr/Payment_return/"

    payload = {"state": "successful", "order_id": 1}
    res = requests.post(url, json=payload)
    data = res.json()
    print(data)


def sup():
    url = "http://192.168.43.227:8080/Payment_nnr/signup/"

    payload = {"username": "testman", "password": "111111", "name": "tsm"}
    res = requests.post(url, json=payload)
    data = res.json()
    print(data)


def sup1():
    url = "http://192.168.43.227:8080/Payment_nnr/signup/"

    payload = {"username": "testman1", "password": "111111", "name": "tsm1"}
    res = requests.post(url, json=payload)
    data = res.json()
    print(data)


def sta():
    url = "http://192.168.43.227:8080/Payment_nnr/statement/"

    payload = {"uid": 1}
    res = requests.post(url, json=payload)
    data = res.json()
    print(data)


def bla():
    url = "http://192.168.43.227:8080/Payment_nnr/balance/"

    payload = {"uid": 1}
    res = requests.post(url, json=payload)
    data = res.json()
    print(data)


def check():
    url = "http://192.168.43.227:8080/Payment_nnr/Payment_check/"

    payload = {"state": "successful", "order_id": 1}
    res = requests.post(url, json=payload)
    data = res.json()
    print(data)


def por():
    url = "http://192.168.43.227:8080/Payment_nnr/Payment_order/"

    payload = {"uid": 1, "Airline_order": 1}
    res = requests.post(url, json=payload)
    data = res.json()
    print(data)


if __name__ == '__main__':
    sup()
    sup1()
    sin()
    cin()
    por()
    check()
    ere()
    depos()
    tran()
    sta()
    bla()
