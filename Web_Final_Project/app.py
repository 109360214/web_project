from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_cors import CORS
from datetime import datetime, date
from function import *

app = Flask(__name__)

cors = CORS(app,resources={r"/api/*":{"origins":'*'}})


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/api/user_identity', methods=['POST'])
def user_identity():
    user = request.get_json()["user"] #user 決定他是哪一個身分 
    response = {}
    if user == "client":
        store_date = booking().judge_weekday()
        response = {
            "store_name": "蟹堡王",
            "store_address": "比奇堡",
            "store_date":  store_date
            }
        return jsonify(response)
    elif user == "staff":
        res=booking().return_today_booking_info()
        response = {
            "res": res
            }
        return jsonify(response)


@app.route('/api/reservation_Info', methods=['POST'])
def reservation_Info():
    
    phonenumber = request.get_json()['phoneNumber']
    name = request.get_json()['name']
    client_num = request.get_json()['peopleNum']
    time_for_front = request.get_json()['time']
    date_for_front = request.get_json()['date']
    #self. 的寫法是因為要把這些資料寫入到function.py裡面的booking class裡面，
    reservation = booking(phonenumber=phonenumber, name=name, client_num=client_num).write(date_for_front=date_for_front, time_for_front=time_for_front)
    response = {
        'res' : reservation
    }
    return jsonify(response)


@app.route('/api/delete_client_info', methods=['POST'])
def delete_client_info():
    phonenumber = request.get_json()['phoneNumber']
    date_for_front = request.get_json()['date']
    time_for_front = request.get_json()['time']
    res = booking(phonenumber=phonenumber).delete(date_for_front=date_for_front, time_for_front=time_for_front)
    response = {
        'res' : res
    }
    return jsonify(response)
    


@app.route('/api/get_booking_info', methods=['POST'])
def get_booking_info():
    check_date = request.get_json()['dateChoice']
    client_num = request.get_json()['peopleNum']
    res = booking(client_num=client_num).judge_time(check_date=check_date)
    response = {
        'res' : res
    }
    return jsonify(response)


@app.route('/', defaults={'path':'index.html'})
@app.route('/<path:path>')
def catch_all(path):
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='172.20.10.4', port=5000, debug=True)