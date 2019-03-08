#!/usr/bin/env python2
# vim: set syntax=none nospell:


import subprocess
import os
import fnmatch
import datetime
from bottle import default_app, route, run, template, response, redirect, debug, error, static_file
from wraphtml import WrapHtml


# for WSGI use:
application = default_app()

# config option #
debug(True)

# globals @
DLFILES_PATH = "/data/share/dlfiles"
application.config.setdefault('dlpath', "/data/share/dlfiles")
# application.config.setdefault('db_dir',"/data/share/db_dir")

# functions #


def run_cmd(cmd, ret_type="str"):
    """
    run a command and return either a str or a list
    """
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  # returns a class object
    proc = proc.communicate()[0]  # returns a string
    if ret_type == "str":
        return proc
    if ret_type == "br":
        # useful for html
        br_proc = proc.replace('\n', "<br>\n")
        return br_proc
    list_proc = proc.split("\n")
    return list_proc


# def _request(request, request_fallback=None):
#         '''
#         Extract request fields wherever they may come from: GET, POST, forms, fallback
#         '''
#         # Use lambdas to avoid evaluating bottle.request.* which may throw an Error
#         all_dicts = [
#             lambda: request.json,
#             lambda: request.forms,
#             lambda: request.query,
#             lambda: request.files,
#             #lambda: request.POST,
#             lambda: request_fallback
#         ]
#         request_dict = dict()
#         for req_dict_ in all_dicts:
#             try:
#                 req_dict = req_dict_()
#             except KeyError:
#                 continue
#             if req_dict is not None and hasattr(req_dict, 'items'):
#                 for req_key, req_val in req_dict.items():
#                     request_dict[req_key] = req_val
#         return request_dict
#
#
# def html_table(rows):
#     '''
#     input: data (list of lists)
#     return: html_table
#     '''
#     table = "<table>"
#     for row in rows:
#         table += "<tr>"
#         for cell in row:
#             table += "<td>" + cell + "</td>"
#         table += "</tr>"
#     table += "</table>"
#     return table
#
#
# def get_cols(db_conn,table):
#     '''
#     input: table
#     return: cols (tuple?list)
#     '''
#     cur = db_conn.cursor()
#     sql = "PRAGMA table_info(" + table + ")"
#     cur.execute(sql)
#     data = cur.fetchall()
#     return data
#
# def doRows(cur, table=""):
#     '''
#     input: table
#     get_cols
#     get_pg_size
#     truncateData (by rows and cols)
#     addDERlinks (Details, Edit, Remove)
#     return: htmltable
#     '''
#     # sql = "PRAGMA table_info(table)"
#     # return = cur.execute(sql)
#     # or .headers ON
#     pass
#
#
#
# # EOFunctions #


# routes #

# @route('/static/<filepath:path>')
# def static(filepath):
#     """
#     docstring needed
#     """
#     return static_file(filepath, root='./static')


@error(404)
def err404(error):
    return template('404.tpl', e=response.status_code)


# @route('/<s:path>/')
# def basename(s):
#     print("basename :" + s)
#     content = s
#     html = WrapHtml(content)
#     return html.wraphtml()

@route('/')
def home():
    """
    Landing page: /index.html
    WIP
    """
    return redirect("/flist")


@route('/flist')
def flist():
    """
    Purpose: to present "selected" files for download with a description for each
    Requires: import os, import fnmatch
    Selected files: !!! only files that have an associated description note file will get listed
      The description note file must be in the same directory with the name of "." + filename + ".nts"
      The first line of this file will get used as the file description. It has to be more than 4 characters...
    """
    # mypath = "/data/share/dlfiles"
    # application.config.setdefault('dlpath',mypath)
    mypath = application.config['dlpath']
    # import fnmatch
    # import os
    flist = os.listdir(mypath)
    content = "<center>"
    content += "<table>"
    content += "<tr><th>Filename</th><th>Size</th><th>mTime</th><th>Description</th></tr>"
    for fname in flist:
        if fnmatch.fnmatch(fname, "*"):
            note_file = mypath + "/." + fname + ".nts"
            if os.path.isfile(note_file):
                with open(note_file) as f:
                    first_line = f.readline()
                    if len(first_line) > 4:
                        size = os.path.getsize(mypath + "/" + fname)
                        # mtime = os.path.getmtime(mypath + "/" + fname)
                        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(mypath + "/" + fname))
                        # print(fname + " " + "{:,}".format(size) + " " + str(mtime))
                        content += '<tr><td><a href="/dl/' + fname + '">' + fname + '</a></td><td>' + "{:,}".format(size) + '</td><td>' + str(mtime) + '</td><td>' + first_line + '</td></tr>'
    content += "</table>"
    content += "</center>"
    # proc = run_cmd("ls -ltra " + mypath,"br")
    # print("type(proc): " + str(type(proc)))
    # proc.replace("\n","<br>")
    # proc.replace(",","<br>")
    # content += "<hr>" + str(proc) + "<hr>"
    # html = WrapHtml(content=content, title="Files for download",render_now=True,nav_d={"Home": "/"})
    html = WrapHtml(content, nav_d={"Home": "/"})
    html.nav_d = {"Home": "/"}
    html.title = 'File for download'
    return html.render()


@route('/dl/<filename:path>')
def download(filename):
    mypath = application.config['dlpath']
    note_file = mypath + "/." + filename + ".nts"
    found = False
    # import fileinput
    # for line in fileinput.input(note_file, inplace = 1):
    with open(note_file, "r") as f:
        flines = f.read().splitlines()
    f.close()

    new_flines = []

    # print("flines: " + str(flines))
    for line in flines:
        if line.startswith("[cnt]:"):
            found = True
            words = line.split()
            cnt = int(words[1]) + 1
            print("[cnt]: " + str(cnt))
            new_flines.append("[cnt]: " + str(cnt))
        else:
            print(line)
            new_flines.append(line)

    if not found:
        f = open(note_file, "a")
        f.write("[cnt]: 1")
        print("Adding: [cnt] 1")
    else:
        print("write new_lines to note_file")
        nf = open(note_file, "w+")  # noqa:
        for line in new_flines:
            nf.write(line + "\n")
        nf.close()

    print("new_flines: " + str(new_flines))

    # return static_file(filename, root='/path/to/static/files', download=filename)
    return static_file(filename, root='/data/share/dlfiles', download=True)  # download=True keeps the filename the same


# ## ####### ## #

if __name__ == '__main__':
    # run(port=8080, debug=True, reloader=True)
    run()
