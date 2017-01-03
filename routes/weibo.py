from routes import *

from models.weibo import Weibo

main = Blueprint('weibo', __name__)


@main.route('/')
@login_required
def index(user):
    items_per_page = 20
    weibo_top = Weibo.query.filter(Weibo.id == 1).first()
    page = request.args.get('page', 1, type=int)
    p = Weibo.query.filter(Weibo.id > 1).\
        order_by(Weibo.id.desc()).\
        paginate(page, items_per_page, False)
    return render_template('weibo_index.html', user=user, top=weibo_top, p=p)
