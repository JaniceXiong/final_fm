import bottle
from bottle import get,post,request
import json,os
import db_operation
import recom_operation
import analysis_operation

db = db_operation.Db("fm.db")
recom = None
analy = None
idx=0
cnt_song = -1
base_song_list = None #约80首


def check_login(name,password):
    #查询数据库
    return False

def save_new_user(name,password,email):
    #写入数据库
    return True

app = bottle.Bottle()

@app.route('/fm')
@app.route('/fm.html')
def load_fm():
    return bottle.static_file('fm.html','./')

@app.route('/fm',method="GET")
def handle_fm_rq():
    global recom,base_song_list,cnt_song,idx,current_user,analy
    
    rq_name = bottle.request.query.rq_name

    
    if(rq_name == "rq_nextsong"):
        print("backend get next song")
        global idx,base_song_list
        if(idx == cnt_song-1):
            base_song_list = recom.get_songs()
            idx = -1

        idx = idx+1
        print("这是第%d" % idx)
        print(base_song_list[idx])
        return base_song_list[idx]

    elif(rq_name == "rq_likesong"):
        print("backend like song")
        like_song_id = bottle.request.query.liked_song
        print(like_song_id)
        print(current_user)
        #db.add_to_songlist(current_user,like_song_id,"我喜欢")

        recom_song_list = recom.get_one_by_like(like_song_id)
        
        print(recom_song_list)
        return json.dumps(recom_song_list)
    
    elif(rq_name == "rq_init"):
        print("rq init")
        user_name = bottle.request.query.name
        print(user_name)
        
        base_song_list = recom.get_songs()
        cnt_song = len(base_song_list)

        #print("base song list:")
        #print(base_song_list)

        init_info = {}
        song_list = db.load_songlist(user_name)
        user_info = db.get_user_info(user_name)
        report_info = db.get_analysis(user_name)

        init_info['song_list'] = song_list
        init_info['user_info'] = user_info
        init_info['first_song'] = base_song_list[0]
        init_info['report_info'] = report_info

        #print(init_info)
        
        return json.dumps(init_info)
    
    elif(rq_name=="rq_play"):
        print("rq play")
        play_id = bottle.request.query.play_song
        db.play_song(current_user,play_id)

        



@app.route('/focus')
@app.route('/focus.html')
def load_focus():
    return bottle.static_file('focus.html','./')

@app.route('/focus',method='GET')
def load_focus_data():
    #print(bottle.request.query)
    user_name = bottle.request.query.name
    print("user name:")
    print(user_name)
    focus_info={}
    focus_info['song_list'] = db.load_songlist("user0")
    
    return json.dumps(focus_info)


@app.route('/login')
@app.route('/login.html')
def login():    
    return bottle.static_file('login.html','./')

current_user = ""
@app.route('/login',method='POST')
def login_submit():
    global current_user,recom,analy
    submitdata = bottle.request.headers.get('submitdata')
    user = json.loads(submitdata)
    name = user['name']
    password = user['password']
    
    flag = db.user_sign_in(name,password)
    if(flag==1):
        current_user = name
        print("flag=1")
        print(current_user)
        recom = recom_operation.Recom(current_user)
        #analy = analysis_operation.Analy(current_user)
   
    return_info = {
        "msg": "登录失败",
        "success": flag
    }
    
    return return_info


@app.route('/register')
@app.route('/register.html')
def register():
    return bottle.static_file('register.html','./')

@app.route('/register',method='POST')
def register_submit():
    #print("here2")
    submitdata = bottle.request.headers.get('registerdata')
    new_user = json.loads(submitdata)
    print(new_user)
    
    name = new_user['name']
    password = new_user['password']

    if db.user_sign_up(name,password):
        return "注册成功"
    else:
        return '注册失败'



@app.route('/ref/<filename>')
def ref(filename):
    return bottle.static_file(filename, './ref/')


bottle.run(app,host='localhost',port=9000)