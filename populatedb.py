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
oral1 = Oral(emma, 'Oral_Emma', '20160502 10:00:00 AM', '20160502 12:00:00 PM', griffinj)
oral1.readers = [pearson, becker, hovda, somda]

oral2 = Oral(richard, 'Oral_Richard', '20160502 03:00:00 PM', '20160502 05:00:00 PM', griffinj)
oral2.readers = [becker, gruber, minardi, kroll]
 
oral3 = Oral(manon, 'Oral_Manon', '20160503 10:00:00 AM', '20160503 12:00:00 PM', griffinj)
oral3.readers = [pearson, gruber, becker, witt]
 
oral4 = Oral(knar, 'Oral_Knar', '20160503 01:00:00 PM', '20160503 03:00:00 PM', griffinj)
oral4.readers = [gruber, pearson, khan, bershtein]
 
oral5 = Oral(syd, 'Oral_Syd', '20160503 03:00:00 PM', '20160503 05:00:00 PM', griffinj)
oral5.readers = [becker, pearson, ditter, makley]
 
oral6 = Oral(miriam, 'Oral_Miriam', '20160504 01:00:00 PM', '20160504 03:00:00 PM', griffinj)
oral6.readers = [gruber, becker, hancock, faletra]
 
oral7 = Oral(sarah, 'Oral_Sarah', '20160505 10:00:00 AM', '20160505 12:00:00 PM', griffinj)
oral7.readers = [pearson]

oral8 = Oral(arthur, 'Oral_Arthur', '20160505 03:00:00 PM', '20160505 05:00:00 PM', griffinj)
oral8.readers = [gruber, pearson, becker, luker]

oral9 = Oral(edmond, 'Oral_Edmond', '20160502 10:00:00 AM', '20160502 12:00:00 PM', griffinj)
oral9.readers = [bershtein, gruber, faletra, minardi]

db.session.add(oral1)
db.session.add(oral2)
db.session.add(oral3)
db.session.add(oral4)
db.session.add(oral5)
db.session.add(oral6)
db.session.add(oral7)
db.session.add(oral8)
db.session.add(oral9)

# Made-up Events

event1 = Event('at home', '20160502 08:00:00 AM', '20160502 10:00:00 AM', pearson)
event2 = Event('out of town', '20160506 10:00:00 AM', '20160506 10:00:00 PM', pearson, private = False)

db.session.add(event1)
db.session.add(event2)

db.session.commit()

