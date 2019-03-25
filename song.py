import db_operation
import json

class Song:
    songid = ''
    label = ''
    singer = ''
    songurl = ''
    picurl = ''
    lrcurl = ''
    name = ''


    def set_songid(self,songid):
        self.songid=songid

    def get_details_from_songid(self):
        da = db_operation.Db('fm.db')
        details=json.loads(da.get_song(self.songid))
        self.label=details["song"]["label"]
        self.name=details["song"]["name"]
        self.lrcurl=details["song"]["lrcurl"]
        self.picurl=details["song"]["picurl"]
        self.singer=details["song"]["singer"]
        self.songurl=details["song"]["songurl"]


