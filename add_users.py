"""
adds profs,stus and FACs from ldap
"""
import ldap3
from string import ascii_lowercase
from kronos.models import FAC, Stu, Prof
from kronos import db
db.create_all()

server = ldap3.Server('ldap.reed.edu', port=389, get_info=ldap3.ALL)
conn = ldap3.Connection(server, auto_bind=True)
# syntax for the filter outlined at
# http://ldap3.readthedocs.io/tutorial.html#performing-searches
query='ou=people,dc=reed,dc=edu'
filter=  '(&'
filter +=  '(|'
filter +=    '(&'
filter +=      '(eduPersonPrimaryAffiliation=student)'
filter +=      '(!(eduPersonAffiliation=alumni))'
filter +=    ')'
filter +=    '(eduPersonPrimaryAffiliation=faculty)'
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
        if att.get('eduPersonPrimaryAffiliation') == 'faculty':
            

