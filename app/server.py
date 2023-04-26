from flask import Flask, session, request, render_template, redirect, url_for, jsonify, abort
from datetime import datetime


import connectDB
from conf import DB_ID, DB_PWD, DB_NAME, sites, SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY
connectDB.connect(DB_ID, DB_PWD, DB_NAME)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))
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
            return render_template('register.html', msg = "your ID has been added. go to login.")
        else:
            abort(500)
        
@app.route('/profile/login', methods = ['GET', 'POST'])
def login():
    if 'user' in session:
        return render_template('main.html', msg='logout first.', error=True)
    
    if request.method == 'GET':
        return render_template('login.html')
    
    elif request.method == 'POST':
        userid = request.form['id']
        userpwd = request.form['passwd']
        
        flag = connectDB.login(userid, userpwd)
        if flag is True:
            session['user'] = userid
            return render_template('main.html', msg='logged in')
        elif flag is False:
            return render_template('login.html', msg='Wrong ID or password.', error=True)

@app.route('/profile/logout')
def logout():
    if 'user' in session:
        session.pop('user')
        return render_template('main.html', msg="logged out")
    else:
        return render_template('main.html', msg='error. try again.', error=True)
    
        
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
                return render_template('websites.html', websites = sites, msg = site['name'] + 'has been added your list.')
            elif flag is False:
                return render_template('websites.html', websites=sites, msg="You already have the site.", error=True)
            else:
                abort(500)
        
        

@app.route('/websites/ask', methods = ['GET', 'POST'])
def ask():
    if request.method == 'GET':
        asks = connectDB.get_asks()
        return render_template('ask.html', asks = asks)
    
    elif request.method == 'POST':
        site = request.get_json()
        
        flag = connectDB.push_ask(site['name'], site['url'])
        asks = connectDB.get_asks()
        if flag is True:
            return render_template('ask.html', asks=asks, msg="Your ask has been added.")
        elif flag is False:
            return render_template('ask.html', asks=asks, msg="Your ask has already been added.", error=True)
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
        notices = connectDB.get_notices()
        if flag is True:
            return render_template('notice.html', notices=notices, msg="Your notice has been added.")
        else:
            return render_template('notice.html', notices=notices, msg="Your notice cannot be added.", error=True)




### API server requests post, delete with json file ###
@app.route('/api/email', methods = ['POST', 'DELETE'])
def api_email():
    
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
    parameter = request.args.to_dict()
    
    if 'user' in parameter:
        website_list = connectDB.get_user_websites(parameter['user'])
        return jsonify(website_list)
        
    else:
        # get list of providing websites #
        ret = {}
        for site in sites:
            ret[site['name']] = site['url']
                
        return jsonify(ret)

@app.route('/api/id_overlap_check', methods = ['POST'])
def api_id_overlap_check():
    json = request.get_json()
    
    flag = connectDB.id_overlap_check(json['id'])
    
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