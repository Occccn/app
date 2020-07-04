import sqlite3

dbname = 'kenco.db'
conn = sqlite3.connect(dbname)
c = conn.cursor()
ddl = 'CREATE TABLE if not exists kenco(date NOT NULL, weight REAL , abura REAL);'

#sqlの発行
c.execute(ddl)

weight = 65.7
abura = 20.1
year = 2020
month = 6
day = 23
date = '"{}-{}-{}"'.format(year , month , day)

c.execute('INSERT INTO kenco VALUES({} , {} , {})'.format(date , weight ,abura))

conn.commit()
