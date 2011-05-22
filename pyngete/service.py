#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo

config = None

def _oped(func):
    def wrapper(self, *args, **kwargs):
        db_host = kwargs['config']['db']['host']
        db_port = kwargs['config']['db']['port']
        db_name = kwargs['config']['db']['name']

        connect = pymongo.Connection(db_host, db_port) # db open
        db = connect[db_name]
        kwargs['db'] = {'connect' : connect, 'db' : db}

        retval = func(self, *args, **kwargs)

        kwargs['db']['connect'].disconnect() # db close
        return retval

    wrapper.__name__ = func.__name__
    wrapper.__dict__ = func.__dict__
    wrapper.__doc__ = func.__doc__
    return wrapper

@_oped
def save(self, *args, **kwargs):
    data = kwargs['data']
    db = kwargs['db']['db']
    col = db['rss']
    col.save(data)

@_oped
def get(self, *args, **kwargs):
    data = kwargs['data']
    col = kwargs['db']['db']['rss']

    query = {}

    if 1 <= len(data) and data[0]:
        query['prefix'] = data[0]

    if 2 <= len(data) and data[1]:
        query['level'] = data[1]

    print query
    return col.find(query).limit(10)
