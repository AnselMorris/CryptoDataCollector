from sesh import session
import model
import json
import sqlalchemy
from sqlalchemy import orm
import datetime
from sqlalchemy import schema, types

from websocket import create_connection

bitFin = create_connection("wss://api.bitfinex.com/ws")
gDax = create_connection("wss://ws-feed.gdax.com")
bitFin.send(json.dumps({
    "event": "subscribe",
    "channel": "book",
    "pair": "BTCUSD",
    "prec": "P0"
}))

gDax.send(json.dumps({

    "type": "subscribe",
    "product_ids": [
        "BTC-USD",

    ],
    "channels": [

        {
            "name": "full",
            "type": "open"

        }
    ]

}))

count = 0;


def parseD(res):
    res = str(res)
    res = res[1:-1]
    return res

def bitFinParse(res, c):
    res = res.split(",");
    if len(res) > 2:
        test_cTable = model.CryptoTable()
        temp = float(str(res[1])[1:])
        test_cTable.price = temp;
        temp = float(str(res[3])[1:])
        test_cTable.count = abs(temp)
        if temp > 0:
            test_cTable.type = "bid"
        else:
            test_cTable.type = "ask"
        test_cTable.exchange = "GDAX"
        test_cTable.pairname = "USDBTC"
        test_cTable.id = c;
        session.add(test_cTable)
        session.flush()
        session.commit()

for i in range(100):
    result = bitFin.recv()
    result = json.loads(result)
    result = parseD(result)
    if (i == 2):
        result = result.split("[[")
        result = result[1]
        result = result[:-2]
        result = result.split("]")
        for t in range(len(result)):
            if t == 0:
                temp = str(" , " + result[t])
                bitFinParse(temp, count)
                count += 1
            else:
                temp = str(" , " + (result[t])[3:])
                bitFinParse(temp, count)
                count += 1
    if i > 2:
        bitFinParse(result, count)
        count += 1


# for i in range(100):
#     result = gDax.recv()
#     result = json.loads(result)
#     result = parseD(result)
#     result = result.split(",")
#     if (i > 0) & ((result[0])[9] == 'r'):
#         test_cTable = model.CryptoTable()
#         temp = float(str(result[4])[11:-1])
#         test_cTable.price = temp;
#         temp = float(str(result[3])[10:-1])
#         test_cTable.count = temp
#         test_cTable.exchange = "GDAX"
#         test_cTable.pairname = "USDBTC"
#         if (result[5])[12] == 'b':
#             test_cTable.type = "bid"
#         else:
#             test_cTable.type = "ask"
#         test_cTable.id = count
#         session.add(test_cTable)
#         session.flush()
#         session.commit()
#         count += 1

cTable_t = session.query(model.CryptoTable)
for cryptoTable in cTable_t:
    print(cryptoTable.count)
