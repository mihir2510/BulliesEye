# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
from app.main.get_data import search
from sqlalchemy.engine import create_engine 
from sqlalchemy import inspect
from flask_cors import CORS, cross_origin
import ast, requests

# engine = create_engine('sqlite:////home/vtg/Desktop/BulliesEye/Ourapp/database.db')
# conn = engine.connect()
# data = conn.execute("SELECT * FROM Tweets")

engine1 = create_engine('sqlite:////home/vtg/Desktop/BulliesEye/Ourapp/app/main/tweets.db')
conn1 = engine1.connect()
data = conn1.execute("SELECT * FROM Tweets")
data1 = conn1.execute("SELECT * FROM affective_sense")
# print(inspector.get_table_names())

# print(inspector.get_columns('Tweets'))
temp = []
senses = []
locs = []
for da in data:
    if da[8]>0.5:
        temp.append([da[3],da[1],da[2],da[8]])
        locs.append(da[4])

for sense in data1:
    senses.append(sense)
print(senses)

final=[temp,[dict(row) for row in senses]]

@blueprint.route("/api/data")
def geo_code():
    return jsonify(final)

@blueprint.route("/api/senses")
def sens():
    return jsonify({'senses': [dict(row) for row in senses]})


# Returns (lat, long)
def geocode(location):
    token = '72e31e4798af49'
    url = "https://us1.locationiq.com/v1/search.php"
    data = {
        'key': token,
        'q': location,
        'format': 'json'    
    }
    response = requests.get(url, params=data)
    return ast.literal_eval(response.text)[0]['lat'], ast.literal_eval(response.text)[0]['lon']


@blueprint.route('/index')
@login_required
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('base_blueprint.login'))
    return render_template('index2.html',data = temp)

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


