import re
import psycopg2

class BankParser:

	DATABASE = "fyle"
	USER = "postgres"
	PASSWORD = "alexkay728"
	HOST = "127.0.0.1"
	PORT = "5432"

	def __init__(self):
		self.conn = psycopg2.connect(database=self.DATABASE, user = self.USER, 
			password = self.PASSWORD, host = self.HOST, port = self.PORT)

	def fetchByIFSC(self,ifsc):
		cursor = self.conn.cursor()

		cursor.execute("SELECT * FROM banks b,branches br WHERE b.id=br.bank_id AND br.ifsc='"+ifsc+"'")
		
		if(cursor.rowcount > 0):
			rows = cursor.fetchone()

			columns = [col.name for col in cursor.description]

			data = {}

			for c1,c2 in zip(columns,rows):
				data[c1] = c2

			return data
		else:
			return {'message':'No Data Found'}

	def fetchByName(self,name,city,limit='1000',offset='0'):
		cursor = self.conn.cursor()

		cursor.execute("SELECT * FROM banks b,branches br WHERE b.id = br.bank_id AND \
			(b.name ILIKE '%"+name+"%' AND br.city ILIKE '%"+city+"%') ORDER BY br.branch \
			LIMIT "+limit+" OFFSET "+offset);

		if(cursor.rowcount > 0):

			rows = cursor.fetchall()

			columns = [col.name for col in cursor.description]

			data=[]

			for row in rows:
			    e = {}
			    for c1,c2 in zip(columns,row):
			        e[c1] = c2
			    data.append(e)

			return data
		else:
			return {'message':'No Data Found'}
