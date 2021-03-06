from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, make_response, current_app as app
)

from datetime import datetime as dt
from .models import db, Product, User
from flaskr.auth import login_required
from datetime import datetime

bp = Blueprint('routes', __name__, url_prefix='/products')


@bp.route('/')
@login_required
def index():
    return render_template('market/index.html', products=Product.query.all())


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        brand = request.form['brand']
        validity = request.form['validity']
        error = None
        format = "%Y-%m-%d"
        existing_product = Product.query.filter(Product.name == name or Product.brand == brand).first()

        if not name or not validity:
            error = 'Name is required.'
        else:
            validity = datetime.strptime(validity, format)

        if existing_product:
            error = 'Product {} is already registered.'.format(name)

        if error is None:
            new_product = Product(name=name,
                                  quantity=quantity,
                                  brand=brand,
                                  validity=validity)
            db.session.add(new_product)  # Adds new Product record to database
            db.session.commit()  # Commits all changes
            return redirect(url_for('routes.index'))

        flash(error)

    return render_template('market/create.html')


def get_product(id):
    product = Product.query.filter(Product.id == id).first()

    if product is None:
        abort(404, "Product id {0} doesn't exist.".format(id))

    return product


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_product(id)
    Product.query.filter(Product.id == id).delete()
    db.session.commit()
    return redirect(url_for('routes.index'))


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    product = get_product(id)

    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        brand = request.form['brand']
        validity = request.form['validity']
        error = None
        format = "%Y-%m-%d"
        existing_product = Product.query.filter(Product.name == name or Product.brand == brand).first()

        if not name or not validity:
            error = 'Name and validity is required.'
        else:
            validity = datetime.strptime(validity, format)

        if error is not None:
            flash(error)
        else:
            product.name = name
            product.quantity = quantity
            product.brand = brand
            product.validity = validity
            db.session.commit()
            return redirect(url_for('routes.index'))

    return render_template('market/update.html', product=product)
