#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Javier G. Sogo'
SITEURL = u'http://localhost:8000'
SITENAME = u"Javier G. Sogo's blog"
SITETITLE = AUTHOR
SITESUBTITLE = u'Software engineer | Data Scientist'
SITEDESCRIPTION = 'Thoughts and Writings'
SITELOGO = SITEURL + '/images/profile.png'
FAVICON = SITEURL + '/images/favicon.ico'

ROBOTS = 'index, follow'

THEME = u'themes/Flex'  # https://github.com/alexandrevicenzi/Flex
PATH = u'content'
TIMEZONE = 'Europe/Madrid'
DEFAULT_LANG = u'es'
OG_LOCALE = u'es_ES'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

USE_FOLDERS_AS_CATEGORY = True
MAIN_MENU = True

# Blogroll
LINKS = (('Lingẅars', 'https://lingwars.github.io/blog/'),)

# Social widget
SOCIAL = (('linkedin', 'https://es.linkedin.com/in/jgsogo'),
          ('github', 'https://github.com/jgsogo'),
          ('twitter', 'https://twitter.com/jgsogo'),
          ('rss', SITEURL + FEED_ALL_ATOM),
          )

MENUITEMS = (('Archives', '/archives.html'),
             ('Categories', '/categories.html'),)
             
CC_LICENSE = {
    'name': 'Creative Commons Attribution-ShareAlike',
    'version':'4.0', 
    'slug': 'by-sa',
}
COPYRIGHT_YEAR = 2015

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

