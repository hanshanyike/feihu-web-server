from mp_feihu.extensions import db

# Models
class AddInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mailaddress = db.Column(db.String)
    address = db.Column(db.String)
    phone = db.Column(db.String)
    hobby = db.Column(db.String)

    # optional
    def __repr__(self):
        return '<Note %r>' % self.phone