from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from models.reply import Reply
from models.topic import Topic
from models.board import Board
from routes import *


main = Blueprint('admin', __name__)


@main.route("/")
def index():
    u = current_user()
    if u.username == 'admin':
        ts = Topic.topics_reverse_order(u.id)
        r = Reply.find_all(user_id=u.id)
        rt = remove_repeat(r)
        return render_template('admin/index.html', user=u, topic=ts, rt=rt)


@main.route("/manage_board")
def manage_board():
    u = current_user()
    bs = Board.all()
    if u.username == 'admin':
        return render_template('admin/manage_board.html', bs=bs, administrator=u)


@main.route("/manage_setting")
def manage_setting():
    user_id = int(request.args.get('id'))
    user = User.find(user_id)
    administrator = current_user()
    return render_template('admin/setting.html', user_id=user_id, user=user, administrator=administrator)


@main.route("/manage_topic")
def manage_topic():
    user_id = int(request.args.get('id'))
    print('用户id是', user_id, type(user_id))
    ts = Topic.topics_reverse_order(user_id)
    user = User.find(user_id)
    u = current_user()
    if u.username == 'admin':
        return render_template('admin/manage_topic.html', ts=ts, user=user, administrator=u)


@main.route("/manage_user")
def manage_user():
    us = User.all()
    administrator = current_user()
    return render_template('admin/manage_user.html', us=us, administrator=administrator)


@main.route("/board_add", methods=["POST"])
def board_add():
    form = request.form
    u = current_user()
    Board.new(form)
    return redirect(url_for('admin.manage_board'))


@main.route("/board_delete")
def board_delete():
    board_id = int(request.args.get('id'))
    u = current_user()
    if u.username == 'admin':
        # print('删除的board_id是', board_id, type(board_id))
        Board.delete(board_id)
        delete_topics_for_board(board_id)

    bs = Board.all()
    return render_template('admin/manage_board.html', bs=bs, administrator=u)


@main.route("/user_delete")
def user_delete():
    user_id = int(request.args.get('id'))
    u = current_user()
    if u.username == 'admin':
        # print('删除的用户id是', user_id, type(user_id))
        User.delete(user_id)
        delete_topics_for_user(user_id)
        delete_replys_for_user(user_id)

    return redirect(url_for('.manage_user'))


@main.route("/topic_delete")
def topic_delete():
    topic_id = int(request.args.get('id'))
    t = Topic.find(topic_id)
    user_id = t.user().id
    u = current_user()
    if u.username == 'admin':
        print('删除的帖子id是', topic_id, type(topic_id))
        Topic.delete(topic_id)

    ts = Topic.topics_reverse_order(user_id)
    user = User.find(user_id)
    return render_template('admin/manage_topic.html', ts=ts, user=user)


@main.route("/setting_info", methods=["POST"])
def setting_info():
    user_id = int(request.args.get('user_id'))
    u = User.find(user_id)
    form = request.form
    u.signature = form.get('signature')
    u.username = form.get('username')
    u.save()
    return redirect(url_for('.manage_setting', signature=u.signature, username=u.username))


@main.route("/setting_changing_password", methods=["POST"])
def setting_changing_password():
    form = request.form
    user_id = int(form.get('user_id'))
    u = User.find(user_id)

    new_password = form.get('new_pass', u.password)
    administrator = current_user()
    u.password = u.salted_password(new_password)
    u.save()
    return render_template('admin/setting.html', user_id=user_id, user=u, administrator=administrator)


