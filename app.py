from flask import Flask,render_template,request
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

@app.route('/data/goods/')
def getgoods():
	data = {"code": 0, "msg": ""}
	name=request.args.get('name')
	lst=sqldb.select_goods(name)
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
		sqldb.insert_goods(name,size)
	else:
		id=request.args.get('id')
		sqldb.del_goods(id)
	return render_template('goods.html')




if __name__ == '__main__':
	webbrowser.open("http://127.0.0.1:5000/")
	app.run()
