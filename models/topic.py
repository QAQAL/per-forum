from models.board import Board
from models.monbase import Monbase
from models.user import User


class Topic(Monbase):
    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            ('views', int, 0),
            ('title', str, ''),
            ('content', str, ''),
            ('user_id', int, 0),
            ('board_id', int, 0),
        ]
        return names

    @classmethod
    def get(cls, id):
        m = cls.find_by(id=id)
        m.views += 1
        m.save()
        return m

    def replies(self):
        from .reply import Reply
        ms = Reply.find_all(topic_id=self.id)
        return ms

    def board(self):
        from .board import Board
        m = Board.find(self.board_id)
        return m

    def user(self):
        from .user import User
        u = User.find(self.user_id)
        return u

    @classmethod
    def topics_for_board(cls, bid):
        ts = Topic.find_all(board_id=bid)
        return ts

    @classmethod
    def topics_for_user(cls, uid):
        ts = Topic.find_all(user_id=uid)
        return ts

    @classmethod
    def topics_reverse_order(cls, uid):
        ts = cls.topics_for_user(uid)
        ts = cls.reverse_order(ts)
        return ts

    @classmethod
    def all_topics_reverse_order(cls,ts):
        ts = cls.reverse_order(ts)
        return ts

    @classmethod
    def reverse_order(cls, ms):
        if len(ms) > 0:
            for i in range(0, len(ms)):
                k = ms[i]
                for j in range(i, len(ms)):
                    if ms[j].created_time > k.created_time:
                        ms[i], ms[j] = ms[j], ms[i]
                        k = ms[i]
        return ms