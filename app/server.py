from flask import Flask, session, request, render_template, redirect, url_for, jsonify, abort
from datetime import datetime


import connectDB
from conf import DB_ID, DB_PWD, DB_NAME, sites

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/profile')
def profile():
    if 'user' not in session:
        return render_template('login')
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
        
        if connectDB.push_user(info) is True:
            return redirect(url_for('main'))
        else:
            abort(500)
        
@app.route('/profile/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    elif request.method == 'POST':
        userid = request.form['id']
        userpwd = request.form['passwd']
        
        flag = connectDB.login(userid, userpwd)
        if flag is True:
            session['user'] = userid
            return redirect(url_for('main'))
        elif flag is False:
            return redirect(url_for('login', notLogin = True))
        
@app.route('/websites', methods = ['GET', 'POST'])
def websites():
    if request.method == 'GET':
        return render_template('websites.html', websites = sites)
    
    elif request.method == 'POST':
        if 'user' not in session:
            return redirect(url_for('login'))
        else:
            site = request.get_json()
            userInfo = connectDB.get_user_info(session['user'])
            
            flag = connectDB.push_email(userInfo['id'], userInfo['email'], site['name'])
            if flag is True:
                return redirect(url_for('websites'))
            elif flag is False:
                return redirect(url_for('websites', plus = site['name']))
            else:
                abort(500)
        
        

@app.route('/websites/ask', methods = ['GET', 'POST'])
def ask():
    if request.method == 'GET':
        asks = connectDB.get_asks()
        return render_template('websites.html', asks = asks)
    
    elif request.method == 'POST':
        site = request.get_json()
        
        flag = connectDB.push_ask(site['name'], site['url'])
        if flag is True:
            return redirect(url_for('ask', plus = site['name']))
        elif flag is False:
            return redirect(url_for('aks', plus = 'no'))
        else:
            abort(500)
        
        

@app.route('/notice', methods = ['GET', 'POST'])
def notice():
    if request.method == 'GET':
        notices = connectDB.get_notices()
        return render_template('notice.html', notices = notices)
    
    elif request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        clock = datetime.now().strftime('%Y-%m-%d')
        
        flag = connectDB.push_notice(title, content, clock)
        if flag is True:
            return redirect(url_for('notice', plus=title))
        else:
            return redirect(url_for('notice', plus='no'))




### API server requests post, delete with json file ###
@app.route('/api/email', methods = ['POST', 'DELETE'])
def api_email():
    
    connectDB.connect(DB_ID, DB_PWD, DB_NAME)
    
    if request.method == 'POST':
        # insert to database user email #
        
        data = request.get_json()
        
        res = connectDB.push_email(data['user'], data['email'], data['website'])
        if res is True:
            return jsonify({'msg' : 'ok'})
        else:
            return jsonify({'msg' : res})
    
    if request.method == 'DELETE':
        # drop row from email_list #
        
        data = request.get_json()
        
        res = connectDB.delete_email(data['user'], data['email'], data['website'])
        if res is True:
            return jsonify({'msg' : 'ok'})
        else:
            return jsonify({'msg' : res})

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