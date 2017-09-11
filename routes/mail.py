from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import *
from models.mail import Mail
from utils import log

main = Blueprint('mail', __name__)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    receiver_name = form['receiver_name']
    receiver = User.find_by(username=receiver_name)
    # JSON.stringify(form)
    form = {key: dict(form)[key][0] for key in dict(form)}
    form['receiver_id'] = receiver.id
    del form['receiver_name']
    u = current_user()
    Mail.new(form, sender_id=u.id)
    return redirect(url_for("mail.index"))


@main.route("/", methods=["GET"])
def index():
    u = current_user()
    send_mail = Mail.send_mails_reverse_order(u.id)
    received_mail = Mail.received_mails_reverse_order(u.id)
    t = render_template(
        "mail/index.html",
        sends=send_mail,
        receives=received_mail,
        user=u
    )
    return t


@main.route("/view/<int:id>")
def view(id):
    mail = Mail.find(id)
    sender = User.find(mail.sender_id).username
    receiver = User.find(mail.receiver_id).username
    # 不是你自己收发的，你肯定不能看
    # 不是收的人，那你看了也不会变成已读
    user = current_user()
    if user.id == mail.receiver_id:
        mail.mark_read()
    if user.id in [mail.receiver_id, mail.sender_id]:
        return render_template("mail/detail.html", mail=mail, user=user, sender=sender, receiver=receiver)
    else:
        return redirect(url_for(".index"))


