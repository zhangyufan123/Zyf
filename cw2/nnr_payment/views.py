import jsonify as jsonify
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import user, consumption_record
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import secrets
import requests


# Create your views here.
@csrf_exempt
def signin(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        print(req)
        kg = req.get("username") and req.get("password") and len(req) == 2
        if kg:
            username = req["username"]
            password = req["password"]
        uinfo = user.objects.filter(username=username, password=password)
        if len(uinfo) == 0:
            return JsonResponse({"msg": "You have no account, please sign up."})
        u = user.objects.get(username=username, password=password)
        return JsonResponse({"msg": u.id})


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        kg = req.get("username") and req.get("password") and req.get("name") and len(req) == 3
        if kg:
            username = req["username"]
            password = req["password"]
            name = req["name"]
            uinfo = user.objects.filter(username=username)
            if len(uinfo) != 0:
                return JsonResponse({"msg": "Username already exists."})
            add_u = user(username=username, password=password, balance=1000, name=name)
            add_u.save()
            u = user.objects.get(username=username, password=password)
            return JsonResponse({"msg": u.id})


@csrf_exempt
def deposit(request):
    if request.method == 'POST' or request.method == 'GET':
        req = json.loads(request.body)
        kg = req.get("uid") and len(req) == 1
        if kg:
            uid = req["uid"]
        u = user.objects.get(id=uid)
        return JsonResponse({"msg": u.balance})


@csrf_exempt
def payment_information(request):
    if request.method == 'POST' or request.method == 'GET':
        req = json.loads(request.body)
        kg = req.get("order_id") and req.get("seat_price") and req.get("air_name") and req.get("payer_id") and len(req) == 4
        if kg:
            order_id = req["order_id"]
            seat_price = req["seat_price"]
            airline_name = req["air_name"]
        time = datetime.now()
        sek = secrets.token_hex(8)
        c_info = consumption_record(Time=time, Recipient="expense", Amount=1, Money=seat_price, secret_key=sek,
                                    UserId=0, Airline_order=order_id, State=False)
        c_info.save()
        return JsonResponse({"payment_provider": "nnr", "secret_key": c_info.secret_key})


@csrf_exempt
def statement(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        kg = req.get("uid") and len(req) == 1
        if kg:
            uid = req["uid"]
        query_art = consumption_record.objects.all()
        conl = {}
        num = 0
        for i in query_art:
            if i.UserId == uid:
                conl1 = {"Time": i.Time, "Money": i.Money, "Recipient": i.Recipient}
                conl[num] = conl1
                num += 1
        return JsonResponse({"msg": conl})


@csrf_exempt
def payment_order(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        kg = req.get("uid") and req.get("Airline_order") and len(req) == 2
        if kg:
            uid = req["uid"]
            Aie_line = req["Airline_order"]
        c_r = consumption_record.objects.filter(Airline_order=Aie_line)
        c_r = c_r[0]
        u = user.objects.get(id=uid)
        if u.balance >= c_r.Money:
            c_r.UserId = uid
            c_r.save()
            return JsonResponse({"msg": c_r.secret_key})
        else:
            return JsonResponse({"msg": "No enough money!"})


@csrf_exempt
def payment_check(request):
    # successful, unsuccessful / paid, unpaid
    if request.method == 'POST':
        req = json.loads(request.body)
        kg = req.get("state") and req.get("order_id") and len(req) == 2
        if kg:
            state = req["state"]
            Aie_line = req["order_id"]
        if state == "successful":
            c_r = consumption_record.objects.filter(Airline_order=Aie_line)
            c_r = c_r[0]
            c_r.State = True
            c_r.save()
            u = user.objects.get(id=c_r.UserId)
            u.balance = float(u.balance) - float(c_r.Money)
            u.save()
            return JsonResponse({"state": "paid"})
        else:
            return JsonResponse({"state": "unpaid"})


@csrf_exempt
def payment_return(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        kg = req.get("state") and req.get("order_id") and len(req) == 2
        if kg:
            state = req["state"]
            Aie_line = req["order_id"]
        if state == "successful":
            c_r = consumption_record.objects.filter(Airline_order=Aie_line)
            c_r = c_r[0]
            c_r.State = False
            c_r.save()
            time = datetime.now()
            sk = secrets.token_hex(8)
            c_order1 = consumption_record(Time=time, Recipient="income", Amount=1, Money=c_r.Money,
                                          secret_key=sk, UserId=c_r.UserId, Airline_order=0, State=True)
            c_order1.save()
            u = user.objects.get(id=c_r.UserId)
            u.balance = float(u.balance) + float(c_r.Money)
            u.save()
            return JsonResponse({"state": "canceled"})
        else:
            return JsonResponse({"state": "uncanceled"})


@csrf_exempt
def Transfer(request):
    if request.method == "POST":
        u = json.loads(request.body)
        userid = u["uid"]
        password = u["password"]
        username2 = u["u2"]
        username3 = u["u3"]
        money = u["money"]
        exist_user = user.objects.get(id=userid)
        if password != exist_user.password:
            return JsonResponse({"msg": "Wrong password."})
        if username2 != username3:
            return JsonResponse({"msg": "Input different usernames for transfering. Please check"})
        another_user = user.objects.get(username=username2)
        if another_user is None:
            return JsonResponse({"msg": "We can not find the user with this username."})
        if exist_user.balance < money:
            return JsonResponse({"msg": "Insufficient deposit!"})
        exist_user.balance -= money
        another_user.balance += money
        exist_user.save()
        another_user.save()
        time = datetime.now()
        sk = secrets.token_hex(8)
        o1 = consumption_record(Time=time, Recipient="expense", Amount=1,
                                Money=money, secret_key=sk, UserId=exist_user.id, Airline_order=0, State=True)
        o2 = consumption_record(Time=time, Recipient="income", Amount=1,
                                Money=money, secret_key=sk, UserId=another_user.id, Airline_order=0, State=True)
        o1.save()
        o2.save()
        return JsonResponse({"msg": "Transfer successfully!"})


@csrf_exempt
def Balance(request):
    if request.method == "POST":
        income = 0
        expense = 0
        u = json.loads(request.body)
        uid = u["uid"]
        exist_user = user.objects.filter(id=uid).first()
        Records = consumption_record.objects.filter(UserId=exist_user.id).all()
        for record in Records:
            if record.Recipient == "income":
                income += record.Money
            else:
                expense += record.Money
        con = {"income": income, "expense": expense}
        data = {"income": con.get("income"), "expense": con.get("expense")}
        return JsonResponse(data, safe=False)
