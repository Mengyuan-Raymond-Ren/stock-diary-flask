from flask import Flask
from flask import Response
from flask import jsonify

import sys
sys.path.insert(0, 'models/')
sys.path.insert(1, 'cqls/')

import requests
import json

from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

import BasicCQL
from StockOperationModel import StockOperationModel

session = BasicCQL.createSession()
BasicCQL.createKeySpace(session)
BasicCQL.createTables(session)

app = Flask(__name__)

@app.route('/')
def indexPage():
    session = BasicCQL.createSession()
    for i in range(9) :
        stockOperationModel = StockOperationModel('2018-07-28 12:12:12', 'Ray', 'SLM', 11.28, i * 10, 1)
        print('Get Query.')
        query = stockOperationModel.getInsertQuery()
        print('Get ValuesList.')
        valuesList = stockOperationModel.getValuesAsList()
        print('Perform Insert Operation.')
        feedback = BasicCQL.operationInsert(session, query, valuesList)

    # API_URL = "https://www.alphavantage.co/query"

    # data = {"function": "TIME_SERIES_DAILY", "symbol": "MSFT", "outputsize": "compact", "datatype": "txt", "apikey": "L1J902V5ANFIWZYK"}
    # response = requests.get(API_URL, params=data)
    # print(response.json()[u'Meta Data'])

    # with open("tempJSON", 'wb') as fd:
    #     for chunk in response.iter_content(chunk_size=128):
    #         fd.write(chunk)
    
    # BasicCQL.dropKeySpace(session)
    return "Insert Sueccessful!"

@app.route('/user/<username>', methods=['GET'])
def userPage(username):
    session = BasicCQL.createSession()
    stockOperationModel = StockOperationModel()
    feedback = BasicCQL.operationSelect(session, stockOperationModel.getSelectQuery([]))
    operations = {'TimeCreated': '', 'Username': '', 'StockCode': '', 'StockPrice': '', 'TradeVolume': '', 'TradeType': '', }
    for row in feedback :
        print(row.timecreated)
        print(row.username)
        print(row.stockcode)
        print(row.stockprice)
        print(row.tradevolume)
        print(row.tradetype)
        operations['TimeCreated'] += '%s,' % row.timecreated
        operations['Username'] += '%s,' % row.username
        operations['StockCode'] += '%s,' % row.stockcode
        operations['StockPrice'] += '%f,' % round(row.stockprice, 2)
        operations['TradeVolume'] += '%d,' % row.tradevolume
        operations['TradeType'] += '%d,' % row.tradetype
    js = json.dumps(operations)

    # data = {
    #     'Timestamp': '2018-08-31', 
    #     'UserID': userid, 
    #     'StockCode': 'SLM', 
    #     'StockPrice': 12.15, 
    #     'TradeVolume': 10, 
    #     'TradeType': 1,
    # }
    # js = json.dumps(data)

    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
