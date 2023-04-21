from flask import Flask, request
from flask_restx import Api, Resource


from . import connectDB
from .conf import DB_ID, DB_PWD, DB_NAME, sites

app = Flask(__name__)
api = Api(app)

@api.route('/quick_work')
class addEmail(Resource):
    
    connectDB.connect(DB_ID, DB_PWD, DB_NAME)
    
    def post(self):
        # insert to database user email #
        
        data = request.json.get('data')
        
        if connectDB.push_email(data['user'], data['email'], data['website']):
            return {
                'post' : 'success'
            }
        else:
            return{
                'post' : 'fail'
            }
    
    def delete(self):
        # drop row from email_list #
        
        data = request.json.get('data')
        
        if connectDB.delete_email(data['user'], data['email'], data['website']):
            return {
                'delete' : 'success'
            }
        else:
            return{
                'delete' : 'fail'
            }
        
    def get(self):
        # get list of providing websites #
        
        ret = {}
        for site in sites:
            ret[site['name']] = site['url']
            
        return ret
        