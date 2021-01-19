#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'Javier G. Sogo'
SITETITLE = AUTHOR
SITENAME = "Javier G. Sogo's blog"
SITEURL = 'http://localhost:8000'
SITEDESCRIPTION = 'Thoughts and Writings'
SITELOGO = SITEURL + '/images/profile.png'
FAVICON = SITEURL + '/images/favicon.ico'

THEME = 'Flex'
PATH = 'content'

TIMEZONE = 'Europe/Madrid'

DEFAULT_LANG = 'es'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

USE_FOLDERS_AS_CATEGORY = True
MAIN_MENU = True

# Blogroll
LINKS = (('Lingẅars', 'http://lingwars.github.io/blog/'),)

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
COPYRIGHT_YEAR = 2021

DEFAULT_PAGINATION = 10
SUMMARY_MAX_LENGTH = 50

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

STATIC_PATHS = ['images', 'extra', 'pdfs',]
EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'},
                       'extra/README': {'path': 'README'},
                       'extra/custom.css': {'path': 'static/custom.css'},
                       }

PLUGIN_PATHS = ['./pelican-plugins']
PLUGINS = ['extract_toc']
CUSTOM_CSS = 'static/custom.css'
