from flask import Flask,request
from flask_cors import CORS, cross_origin
import json
import calendar
from datetime import datetime
from datetime import date

app = Flask(__name__)
cors = CORS(app)

def StoreFitnessData(new_data):
    with open('db.json','r+') as file:
        data = json.load(file)
        data["fitnessData"].append(new_data)
        file.seek(0)
        json.dump(data,file,indent=4)
        return ("Success")


def RetrivePremium():
    current_month = str(datetime.now().month)
    if(len(current_month) == 1):
        current_month = "0"+current_month
    with open('db.json','r+') as file:
        data = json.load(file)
        fitness_aggregate = data["fitnessData"]
        aggregate_data = {
            "stepCount": 0,
            "heartRate": 0,
            "spO2": 0,
        }
        counter = 0
        for i in fitness_aggregate:
            if (i["Date"][4:6] == current_month):
                counter = counter + 1
                aggregate_data["stepCount"] = aggregate_data["stepCount"] + i["stepCount"]
                aggregate_data["heartRate"] = aggregate_data["heartRate"] + i["heartRate"]
                aggregate_data["spO2"] = aggregate_data["spO2"] + i["spO2"]
        aggregate_data["stepCount"] = int(aggregate_data["stepCount"]/counter)
        aggregate_data["heartRate"] = int(aggregate_data["heartRate"]/counter)
        aggregate_data["spO2"] = int(aggregate_data["spO2"]/counter)

        multiplier = 0

        if (aggregate_data["heartRate"] < 100):
            multiplier = 0.25
        elif (aggregate_data["heartRate"] < 150):
            multiplier = 0.5
        else:
            multiplier = 0.75
        
        total_discount = (aggregate_data["stepCount"]/10000)*multiplier
        amount = 500 - (total_discount * 500)
        
        next_month = int(current_month)+1
        next_month = "0" + str(next_month)
        due_date = "01/"+next_month+"/"+str(datetime.now().year)

        result = {
            "amount":amount,
            "discount":total_discount,
            "due_date":due_date
        }

        return (result)


@app.route("/fitness-data",methods=['POST'])
def postFitnessData():
    data = request.get_json()
    StoreFitnessData(data)
    return "OK",201

@app.route("/getInsuranceValue",methods=['GET'])
def getPremium():
    data = RetrivePremium()
    return data,200

if __name__ == '__main__':
    app.run(host='192.168.184.161',port=8080,debug=True)
