
class WeiBoDto():

    def __init__(self,id,comments,type,time,good,comment,transfer):
        self.id = id
        self.comments = comments
        self.type = type
        self.time  = time
        self.good = good
        self.comment =  comment
        self.transfer = transfer




class WeiBoDtoPure():

    def __init__(self,id,countName,contents,time,good,comment,transfer):
        self.mid = id
        self.countName =countName
        self.contents = contents
        self.time  = time
        self.good = good
        self.comment =  comment
        self.transfer = transfer