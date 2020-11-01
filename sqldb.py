import sqlite3

def create(conn,cursor):
	try:
		cursor.execute(
			'create table goods(id integer primary key autoincrement,name varchar(20) not null ,size varchar(20) not null,factory varchar(20),place varchar(10) not null,price float,number integer not null);')
	except:
		pass
	try:
		cursor.execute('create table records(id integer not null,time date not null,kind varchar(10) not null,change integer not null,foreign key (id) references goods(id));')
	except:
		pass


def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d


def select_goods(name,size,place):
	conn = sqlite3.connect('kucun.db')
	conn.row_factory = dict_factory
	cursor = conn.cursor()
	create(conn,cursor)
	sql='select * from goods where name like \'%'+name+'%\' and size like \'%'+size+'%\' and place like\'%'+place+'%\';'
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
	cursor.execute('select time,name,size,place,kind,change from goods left join records on records.id=goods.id order by time desc ;')
	records = cursor.fetchall()
	cursor.close()
	conn.commit()
	conn.close()
	return records


def insert_goods(name, size,factory,place,price):
	conn = sqlite3.connect('kucun.db')
	conn.row_factory = dict_factory
	cursor = conn.cursor()
	create(conn, cursor)
	cursor.execute('insert into goods values(null,?,?,?,?,?,0);', (name, size,factory,place,price,))
	cursor.close()
	conn.commit()
	conn.close()

def del_goods(id):
	conn = sqlite3.connect('kucun.db')
	conn.row_factory = dict_factory
	cursor = conn.cursor()
	create(conn, cursor)
	cursor.execute('delete from goods where id=?;',(id,))
	cursor.close()
	conn.commit()
	conn.close()

def insert_records(id, kind ,change):
	conn = sqlite3.connect('kucun.db')
	conn.row_factory = dict_factory
	cursor = conn.cursor()
	create(conn, cursor)
	if kind==1:
		cursor.execute('insert into records values(?,datetime(\'now\',\'localtime\'),?,?);', (id, '入库',change,))
		cursor.execute('update goods set number=number+? where id=?;', (change, id,))
	else:
		cursor.execute('insert into records values(?,datetime(\'now\',\'localtime\'),?,?);', (id, '出库', change,))
		cursor.execute('update goods set number=number-? where id=?;', (change, id,))
	cursor.close()
	conn.commit()
	conn.close()

def update_goods(id,name,size,place,factory,price):
	conn = sqlite3.connect('kucun.db')
	conn.row_factory = dict_factory
	cursor = conn.cursor()
	create(conn, cursor)
	cursor.execute('update goods set name=? ,size=?,place=?,factory=?,price=? where id=?;',(name,size,place,factory,price,id,))
	cursor.close()
	conn.commit()
	conn.close()

def count_goods(place,kind,date1,date2):
	conn = sqlite3.connect('kucun.db')
	conn.row_factory = dict_factory
	cursor = conn.cursor()
	create(conn, cursor)
	cursor.execute('select goods.id as id,name,size,place,factory,price,number,kind,sum(change) as sum_change,price*sum(change) as money from goods left join records on goods.id = records.id where place=? and kind=? and time >=? and time<=? group by kind,goods.id order by goods.id;',(place,kind,date1,date2),)
	counts = cursor.fetchall()
	cursor.close()
	conn.commit()
	conn.close()
	return counts

if __name__ == '__main__':
	conn = sqlite3.connect('kucun.db')
	cursor = conn.cursor()
	create(conn, cursor)
	cursor.close()
	conn.commit()
	conn.close()