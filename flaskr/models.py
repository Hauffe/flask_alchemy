from . import db


class Product(db.Model):
    """Data model for 'produtos'"""

    __tablename__ = 'products'
    id = db.Column(db.Integer,
                        primary_key=True)
    name = db.Column(db.String(80),
                        index=False,
                        unique=True,
                        nullable=False)
    quantity = db.Column(db.Integer,
                        index=False,
                        unique=False,
                        nullable=False)
    brand = db.Column(db.String(80),
                        index=False,
                        unique=False,
                        nullable=False)
    validity = db.Column(db.DateTime,
                        index=False,
                        unique=False,
                        nullable=True)

    def __repr__(self):
        return '<Produto {}>'.format(self.name)
