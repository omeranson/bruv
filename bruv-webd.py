#!/bin/env python

import bottle
import bruv
import collections
from Cheetah.Template import Template
from itertools import imap, ifilter
from gerrit import (
    QueryOptions,
    Gerrit,
)

templateDef = """
<HTML>
<HEAD><TITLE>BRUV</TITLE></HEAD>
<BODY>
#set $TOPIC_COL_WIDTH = 22
#set $PROJECT_COL_WIDTH = 20
#set $MESSAGE_COL_WIDTH = 55
#set $FLAGS_COL_WIDTH = 1
#set $USER_COL_WIDTH = 12
#set $NUMBER_COL_WIDTH = 6
#set $URL_COL_WIDTH = 34
<table border=1>
</tr><td>Number</td><td>Flags</td><td>Message</td><td>Project</td><td>User Name</td><td>URL</td><td>Change size</td><td/><td>Bugs</td></tr>
#set $count = 0
#for $change in reversed(list($changes))
#set $count = $count + 1
#set $flags = ""
#if $change.change_since_last_comment
#if $change.last_checked_patch_set == -1
#set $flags = $flags + "N"
#else
#set $flags = $flags + "U"
#end if
#else
#set $flags = $flags + "C"
#end if
#if $change.related_bugs
#set $flags = $flags + "B"
#end if
#if $change.is_blueprint
#set $flags = $flags + "P"
#end if 
#set bugs = ""
#for $bug in $change.related_bugs
#set $bugs = $bugs + '<a href=\"https://bugs.launchpad.net/bugs/' + $bug.replace('#','').strip() + '\">' + $bug + '</a>, '
#end for
<tr><td>$change.number</td><td>$flags</td><td>$change.subject</td><td>$change.project</td><td>$change.owner.name</td><td><a href="$change.diff_url">$change.diff_url</a></td><td>+$change.currentPatchSet.sizeInsertions $change.currentPatchSet.sizeDeletions</td><td><a href="/read/$change.number">R</a></td><td>$bugs</td></tr>
#end for
</table>
<br>
$count items left to review

 -- Flags: [N]ew, [U]pdated Patch Set, New [C]omments, Relates to a [B]ug, Blue-[P]rint 
</BODY>
</HTML>"""

@bottle.route('/')
def index():
    changes = bruv.get_changes()
    return str(Template(templateDef,
        searchList=[{"changes": changes,
                     }]))

@bottle.route('/list/<query>')
def list(query):
    changes = bruv.get_changes(query)
    return str(Template(templateDef,
        searchList=[{"changes": changes,
                     }]))

@bottle.route('/read/<number>')
def read(number):
    args = collections.namedtuple('Args', ('review'))(number)
    bruv.handle_read(args)
    bottle.response.status = 204

bottle.run(host='localhost', port=8080)
#print (index())
#bruv.handle_list()
