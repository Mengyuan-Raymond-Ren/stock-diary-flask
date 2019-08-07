import sys
sys.path.insert(0, 'models/')
sys.path.insert(1, 'cqls/')
import requests
import json
import BasicCQL

from flask import Flask, Response, request, jsonify
from flask_cors import CORS, cross_origin
from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from StockOperationModel import StockOperationModel
from UserProfileModel import UserProfileModel

app = Flask(__name__)
CORS(app, resources=r'/*')
app.config['CORS_HEADERS'] = 'Content-Type'

session = BasicCQL.createSession()
BasicCQL.createKeySpace(session)
BasicCQL.createTables(session)

@app.route('/')
@cross_origin(supports_credentials=True)
def indexPage():
    # session = BasicCQL.createSession()
    # for i in range(9) :
    #     stockOperationModel = StockOperationModel('toTimestamp(now())', 'Ray', 'SLM', 11.28, i * 10, 1)
    #     query = stockOperationModel.getInsertQuery()
    #     valuesList = stockOperationModel.getValuesAsList()
    #     feedback = BasicCQL.operationInsert(session, query, valuesList)

    # API_URL = "https://www.alphavantage.co/query"

    # data = {"function": "TIME_SERIES_DAILY", "symbol": "MSFT", "outputsize": "compact", "datatype": "txt", "apikey": "L1J902V5ANFIWZYK"}
    # response = requests.get(API_URL, params=data)
    # print(response.json()[u'Meta Data'])

    # with open("tempJSON", 'wb') as fd:
    #     for chunk in response.iter_content(chunk_size=128):
    #         fd.write(chunk)
    
    # BasicCQL.dropKeySpace(session)
    return "Load Sueccessful!"

@app.route('/user/<username>', methods=['GET'])
@cross_origin(supports_credentials=True)
def retrieveUserInformationHandler(username):
    session = BasicCQL.createSession()
    stockOperationModel = StockOperationModel()
    feedback = BasicCQL.operationSelect(session, stockOperationModel.getSelectQuery([]))
    operations = {'TimeCreated': '', 'Username': '', 'StockCode': '', 'StockPrice': '', 'TradeVolume': '', 'TradeType': '', }
    for row in feedback :
        operations['TimeCreated'] += '%s,' % row.timecreated
        operations['Username'] += '%s,' % row.username
        operations['StockCode'] += '%s,' % row.stockcode
        operations['StockPrice'] += '%f,' % round(row.stockprice, 2)
        operations['TradeVolume'] += '%d,' % row.tradevolume
        operations['TradeType'] += '%d,' % row.tradetype
    js = json.dumps(operations)
    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/user/register/', methods=['POST'])
@cross_origin(supports_credentials=True, origin='http://127.0.0.1:5000/', headers=['Content-Type'])
def registerUserHandler():
    content = request.json
    username = content['Username']
    password = content['Password']
    userProfileModel = UserProfileModel(username, password)

    session = BasicCQL.createSession()
    query = userProfileModel.getInsertQuery()
    valuesList = userProfileModel.getValuesAsList()
    feedback = BasicCQL.operationInsert(session, query, valuesList)
    js = json.dumps({})
    resp = Response(js, status=200, headers={'Access-Control-Allow-Origin': '*'}, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    # feedback = BasicCQL.operationSelect(session, userProfileModel.getSelectQuery([]))
    return resp