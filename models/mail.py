from models.monbase import Monbase
from utils import log


class Mail(Monbase):
    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            ('title', str, ''),
            ('content', str, ''),
            ('sender_id', int, 0),
            ('receiver_id', int, 0),
            ('read', bool, False),
        ]
        return names

    def mark_read(self):
        self.read = True
        self.save()

    @classmethod
    def received_mails_reverse_order(cls, id):
        ms = cls.find_all(receiver_id=id)
        ms = cls.reverse_order(ms)
        return ms

    @classmethod
    def send_mails_reverse_order(cls, id):
        ms = cls.find_all(sender_id=id)
        log('type(ms)', type(ms), ms)
        ms = cls.reverse_order(ms)
        return ms

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
