#
#   The contents of this file are subject to the HACOS License Version 1.2
#   (the "License"); you may not use this file except in compliance with
#   the License.  Software distributed under the License is distributed
#   on an "AS IS" basis, WITHOUT WARRANTY OF ANY KIND, either express or
#   implied. See the LICENSE file for the specific language governing
#   rights and limitations under the License.  The Original Software
#   is "NetEpi Collection". The Initial Developer of the Original
#   Software is the Health Administration Corporation, incorporated in
#   the State of New South Wales, Australia.
#
#   Copyright (C) 2004-2011 Health Administration Corporation, Australian
#   Government Department of Health and Ageing, and others.
#   All Rights Reserved.
#
#   Contributors: See the CONTRIBUTORS file for details of contributions.
#
from cocklebur import dbobj
from casemgr import paged_search
from pages import page_common
import config

class PageOps(page_common.PageOpsBase):
    def do_edit(self, ctx, group_id):
        ctx.locals.group_result.reset()
        ctx.push_page('admin_group', int(group_id))

    def do_add(self, ctx, ignore):
        ctx.locals.group_result.reset()
        ctx.push_page('admin_group', None)

pageops = PageOps()


def page_enter(ctx, group_result):
    group_result.headers = [
        ('group_name', 'Name'),
        ('description', 'Description'),
        ('rights', 'Rights'),
    ]
    ctx.locals.group_result = group_result
    paged_search.push_pager(ctx, ctx.locals.group_result)
    ctx.add_session_vars('group_result')

def page_leave(ctx):
    paged_search.pop_pager(ctx)
    ctx.del_session_vars('group_result')

def page_display(ctx):
    ctx.run_template('admin_groups.html')

def page_process(ctx):
    pageops.page_process(ctx)
