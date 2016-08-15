"""
adds profs,stus and FACs from ldap
"""
import ldap3
from string import ascii_lowercase
from kronos.models import FAC, Stu, Prof, User
from kronos.util import get_div_from_dept
from kronos import db
db.create_all()

server = ldap3.Server('ldap.reed.edu', port=389, get_info=ldap3.ALL)
conn = ldap3.Connection(server, auto_bind=True)
# syntax for the filter outlined at
# http://ldap3.readthedocs.io/tutorial.html#performing-searches
query='ou=people,dc=reed,dc=edu'
filter=  '(&'
filter +=  '(|'
filter +=    '(|'
filter +=      '(&'
filter +=        '(eduPersonPrimaryAffiliation=student)'
filter +=        '(!(eduPersonAffiliation=alumni))'
filter +=      ')'
filter +=      '(&'
filter +=        '(eduPersonPrimaryAffiliation=staff)'
filter +=        '(rcDepartment=Admin Assistant to Faculty)'
filter +=      ')'
filter +=    ')'
filter +=    '(&'
filter +=      '(eduPersonPrimaryAffiliation=faculty)'
filter +=      '(&'
filter +=        '(!(eduPersonAffiliation=trustee))'
filter +=        '(&'
filter +=          "(rcDepartment=*)"
filter +=          '(&'
filter +=            "(!(rcDepartment=President's Office))"
filter +=            '(&'
filter +=              "(!(rcDepartment=Institutional Diversity))"
filter +=              '(&'
filter +=                "(!(rcDepartment=Library))"
filter +=                '(&'
filter +=                  "(!(rcDepartment=Department of Athletics))"
filter +=                  "(!(rcDepartment=Dean of the Faculty))"
filter +=                ')'
filter +=              ')'
filter +=            ')'
filter +=          ')'
filter +=        ')'
filter +=      ')'
filter +=    ')'
filter +=  ')'
filter +=  '(uid=a*)'
filter +=')'


# Does a separate search for uids beginning with each letter of the 
# alphabet because ldap limits searches to 500 entries, so otherwise we
# would not be able to get everyone 
for i in ascii_lowercase:
    myfilter = filter.replace("a*", i + "*")
    conn.search(search_base=query,
                search_filter=myfilter,
                search_scope=ldap3.SUBTREE,
                attributes=ldap3.ALL_ATTRIBUTES)
    for person in conn.response:
        att = person.get('attributes')
        uid = att.get('uid')[0] or "username"
        name = att.get('gecos') or "name"
        email = att.get('eduPersonPrincipalName') or "placeholder@reed.edu"
        role = att.get('eduPersonPrimaryAffiliation')  
        if name is None:
            print(uid)
        # only add if no one else has this username
        if User.query.filter(User.username == uid).all() == []:
            if role == 'faculty':
                # adding new professor
                dept = att.get('rcDepartment')[0] 
                div = get_div_from_dept(dept)
                newuser = Prof(uid, name, email, dept, div)
                db.session.add(newuser)
            elif role == 'student':
                # adding new student
                newuser = Stu(uid, name, email, 'Dance', 'The Arts')
                db.session.add(newuser)
            # all staff in this query are FACs beacuse of rules in the filter
            elif role == 'staff':
                # For the time being, FACs should not be added from ldap
                # it does not seem that their listing of 
                # 'Administrative Assistants' is very current. By that I mean
                # it includes people who are not listed as administrative
                # assistants on the department websites and it does not
                # include current admin assistants like Kim Kadas
                # Since there are a small number of FACs and since they have
                # a lot of power on the site, we should enter them in manually
                # newuser = FAC(uid, name, email)
                # db.session.add(newuser)
                pass
db.session.commit()

