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
    if 'user' in param:
        info = connectDB.get_user_info(param['user'])
        return jsonify(info)
    
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
            return render_template('register.html', msg = "your ID has been added. go to login.", error=0)
        else:
            return render_template('register.html', msg='Error. try agian later', error=1)
        
@app.route('/profile/login', methods = ['GET', 'POST'])
def login():
    if 'user' in session:
        return render_template('main.html', msg='Logout first.', error=1)
    
    if request.method == 'GET':
        return render_template('index.html')
    
    elif request.method == 'POST':
        userid = request.form['id']
        userpwd = request.form['passwd']
        
        flag = connectDB.login(userid, userpwd)
        if flag is True:
            session['user'] = userid
            return render_template('main.html', msg='Logged in', error = 0)
        elif flag is False:
            return render_template('index.html', msg='Wrong ID or password.', error = 1)

@app.route('/profile/logout')
def logout():
    if 'user' in session:
        session.pop('user')
        return render_template('main.html', msg="Logged out")
    else:
        return render_template('main.html', msg='Login first', error=1)
      
@app.route('/websites', methods = ['GET', 'POST', 'DELETE'])
def websites():
    if request.method == 'GET':
        return render_template('websites.html')
    
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
        return render_template('ask.html')
    
    elif request.method == 'POST':
        
        flag = connectDB.push_ask(request.form['name'], request.form['url'])
        if flag is True:
            return render_template('ask.html', msg="Your ask has been added.", error=0)
        elif flag is False:
            return render_template('ask.html', msg="Your ask has already been added.", error=1)
        else:
            return render_template('ask.html', msg=flag, error=1)
        
@app.route('/notice', methods = ['GET', 'POST', 'DELETE'])
def notice():
    if request.method == 'GET':
        return render_template('notice.html')
    
    elif request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        clock = datetime.now().strftime('%Y-%m-%d')
        
        flag = connectDB.push_notice(title, content, clock)
        if flag is True:
            return render_template('notice.html', msg="Your notice has been added.", error=0)
        else:
            return render_template('notice.html', msg="Your notice cannot be added.", error=1)
        
    elif request.method == 'DELETE':
        data = request.get_json()
        
        flag = connectDB.delete_notice(data['num'])
        if flag is True:
            return jsonify({'msg' : 'The notice has been deleted', 'error' : 0})
        elif flag is False:
            return jsonify({'msg' : 'The notice is not exists', 'error' : 1})
        else:
            return jsonify({'msg' : flag, 'error' : 1})



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
        
        flag = connectDB.push_user_website(data['user'], data['email'], data['website'])
        if flag is True:
            return jsonify({'msg' : 'The website has been added', 'error' : 0})
        elif flag is False:
            return jsonify({'msg' : 'You already has the website', 'error' : 1})
        else:
            return jsonify({'msg' : flag, 'error' : 1})
            
@app.route('/api/change/password', methods=['POST'])
def api_change_password():
    data = request.get_json()
    
    userId = data['user']
    currPwd = data['currPass']
    newPwd = data['newPass']
    
    flag = connectDB.update_password(userId, currPwd, newPwd)
    
    if flag is True:
        return jsonify({'msg' : 'Your password has been change', 'error' : 0})
    elif flag is False:
        return jsonify({'msg' : 'Error. Check your current password', 'error' : 1})
    else:
        return jsonify({'msg' : flag, 'error' : 1})
    
@app.route('/api/change/email', methods=['POST'])
def api_change_email():
    data = request.get_json()
    
    userId = data['user']
    newEmail = data['newEmail']
    
    flag = connectDB.update_email(userId, newEmail)
    
    if flag is True:
        return jsonify({'msg' : 'Your email has been changed', 'error' : 0})
    else:
        return jsonify({'msg' : flag, 'error' : 1})
    
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
            return jsonify({'msg' : 'The ask has been deleted', 'error' : 0})
        elif flag is False:
            return jsonify({'msg' : 'The url of ask is not eixist', 'error' : 1})
        else:
            return jsonify({'msg' : flag, 'error' : 1})
        
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