import sqlite3
import numpy as np
import json
import random

class Db:
    db_name = ''
    #初始化数据库对象
    def __init__(self,db_name):
        self.db_name = db_name
        print('init successfully')

    # 查找当前账号是否存在
    def search_uid(self,uid):
        print('in search_uid')
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        select_string = "SELECT COUNT(UID) FROM USER WHERE UID=?"

        cursor = c.execute(select_string, (uid,))

        num = cursor.fetchone()

        num = np.array(num[0])

        conn.commit()
        conn.close()
        if (num > 0):
            print('True')
            return True
        else:
            print('False')
            return False


    # 用户登陆功能
    def user_sign_in(self,uid,pswd):
        print('in user_sign_in')
        conn=sqlite3.connect(self.db_name)
        c= conn.cursor()
        # print("opened db sucessfully")
        if(Db.search_uid(self,uid)==False):
            conn.close()
            return -1
        else:
            select_string="SELECT PASSWORD FROM USER WHERE UID = ?"
            cursor = c.execute(select_string,(uid,))
            pswd_ = cursor.fetchone()
            pswd_ = np.array(pswd_[0])

            conn.commit()
            conn.close()

            if(pswd==pswd_):
                return 1
            else:
                return 0


    #用户注册功能
    def user_sign_up(self,uid,pswd):
        print('in user_sign_up')
        conn = sqlite3.connect('fm.db')
        print(self.db_name)
        c = conn.cursor()

        if(Db.search_uid(self,uid)==True):
            conn.close()
            return 0
        else:
            print('inserting')
            insert_string='INSERT INTO USER(UID,PASSWORD) VALUES(?,?)'
            c.execute(insert_string,(uid,pswd))
            conn.commit()
            conn.close()
            return 1


    #更新完善用户信息
    def update_user_info(self,uid,username,sex,age,profile):
        print('in update_user_info')
        conn = sqlite3.connect(self.db_name)

        c = conn.cursor()

        insert_string = 'UPDATE USER SET USERNAME = ? ,SEX = ? ,AGE = ? , PROFILE = ? WHERE UID = ? '
        try:
            c.execute(insert_string,(username,sex,age,sqlite3.Binary(profile),uid))
            print('here')
            conn.commit()
            conn.close()
        except BaseException:
            print('lalala')
            return 0
        else:
            return 1


    #获取用户个数
    def get_user_num(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        try:
            select_string = 'SELECT COUNT(*) FROM USER'
            c.execute(select_string)
            user_num = c.fetchone()
            user_num = np.array(user_num[0])
            conn.commit()
            conn.close()
        except BaseException:
            return -1
        else:
            return user_num


    # 获取歌曲个数
    def get_song_num(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        try:
            select_string = 'SELECT COUNT(*) FROM SONG'
            c.execute(select_string)
            song_num = c.fetchone()
            song_num = np.array(song_num[0])
            conn.commit()
            conn.close()
        except BaseException:
            return -1
        else:
            return song_num


    #读取用户信息
    def get_user_info(self,uid):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        select_string = 'SELECT * FROM USER WHERE UID = ?'
        c.execute(select_string,(uid,))
        user_info = c.fetchone()
        info={}
        info["name"] = user_info[2]
        info["sex"] = user_info[3]
        info["birth"] = user_info[4]
        # print(info["birth"])
        info["profile"] = user_info[5]
        # print(type(info["profile"]))

        info = Db.list_to_json(self,'userinfo',info)
        # print(user_info)
        conn.commit()
        conn.close()
        return info


    #歌单管理/加入我喜欢:songlist==null
    def add_to_songlist(self,uid,songid,songlist):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        insert_string = 'INSERT INTO USER_SONG(UID,SONGID,SONGLIST,PLAYCOUNT) VALUES(?,?,?,?)'
        try:
            c.execute(insert_string,(uid,songid,songlist,0))
        except BaseException:
            pass
        conn.commit()
        conn.close()

    #从歌单或我喜欢中删除歌曲
    def delete_from_songlist(self,uid,songid):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        delete_string = 'DELETE FROM USER_SONG WHERE UID = ? AND SONGID = ? ;'
        try:
            c.execute(delete_string,(uid,songid))
        except BaseException:
            pass
        conn.commit()
        conn.close()

    #加载歌单
    def load_songlist(self,uid):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        #加载该用户所有歌单
        select_string = 'SELECT distinct SONGLIST FROM USER_SONG WHERE UID = ? '
        c.execute(select_string,(uid,))

        songlist = c.fetchall()
        #获得歌单的数量
        c.execute('SELECT COUNT(distinct SONGLIST) FROM USER_SONG WHERE UID = ?',(uid,))
        totalnum = c.fetchone()
        totalnum = np.array(totalnum[0])
        print(totalnum)
        songlist_=[]

        for i in range(totalnum):
            songlistdict={}
            songlistdict["name"]=songlist[i][0]
            songlistdict["index"]= str(i+1)
            songs=[]
            # print(songlist[i][0])
            select_string = 'SELECT SONGNAME,SONGLINK,PICLINK,LRCLINK FROM SONG,USER_SONG WHERE SONGLIST = ? \
                            AND SONG.SONGID=USER_SONG.SONGID \
                                AND UID = ?'
            select_string_ = 'SELECT COUNT(SONGNAME) FROM SONG,USER_SONG WHERE SONGLIST = ? \
                                AND SONG.SONGID=USER_SONG.SONGID \
                                AND UID = ?'
            c.execute(select_string,(songlist[i][0],uid))
            song = c.fetchall()
            c.execute(select_string_,(songlist[i][0],uid))
            songnum=c.fetchone()
            songnum = np.array(songnum[0])
            for j in range(songnum):
                songdict = {}
                songdict["name"]=song[j][0]
                songdict["songurl"]=song[j][1]
                songdict["picurl"]=song[j][2]
                songdict["lrcurl"]=song[j][3]
                songdict["index"]=str(i+1)+'-'+str(j+1)
                songs.append(songdict)
            songlistdict["songs"]=songs

            songlist_.append(songlistdict)

        songlist = Db.list_to_json(self,'songlist',songlist_)
        conn.commit()
        conn.close()
        return songlist

    #建立曲库
    def build_song_db(self,musicjson):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        insert_string = 'INSERT INTO SONG(SONGID,LABEL,SINGER,SONGLINK,PICLINK,LRCLINK,SONGNAME)\
                         VALUES(?,?,?,?,?,?,?) ;'

        song = musicjson
        for i in range(len(song)):
            label = song[i]['label']
            # print(label)
            songname = song[i]['song']
            # print(songname)
            songlink = song[i]['songlink']
            # print(songlink)
            piclink = song[i]['piclink']
            # print(piclink)
            lrclink = song[i]['lrclink']
            # print(lrclink)
            songid = song[i]['songmid']
            # print(songid)
            for j in range(len(song[i]['singer'])):
               singer = '@'.join(song[i]['singer'])
            # print(singer)
            #如果发生插入错误（例如重复），跳过异常继续处理
            try:
                c.execute(insert_string,(songid,label,singer,songlink,piclink,lrclink,songname))

                # print('add song successfully')
            except BaseException:
                 pass
            continue

        conn.commit()
        conn.close()


    #播放歌单内/我喜欢的歌曲
    def play_song(self,uid,songid):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        select_string = 'SELECT PLAYCOUNT FROM USER_SONG WHERE UID= ? AND SONGID= ?'
        try:
            c.execute(select_string,(uid,songid))
        except BaseException:
            return 0

        playcount = c.fetchone()
        playcount = int(np.array(playcount[0]))+1
        # print(playcount)
        update_string = 'UPDATE USER_SONG SET PLAYCOUNT = ? WHERE UID=? AND SONGID=?'
        # print(playcount)
        try:
            c.execute(update_string,(playcount,uid,songid))
        except BaseException:
            return -1
            pass
        conn.commit()
        conn.close()
        return playcount

    #获得歌曲信息
    def get_song(self,songid):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        select_string = 'SELECT * FROM SONG WHERE SONGID= ?'
        try:
            c.execute(select_string,(songid,))
        except BaseException:
            return -1
        song = c.fetchone()
        song_info = {}
        song_info["label"] = song[1]
        song_info["singer"] = song[2]
        song_info["songurl"] = song[3]
        song_info["picurl"] = song[4]
        song_info["lrcurl"] = song[5]
        song_info["name"] = song[6]
        # print(type(song))
        song_info = Db.list_to_json(self,'song',song_info)
        conn.commit()
        conn.close()

        return song_info
    #获得用户歌曲喜好信息
    def get_user_song(self,uid):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        select_string = 'SELECT UID,SONGID FROM USER_SONG'
        try:
            c.execute(select_string)
        except BaseException:
            return -1
        res = c.fetchall()
        print(type(res))
        conn.commit()
        conn.close()
        return res

    #list转json
    def list_to_json(self,listname,infolist):
        # 构造字典
        python2json = {}
        # 构造list

        python2json[listname] = infolist

        # 转换成json字符串
        json_str = json.dumps(python2json)
        # print(type(json_str))
        return json_str

    #基于用户喜好表获得歌曲推荐
    def get_recom(self,uid):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        select_string = 'SELECT SONGID FROM USER_SONG WHERE uid = ? and PLAYCOUNT = (SELECT max(PLAYCOUNT) FROM USER_SONG WHERE uid = ?)'
        try:
            c.execute(select_string,(uid,uid))
        except BaseException:
            return -1
        res = c.fetchall()
        best_songid = res[0][0]         #获取用户听取最多的歌曲
        #print(best_songid)

        select_string = 'SELECT SONGID FROM SONG WHERE LABEL = (SELECT LABEL FROM SONG WHERE SONGID = ?)'
        try:
            c.execute(select_string,(best_songid,))
        except BaseException:
            return -1
        res=c.fetchall()
        #print(res)
        label_list=[]           #获取最多20首基于标签推荐的歌曲
        res=list(map(lambda l:l[0],res))
        res_size=len(res)
        if res_size <= 20:
            label_list=res
        else:
            label_list=random.sample(res,20)

        select_string = 'SELECT SONGID FROM SONG WHERE SINGER = (SELECT SINGER FROM SONG WHERE SONGID = ?) AND LABEL != "白噪音"'
        try:
            c.execute(select_string, (best_songid,))
        except BaseException:
            return -1
        res = c.fetchall()
        #print(res)
        singer_list = []  # 获取最多15首基于歌手推荐的歌曲
        res = list(map(lambda l: l[0], res))
        res_size = len(res)
        if res_size <= 15:
            singer_list = res
        else:
            singer_list = random.sample(res, 15)

        select_string = 'SELECT * FROM SONG WHERE LABEL != "白噪音"'
        try:
            c.execute(select_string)
        except BaseException:
            return -1
        res = c.fetchall()
        #print(res)
        rand_list = []  # 获取最多20首基于歌手推荐的歌曲
        res = list(map(lambda l: l[0], res))
        rand_list = random.sample(res, 20)
        conn.commit()
        conn.close()

        return label_list,singer_list,rand_list

    #根据标签获取歌曲id
    def get_songs_by_label(self,label):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        select_string = 'SELECT SONGID FROM SONG WHERE LABEL= ?'
        try:
            c.execute(select_string, (label,))
        except BaseException:
            return -1
        res = c.fetchall()
        res = list(map(lambda l: l[0], res))
        return res

    #基于歌曲推荐歌曲
    def get_recom_by_song(self,songid):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        select_string = 'SELECT SONGID FROM SONG WHERE LABEL = (SELECT LABEL FROM SONG WHERE SONGID = ?)'
        try:
            c.execute(select_string, (songid,))
        except BaseException:
            return -1
        res = c.fetchall()
        # print(res)
        label_list = []  # 获取最多20首基于标签推荐的歌曲
        res = list(map(lambda l: l[0], res))
        res_size = len(res)
        if res_size <= 20:
            label_list = res
        else:
            label_list = random.sample(res, 20)

        select_string = 'SELECT SONGID FROM SONG WHERE SINGER = (SELECT SINGER FROM SONG WHERE SONGID = ?)'
        try:
            c.execute(select_string, (songid,))
        except BaseException:
            return -1
        res = c.fetchall()
        # print(res)
        singer_list = []  # 获取最多15首基于歌手推荐的歌曲
        res = list(map(lambda l: l[0], res))
        res_size = len(res)
        if res_size <= 15:
            singer_list = res
        else:
            singer_list = random.sample(res, 15)
        conn.commit()
        conn.close()

        return singer_list+label_list

    def get_analysis(self, uid):
        conn = sqlite3.connect(self.db_name)
        analysis_ = {}
        c = conn.cursor()
        # select_string = 'SELECT * FROM USER_SONG where UID = ? Order by Playcount DESC'
        # c.execute(select_string,(uid,))
        # playcnt=c.fetchall()
        # print(playcnt)
        select_string = 'SELECT PLAYCOUNT,SONGNAME,SONG.SONGID FROM USER_SONG,SONG WHERE USER_SONG.SONGID=SONG.SONGID \
                        and UID= ? ORDER BY PLAYCOUNT DESC'
        c.execute(select_string, (uid,))

        fav_song = c.fetchall()
        # print(fav_song)

        song_ = {}
        # fav_song_play_count = np.array(fav_song[0])
        # fav_song = np.array(fav_song[1])
        song_["playcount"] = fav_song[0][0]
        song_["name"]= fav_song[0][1]
        analysis_["favorite_song"] = song_
        select_string = 'SELECT SUM(PLAYCOUNT),SINGER FROM USER_SONG,SONG WHERE UID = ? \
                         AND SONG.SONGID=USER_SONG.SONGID GROUP BY SINGER ORDER BY SUM(PLAYCOUNT) DESC'
        c.execute(select_string, (uid,))
        fav_singer = c.fetchall()
        singer_ = {}
        singer_["first_singer"] = fav_singer[0][1]
        singer_["second_singer"] = fav_singer[1][1]
        # print(singer_)
        analysis_["favorite_singer"] = singer_

        select_string = 'SELECT COUNT(SONGID) FROM USER_SONG WHERE UID = ? '
        c.execute(select_string, (uid,))
        sum = c.fetchone()
        analysis_["total_sum"] = sum[0]

        select_string = 'SELECT LABEL FROM USER_SONG,SONG WHERE UID = ? \
                                 AND SONG.SONGID=USER_SONG.SONGID GROUP BY LABEL ORDER BY SUM(PLAYCOUNT) DESC'
        c.execute(select_string,(uid,))
        label_=c.fetchone()
        print(label_)
        analysis_["type"]=label_[0]
        # print(analysis_)
        analysis_ = Db.list_to_json(self,'analysis', analysis_)
        conn.commit()
        conn.close()
        return analysis_