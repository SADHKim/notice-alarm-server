from flask import Flask, session, request, render_template, redirect, url_for
from flask_restx import Api, Resource


import connectDB
from conf import DB_ID, DB_PWD, DB_NAME, sites

app = Flask(__name__)
api = Api(app)

@app.route('/')
def main():
    info = {}
    if session['user'] is not None:
        info['user'] = session['user']
        info['email'] = session['email']
        
    return render_template('main.html', info=info)

@app.route('/profile')
def profile():
    if session['user'] is None:
        return render_template('not_login.html')
    else:
        info = connectDB.get_user_info(session['user'])
        
        return render_template('profile.html', info=info)
        
@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    elif request.method == 'POST':
        info = {}
        
        info['id'] = request.form['id']
        info['passwd'] = request.form['passwd']
        info['email'] = request.form['email']
        
        if connectDB.push_user(info):
            return redirect(url_for('main'))
        else:
            return redirect(url_for('error', code = 500))







### API server requests post, delete with json file ###
@api.route('/api/email')
class Email(Resource):
    
    connectDB.connect(DB_ID, DB_PWD, DB_NAME)
    
    def post(self):
        # insert to database user email #
        
        data = request.get_json()
        
        res = connectDB.push_email(data['user'], data['email'], data['website'])
        return {'post' : res}
    
    def delete(self):
        # drop row from email_list #
        
        data = request.get_json()
        
        res = connectDB.delete_email(data['user'], data['email'], data['website'])
        return {'delete' : res}

@api.route('/api/websites')
class Website(Resource):
    def get(self):
        # get list of providing websites #
        
        ret = {}
        for site in sites:
            ret[site['name']] = site['url']
            
        return ret
        

def start():
    app.run()
    
if __name__ == '__main__':
    start()