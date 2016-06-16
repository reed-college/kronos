import datetime
from kronos import db
from kronos.models import FAC, Stu, Prof, Oral, Event

db.create_all()


# FACs

gonyerk = FAC('gonyerk', 'Kristy', 'asdf', 'gonyerk@reed.edu')
griffinj = FAC('griffinj', 'Jolie', 'asdf', 'griffinj@reed.edu')

db.session.add(gonyerk)
db.session.add(griffinj)

# Linguistic Seniors

emma = Stu('erennie', 'Emma Rennie', '123', 'erennie@reed.edu', 'Linguistics', 'Philosophy, Religion, Psychology and Linguistics')
richard = Stu('adcockr', 'Richard Adcock', 'asd', 'adcockr@reed.edu', 'Linguistics', 'Philosophy, Religion, Psychology and Linguistics')
manon = Stu('gilmorem', 'Manon Gilmore', 'sdf', 'gilmorem@reed.edu', 'Linguistics', 'Philosophy, Religion, Psychology and Linguistics')
knar = Stu('knhovakim', 'Knar', 'asdf', 'knhovakim@reed.edu', 'Linguistics', 'Philosophy, Religion, Psychology and Linguistics')
syd = Stu('lows', 'Syd', 'asdf', 'lows@reed.edu', 'Linguistics', 'Philosophy, Religion, Psychology and Linguistics')
miriam = Stu('golzm', 'Miriam', 'asdf', 'golzm@reed.edu', 'Linguistics', 'Philosophy, Religion, Psychology and Linguistics')
sarah = Stu('allens', 'Sarah', 'asdf', 'allens@reed.edu', 'Linguistics', 'Philosophy, Religion, Psychology and Linguistics')
arthur = Stu('sillersa', 'Arthur', 'asdf', 'sillersa@reed.edu', 'Linguistics', 'Philosophy, Religion, Psychology and Linguistics')

# 1 Russian Senior so that we have 2 orals at the same time

edmond = Stu('eedmonds', 'Edmond Soun', 'pass', 'eedmonds@reed.edu', 'Russian', 'Literature and Languages')

db.session.add(emma)
db.session.add(richard)
db.session.add(manon)
db.session.add(knar)
db.session.add(syd)
db.session.add(miriam)
db.session.add(sarah)
db.session.add(arthur)
db.session.add(edmond)

# Profs

hovda = Prof('hovdap', 'Paul Hovda', 'asdf', 'hovdap@reed.edu', 'Philosophy', 'Philosophy, Religion, Psychology and Linguistics')
hancock = Prof('hancockv', 'Ginny', 'asdf', 'hancockv@reed.edu', 'Music', 'The Arts')
pearson = Prof('pearson', 'Pearson', 'asdf', 'pearson@reed.edu', 'Linguistics', 'Philosophy, Religion, Psychology and Linguistics')
becker = Prof('becker', 'becker', 'asdf', 'becker@reed.edu', 'Linguistics', 'Philosophy, Religion, Psychology and Linguistics')
somda = Prof('somda', 'Somda', 'asdf', 'somda@reed.edu', 'English', 'Literature and Languages')
gruber = Prof('guber', 'Gruber', 'asdf', 'gruber@reed.edu', 'Linguistics', 'Philosophy, Religion, Psychology and Linguistics')
faletra = Prof('faletra', 'Faletra', 'asdf', 'faletra@reed.edu', 'English', 'Literature and Languages')
minardi = Prof('minardi', 'Margot', 'asdf', 'minardi@reed.edu', 'History', 'Literature and Languages')
kroll = Prof('chkroll', 'Christian', 'asdf', 'chkroll@reed.edu', 'Spanish', 'Literature and Languages')
witt = Prof('wittc', 'Catherine', 'asdf', 'wittc@reed.edu', 'French', 'Literature and Languages')
khan = Prof('skhan', 'Sameer', 'asdf', 'skhan@reed.edu', 'Linguistics', 'Philosophy, Religion, Psychology and Linguistics')
bershtein = Prof('bershtee', 'Zhenya', 'asdf', 'bershtee@reed.edu', 'Russian', 'Literature and Languages')
ditter = Prof('dittera', 'Alexei', 'asdf', 'dittera@reed.edu', 'Chinese', 'Literature and Languages')
makley = Prof('makleyc', 'Charlene', 'asdf', 'makleyc@reed.edu', 'Anthropology', 'History and Social Sciences')
mckinney = Prof('mckinnek', 'Katy', 'asdf', 'mckinnek@reed.edu', 'English', 'Literature and Languages')
simpson = Prof('dsimpson', 'Dustin', 'asdf', 'dsimpson@reed.edu', 'English', 'Literature and Languages')
luker = Prof('mluker', 'Morgan', 'asdf', 'mluker@reed.edu', 'Music', 'The Arts')

db.session.add(hovda)
db.session.add(hancock)
db.session.add(pearson)
db.session.add(becker)
db.session.add(somda)
db.session.add(gruber)
db.session.add(faletra)
db.session.add(minardi)
db.session.add(kroll)
db.session.add(witt)
db.session.add(khan)
db.session.add(bershtein)
db.session.add(ditter)
db.session.add(makley)
db.session.add(mckinney)
db.session.add(simpson)
db.session.add(luker)

# Orals
oral1 = Oral(emma, 'Oral_Emma', datetime.datetime(2016,5,2,10), datetime.datetime(2016,5,2,12), griffinj)
oral1.readers = [pearson, becker, hovda, somda]

oral2 = Oral(richard, 'Oral_Richard', datetime.datetime(2016,5,2,15), datetime.datetime(2016,5,2,17), griffinj)
oral2.readers = [becker, gruber, minardi, kroll]
 
oral3 = Oral(manon, 'Oral_Manon', datetime.datetime(2016,5,3,10), datetime.datetime(2016,5,3,12), griffinj)
oral3.readers = [pearson, gruber, becker, witt]
 
oral4 = Oral(knar, 'Oral_Knar', datetime.datetime(2016,5,3,13), datetime.datetime(2016,5,3,15), griffinj)
oral4.readers = [gruber, pearson, khan, bershtein]
 
oral5 = Oral(syd, 'Oral_Syd', datetime.datetime(2016,5,3,15), datetime.datetime(2016,5,3,17), griffinj)
oral5.readers = [becker, pearson, ditter, makley]
 
oral6 = Oral(miriam, 'Oral_Miriam', datetime.datetime(2016,5,4,13), datetime.datetime(2016,5,4,15), griffinj)
oral6.readers = [gruber, becker, hancock, faletra]
 
oral7 = Oral(sarah, 'Oral_Sarah', datetime.datetime(2016,5,5,10), datetime.datetime(2016,5,5,12), griffinj)
oral7.readers = [pearson]

oral8 = Oral(arthur, 'Oral_Arthur', datetime.datetime(2016,5,5,15), datetime.datetime(2016,5,5,17), griffinj)
oral8.readers = [gruber, pearson, becker, luker]

oral9 = Oral(edmond, 'Oral_Edmond', datetime.datetime(2016,5,2,10), datetime.datetime(2016,5,2,12), griffinj)
oral9.readers = [bershtein, gruber, faletra, minardi]

# made-up oral just for testing
oral10 = Oral(emma, 'Oral_test', datetime.datetime(2016,5,2,10), datetime.datetime(2016,5,2,12), griffinj)
oral10.readers = [pearson, becker, hovda, somda]


db.session.add(oral1)
db.session.add(oral2)
db.session.add(oral3)
db.session.add(oral4)
db.session.add(oral5)
db.session.add(oral6)
db.session.add(oral7)
db.session.add(oral8)
db.session.add(oral9)
db.session.add(oral10)

# Made-up Events

event1 = Event('at home', datetime.datetime(2016,5,2,8), datetime.datetime(2016,5,2,10), pearson)
event2 = Event('out of town', datetime.datetime(2016,5,6,10), datetime.datetime(2016,5,6,22), pearson, private = False)
# event3 = Event('not doing much now', datetime.datetime(2016,5,6,11), datetime.datetime(2016,5,6,10), hovda, private = False)

db.session.add(event1)
db.session.add(event2)
# db.session.add(event3)

db.session.commit()

