from models.monbase import Monbase


class Reply(Monbase):
    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            ('content', str, ''),
            ('topic_id', int, 0),
            ('user_id', int, 0),
        ]
        return names

    def user(self):
        from .user import User
        u = User.find(self.user_id)
        return u

    def topic(self):
        from .topic import Topic
        t = Topic.find(self.topic_id)
        return t


    @classmethod
    def replys_for_user(cls, uid):
        rs = cls.find_all(user_id=uid)
        return rs


    @classmethod
    def replys_for_topic(cls, tid):
        rs = cls.find_all(topic_id=tid)
        return rs