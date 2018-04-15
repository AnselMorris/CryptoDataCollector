from sqlalchemy import orm
import datetime
from sqlalchemy import schema, types

metadata = schema.MetaData()

def now():
    return datetime.datetime.now()

cryptoTable = schema.Table('table', metadata,
    schema.Column('type', types.String, default= "Null"),
    schema.Column('price', types.Float, default= 0),
    schema.Column('count', types.Float, default=0),
    schema.Column('exchange', types.String, default=u''),
    schema.Column('pairname', types.String, default=u''),
    schema.Column('id', types.Integer, primary_key= True),
)

class CryptoTable(object):
    pass


orm.mapper(CryptoTable, cryptoTable)
