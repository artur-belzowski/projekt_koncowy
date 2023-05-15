from flask import Flask
from flask import render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask import session
from collection import Collection
from get_nft_data import get_nft_data
from floor_price_minted import get_floor_price_minted
from ebisus import get_nfts_ebisus

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'nbiwbfui98523h8we34ty98wt8w#$%@MN$#NBJ^%$#@HBB'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        user = User.query.filter_by(username=username).first()
        if user:
            message = 'Użytkownik o takiej nazwie już istnieje.'
            return render_template('register.html', message=message)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    collections = Collection.get_collections()
    change24 = collections[0].change24
    reward_points = collections[0].reward_points
    floor_price = collections[0].floor_price
    return render_template('index.html', collections=collections, change24=change24, reward_points=reward_points, floor_price=floor_price)


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.session.query(User.id).filter_by(username=username).first()
        if user:
            session['user_id'] = user[0] 
            return redirect(url_for('index'))
        else:
            error = 'Nieprawidłowa nazwa użytkownika lub hasło'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')


@app.before_request
def before_request():
    if 'user_id' not in session and request.endpoint not in ['login', 'register', 'index', 'collection', 'logout']:
        return redirect(url_for('login'))


@app.route('/wallet')
def wallet():
    return render_template('wallet.html')


@app.route('/ebisus', methods=['GET', 'POST'])
async def ebisus():
    wallet = request.form.get("wallet")
    session = {}
    if wallet:
        session["wallet"] = wallet
    else:
        wallet = session.get("wallet")
    if not wallet:
        return redirect(url_for("index"))
    nfts_ebisus, suma = await get_nfts_ebisus(wallet)
    return render_template('ebisus.html', wallet=wallet, nfts_ebisus=nfts_ebisus, suma=suma)


@app.route('/minted')
def minted():
    suma, nfts_minted = get_floor_price_minted()
    return render_template('minted.html', nfts_minted=nfts_minted, suma=suma)


@app.route('/<collection_name>/')
def floor_price(collection_name):
    if collection_name == 'logout':
        return redirect(url_for('logout'))
    elif collection_name == 'ebisus':
        return redirect(url_for('ebisus'))
    else:
        nft_data = get_nft_data(collection_name)
        return render_template('collection.html', collection_name=collection_name, nft_data=nft_data)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
