from sesh import session
import model

test_cTable = model.CryptoTable()
test_cTable.type = False
test_cTable.price = 100
test_cTable.count = 100
test_cTable.exchange = "GDAX"
test_cTable.pairname = "USDBTC"
session.add(test_cTable)

session.flush()
session.commit()


cTable_t = session.query(model.CryptoTable)
for cryptoTable in cTable_t:
    print(cryptoTable.pairname)

