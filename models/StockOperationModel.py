class StockOperationModel:
    _timeCreated = ''
    _username = ''
    _stockCode = ''
    _stockPrice = -1
    _tradeVolume = -1
    _tradeType = -1

    def __init__(self, timeCreated = "", username = '', stockCode = "", stockPrice = -1, tradeVolume = -1, tradeType = -1):
        ''' Constructor for this class. '''
        # Create some member animals
        self._timeCreated = timeCreated
        self._username = username
        self._stockCode  = stockCode
        self._stockPrice = stockPrice
        self._tradeVolume = tradeVolume
        self._tradeType = tradeType
        
    def getInsertQuery(self) :
        return """
                  INSERT INTO StockOperation 
                  (OperationID, TimeCreated, Username, StockCode, StockPrice, TradeVolume, TradeType)
                  VALUES (now(), ?, ?, ?, ?, ?, ?);
               """

    def getValuesAsList(self) :
        return [self._timeCreated, self._username, self._stockCode, 
                self._stockPrice, self._tradeVolume, self._tradeType]

    def getSelectQuery(self, attributes) :
        rawQuery = "SELECT "

        if(len(attributes) == 0) :
            rawQuery += "* "
        else :
            for key in attributes.keys() :
                rawQuery += "%s, " % key
        
        rawQuery += ("FROM StockOperation ")

        # if(len(criterias) != 0) :
        #     rawQuery += ("WHERE ")
        #     for key in criterias.keys() :
        #         rawQuery += "%s=" % key + "%s AND " % criterias[key]

        # if(rawQuery[len(rawQuery) - 4 : ] == "AND ") :
        #     rawQuery = rawQuery[0 : len(rawQuery) - 5]

        rawQuery += ";"

        return rawQuery
        # preparedQuery = session.prepare(rawQuery)

        # feedback = session.execute_async(preparedQuery)
        # rows = feedback.result()

        # for row in rows:
        #     print("%s\t%i\t%s\t%.2f\t%i\t%i" % (row.timestamp, row.userid, row.stockcode, round(row.stockprice, 2), row.tradevolume, row.tradetype))
