# -*- coding: iso-8859-1 -*-
#
# Copyright (C) 2003-2005 Edgewall Software
# Copyright (C) 2003-2004 Jonas Borgstr�m <jonas@edgewall.com>
# Copyright (C) 2005 Christopher Lenz <cmlenz@gmx.de>
# All rights reserved.
#
# This software is licensed as described in the file Trac_licence.txt, which
# you should have received as part of this distribution. The terms
# are also available at http://trac.edgewall.com/license.html.
#
# This software consists of voluntary contributions made by many
# individuals. For the exact contribution history, see the revision
# history and logs, available at http://projects.edgewall.com/trac/.
#
# Author: Jonas Borgstr�m <jonas@edgewall.com>
#         Christopher Lenz <cmlenz@gmx.de>

from urllib import quote, urlencode


class Href(object):
    """
    Implements a callable that constructs URLs with the given base. The
    function can be called with any number of positional and keyword
    arguments which than are used to assemble the URL.

    Positional arguments are appended as individual segments to
    the path of the URL:

    >>> href = Href('/trac')
    >>> href('ticket', 540)
    '/trac/ticket/540'
    >>> href('ticket', 540, 'attachment', 'bugfix.patch')
    '/trac/ticket/540/attachment/bugfix.patch'
    >>> href('ticket', '540/attachment/bugfix.patch')
    '/trac/ticket/540/attachment/bugfix.patch'

    If a positional parameter evaluates to None, it will be skipped:

    >>> href('ticket', 540, 'attachment')
    '/trac/ticket/540/attachment'

    The first path segment can also be specified by calling an attribute
    of the function, as follows:

    >>> href.ticket(540)
    '/trac/ticket/540'
    >>> href.changeset(42, format='diff')
    '/trac/changeset/42?format=diff'

    Simply calling the Href object with no arguments will return the base URL:

    >>> href()
    '/trac'

    Keyword arguments are added to the query string, unless the value is None:

    >>> href = Href('/trac')
    >>> href('timeline', format='rss')
    '/trac/timeline?format=rss'
    >>> href('timeline', format=None)
    '/trac/timeline'
    >>> href('search', q='foo bar')
    '/trac/search?q=foo+bar'

    Multiple values for one parameter are specified using a sequence (a list or
    tuple) for the parameter:

    >>> href('timeline', show=['ticket', 'wiki', 'changeset'])
    '/trac/timeline?show=ticket&show=wiki&show=changeset'

    Alternatively, query string parameters can be added by passing a dict or
    list as last positional argument:

    >>> href('timeline', {'from': '02/24/05', 'daysback': 30})
    '/trac/timeline?daysback=30&from=02%2F24%2F05'

    If the order of query string parameters should be preserved, you may also
    pass a sequence of (name, value) tuples as last positional argument:

    >>> href('query', (('group', 'component'), ('groupdesc', 1)))
    '/trac/query?group=component&groupdesc=1'

    >>> params = []
    >>> params.append(('group', 'component'))
    >>> params.append(('groupdesc', 1))
    >>> href('query', params)
    '/trac/query?group=component&groupdesc=1'

    By specifying an absolute base, the function returned will also generate
    absolute URLs:

    >>> href = Href('http://projects.edgewall.com/trac')
    >>> href('ticket', 540)
    'http://projects.edgewall.com/trac/ticket/540'

    >>> href = Href('https://projects.edgewall.com/trac')
    >>> href('ticket', 540)
    'https://projects.edgewall.com/trac/ticket/540'

    Finally, the first path segment of the URL to generate can be specified in
    the following way, mainly to improve readability:

    >>> href = Href('/trac')
    >>> href.ticket(540)
    '/trac/ticket/540'
    >>> href.browser('/trunk/README.txt', format='txt')
    '/trac/browser/trunk/README.txt?format=txt'
    """

    def __init__(self, base):
        self.base = base
        self._derived = {}

    def __call__(self, *args, **kw):
        href = self.base
        if href and href[-1] == '/':
            href = href[:-1]
        params = []

        def add_param(name, value):
            if type(value) in (list, tuple):
                for i in [i for i in value if i != None]:
                    params.append((name, i))
            elif v != None:
                params.append((name, value))

        if args:
            lastp = args[-1]
            if lastp and type(lastp) is dict:
                for k,v in lastp.items():
                    add_param(k, v)
                args = args[:-1]
            elif lastp and type(lastp) in (list, tuple):
                for k,v in lastp:
                    add_param(k, v)
                args = args[:-1]

        # build the path
        path = '/'.join([quote(str(arg).strip('/')) for arg in args
                         if arg != None])
        if path:
            href += '/' + path

        # assemble the query string
        for k,v in kw.items():
            add_param(k, v)

        if params:
            href += '?' + urlencode(params)

        return href

    def __getattr__(self, name):
        if not self._derived.has_key(name):
            self._derived[name] = lambda *args, **kw: self(name, *args, **kw)
        return self._derived[name]


if __name__ == '__main__':
    import doctest, sys
    doctest.testmod(sys.modules[__name__])
