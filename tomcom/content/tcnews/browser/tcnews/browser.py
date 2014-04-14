# -*- coding: utf-8 -*-
from tomcom.browser.public import *

class ITcNews(Interface):

    def getTcNews(self):
        """ """

class Browser(BrowserView):

    implements(ITcNews)

    def getTcNews(self):
        """ """
        context=self.context
        pc=context.getAdapter('pc')()
        rc=context.getAdapter('rc')()
        time=DateTime()

        query={}
        query['portal_type']='TCNews'
        query['sort_on']='start'
        query['expires']={'query': time,'range': 'min'}
        query['effective']={'query': time,'range': 'max'}

        return pc(query)
