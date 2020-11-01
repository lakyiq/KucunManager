from flask import Flask,render_template,request,jsonify
import webbrowser
import sqldb

app = Flask(__name__)

@app.route('/')
@app.route('/index/')
def index():
	return render_template('goods.html')

@app.route('/other/')
def other():
	return render_template('records.html')

@app.route('/count/')
def count():
	return render_template('count.html')

@app.route('/data/goods/')
def getgoods():
	data = {"code": 0, "msg": ""}
	name=request.args.get('name') or ''
	size = request.args.get('size') or ''
	place=request.args.get('place') or ''
	lst=sqldb.select_goods(name,size,place)
	data['count']= len(lst)
	data['data']=lst
	return data

@app.route('/data/records/')
def getrecords():
	data = {"code": 0, "msg": ""}
	lst = sqldb.select_records()
	data['count'] = len(lst)
	data['data'] = lst
	return data

@app.route('/data/counts/')
def getcounts():
	place = request.args.get('place')
	kind = request.args.get('kind')
	date1= request.args.get('date1')
	date2 = request.args.get('date2')
	data = {"code": 0, "msg": ""}
	lst = sqldb.count_goods(place, kind, date1, date2)
	data['count'] = len(lst)
	data['data'] = lst
	return data

@app.route('/op/<kind>')
def op(kind):
	if kind=='in':
		id=request.args.get('id')
		change=request.args.get('change')
		sqldb.insert_records(id,1,change)
	elif kind=='out':
		id = request.args.get('id')
		change = request.args.get('change')
		sqldb.insert_records(id, 0, change)
	elif kind=='add':
		name=request.args.get('name')
		size=request.args.get('size')
		factory = request.args.get('factory') or ''
		place=request.args.get('place')
		price=request.args.get('price') or 0
		sqldb.insert_goods(name, size,factory,place,price)
	elif kind=='del':
		id=request.args.get('id')
		sqldb.del_goods(id)
	else:
		print('get it !')
		print(request)
		id = request.args.get('id')
		name = request.args.get('name')
		size = request.args.get('size')
		place = request.args.get('place')
		factory = request.args.get('factory') or ''
		price = request.args.get('price') or 0
		sqldb.update_goods(id,name,size,place,factory,price)
	return jsonify()

@app.route('/error/')
def error():
	return "500"

if __name__ == '__main__':
	webbrowser.open("http://127.0.0.1:5000/")
	app.run()
