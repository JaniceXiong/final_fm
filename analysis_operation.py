import db_operation

class Analy:
    uid = ''
    favorite_singer = ''
    favorite_label = ''
    tot_like_num = 0

    def init(self,uid):
        self.uid = uid

    def get_analysis(self):
        da = db_operation.Db('fm.db')
        return da.get_analysis(self.uid)