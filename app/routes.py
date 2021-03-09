from flask import render_template, flash, redirect, url_for, request, make_response
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, LoginManager, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from werkzeug.datastructures import ImmutableOrderedMultiDict
import requests


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

#-------- Paypal integration --------#

@app.route('/purchase')
def purchase():
    try:
        return render_template('purchase.html')
    except Exception as e:
        return(str(e))

@app.route('/success')
def success():
    try:
        return render_template("success.html")
    except Exception as e:
        return(str(e))

@app.route('/ipn/',methods=['POST'])
def ipn():
    try:
        arg = ''
        request.parameter_storage_class = ImmutableOrderedMultiDict
        values = request.form
        for x, y in values.iteritems():
            arg += "&{x}={y}".format(x=x,y=y)

        validate_url = 'https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_notify-validate{arg}.format(arg=arg)'
        r = requests.get(validate_url)
        if r.text == 'VERIFIED':
            try:
                payer_email =  thwart(request.form.get('payer_email'))
                unix = int(time.time())
                payment_date = thwart(request.form.get('payment_date'))
                username = thwart(request.form.get('custom'))
                last_name = thwart(request.form.get('last_name'))
                payment_gross = thwart(request.form.get('payment_gross'))
                payment_fee = thwart(request.form.get('payment_fee'))
                payment_net = float(payment_gross) - float(payment_fee)
                payment_status = thwart(request.form.get('payment_status'))
                txn_id = thwart(request.form.get('txn_id'))
            except Exception as e:
                with open('/tmp/ipnout.txt','a') as f:
                    data = 'ERROR WITH IPN DATA\n'+str(values)+'\n'
                    f.write(data)
            
            with open('/tmp/ipnout.txt','a') as f:
                data = 'SUCCESS\n'+str(values)+'\n'
                f.write(data)

            c,conn = connection()
            c.execute("INSERT INTO ipn (unix, payment_date, username, last_name, payment_gross, payment_fee, payment_net, payment_status, txn_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (unix, payment_date, username, last_name, payment_gross, payment_fee, payment_net, payment_status, txn_id))
            conn.commit()
            c.close()
            conn.close()
            gc.collect()

        else:
            with open('/tmp/ipnout.txt','a') as f:
                data = 'FAILURE\n'+str(values)+'\n'
                f.write(data)
                
        return r.text
    except Exception as e:
        return str(e)



if __name__=='__main__':
    app.run(debug=True)
