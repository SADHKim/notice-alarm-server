import re
from flask import Flask, session, request, render_template, redirect, url_for, jsonify, abort
from datetime import datetime

import connectDB
from conf import SECRET_KEY

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
def check_email(email):
    if(re.fullmatch(regex, email)):
        return True
 
    else:
        return False

app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.before_request
def before_request():
    connectDB.connect()

@app.after_request
def after_request(response):
    connectDB.disconnect()
    return response


@app.route('/')
def main():
    return render_template('main.html')

@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user_websites = connectDB.get_user_websites(session['user'])
    param = request.args.to_dict()
    if 'error' in param and param['error'] == '1':
        return render_template('profile.html', msg='Check your password', websites=user_websites)
    elif 'error' in param and param['error'] == '2':
        return render_template('profile.html', msg='Invalid E-mail format. try again', websites=user_websites)
    elif 'error' in param and param['error'] == '-1':
        return render_template('profile.html', msg='Error try again later', websites=user_websites)
    else:
        return render_template('profile.html', websites=user_websites)
            
@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    elif request.method == 'POST':
        info = {}
        info['id'] = request.form['id']
        info['passwd'] = request.form['passwd']
        info['email'] = request.form['email']
        
        email_flag = check_email(info['email'])
        if email_flag == False:
            return render_template('register.html', msg="Check your E-mail format")
        
        if connectDB.push_user(info):
            return render_template('register.html', msg = "your ID has been added. go to login.")
        else:
            return render_template('register.html', msg='Error. try agian later')
        
@app.route('/profile/login', methods = ['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('main'))
    
    if request.method == 'GET':
        return render_template('index.html')
    
    elif request.method == 'POST':
        userid = request.form['id']
        userpwd = request.form['passwd']
        
        if not userid.isalnum():
            return render_template('index.html', msg='Do not try hacking')
        
        flag = connectDB.login(userid, userpwd)
        if flag is True:
            email = connectDB.get_user_info(userid)['email']
            
            session['user'] = userid
            session['email'] = email
            session['key'] = hash(userpwd)
            
            if userid == 'admin':
                session['admin'] = 'true'
            return redirect(url_for('main'))
        elif flag is False:
            return render_template('index.html', msg='Wrong ID or PASSWORD')

@app.route('/profile/logout')
def logout():
    if 'user' in session:
        session.pop('user')
        session.pop('email')
        session.pop('key')
        if 'admin' in session:
            session.pop('admin')
        return redirect(url_for('main'))
    else:
        return redirect(url_for('main'))
      
@app.route('/websites', methods = ['GET', 'POST', 'DELETE'])
def websites():
    if request.method == 'GET':
        if 'user' in session:
            info = connectDB.get_user_websites(session['user'])
            user_websites = []
            for website in info:
                user_websites.append(website['website_name'])
            
            sites = connectDB.get_websites()
            
            return render_template('websites.html', sites=sites, user_websites=user_websites)
        else:
            sites = connectDB.get_websites()
            return render_template('websites.html', sites=sites)
    
    elif request.method == 'POST':
        if 'user' not in session:
            return redirect(url_for('login'))
        elif 'admin' not in session or session['admin'] != 'true':
            return redirect(url_for('main'))
        elif session['key'] != hash(connectDB.get_user_info(session['user'])['passwd']):
            return redirect(url_for('main'))
        
        else:
            flag = connectDB.push_website(request.form)
            websites=connectDB.get_websites()
            if flag is True:
                return render_template('websites.html', sites=websites)
            elif flag is False:
                return render_template('websites.html', sites=websites)
            else:
                return render_template('websites.html', msg=flag, error=1)
    
    elif request.method == 'DELETE':
        if 'user' not in session:
            return redirect(url_for('login'))
        elif 'admin' not in session or session['admin'] != 'true':
            return redirect(url_for('main'))
        elif session['key'] != hash(connectDB.get_user_info(session['user'])['passwd']):
            return redirect(url_for('main'))
        
        info = request.get_json()
        flag = connectDB.delete_website(info['name'])
        
        if flag is True:
            return jsonify({'error' : 0})
        elif flag is False:
            return jsonify({'error' : 1})
        else:
            return jsonify({'msg' : str(flag), 'error' : -1})
        
@app.route('/websites/ask', methods = ['GET', 'POST'])
def ask():
    if request.method == 'GET':
        asks = connectDB.get_asks()
        return render_template('ask.html', asks=asks)
    
    elif request.method == 'POST':
        if 'user' not in session:
            return redirect(url_for('login'))
        
        flag = connectDB.push_ask(request.form['name'], request.form['url'])
        asks = connectDB.get_asks()
        
        return render_template('ask.html', asks=asks)
        
@app.route('/notice', methods = ['GET', 'POST', 'DELETE'])
def notice():
    if request.method == 'GET':
        notices = connectDB.get_notices()
        return render_template('notice.html', notices=notices)
    
    elif request.method == 'POST':
        if 'user' not in session:
            return redirect(url_for('login'))
        elif 'admin' not in session or session['admin'] != 'true':
            return redirect(url_for('main'))
        elif session['key'] != hash(connectDB.get_user_info(session['user'])['passwd']):
            return redirect(url_for('main'))
        
        title = request.form['title']
        content = request.form['content']
        clock = datetime.now().strftime('%Y-%m-%d')
        
        flag = connectDB.push_notice(title, content, clock)
        notices = connectDB.get_notices()
        return render_template('notice.html', notices=notices)
        
    elif request.method == 'DELETE':
        if 'user' not in session:
            return redirect(url_for('login'))
        elif 'admin' not in session or session['admin'] != 'true':
            return redirect(url_for('main'))
        elif session['key'] != hash(connectDB.get_user_info(session['user'])['passwd']):
            return redirect(url_for('main'))
        
        data = request.get_json()
        
        flag = connectDB.delete_notice(data['num'])
        if flag is True:
            return jsonify({'error' : 0})
        elif flag is False:
            return jsonify({'error' : 1})
        else:
            return jsonify({'msg' : flag, 'error' : -1})



### API server requests post, delete with json file ###
@app.route('/api/websites', methods=['DELETE', 'POST'])
def api_websites():
    if request.method == 'DELETE':
        data = request.get_json()
        
        if session['key'] != hash(connectDB.get_user_info(data['user'])['passwd']):
            return jsonify({'msg' : 'Bad request', 'error' : -1})
        
        flag = connectDB.delete_user_webiste(data['user'], data['website'])
        if flag is True:
            return jsonify({'error' : 0})
        elif flag is False:
            return jsonify({'error' : 1})
        else:
            return jsonify({'msg' : flag, 'error' : -1})
        
    elif request.method == 'POST':
        data = request.get_json()
        
        if session['key'] != hash(connectDB.get_user_info(data['user'])['passwd']):
            return jsonify({'msg' : 'Bad request', 'error' : -1})
        
        
        email = connectDB.get_user_info(data['user'])['email']
        
        flag = connectDB.push_user_website(data['user'], email, data['website'])
        if flag is True:
            return jsonify({'error' : 0})
        elif flag is False:
            return jsonify({'error' : 1})
        else:
            return jsonify({'error' : flag})
            
@app.route('/api/change/password', methods=['POST'])
def api_change_password():
    
    userId = request.form['user']
    currPwd = request.form['currPass']
    newPwd = request.form['newPass']
    
    if session['key'] != hash(connectDB.get_user_info(userId)['passwd']):
        return redirect(url_for('profile'))
    
    flag = connectDB.update_password(userId, currPwd, newPwd)
    
    if flag is True:
        session.pop('user')
        session.pop('email')
        session.pop('key')
        if 'admin' in session:
            session.pop('admin')
        
        return redirect(url_for('login'))
    elif flag is False:
        return redirect(url_for('profile', error=1))
    else:
        return redirect(url_for('profile', error=-1))
        
    
@app.route('/api/change/email', methods=['POST'])
def api_change_email():
    
    userId = request.form['user']
    newEmail = request.form['newEmail']
    
    if session['key'] != hash(connectDB.get_user_info(userId)['passwd']):
        return redirect(url_for('profile'))
    
    email_flag = check_email(newEmail)
    if email_flag == False:
        return redirect(url_for('profile', error=2))
    
    flag = connectDB.update_email(userId, newEmail)
    
    if flag is True:
        session.pop('user')
        session.pop('email')
        if 'admin' in session:
            session.pop('admin')
        
        return redirect(url_for('login'))
    else:
        return redirect(url_for('profile', error=-1))

@app.route('/api/id_overlap', methods = ['POST'])
def api_id_overlap():
    json = request.get_json()
    
    if not json['id'].isalnum():
        return jsonify({'msg' : 'Invalid ID', 'error' : 1})
    
    flag = connectDB.id_overlap_check(json['id'])
    
    if flag is True:
        return jsonify({'msg' : 'You can use the ID', 'error' : 0})
    elif flag is False:
        return jsonify({'msg' : "You can not use the ID", 'error' : 1})
    else:
        return jsonify({'msg' : flag, 'error' : 1})

def start():
    app.run(host='0.0.0.0')
    
if __name__ == '__main__':
    start()