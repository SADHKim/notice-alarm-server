from flask import Flask, session, request, render_template, redirect, url_for, jsonify


import connectDB
from conf import DB_ID, DB_PWD, DB_NAME, sites

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/profile')
def profile():
    if 'user' not in session:
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
        
@app.route('/profile/login')
def login():
    return 'login'
        
@app.route('/websites')
def websites():
    return 'websites'    

@app.route('/websites/ask')
def ask():
    return 'ask'

@app.route('/notice')
def notice():
    return 'notice'




### API server requests post, delete with json file ###
@app.route('/api/email', methods = ['POST', 'DELETE'])
def api_email():
    
    connectDB.connect(DB_ID, DB_PWD, DB_NAME)
    
    if request.method == 'POST':
        # insert to database user email #
        
        data = request.get_json()
        
        res = connectDB.push_email(data['user'], data['email'], data['website'])
        return jsonify({'post' : res})
    
    if request.method == 'DELETE':
        # drop row from email_list #
        
        data = request.get_json()
        
        res = connectDB.delete_email(data['user'], data['email'], data['website'])
        return jsonify({'delete' : res})

@app.route('/api/websites')
def api_websites():
    # get list of providing websites #
        
    ret = {}
    for site in sites:
        ret[site['name']] = site['url']
            
    return jsonify(ret)

@app.route('/api/id_overlap_check', methods = ['POST'])
def api_id_overlap_check(id):
    flag = connectDB.id_overlap_check(id)
    
    if flag is True:
        return jsonify({'msg' : 'ok'})
    elif flag is False:
        return jsonify({'msg' : 'no'})
    else:
        return jsonify({'msg' : flag})

def start():
    app.run()
    
if __name__ == '__main__':
    start()