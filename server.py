from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import os
import boto3
import mysql.connector

import os

DATABASE_REGION = 'us-east-2'
PORT = 3306

rds = boto3.client('rds')

try:
    mydb =  mysql.connector.connect(
        host='blogdb-instance-1.cz60hqkylf4i.us-east-2.rds.amazonaws.com' ,
        user='admin',
        passwd='helloworld',
        port=3306,
        database='bookcase',        
    )
except Exception as e:
    print('Database connection failed due to {}'.format(e))          

def all_books(request):
    mycursor = mydb.cursor()
    mycursor.execute('SELECT name, title, year FROM authors, books WHERE authors.authorId = books.authorId ORDER BY year')
    title = 'Books'
    message = '<html><head><title>' + title + '</title></head><body>'
    message += '<h1>' + title + '</h1>'
    message += '<ul>'
    for (name, title, year) in mycursor:
        message += '<li>' + name + ' - ' + title + ' (' + str(year) + ')</li>'
    message += '</ul>'
    message += '</body></html>'
    return Response(message)

if __name__ == '__main__':

    with Configurator() as config:
        config.add_route('all_books', '/')
        config.add_view(all_books, route_name='all_books')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', PORT, app)
    server.serve_forever()