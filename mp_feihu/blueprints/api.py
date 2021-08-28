import json
from flask import request, Blueprint ,make_response
from mp_feihu.models import AddInfo
from mp_feihu.extensions import db
api_bp = Blueprint('api', __name__)



@api_bp.route('/')
def index():
    #return render_template('index.html')
    return ("首页")

@api_bp.route('/addinfo', methods=['POST'])
def new_AddInfo():
    data = json.loads(request.get_data().decode("utf-8"))
    if data and request.method == 'POST':
        addinfo = AddInfo(mailaddress=data['mailaddress'],address=data['address'],phone=data['phone'],hobby=data['hobby'])
        db.session.add(addinfo)
        db.session.commit()
        return make_response("add success")