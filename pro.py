#website of 4 products..
from flask import Flask, jsonify, request, url_for, redirect, session, render_template, g
import sqlite3

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template('first.html')

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    return render_template('sign_in.html')

@app.route('/processed', methods=['GET', 'POST'])
def processed():

	name = request.form['name']
	location = request.form['location']
	ter = 0
	if name == "" or location == "":		
		ter = 1.95
		return render_template('sign_in.html', ter=ter)

	db = get_db()
	cur = db.execute('select id, first_name, second_name, location, password from userdetails')
	results = cur.fetchall()
	cursor = db.execute("select id from userdetails where second_name == ?", [name])
	acc_id = cursor.fetchone()

	for row in results:
	    if row[2] == name and row[4] == location:
	    	acc_no = acc_id[0] 
	    	return render_template('welcome.html', name=name, logged=True, results=results, acc_no=acc_no)

	return render_template('sign_in.html', ter=ter)

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        return render_template('sign_up.html')
    return render_template('sign_up.html')

@app.route('/form_details', methods=['GET', 'POST'])
def form_details():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        first_name = request.form['first_name']
        second_name = request.form['second_name']
        location = request.form['location']
        password = request.form['password']
        
        db = get_db()
        db.execute('insert into userdetails (first_name, second_name, location, password) values (?, ?, ?, ?)', [first_name, second_name, location, password])
        db.commit()
        
        return redirect(url_for('sign_in'))

@app.route('/logout', methods=[ 'POST'])
def logout():
	return render_template('logout.html')

@app.route('/runhome', methods=['GET', 'POST'])
def runhome():
    if request.method == 'GET':
        return render_template('first.html')
    return render_template('first.html')

@app.route('/elec', methods=[ 'GET','POST'])
def elec():
	acc_no = request.args.get('acc_no')
	db = get_db()
	cur = db.execute('select id, name, cost, img_key from price')
	results = cur.fetchall()
		
	return render_template('electronics.html', display=True , results=results, acc_no=acc_no)

@app.route('/non_elec', methods=[ 'GET', 'POST'])
def non_elec():
	acc_no = request.args.get('acc_no')
	db = get_db()
	cur = db.execute('select id, name, cost, img_key from price')
	results = cur.fetchall()

	return render_template('essentials.html', display=True , results=results, acc_no=acc_no)

#--------------Fn to append to a table called cart-------------------------------- 
@app.route('/cart', methods=[ 'GET', 'POST'])
def cart():
	game_id = request.args.get("id")
	acc_no = request.args.get('acc_no')
	db = get_db()

	acc_game = []
	abc = 0
	de = 0

	cur = db.execute('select acc_id,game_id from cart')
	acc_games = cur.fetchall()

	if int(game_id) == -1:
		de = 1

	for row in acc_games:
		if row[0] == int(acc_no) :
			if row[1] == int(game_id):
				game_id = 0
				abc = 1.5
	
	db.execute("insert into cart(acc_id,game_id) values (? ,?)", [acc_no, game_id])
	db.commit()
	cursor = db.execute('select id,name,cost,img_key from price')
	games = cursor.fetchall()

	cur = db.execute('select acc_id,game_id from cart')
	acc_game = cur.fetchall()

	games_cart = []

	for row in acc_game:
	    if row[0] == int(acc_no):
	        for game in games:
	            if game[0] == row[1] :	            
	                games_cart.append(game)
	        
	total = 0
	for g in games_cart:
	    total += int(g[2])

	return render_template('cart.html', display=True, total=total, de=de,abc=abc,games_cart=games_cart, acc_no=acc_no, acc_game=acc_game)

@app.route('/delete_item', methods=['GET', 'POST'])
def delete_item():
    game_id = request.args.get('id')
    acc_no = request.args.get('acc_no')

    db = get_db()
    cur = db.execute('select acc_id,game_id from cart')
    acc_games = cur.fetchall()

    for row in acc_games:
     if row[0] == int(acc_no):
      if row[1] == int(game_id):	
       db.execute('delete from cart where game_id = ?', [game_id])
       db.commit()

    cursor = db.execute('select id,name,cost,img_key from price')
    games = cursor.fetchall()

    cur = db.execute('select acc_id,game_id from cart')
    acc_game = cur.fetchall()
    games_cart = []

    for row in acc_game:
        if row[0] == int(acc_no):
            for game in games:
                if game[0] == row[1] :
                    games_cart.append(game)

    total = 0
    for g in games_cart:
        total += int(g[2])     

    return render_template('delete.html', display=True, total=total, games_cart=games_cart, acc_no=acc_no)

#---------------------------------------------------------------------------------------------
#------------------------------------end of pgm-------------------------------------------------
#----------------------------function to add new items to the DB...----------------------------

@app.route('/itemadd', methods=['GET', 'POST'])
def itemadd():
    if request.method == 'GET':
        return render_template('add_items.html')
    else:
        item = request.form['name']
        cost = request.form['cost']
        img_key = request.form['img_key']
       
        db = get_db()
        db.execute('insert into price (name, cost, img_key) values (?, ?, ?)', [item, cost, img_key])
        db.commit()

        return ('Item added successfully!')
       
@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
	return render_template('admin_sign_in.html')

@app.route('/add_item_admin', methods=['GET', 'POST'])
def add_item_admin():
	name = request.form['name']
	location = request.form['location']

	xyz = 0
	if name == "":
		return render_template('admin_sign_in.html', xyz=xyz)

	if name == location:
		if name == 'aksir':
			return render_template('add_items.html')

	return render_template('admin_sign_in.html', xyz=xyz)


def connect_db():
    sql = sqlite3.connect('/home/arjun1995/ecommerce/ecommerce/sqlite3/usercr.db')
    #sql = sqlite3.connect('sqlite3/usercr.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

if __name__ == '__main__':
	app.run()