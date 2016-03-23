from flask import Flask, render_template, request, flash, url_for, redirect, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurant/')
@app.route('/restaurants/')
def show_restaurant():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurant.html', restaurants=restaurants)


@app.route('/restaurant/new/', methods=['GET', 'POST'])
def new_restaurant():
    if request.method == 'POST':
        restaurant = Restaurant(name=request.form['name'])
        session.add(restaurant)
        session.commit()
        flash("New restaurant created!")
        return redirect(url_for('show_restaurant'))
    else:
        return render_template('new_restaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def edit_restaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        restaurant.name = request.form['name']
        session.add(restaurant)
        session.commit()
        flash("Restaurant successfully edited!")
        return redirect(url_for('show_restaurant'))
    else:
        return render_template('edit_restaurant.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def delete_restaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['confirmation'] == "Yes":
            session.delete(restaurant)
            session.commit()
            flash("Restaurant successfully deleted!")
            return redirect(url_for('show_restaurant'))
        if request.form['confirmation'] == "No":
            flash("Deletion cancelled!")
            return redirect(url_for('show_restaurant'))
    else:
        return render_template('delete_restaurant.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def show_menu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return render_template('menu.html', restaurant=restaurant, items=items)


@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def new_menu_item(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        new_item = MenuItem(name=request.form['name'],price=request.form['price'],course=request.form['course'],
                            description=request.form['description'], restaurant_id=restaurant.id)
        session.add(new_item)
        session.commit()
        flash("Menu item created!")
        return redirect(url_for('show_menu', restaurant_id=restaurant.id))
    else:
        return render_template('new_menu_item.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET', 'POST'])
def edit_menu_item(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).filter_by(id=menu_id).one()
    if request.method == 'POST':
        item.name=request.form['name']
        item.price=request.form['price']
        item.course=request.form['course']
        item.description=request.form['description']
        session.add(item)
        session.commit()
        flash("Menu item successfully edited!")
        return redirect(url_for('show_menu', restaurant_id=restaurant.id))
    else:
        return render_template('edit_menu_item.html', restaurant=restaurant, item=item)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET', 'POST'])
def delete_menu_item(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['confirmation'] == "Yes":
            session.delete(item)
            session.commit()
            flash("Menu item successfully deleted!")
            return redirect(url_for('show_menu', restaurant_id=restaurant.id))
        if request.form['confirmation'] == "No":
            flash("Deletion cancelled!")
            return redirect(url_for('show_menu', restaurant_id=restaurant.id))
    else:
        return render_template('delete_menu_item.html', restaurant=restaurant, item=item)


@app.route('/restaurant/JSON/')
@app.route('/restaurants/JSON/')
def restaurants_json():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurant=[r.serialize for r in restaurants])

@app.route('/restaurant/<int:restaurant_id>/JSON/')
@app.route('/restaurant/<int:restaurant_id>/menu/JSON/')
def menu_JSON(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItem=[i.serialize for i in items])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def item_JSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).filter_by(id=menu_id).one()
    return jsonify(MenuItem=item.serialize)


if __name__ == '__main__':
    app.secret_key = 'unsecure_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
