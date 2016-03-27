# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
3.http.middleware.py
"""

MIDDLEWARE_TOP = "<div class='top'>Middleware TOP</div>"
MIDDLEWARE_BOTTOM =  "<div class='botton'>Middleware BOTTOM</div>"


class MyMiddleWare(object):
 	def __init__(self, app):
 		self.app = app

 	def __call__(self, environ, start_response):
 		#Вставляем TOP and BOTTOM
 		response = self.app(environ, start_response)[0].decode()
 		if response.find('<body>') >-1:
 				#отделяем заголовок от тела
 				header,body = response.split('<body>')
 				#отделяем тело документа от конца
 				bodycontent,htmlend = body.split('</body>')
 				#"склеиваем" новую страницу
 				bodycontent = '<body>'+ MIDDLEWARE_TOP + bodycontent + MIDDLEWARE_BOTTOM+'</body>'
 				return [header.encode() + bodycontent.encode() + htmlend.encode()]
 		else:
 			        return [MIDDLEWARE_TOP + response.encode() + MIDDLEWARE_BOTTOM]

import os
def app(environ, start_response):
 	#Генерируем ответ на запрос
 	res = environ['PATH_INFO']

 	if res == '/' or res == '/index.html':
 		path = './index.html'
 		print('i')
 	if res == '/about/aboutme.html':
 		filePath = './about/aboutme.html'
 		print('a')
 	else:
 		filePath = './index.html'
 	
 	fd = open(filePath,'r')
 	fileContent = fd.read()
 	fd.close() 	
 		

 	start_response('200 OK', [('Content-Type', 'text/html')])
 	return [fileContent.encode()]


app = MyMiddleWare(app)
if __name__ == '__main__':
    from waitress import serve

    serve(app, host='localhost', port=8000)
