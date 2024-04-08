# from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import func
# from sqlalchemy import or_
# db = SQLAlchemy()


# class Product(db.Model):
#     product_id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.VARCHAR(100), nullable=False)
#     description = db.Column(db.Text, nullable=False)
#     price = db.Column(db.DECIMAL(10,2), nullable=False)
#     image = db.Column(db.VARCHAR(100),nullable=False)
#     category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)