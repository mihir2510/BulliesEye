# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
from app.main.get_data import search

@blueprint.route('/index')
@login_required
def index():

    if not current_user.is_authenticated:
        return redirect(url_for('base_blueprint.login'))

    return render_template('index2.html')

@blueprint.route('/<template>')
def route_template(template):

    if not current_user.is_authenticated:
        return redirect(url_for('base_blueprint.login'))

    try:

        return render_template(template + '.html')

    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except:
        return render_template('page-500.html'), 500

'''
@blueprint.route('/search')
def pdf():
    rendered= render_template('search.html')
    pdf = pdfkit.from_string(rendered,False)

    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Dispostion'] = 'inline,filename=output.pdf'
'''

@blueprint.route('/search', methods=['GET','POST'])
@login_required
def search_page():
    results = None
    if request.method == 'POST':
        # results = [1,2,3]
        formdata = dict(request.form)
        if len(formdata.keys())==3:
            for i in formdata.keys():
                if i=='user':
                    formdata.pop(i)
                    break
        # '#'*int(formdata.get('hashtag',0))
        print(formdata['search'])
        results = search(formdata['search'],4)
        # print(results)
        urls = []
        print('Showing results now')
        print('Len results',len(results))
        for result in results:
            print(result)
            url = result.get('id',{})
            urls.append(url)
            print('End')
        htmls = []
        import requests
        for url in urls:
            url = 'https://publish.twitter.com/oembed?url=https://twitter.com/web/status/' + str(url)
            try:
                res = requests.get(url).json()
                htmls.append(res['html'])
                print(htmls[-1])
            except Exception as e:
                print(e)
                # continue

            # res = requests.get(url).json()
            # htmls.append(res['html'])
            # print(htmls[-1])

        results = htmls
    print('Final data length is','None' if results==None else len(results))
    return render_template('search.html', results = results)


