import sqlite3

def create(conn,cursor):
	try:
		cursor.execute(
			'create table goods(id integer primary key autoincrement,name varchar(20) not null ,size varchar(20) not null,number float not null);')
	except:
		pass
	try:
		cursor.execute('create table records(id integer not null,time date not null,kind varchar(10) not null,change float not null,foreign key (id) references goods(id));')
	except:
		pass


def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d


def select_goods(name):
	conn = sqlite3.connect('kucun.db')
	conn.row_factory = dict_factory
	cursor = conn.cursor()
	create(conn,cursor)
	sql='select * from goods '
	if name:
		sql+='where name like \'%'+name+'%\';'
	else:
		sql+=';'
	cursor.execute(sql)
	goods = cursor.fetchall()
	cursor.close()
	conn.commit()
	conn.close()
	return goods


def select_records():
	conn = sqlite3.connect('kucun.db')
	conn.row_factory = dict_factory
	cursor = conn.cursor()
	create(conn, cursor)
	cursor.execute('select time,name,size,kind,change from records left join goods on records.id=goods.id order by time;')
	records = cursor.fetchall()
	cursor.close()
	conn.commit()
	conn.close()
	return records


def insert_goods(name, size):
	conn = sqlite3.connect('kucun.db')
	conn.row_factory = dict_factory
	cursor = conn.cursor()
	create(conn, cursor)
	cursor.execute('insert into goods values(null,?,?,0);', (name, size,))
	cursor.close()
	conn.commit()
	conn.close()

def del_goods(id):
	conn = sqlite3.connect('kucun.db')
	conn.row_factory = dict_factory
	cursor = conn.cursor()
	create(conn, cursor)
	cursor.execute('delete from goods where id=?',(id,))
	cursor.close()
	conn.commit()
	conn.close()

def insert_records(id, kind ,change):
	conn = sqlite3.connect('kucun.db')
	conn.row_factory = dict_factory
	cursor = conn.cursor()
	create(conn, cursor)
	if kind==1:
		cursor.execute('insert into records values(?,datetime(\'now\'),?,?);', (id, '入库',change,))
		cursor.execute('update goods set number=number+? where id=?;', (change, id,))
	else:
		cursor.execute('insert into records values(?,datetime(\'now\'),?,?);', (id, '出库', change,))
		cursor.execute('update goods set number=number-? where id=?;', (change, id,))
	cursor.close()
	conn.commit()
	conn.close()


