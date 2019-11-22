from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.store import StoreModel
class store(Resource):
    """
    reqparse module helps to make sure that required datapoints are there in the payload.
    Also, we can extract the datapoints which are required to update or insert instead of
    sending all the datapoints to the final operation.

    """

    def get(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message":"Store not found"}, 404

    def post(self,name):
        if StoreModel.find_by_name(name):
            return {'message' : "A store with name {} already exists".format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message":"An error occurred while inserting store"}, 500
        return store.json(), 201

    def delete(slef,name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message':'store deleted'}


class storeList(Resource):
    def get(self):
        # using lambda
        # return {'stores':list(map(lambda x: x.json(), StoreModel.query.all()))}
        return {'stores':[store.json() for store in StoreModel.query.all()]}
