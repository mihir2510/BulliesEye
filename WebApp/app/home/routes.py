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
from app.main.get_data import search, search_by_id
from app.main.preprocess import preprocess
from app.main.model import predict
from app.main.model import labels
# import smtplib, ssl,csv
import json
from datetime import datetime
from app.main.report_generator.report import fill_jinja
import os

sender_email = "kaustubh.damania@gmail.com"  # Enter your address
#receiver_email = "xyz@gmail.com"  # Enter receiver address if 1-to-1 communication
password = "tempfakepassword"

# Python code to illustrate Sending mail with attachments
# from your Gmail account

# libraries to be imported
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_mail(receiver_email, attach_path):
    fromaddr = "kaustubh.damania@gmail.com"
    toaddr = receiver_email

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Cyberbullying report"

    # string to store the body of the mail
    body = """
    Hi,
    This is an autogenerated email sent using Python. PFA report on Cyberbullying

    Regards,
    Bullieseye
    """

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = "report.docx" #"File_name_with_extension"
    attachment = open(attach_path, "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, password)

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()

from app.main.get_data import search
from sqlalchemy.engine import create_engine
from sqlalchemy import inspect
from flask_cors import CORS, cross_origin
import ast, requests

# engine = create_engine('sqlite:////home/vtg/Desktop/BulliesEye/Ourapp/database.db')
# conn = engine.connect()
# data = conn.execute("SELECT * FROM Tweets")

engine1 = create_engine('sqlite:////home/kaustubhdamania/CodingStuff/Hackathons/SIH2020/BulliesEye/Ourapp/app/main/tweets.db')
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
def api_call():
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
        results = search(formdata['search'],25)
        # for result in results:
        #     print(result['text'],'type is',type(result['text']),end='-----------------\n')
        #     print('preprocessed data is',preprocess(result['text']))

        scores = [ predict(i['text']) for i in results]
        print(scores)
        #parsing begins
        urls = []
        print('Showing results now')
        print('Len results',len(results))
        for result in results:
            # print(result)
            url = result.get('id',{})
            urls.append(url)
            # print('End')
        htmls = []
        import requests
        # cnt = 0
        for i in range(len(urls)):
            url = urls[i]
            url = 'https://publish.twitter.com/oembed?url=https://twitter.com/web/status/' + str(url)
            try:
                res = requests.get(url).json()
                score = scores[i]
                # cnt += 1
                # print('score is',score)
                display_txt = []
                print('ssdsdsd',score)
                if score[1]: #offensive or not offensive
                    for idx in range(len(score[0])):
                        count = score[0][idx]
                        # print('idx is',idx,score[0])
                        if count=='1':
                            display_txt.append(labels[idx])

                    # print('display_txt',display_txt)
                    display_txt = ', '.join(display_txt)
                    htmls.append("""
                    <div style="margin-left: 15px; margin-top: 15px; width: 20%; transform: scale(1.2);">
                        <span style="margin-right: 5px;" class="label label-primary">{}</span>
                        <span style="margin-left: 5px;" class="label label-danger">{}</span>
                        <span style="margin-left: 5px;" class="label label-success">
                            <button id="{}" class="generate_report">
                                Generate report
                            </button>
                        </span>
                    </div>""".format(display_txt, score[2], url.split('?url=')[1])+res['html'])
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

@blueprint.route('/get_report', methods=['POST'])
@login_required
def get_report():
    print('Get report called')
    data = request.get_data()
    data = json.loads(data)
    print('data received is',data)
    url = data['id']
    id = url.split('/')[-1]
    result = search_by_id(id)._json
    if not result['entities']['user_mentions']:
        witnesses = 'None'
    else:
        witnesses = ', '.join([item['screen_name'] for item in result['entities']['user_mentions']])
    context = {
        'name': 'mihir',
        'date': result['created_at'],
        'sign': 'null',
        'list_criminals': '@'+result['user']['screen_name'],
        'desc': 'Cyberbullying found on following URL: {}'.format(url),
        'witnesses': witnesses,
        'reported_to': 'admin @ IT Cell',
        'reporting_date': str(datetime.now()),
        'actions': 'null'
    }

    fill_jinja('./app/main/report_generator/report_template.docx','./app/base/static/{}.docx'.format(id),context)
    send_mail('kaustubh.damania@gmail.com', './app/base/static/{}.docx'.format(id))
    return jsonify({'url': '/static/{}.docx'.format(id)})
