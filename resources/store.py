from models.store import StoreModel
from flask_restful import Resource
from db import db

class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message':'a store by that name does not exist'}, 404
    
    def post(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {'message':f'a store by the name {name} already exists'}, 400
        store = StoreModel(name)
        store.save_to_db()

        return store.json()
        
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message':'store deleted successfully'}

    
class StoreList(Resource):
    def get(self):
        return {'stores':[store.json() for store in StoreModel.query.all()]}