from pymongo import MongoClient
from datetime import datetime, date, timedelta


class booking:
    def __init__(self,phonenumber='',name='',client_num=0, table_num=''):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['restaurant']
        self.collection = self.db['booking']
        self.phonenumber=phonenumber
        self.name=name
        self.client_num=client_num
        self.table_num=table_num


    def init_data(self):
        booking_info = {"info": {
        "1": [
            {
            'type':'table_info',
            'size':4
            }
        ],
        "2":[
            {
            'type':'table_info',
            'size':4
            }
        ],
        "3":[
            {
            'type':'table_info',
            'size':2
        }
        ],
        "4":[
            {
            'type':'table_info',
            'size':2
            }
        ]  
        }   
        }
        self.collection.insert_one(booking_info)
    

    def res_booking_info(self):
        info = self.collection.find_one()
        return info

    #送出訂位資訊後 寫入資料庫
    def write(self, date_for_front, time_for_front):
        info={
            'phonenumber':self.phonenumber,
            'name':self.name,
            'client_num':self.client_num,
            'type':'client_info',
            'date':date_for_front,
            'time':time_for_front
        }
        try:
            table_info = self.collection.find_one({})
            table_info['info'][self.judge_num(date=date_for_front,time=time_for_front)].append(info)
            self.collection.update_one({},{'$set':table_info})
            return True
        except:
            return False

    
    def delete(self, date_for_front, time_for_front):
        table_info = self.collection.find_one({})
        for i in range(1,5):
            index=str(i)
            for j in range(len(table_info['info'][index])):
                try:
                    if table_info['info'][index][j+1]['date'] == date_for_front and table_info['info'][index][j+1]['time'] == time_for_front:
                        table_info['info'][index].pop(j+1)
                        self.collection.update_one({},{'$set':table_info})
                        return True
                except:
                    pass
        return False


    #判斷坐哪個桌子
    def judge_num(self,date='',time=''):
        table_info = self.collection.find_one()['info']
        empty_table = []
        #print(date,time,table_info['1'][1]['time'])
        for i in range(1,5):
            index=str(i)
            for j in range(len(table_info[index])):
                try:
                    if table_info[index][j+1]['date'] == date and table_info[index][j+1]['time'] == time:
                        print('booked')
                        break
                    else:
                        pass
                except:
                    empty_table.append(i)
        if int(self.client_num) <= 4 and int(self.client_num) > 2:
            if 1 in empty_table :
                return '1'
            elif 2 in empty_table:
                return '2'
        elif int(self.client_num) <= 2 and int(self.client_num) > 0:
            if 3 in empty_table :
                return '3'
            elif 4 in empty_table:
                return '4'


    def judge_weekday(self):
        weekday_names = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
        today = date.today()
        weekday = today.weekday()
        info = {
            "星期一": 
                {
                'ID' : "星期一",
                'Opening_time':'10:00',
                'Closing':'20:00'
                },
            "星期二":
                {
                'ID' : "星期二",
                'Opening_time':'10:00',
                'Closing':'20:00'
                }
            ,
            "星期三":
                {
                'ID' : "星期三",
                'Opening_time':'10:00',
                'Closing':'20:00'
                }
            ,
            "星期四":
                {
                'ID' : "星期四",
                'Opening_time':'10:00',
                'Closing':'20:00'
                }
            ,
            "星期五":
                {
                'ID' : "星期五",
                'Opening_time':'10:00',
                'Closing':'20:00'
                } 
            }    
        cnt = weekday
        for i in range(len(weekday_names)):
            if cnt == 5 or cnt == 6:
                pass
            elif cnt > 6:
                next_weekday = str(today + timedelta( (cnt - today.weekday()) % 7 ))
                info[weekday_names[cnt-7]]['date'] = next_weekday
            else:
                info[weekday_names[cnt]]['date'] = str(today + timedelta( (cnt - today.weekday()) % 7 ))
            cnt+=1
        return info

    
    def judge_time(self, check_date):
        available_time = ['10:00', '12:00', '14:00', '16:00', '18:00', '20:00']
        table_info = self.collection.find_one({})
        if int(self.client_num) <= 4 and int(self.client_num) > 2 :
            from1 = 1
            end1 = 3
        elif int(self.client_num) > 0 and int(self.client_num) < 3 :
            from1 = 3
            end1 = 5
        cnt = 0
        for i in range(from1, end1):
            index = str(i)
            for day in table_info['info'][index]:
                try:
                    if day['date'] == check_date:
                        cnt+=1
                        if cnt > 1:
                            available_time.remove(day['time'])
                except:
                    pass
        return available_time


    def return_today_booking_info(self):
        table_info = self.collection.find_one()['info']
        today = date.today()
        today = str(today)
        info = []
        for i in range(1,5):
            index = str(i)
            for day in table_info[index]:
                try:
                    if day['date'] == today:
                        day['table'] = index
                        info.append(day)
                except:
                    pass
        return info

            

if __name__ == '__main__':
    booking = booking(client_num='1')
    #booking.init_data()
    print(booking.return_today_booking_info())

