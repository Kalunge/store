from models.item import ItemModel
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help='please enter a price for your item'
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help='an item needs a store id'
    )

    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {'message':'an item with that name doe not exist'}, 404
    
    def post(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return {'message':f'an item with the name {name} already exists'}, 400

        data = self.parser.parse_args()
        item = ItemModel(name, **data)
        
        item.save_to_db()
        return item.json()

    def put(self, name):
        data = self.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)
        item.save_to_db()
    
        return item.json()

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message':'item deleted successfully'}
        else:
            return {'message':'item does not exists'}, 404


class ItemList(Resource):
    def get(self):
        return {'items':[item.json() for item in ItemModel.query.all()]}