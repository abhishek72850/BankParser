import re
import psycopg2
import os
from bank.models import Banks, Branches
from django.core import serializers
import json
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector


class BankParser:

	# DATABASE = os.environ.get('DATABASE')
	# USER = os.environ.get('USER')
	# PASSWORD = os.environ.get('PASSWORD')
	# HOST = os.environ.get('HOST')
	# PORT = os.environ.get('PORT')

	def __init__(self):
		# self.conn = psycopg2.connect(database=self.DATABASE, user = self.USER, 
		# 	password = self.PASSWORD, host = self.HOST, port = self.PORT)
		pass

	def fetchByIFSC(self,ifsc):
		#cursor = self.conn.cursor()

		#cursor.execute("SELECT * FROM banks b,branches br WHERE b.id=br.bank_id AND br.ifsc='"+ifsc+"'")
		
		data = Branches.objects.filter(pk = ifsc)

		if(data.count() > 0):
			
			serialzed_data = serializers.serialize('json', data, use_natural_foreign_keys=True)

			json_data = json.loads(serialzed_data)

			return json_data

		# if(cursor.rowcount > 0):
		# 	rows = cursor.fetchone()

		# 	columns = [col.name for col in cursor.description]

		# 	data = {}

		# 	for c1,c2 in zip(columns,rows):
		# 		data[c1] = c2

		# 	return data
		else:
			return {'message':'No Data Found'}

	def fetchByName(self,name,city,limit='1000',offset='0'):
		#cursor = self.conn.cursor()

		#cursor.execute("SELECT * FROM banks b,branches br WHERE b.id = br.bank_id AND \
		# 	(b.name ILIKE '%"+name+"%' AND br.city ILIKE '%"+city+"%') ORDER BY br.branch \
		# 	LIMIT "+limit+" OFFSET "+offset);

		# data = Branches.objects.raw("SELECT * FROM banks b,branches br WHERE b.id = br.bank_id AND \
		# 	(b.name ILIKE '%"+name+"%' AND br.city ILIKE '%"+city+"%') ORDER BY br.branch \
		# 	LIMIT "+limit+" OFFSET "+offset)

		vector = SearchVector('bank','city')
		query = SearchQuery(name + ' ' + city)
		srank = SearchRank(vector,query)

		data = Branches.objects.annotate(rank = srank).order_by('-rank')[int(offset):int(offset)+int(limit)]

		if(data.count() > 0):
			
			serialzed_data = serializers.serialize('json', data, use_natural_foreign_keys=True)

			json_data = json.loads(serialzed_data)

			return json_data

		# if(cursor.rowcount > 0):

		# 	rows = cursor.fetchall()

		# 	columns = [col.name for col in cursor.description]

		# 	data=[]

		# 	for row in rows:
		# 	    e = {}
		# 	    for c1,c2 in zip(columns,row):
		# 	        e[c1] = c2
		# 	    data.append(e)

		# 	return data
		else:
			return {'message':'No Data Found'}
