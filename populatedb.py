import datetime
from kronos import db
from kronos.models import FAC, Stu, Prof, Oral, Event, OralStartDay

db.create_all()


# FACs

gonyerk = FAC('gonyerk', 'Kristy', 'gonyerk@reed.edu')
griffinj = FAC('griffinj', 'Jolie', 'griffinj@reed.edu')

db.session.add(gonyerk)
db.session.add(griffinj)

# Linguistic Seniors

emma = Stu('erennie', 'Emma Rennie', 'erennie@reed.edu')
richard = Stu('adcockr', 'Richard Adcock', 'adcockr@reed.edu')
manon = Stu('gilmorem', 'Manon Gilmore', 'gilmorem@reed.edu')
knar = Stu('knhovakim', 'Knar', 'knhovakim@reed.edu')
syd = Stu('lows', 'Syd', 'lows@reed.edu')
miriam = Stu('golzm', 'Miriam', 'golzm@reed.edu')
sarah = Stu('allens', 'Sarah', 'allens@reed.edu')
arthur = Stu('sillersa', 'Arthur', 'sillersa@reed.edu')

# 1 Russian Senior so that we have 2 orals at the same time

edmond = Stu('eedmonds', 'Edmond Soun', 'eedmonds@reed.edu')

# Made up Senior

jon = Stu('snowj', 'Jon Snow', 'snowj@reed.edu')

db.session.add(emma)
db.session.add(richard)
db.session.add(manon)
db.session.add(knar)
db.session.add(syd)
db.session.add(miriam)
db.session.add(sarah)
db.session.add(arthur)
db.session.add(edmond)
db.session.add(jon)

# Profs

hovda = Prof('hovdap', 'Paul Hovda', 'hovdap@reed.edu', 'Philosophy', 'Philosophy, Religion, Psychology, and Linguistics')
hancock = Prof('hancockv', 'Ginny', 'hancockv@reed.edu', 'Music', 'The Arts')
pearson = Prof('pearson', 'Pearson', 'pearson@reed.edu', 'Linguistics', 'Philosophy, Religion, Psychology, and Linguistics')
becker = Prof('becker', 'becker', 'becker@reed.edu', 'Linguistics', 'Philosophy, Religion, Psychology, and Linguistics')
somda = Prof('somda', 'Somda', 'somda@reed.edu', 'English', 'Literature and Languages')
gruber = Prof('guber', 'Gruber', 'gruber@reed.edu', 'Linguistics', 'Philosophy, Religion, Psychology, and Linguistics')
faletra = Prof('faletra', 'Faletra', 'faletra@reed.edu', 'English', 'Literature and Languages')
minardi = Prof('minardi', 'Margot', 'minardi@reed.edu', 'History', 'Literature and Languages')
kroll = Prof('chkroll', 'Christian', 'chkroll@reed.edu', 'Spanish', 'Literature and Languages')
witt = Prof('wittc', 'Catherine', 'wittc@reed.edu', 'French', 'Literature and Languages')
khan = Prof('skhan', 'Sameer', 'skhan@reed.edu', 'Linguistics', 'Philosophy, Religion, Psychology, and Linguistics')
bershtein = Prof('bershtee', 'Zhenya', 'bershtee@reed.edu', 'Russian', 'Literature and Languages')
ditter = Prof('dittera', 'Alexei', 'dittera@reed.edu', 'Chinese', 'Literature and Languages')
makley = Prof('makleyc', 'Charlene', 'makleyc@reed.edu', 'Anthropology', 'History and Social Sciences')
mckinney = Prof('mckinnek', 'Katy', 'mckinnek@reed.edu', 'English', 'Literature and Languages')
simpson = Prof('dsimpson', 'Dustin', 'dsimpson@reed.edu', 'English', 'Literature and Languages')
luker = Prof('mluker', 'Morgan', 'mluker@reed.edu', 'Music', 'The Arts')

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

# Made-up Events
# Note that personal events must be added before orals in order to get the validator to work.

event1 = Event('at home', datetime.datetime(2016,5,2,8), datetime.datetime(2016,5,2,9), pearson)
event2 = Event('out of town', datetime.datetime(2016,5,6,10), datetime.datetime(2016,5,6,22), pearson, private = False)
# event3 = Event('not doing much now', datetime.datetime(2016,5,6,11), datetime.datetime(2016,5,6,10), hovda, private = False)

db.session.add(event1)
db.session.add(event2)
# db.session.add(event3)

# Orals
oral1 = Oral(emma, 'Oral_Emma', datetime.datetime(2016,5,2,10), datetime.datetime(2016,5,2,12), 'Linguistics', 'Philosophy, Religion, Psychology, and Linguistics', griffinj)
oral1.readers = [pearson, becker, hovda, somda]

oral2 = Oral(richard, 'Oral_Richard', datetime.datetime(2016,5,2,15), datetime.datetime(2016,5,2,17), 'Linguistics', 'Philosophy, Religion, Psychology, and Linguistics', griffinj)
oral2.readers = [becker, gruber, minardi, kroll]
 
oral3 = Oral(manon, 'Oral_Manon', datetime.datetime(2016,5,3,10), datetime.datetime(2016,5,3,12), 'Linguistics', 'Philosophy, Religion, Psychology, and Linguistics', griffinj)
oral3.readers = [pearson, gruber, becker, witt]
 
oral4 = Oral(knar, 'Oral_Knar', datetime.datetime(2016,5,3,13), datetime.datetime(2016,5,3,15), 'Linguistics', 'Philosophy, Religion, Psychology, and Linguistics', griffinj)
oral4.readers = [gruber, pearson, khan, bershtein]
 
oral5 = Oral(syd, 'Oral_Syd', datetime.datetime(2016,5,3,15), datetime.datetime(2016,5,3,17), 'Linguistics', 'Philosophy, Religion, Psychology, and Linguistics', griffinj)
oral5.readers = [becker, pearson, ditter, makley]
 
oral6 = Oral(miriam, 'Oral_Miriam', datetime.datetime(2016,5,4,13), datetime.datetime(2016,5,4,15), 'Linguistics', 'Philosophy, Religion, Psychology, and Linguistics', griffinj)
oral6.readers = [gruber, becker, hancock, faletra]
 
oral7 = Oral(sarah, 'Oral_Sarah', datetime.datetime(2016,5,5,10), datetime.datetime(2016,5,5,12), 'Linguistics', 'Philosophy, Religion, Psychology, and Linguistics', griffinj)
oral7.readers = [pearson]

oral8 = Oral(arthur, 'Oral_Arthur', datetime.datetime(2016,5,5,15), datetime.datetime(2016,5,5,17), 'Linguistics', 'Philosophy, Religion, Psychology, and Linguistics', griffinj)
oral8.readers = [gruber, pearson, becker, luker]

oral9 = Oral(edmond, 'Oral_Edmond', datetime.datetime(2016,5,2,10), datetime.datetime(2016,5,2,12), 'Russian', 'Literature and Languages', griffinj)
oral9.readers = [bershtein, gruber, faletra, minardi]

oral10 = Oral(jon, 'Oral_Jon', datetime.datetime(2016,5,6,10), datetime.datetime(2016,5,6,12), 'Physics', 'Mathematics and Natural Sciences', griffinj)
oral10.readers = [hovda]

# made-up orals for testing validators.
# oral10 = Oral(emma, 'Oral_test', datetime.datetime(2016,5,2,10), datetime.datetime(2016,5,2,12), 'Linguistics', 'Philosophy, Religion, Psychology, and Linguistics', griffinj)
# oral10.readers = [pearson, becker, hovda, somda]

# oral11 = Oral(emma, 'Oral_test', datetime.datetime(2016,6,1,10), datetime.datetime(2016,6,1,12), 'Linguistics', 'Philosophy, Religion, Psychology, and Linguistics', griffinj)
# oral11.readers = [pearson, ditter, minardi, witt]


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
# db.session.add(oral11)

s16 = OralStartDay("Spring 2016", datetime.date(2016, 5,  2)) 
f16 = OralStartDay("Fall 2016",   datetime.date(2016, 12, 8))
s17 = OralStartDay("Spring 2017", datetime.date(2017, 5,  1)) 
f17 = OralStartDay("Fall 2017",   datetime.date(2017, 12, 7))
s18 = OralStartDay("Spring 2018", datetime.date(2018, 4,  30)) 

db.session.add(s16)
db.session.add(f16)
db.session.add(s17)
db.session.add(f17)
db.session.add(s18)

db.session.commit()

