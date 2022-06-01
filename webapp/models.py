from . import db 

class Prices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_search = db.Column(db.String(300))
    link_picture = db.Column(db.String(100))
    product_name = db.Column(db.String(200))
    product_price = db.Column(db.String(100))
    