from flask import session
from models.reply import Reply
from models.topic import Topic
from models.user import User


def current_user():
    uid = session.get('user_id', '')
    u = User.find_by(id=uid)
    return u


def valid_suffix(suffix):
    valid_type = ['jpg', 'png', 'jpeg']
    return suffix in valid_type


def remove_repeat(d):
    topic_id = set()
    for i in d:
        topic_id.add(i.topic_id)
    rt = []
    for id in topic_id:
        m = Topic.find(id)
        if m is not None:
            rt.append(m)
    return rt


def delete_topics_for_board(id):
    ts = Topic.topics_for_board(id)
    for t in ts:
        Topic.delete(t.id)
        delete_replys_for_topic(t.id)


def delete_topics_for_user(id):
    ts = Topic.topics_for_user(id)
    for t in ts:
        Topic.delete(t.id)
        delete_replys_for_topic(t.id)


def delete_replys_for_user(id):
    rs = Reply.replys_for_user(id)
    for r in rs:
        Reply.delete(r.id)


def delete_replys_for_topic(id):
    rs = Reply.replys_for_topic(id)
    for r in rs:
        Topic.delete(r.id)


def topic_by_board(board_id):
    if board_id == -1:
        ts = Topic.all()
    else:
        ts = Topic.find_all(board_id=board_id)
    ts = Topic.all_topics_reverse_order(ts)
    return ts