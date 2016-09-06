#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
import requests
sys.setdefaultencoding('utf-8')
import json
import math

# https://github.com/caesar0301/treelib
# sudo easy_install -U treelib
from treelib import Tree, Node

def save_data(file_name, data):
	f = open(file_name, "w")
	f.write(data)
	f.close()

def getContent(url):
	session = requests.Session()
	url_request = session.get(url, allow_redirects=True, timeout=50)
	if url_request.status_code == requests.codes.ok:
		source = url_request.content.decode('utf-8')
	else:
		print "Error get content. Status code: %s" %url_request.status_code
		source = ''
	return source

def getDataHHRU(langs=['RU', 'EN', 'UA']):
	base_url = "https://hh.ru/shards/profarea?lang=%s"
	urls = []
	for lang in langs:
		data = getContent(base_url % lang)
		if data:
			save_data("data/"+lang+".json", data)
			print "Save %s data." % lang

def print_tree(lang="RU"):

	str_data = open('data/'+lang+'.json', 'r').read()

	data = json.loads(str_data, strict=False)
	tree = Tree()
	tree.create_node("root", 0)  # root node

	for d in data['items']:
		if int(d["id"]):
			tree.create_node(d['title'], float(d['id']), parent=0, data=d["title"])
			for dd in d['items']:
				if float(dd['id']):
					tree.create_node(dd['title'], dd['id'], parent=math.trunc(float(dd['id'])), data=dd["title"])

	tree.show()

if __name__ == "__main__":
	update_data = False

	if update_data:
		getDataHHRU()

	langs = ['RU', 'EN', 'UA']
	for lang in langs:
		print "===================================="
		print "===================================="
		print "==========  "+lang+"  ===================="
		print "===================================="
		print "===================================="
		print_tree(lang)