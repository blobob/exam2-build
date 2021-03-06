from flask import Blueprint, render_template, request, render_template_string, current_app, flash, redirect, url_for, make_response, send_file
import os
import io
import subprocess
from time import sleep
import re
main = Blueprint('main', __name__)

SAFE_SPACE = os.getcwd() + '/safespace/safe'

def sym_sub(line):
    line = line.replace('/', '')
    line = line.replace('..', '')
    line = line.replace('%%2F', '')
    line = line.replace('%%2f', '')
    return line

@main.errorhandler(404)
def page_not_found(error):
    return '404 page not found', 404

@main.route('/robots.txt')
def robots():
    robots = 'User-agent: *\n'
    robots += 'Disallow: '



    resp = current_app.make_response(robots)
    resp.mimetype = "text/plain"
    return resp

@main.route('/')
def home():
    return render_template('pages/index.html')

@main.route('/about')
def about():
    return render_template('pages/about.html')

full_fpath = '../safe/'

@main.route('/safe/page')
def safe_page():
    if 'p' in request.args:
        try:
            name, ext = request.args['p'].split('.')
        except:
            return '404 page not found (Bad Input)', 404

        safe_pages = ['html']
        if ext not in safe_pages:
            return '404 page not found', 404
        else:
            full_fname = sym_sub(name + '.' + ext)

    else:
        return '404 page not found ("p" Empty)', 404

    safe_path = SAFE_SPACE + '/page/' + full_fname

    print("Safe Path: {}".format(safe_path))
    try:
        fp = open(safe_path, 'r')
    except:
        return '404 page not found (File Not Found)', 404

    file_content = fp.readlines()
    resp = render_template('pages/safe-space.html', lines=file_content)

    return resp


@main.route('/safe/doc')
def safe_doc():
    full_fname = None

    if 'd' in request.args:
        try:
            name, ext = request.args['d'].split('.')
        except:
            return '404 page not found (Bad Input)', 404
        safe_docs = ['md', 'txt']
        if ext not in safe_docs:
            return '404 page not found', 404
        else:
            full_fname = sym_sub(name + '.' + ext)
    else:
        return '404 page not found ("p" Empty)', 404

    safe_path = SAFE_SPACE + '/doc/' + full_fname

    print("Safe Path: {}".format(safe_path))
    try:
        fp = open(safe_path, 'r')
    except:
        return '404 page not found (File Not Found)', 404

    resp = make_response('\n'.join(fp.readlines()))
    resp.mimetype = 'text/plain'

    return resp


@main.route('/safe/img')
def safe_img():

    full_fname = None
    ext = None # Default
    if 'i' in request.args:
         arg = request.args['i']
         base = os.path.basename(arg)
         filename, extension = os.path.splitext(base)
         if extension is not None:
             ext = extension.lstrip('.')
         else:
             return '404 page not found (Unsafe Extension)', 404
         full_fname = arg
    else:
        return '404 page not found ("p" Empty)', 404

    safe_path = SAFE_SPACE + '/img/' + full_fname

    print("Safe Path: {}".format(safe_path))
    try:
        fp = open(safe_path, 'rb')
    except:
        return '404 page not found (File Not Found)', 404

    resp = send_file(io.BytesIO(fp.read()), mimetype='image/' + ext.lstrip('.'))
    return resp

