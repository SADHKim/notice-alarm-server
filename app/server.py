from flask import Flask, session, request, render_template, redirect, url_for, jsonify, abort
from datetime import datetime


import connectDB
from conf import SECRET_KEY

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
    param = request.args.to_dict()
    if 'error' in param and param['error'] == '1':
        return render_template('profile.html', msg='Check your password')
    
    if 'user' not in session:
        return redirect(url_for('login'))
    else:
        user_websites = connectDB.get_user_websites(session['user'])
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
        
        if connectDB.push_user(info) is True:
            return render_template('register.html', msg = "your ID has been added. go to login.", error=0)
        else:
            return render_template('register.html', msg='Error. try agian later', error=1)
        
@app.route('/profile/login', methods = ['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('main'))
    
    if request.method == 'GET':
        return render_template('index.html')
    
    elif request.method == 'POST':
        userid = request.form['id']
        userpwd = request.form['passwd']
        
        flag = connectDB.login(userid, userpwd)
        if flag is True:
            email = connectDB.get_user_info(userid)['email']
            
            session['user'] = userid
            session['email'] = email
            
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
        else:
            flag = connectDB.push_website(request.form)
            
            if flag is True:
                return render_template('websites.html', msg = request.form['name'] + ' has been added', error=0)
            elif flag is False:
                return render_template('websites.html', msg="The name of website already exists", error=1)
            else:
                return render_template('websites.html', msg=flag, error=1)
    
    elif request.method == 'DELETE':
        info = request.get_json()
        flag = connectDB.delete_website(info)
        
        if flag is True:
            return jsonify({'msg' : 'The webiste has been deleted', 'error' : 0})
        elif flag is False:
            return jsonify({'msg' : 'The website does not exists', 'error' : 1})
        else:
            return jsonify({'msg' : flag, 'error' : 1})
        
@app.route('/websites/ask', methods = ['GET', 'POST'])
def ask():
    if request.method == 'GET':
        asks = connectDB.get_asks()
        return render_template('ask.html', asks=asks)
    
    elif request.method == 'POST':
        
        flag = connectDB.push_ask(request.form['name'], request.form['url'])
        asks = connectDB.get_asks()
        if flag is True:
            return render_template('ask.html', asks=asks)
        elif flag is False:
            return render_template('ask.html', asks=asks)
        else:
            return render_template('ask.html', asks=asks)
        
@app.route('/notice', methods = ['GET', 'POST', 'DELETE'])
def notice():
    if request.method == 'GET':
        notices = connectDB.get_notices()
        return render_template('notice.html', notices=notices)
    
    elif request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        clock = datetime.now().strftime('%Y-%m-%d')
        
        flag = connectDB.push_notice(title, content, clock)
        notices = connectDB.get_notices()
        return render_template('notice.html', notices=notices)
        
    elif request.method == 'DELETE':
        data = request.get_json()
        
        flag = connectDB.delete_notice(data['num'])
        if flag is True:
            return jsonify({'error' : 0})
        elif flag is False:
            return jsonify({'error' : 1})
        else:
            return jsonify({'msg' : flag, 'error' : -1})



### API server requests post, delete with json file ###
@app.route('/api/websites', methods=['GET', 'DELETE', 'POST'])
def api_websites():
    if request.method == 'GET':
        parameter = request.args.to_dict()
        
        if 'user' in parameter and 'keyword' not in parameter:
            website_list = connectDB.get_user_websites(parameter['user'])
            return jsonify(website_list)
        elif 'user' not in parameter and 'keyword' in parameter:
            website_list = connectDB.get_keyword_websites(parameter['keyword'])
            return jsonify(website_list)
            
        else:
            # get list of providing websites #
            sites = connectDB.get_websites()
            ret = []
            for site in sites:
                tmp = {}
                tmp['name'] = site['name']
                tmp['url'] = site['url']
                ret.append(tmp)
                
            return jsonify(ret)
        
    elif request.method == 'DELETE':
        data = request.get_json()
        
        flag = connectDB.delete_user_webiste(data['user'], data['website'])
        if flag is True:
            return jsonify({'msg' : 'Your website has been deleted', 'error' : 0})
        elif flag is False:
            return jsonify({'msg' : "You don't have the website", 'error' : 1})
        else:
            return jsonify({'msg' : flag, 'error' : 1})
        
    elif request.method == 'POST':
        data = request.get_json()
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
    
    flag = connectDB.update_password(userId, currPwd, newPwd)
    
    if flag is True:
        session.pop('user')
        session.pop('email')
        if 'admin' in session:
            session.pop('admin')
        
        return redirect(url_for('login'))
    elif flag is False:
        return redirect(url_for('profile', error=1))
    else:
        return
        
    
@app.route('/api/change/email', methods=['POST'])
def api_change_email():
    
    userId = request.form['user']
    newEmail = request.form['newEmail']
    
    flag = connectDB.update_email(userId, newEmail)
    
    if flag is True:
        session.pop('user')
        session.pop('email')
        if 'admin' in session:
            session.pop('admin')
        
        return redirect(url_for('login'))
    else:
        return redirect(url_for('profile', error=-1))
    
@app.route('/api/asks', methods=['GET', 'DELETE'])
def api_asks():
    if request.method == 'GET':   
        parameter = request.args.to_dict()
        if 'keyword' in parameter:
            ret = connectDB.get_keyword_asks(parameter['keyword'])
            return jsonify(ret)
        else:
            ret = connectDB.get_asks()
            return jsonify(ret)
    elif request.method == 'DELETE':
        data = request.get_json()
        
        flag = connectDB.delete_ask(data['url'])
        if flag is True:
            return jsonify({'error' : 0})
        elif flag is False:
            return jsonify({'error' : 1})
        else:
            return jsonify({'msg' : flag, 'error' : -1})
        
@app.route('/api/notices', methods=['GET'])
def api_notices():
    param = request.args.to_dict()
    if 'num' in param:
        ret = connectDB.get_num_notice(param['num'])
        return jsonify(ret)
    else:
        ret = connectDB.get_notices()
        if ret is False:
            return jsonify({})
        else:
            return jsonify(ret)

@app.route('/api/id_overlap', methods = ['POST'])
def api_id_overlap():
    json = request.get_json()
    
    flag = connectDB.id_overlap_check(json['id'])
    
    if flag is True:
        return jsonify({'msg' : 'You can use the ID', 'error' : 0})
    elif flag is False:
        return jsonify({'msg' : "You can not use the ID", 'error' : 1})
    else:
        return jsonify({'msg' : flag, 'error' : 1})

def start():
    app.run()
    
if __name__ == '__main__':
    start()