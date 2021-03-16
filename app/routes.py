from flask import render_template, flash, redirect, url_for, request, make_response, jsonify
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, LoginManager, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from werkzeug.datastructures import ImmutableOrderedMultiDict
import requests
import stripe



@app.route('/')
@app.route('/index')
def index():
    
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():

    # checks the user is logged in, if they are; user is redirected to the
    # to the index page

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    """form.validate_on_submit() returns False if any login fields are incorrect
    and redirects to the login page for resubmission, return True and the user 
    is logged in returning to the homepage"""

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/shop')
def shop():

    return render_template('shop.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/shop/cow_mask')
def purchase_cow():
    return render_template('purchase_cow.html')

@app.route('/shop/boob_mask')
def purchase_boob():
    return render_template('purchase_boob.html')

@app.route('/shop/dino_bag')
def purchase_dino():
    return render_template('purchase_dino.html')

@app.route('/shop/strawb_bag')
def purchase_strawb():
    return render_template('purchase_strawb.html')

@app.route('/shop/cherry_bag')
def purchase_cherry():
    return render_template('purchase_cherry.html')

@app.route('/shop/cherry_mask')
def purchase_cherrymask():
    return render_template('purchase_cherrymask.html')

@app.route('/shop/cat_bag')
def purchase_cat():
    return render_template('purchase_cat.html')





#-------- Stripe integration --------#

stripe.api_key = 'sk_test_51IUK8nJ1H5PF7POC8XHabS6WepwvaXjKYPHZmK1Sae0ErRP2hOLzk9seadB0YlvlUoTdJNg32uciVWkpAKmC0si000xhOni4o6'

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'gbp',
                        'unit_amount': 500,
                        'product_data': {
                            'name': 'Boob Print Face Mask',
                            #TODO: Change to display the image of the item you are buying rather than hardcoded 
                            #image link. Use Jinja templating probably. 
                            'images': ['https://i.imgur.com/EHyR2nP.png'],
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='http://127.0.0.1:5000' + '/success',
            cancel_url='http://127.0.0.1:5000'+ '/cancel',
        )
        return jsonify({'id': checkout_session.id})
    except Exception as e:
        return jsonify(error=str(e)), 403

@app.route('/success')
def payment_success():
    return render_template('success.html')

@app.route('/cancel')
def payment_cancel():
    return render_template('cancel.html')





if __name__=='__main__':
    app.run(debug=True)
