import uuid

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    abort,
)

from models.topic import Topic
from models.board import Board
from routes import current_user, topic_by_board


main = Blueprint('topic', __name__)


csrf_tokens = dict()


@main.route("/")
def index():
    board_id = int(request.args.get('board_id', -1))
    ts = topic_by_board(board_id)
    u = current_user()
    token = str(uuid.uuid4())
    csrf_tokens[token] = u.id
    bs = Board.all()

    return render_template("topic/index.html", ts=ts, token=token, bs=bs, bid=board_id, user=u, current_user=u)


@main.route('/back_index')
def back_index():
    u = current_user()
    if u is None:
        return redirect(url_for('index.index'))
    else:
        return redirect(url_for('.index'))


@main.route('/<int:id>')
def detail(id):
    t = Topic.get(id)
    print('t.created_time', t.created_time)
    # 传递 topic 的所有 reply 到 页面中
    u = current_user()
    board_id = int(request.args.get('board_id', -1))
    return render_template("topic/detail.html", topic=t, user=u, bid=board_id)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()
    token = request.args.get('token')

    if token in csrf_tokens and csrf_tokens[token] == u.id:
        csrf_tokens.pop(token)
        m = Topic.new(form, user_id=u.id)
        return redirect(url_for('.detail', id=m.id))
    else:
        abort(401)


@main.route("/delete")
def delete():
    id = request.args.get('id')
    token = request.args.get('token')
    u = current_user()
    # print('删除 topic 用户是', u, id)
    # 判断 token 是否是我们给的

    if token in csrf_tokens and csrf_tokens[token] == u.id:
        csrf_tokens.pop(token)
        print('删除 topic 用户是', u, id)
        Topic.delete(id)
        return redirect(url_for('.index'))
    else:
        abort(403)


@main.route("/new")
def new():
    board_id = int(request.args.get('board_id'))
    token = new_csrf_token()
    bs = Board.all()
    u = current_user()
    return render_template("topic/new.html", bs=bs, token=token, bid=board_id, user=u)


def new_csrf_token():
    u = current_user()
    token = str(uuid.uuid4())
    csrf_tokens[token] = u.id
    return token
