import os
import uuid

from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
    abort,
    send_from_directory)

from models.board import Board
from models.reply import Reply
from models.topic import Topic
from models.user import User
from routes import *
from utils import log


main = Blueprint('index', __name__)


@main.route("/")
def index():
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        ms = Topic.all()
    else:
        ms = Topic.find_all(board_id=board_id)
    bs = Board.all()
    return render_template("visit/index.html", ms=ms, bs=bs, bid=board_id,)


@main.route('/<int:id>')
def detail(id):
    m = Topic.get(id)
    # 传递 topic 的所有 reply 到 页面中
    board_id = int(request.args.get('board_id', -1))
    u = m.user()
    return render_template("visit/detail.html", topic=m, bid=board_id, user=u)


@main.route('/author')
def author_detail():
    user_id = int(request.args.get('id'))
    u = User.find(user_id)
    ts = Topic.topics_reverse_order(user_id)
    r = Reply.find_all(user_id=user_id)
    rt = remove_repeat(r)

    if u is None:
        abort(404)
    else:
        return render_template('visit/author.html', user=u, topic=ts, rt=rt)


@main.route("/user_login")
def user_login():
    return render_template("login.html")


@main.route("/register", methods=['POST'])
def register():
    form = request.form
    # 用类函数来判断
    u = User.register(form)
    notice = '注册成功'
    if u is None:
        notice = '用户名输入有误或已存在'
    return render_template("login.html", n1=notice)


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)

    if u is None:
        # 转到 topic.index 页面
        notice = '用户名或密码不正确'
        return render_template("login.html", n2=notice)
    else:
        # session 中写入 user_id
        session['user_id'] = u.id
        # 设置 cookie 有效期为 永久
        session.permanent = True
        return redirect(url_for('topic.index'))


@main.route('/user/<username>')
def user_detail(username):
    u = User.find_by(username=username)
    ts = Topic.topics_reverse_order(u.id)
    r = Reply.find_all(user_id=u.id)
    rt = remove_repeat(r)
    cu = current_user()

    if u is None:
        abort(404)
    else:
        return render_template('user/user_detail.html', user=u, topic=ts, rt=rt, current_user=cu)


@main.route('/image/add', methods=['POST'])
def add_img():
    u = current_user()
    file = request.files['avatar']
    suffix = file.filename.split('.')[-1]
    if valid_suffix(suffix):
        filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
        file.save(os.path.join('user_image', filename))
        u.user_image = '/uploads/' + filename
        u.save()
    return redirect(url_for('.user_detail', username=u.username))


@main.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory('user_image', filename)


@main.route('/image/<filename>')
def image(filename):
    return send_from_directory('image', filename)


@main.route("/setting")
def setting():
    u = current_user()
    return render_template('user/setting.html', user=u, user_id=u.id)


@main.route("/setting_user_sig", methods=["POST"])
def setting_user_sig():
    u = current_user()
    form = request.form
    u.signature = form.get('signature')
    u.username = form.get('username')
    u.save()
    return redirect(url_for('.setting'))


@main.route("/changing_password", methods=["POST"])
def changing_password():

    u = current_user()
    form = request.form
    new_password = form.get('new_pass', u.password)
    old_password = form.get('old_pass')

    if u is not None and u.password == u.salted_password(old_password):
        u.password = u.salted_password(new_password)
    u.save()
    return redirect(url_for('.setting', old_pass=old_password, new_pass=new_password))


@main.route('/attack')
def attack():
    # xss 攻击的后台
    cookie = request.args.get('cookie')
    log('cookie', cookie)