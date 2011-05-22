#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import glob
import datetime

import web
from web.contrib.template import render_mako
import PyRSS2Gen

basedir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, basedir)

import service


import simplejson

fp = open('./config.json', 'r')
config = simplejson.load(fp)

render = render_mako(
        directories=['templates'],
            input_encoding='utf-8',
            output_encoding='utf-8',
        )

urls = (
    '/', 'Index',
    '/rss/(.+)', 'Rss',
)

class Rss:
    def GET(self, path):
        web.header("Content-Type", "application/xml; charset=UTF-8")
        params = path.split('/')
        data = service.get(self, config=config, data=params)

        items = []
        for line in data:
            title = ""
            if line.has_key('title'):
                title += line['title'][0]

            if line.has_key('prefix'):
                title += ' - ' + line['prefix']

            if line.has_key('level'):
                title += ' [' + line['level'][0] + ']'

            link = ""
            if line.has_key('link'):
                link = line['link']

            desc = ""
            if line.has_key('content'):
                desc = line['content']

            guid = web.ctx.homedomain + '/' + str(line['_id'])
            pubDate = line['time']


            items.append(PyRSS2Gen.RSSItem(
                title = title,
                link = link,
                description = desc,
                guid = PyRSS2Gen.Guid(guid),
                pubDate = pubDate
                ))

        rss = PyRSS2Gen.RSS2(title = "Notification",
                             link = web.ctx.homedomain,
                             description = "Various notifications to the RSS.",
                             lastBuildDate = datetime.datetime.utcnow(),
                             items=items)
        return rss.to_xml()

class Index:
    def GET(self):
        web.header("Content-Type", "text/html; charset=UTF-8")
        return render.index(title='Notification')

    def POST(self):
        web.header("Content-Type", "text/html; charset=UTF-8")
        form = web.input()
        data = {}

        data['prefix'] = form.prefix,
        data['level'] = form.level,
        data['title'] = form.title,
        data['link'] = form.link,
        data['time'] = datetime.datetime.now()
        data['content'] = form.content

        service.save(self, config=config, data=data)
        return render.index(title='Notification', ans='Added successfully.')

web.internalerror = web.debugerror
app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
