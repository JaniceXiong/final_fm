import db_operation
import random
import json
import song

class Recom:
    uid=''

    #初始化推荐工具类对象
    def __init__(self,uid):
        self.uid=uid
        print('Recom init success')

    def load_matrix(self):  # 加载原始数据
        matrix = {}  # 生成二维喜好矩阵
        da = db_operation.Db('fm.db')
        user_song = da.get_user_song(self.uid)

        return user_song

    def sim_distance(self,matrix, row1, row2):  # 计算用户相似度

        song_list = []  # 获取歌曲单
        for i in matrix:
            if i[1] not in song_list:
                song_list.append(i[1])

        sim = 0.0  # 相似度

        for s in song_list:  # 计算用户相似度
            if (row1, s) in matrix and (row2, s) in matrix:
                sim = sim + 1

        ##改进后的归一化处理，实现用户的去中心化
        ##表现在有些人的喜欢歌单非常庞大，他的权重要相对小一些
        normal_fac = 0
        for item in matrix:
            if item[0] == row1 or item[0] == row2:
                normal_fac += 1

        return sim / normal_fac

    def top_match(self,matrix, row):  # 找出最相似用户
        user_list = []
        for item in matrix:
            if item[0] not in user_list:
                user_list.append(item[0])

        scores = [(self.sim_distance(matrix, row, r), r) for r in user_list if r != row]
        scores.sort()
        scores.reverse()

        return scores

    def get_recommendation(self,matrix, row):
        rows = set(map(lambda l: l[0], matrix))  # 获取所有用户信息
        columns = set(map(lambda l: l[1], matrix))  # 获取所有歌曲信息

        sum_of_sim = 0.0  # 用相似度总和平衡推荐信息
        scores = self.top_match(matrix, row)
        for item in scores:
            sum_of_sim += item[0]
        # print(sum_of_sim)

        recom_list = []

        for s in columns:
            s_recom = 0
            if (row, s) not in matrix:
                for item in scores:
                    if (item[1], s) in matrix:
                        s_recom += item[0]
                recom_list.append((s_recom / sum_of_sim, s))

        recom_list.sort()
        recom_list.reverse()

        return recom_list


    def get_recommendations(self):
        da = db_operation.Db('fm.db')
        return da.get_recom(self.uid)

    def get_one_song(self):
        user_song = self.load_matrix()
        recom_list=self.get_recommendation(user_song,self.uid)    #针对当前用户生成协同过滤推荐列表
        recom_ans = []
        # recom_ans.append(recom_list[0][1])
        song1=song.Song()
        song1.set_songid(recom_list[0][1])
        song1.get_details_from_songid()
        song_info={}
        song_info["label"] = song1.label
        song_info["singer"] = song1.singer
        song_info["songurl"] = song1.songurl
        song_info["picurl"] = song1.picurl
        song_info["lrcurl"] = song1.lrcurl
        song_info["name"] = song1.name
        song_info["songid"] = song1.songid
        recom_ans.append(song_info)
        return recom_ans


    def get_songs(self):            #推荐约80首歌
        user_song = self.load_matrix();
        recom_list = self.get_recommendation(user_song,self.uid)    #针对当前用户生成协同过滤推荐列表
        label_list, singer_list, rand_list=self.get_recommendations()
        recom_list=[l[1] for l in recom_list if l[0] != 0]
        if len(recom_list) >=30:
            recom_list=random.sample(recom_list,30)
        recom_tem = list(set(recom_list+label_list+singer_list+rand_list))
        song1 = song.Song()
        recom_ans = []
        for i in range(len(recom_tem)):
            song1 = song.Song()
            song1.set_songid(recom_tem[i])
            song1.get_details_from_songid()
            song_info = {}
            song_info["label"] = song1.label
            song_info["singer"] = song1.singer
            song_info["songurl"] = song1.songurl
            song_info["picurl"] = song1.picurl
            song_info["lrcurl"] = song1.lrcurl
            song_info["name"] = song1.name
            song_info["songid"] = song1.songid
            recom_ans.append(song_info)
        return recom_ans

    def get_white_noise_songs(self):
        da = db_operation.Db('fm.db')
        recom_tem = da.get_songs_by_label("白噪音")
        song1 = song.Song()
        recom_ans = []
        for i in range(len(recom_tem)):
            song1 = song.Song()
            song1.set_songid(recom_tem[i])
            song1.get_details_from_songid()
            song_info = {}
            song_info["label"] = song1.label
            song_info["singer"] = song1.singer
            song_info["songurl"] = song1.songurl
            song_info["picurl"] = song1.picurl
            song_info["lrcurl"] = song1.lrcurl
            song_info["name"] = song1.name
            song_info["songid"] = song1.songid
            recom_ans.append(song_info)
        recom_ans = random.sample(recom_ans,50)
        return recom_ans

    def get_one_by_like(self,songid):
        da = db_operation.Db('fm.db')
        da.add_to_songlist(self.uid,songid,"我喜欢")
        recom_ans = self.get_one_song()
        rec_song = da.get_recom_by_song(songid)
        #rec_song = random.sample(rec_song,1)
        siz = len(rec_song)
        new_rec=rec_song[int(siz/2)]
        rec_song = new_rec
        song1 = song.Song()
        song1.set_songid(rec_song)
        song1.get_details_from_songid()
        song_info = {}
        song_info["label"] = song1.label
        song_info["singer"] = song1.singer
        song_info["songurl"] = song1.songurl
        song_info["picurl"] = song1.picurl
        song_info["lrcurl"] = song1.lrcurl
        song_info["name"] = song1.name
        song_info["songid"] = song1.songid
        recom_ans.append(song_info)
        return recom_ans





