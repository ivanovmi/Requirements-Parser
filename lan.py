#!/usr/bin/python

import requests
import sys

LAUNCHPAD_ID='dtrishkin@mirantis.com'
LAUNCHPAD_PW='3393YEShq27'

parameters ={
'openid.assoc_handle' : '',
'openid.claimed_id' :   'http://specs.openid.net/auth/2.0/identifier_select',
'openid.ext2.mode' :    'fetch_request',
'openid.ext2.required' :        'FirstName,LastName,Email',
'openid.ext2.type.Email' :      'http://schema.openid.net/contact/email',
'openid.ext2.type.FirstName' :  'http://schema.openid.net/namePerson/first',
'openid.ext2.type.LastName' :   'http://schema.openid.net/namePerson/last',
'openid.identity' :     'http://specs.openid.net/auth/2.0/identifier_select',
'openid.mode' : 'checkid_setup',
'openid.ns' :   'http://specs.openid.net/auth/2.0',
'openid.ns.ext2' :      'http://openid.net/srv/ax/1.0',
'openid.ns.sreg' :      'http://openid.net/sreg/1.0',
'openid.realm' :        'https://review.fuel-infra.org/',
'openid.return_to' :    'https://review.fuel-infra.org/OpenID?gerrit.mode=SIGN_IN&gerrit.token=%2Fq%2Fstatus%3Aopen',
'openid.sreg.required' :        'fullname,email',
}


def getRequirementsFromUrl(url, gerritAccount):
    s = requests.Session()
    s.headers.update({'Cookie' : 'GerritAccount=' + gerritAccount})
    r = s.get(url)

    if r.status_code == 200:
        return r.iter_lines()
    else:
        print  r.status_code
        raise SystemExit


def loginToLaunchpad():
    s = requests.Session()
    r = s.get('https://login.launchpad.net')

    login_data = {
    'openid.usernamepassword' : '',
    'csrfmiddlewaretoken' : requests.utils.dict_from_cookiejar(s.cookies)['csrftoken'],
    'email':        LAUNCHPAD_ID,
    'password' :    LAUNCHPAD_PW,
    'user-intentions' :     'login',
    }

    Cookies = 'C=1; csrftoken=' + requests.utils.dict_from_cookiejar(s.cookies)['csrftoken']
    s.headers.update({'Referer': 'https://login.launchpad.net'})
    s.headers.update({'Cookie': Cookies})
    r = s.post('https://login.launchpad.net/+login', data=login_data)

    ss = requests.Session()
    rf = ss.get('https://review.fuel-infra.org/login/q/status:open')
    start_post = rf.content.find('openid.assoc_handle" type="hidden" value="')
    rf.content[start_post+42 : start_post+42+33]
    parameters['openid.assoc_handle'] = rf.content[start_post+42 : start_post+42+33]

    Cookiess = 'csrftoken=' + requests.utils.dict_from_cookiejar(s.cookies)['csrftoken']
    Cookiess += '; C=1; sessionid=' + requests.utils.dict_from_cookiejar(s.cookies)['sessionid']
    Cookiess += '; openid_referer="https://review.fuel-infra.org/login/q/status:open"'

    ss.headers.update({'Referer': 'https://review.fuel-infra.org/login/q/status:open'})
    ss.headers.update({'Cookie': Cookiess})
    r = ss.post('https://login.launchpad.net/+openid', data=parameters, allow_redirects=True)

    d_data = {
     'csrfmiddlewaretoken': requests.utils.dict_from_cookiejar(s.cookies)['csrftoken'],
     'email': 'on',
     'fullname': 'on',
     'ok': '',
     'openid.usernamepassword': ''
    }

    ss.headers.update({'Referer': r.url})
    header = s.headers

    rd = ss.post(r.url, data=d_data, allow_redirects=True)

    if requests.utils.dict_from_cookiejar(ss.cookies).has_key('GerritAccount'):
        return requests.utils.dict_from_cookiejar(ss.cookies)['GerritAccount']
    else:
        print 'Could not authenticate'
        raise SystemExit

#gerritAccount = loginToLaunchpad ()
#req_url = 'https://review.fuel-infra.org/gitweb?p=openstack/horizon.git;a=blob_plain;f=requirements.txt;hb=refs/heads/master'
#print getRequirementsFromUrl(req_url, gerritAccount)
#r = getRequirementsFromUrl(req_url, gerritAccount)
#def call_it(r):
#    res = dict()
#    for i in r.iter_lines():
#        print i
#    return res
#call_it(r)