
from datamap import *



def find(Model, filter=None, projection=None):
    cursor = db[Model.tblname].find(filter, projection)
    return pd.DataFrame(list(cursor))

def update_one(Model, filter=None, update=None):
    UpdateResult = db[Model.tblname].update_one(filter, update, upsert=False)
    dbg.UpdateResult(UpdateResult)

def insert_data(Model):
    InsertManyResult = db[Model.tblname].insert_many(Model.data)
    dbg.InsertManyResult(InsertManyResult)

def delete_many(Model, filter):
    db[Model.tblname].delete_many(filter)

def drop_tbl(Model):
    db[Model.tblname].drop()

def rename_tbl(Model, new_name):
    db[Model.tblname].rename(new_name)
