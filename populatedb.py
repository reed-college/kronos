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

db.session.add(emma)
db.session.add(richard)
db.session.add(manon)
db.session.add(knar)
db.session.add(syd)
db.session.add(miriam)
db.session.add(sarah)
db.session.add(arthur)

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
oral11 = Oral(emma, pearson, 'Oral_Emma', '20160502 10:00:00 AM', '20160502 12:00:00 PM', griffinj)
oral12 = Oral(emma, becker, 'Oral_Emma', '20160502 10:00:00 AM', '20160502 12:00:00 PM', griffinj)
oral13 = Oral(emma, hovda, 'Oral_Emma', '20160502 10:00:00 AM', '20160502 12:00:00 PM', griffinj)
oral14 = Oral(emma, somda, 'Oral_Emma', '20160502 10:00:00 AM', '20160502 12:00:00 PM', griffinj)

oral21 = Oral(richard, becker, 'Oral_Richard', '20160502 03:00:00 PM', '20160502 05:00:00 PM', griffinj)
oral22 = Oral(richard, gruber, 'Oral_Richard', '20160502 03:00:00 PM', '20160502 05:00:00 PM', griffinj)
oral23 = Oral(richard, minardi, 'Oral_Richard', '20160502 03:00:00 PM', '20160502 05:00:00 PM', griffinj)
oral24 = Oral(richard, kroll, 'Oral_Richard', '20160502 03:00:00 PM', '20160502 05:00:00 PM', griffinj)

oral31 = Oral(manon, pearson, 'Oral_Manon', '20160503 10:00:00 AM', '20160503 12:00:00 PM', griffinj)
oral32 = Oral(manon, gruber, 'Oral_Manon', '20160503 10:00:00 AM', '20160503 12:00:00 PM', griffinj)
oral33 = Oral(manon, becker, 'Oral_Manon', '20160503 10:00:00 AM', '20160503 12:00:00 PM', griffinj)
oral34 = Oral(manon, witt, 'Oral_Manon', '20160503 10:00:00 AM', '20160503 12:00:00 PM', griffinj)

oral41 = Oral(knar, gruber, 'Oral_Knar', '20160503 01:00:00 PM', '20160503 03:00:00 PM', griffinj)
oral42 = Oral(knar, pearson, 'Oral_Knar', '20160503 01:00:00 PM', '20160503 03:00:00 PM', griffinj)
oral43 = Oral(knar, khan, 'Oral_Knar', '20160503 01:00:00 PM', '20160503 03:00:00 PM', griffinj)
oral44 = Oral(knar, bershtein, 'Oral_Knar', '20160503 01:00:00 PM', '20160503 03:00:00 PM', griffinj)

oral51 = Oral(syd, becker, 'Oral_Syd', '20160503 03:00:00 PM', '20160503 05:00:00 PM', griffinj)
oral52 = Oral(syd, pearson, 'Oral_Syd', '20160503 03:00:00 PM', '20160503 05:00:00 PM', griffinj)
oral53 = Oral(syd, ditter, 'Oral_Syd', '20160503 03:00:00 PM', '20160503 05:00:00 PM', griffinj)
oral54 = Oral(syd, makley, 'Oral_Syd', '20160503 03:00:00 PM', '20160503 05:00:00 PM', griffinj)

oral61 = Oral(miriam, gruber, 'Oral_Miriam', '20160504 01:00:00 PM', '20160504 03:00:00 PM', griffinj)
oral62 = Oral(miriam, becker, 'Oral_Miriam', '20160504 01:00:00 PM', '20160504 03:00:00 PM', griffinj)
oral63 = Oral(miriam, hancock, 'Oral_Miriam', '20160504 01:00:00 PM', '20160504 03:00:00 PM', griffinj)
oral64 = Oral(miriam, faletra, 'Oral_Miriam', '20160504 01:00:00 PM', '20160504 03:00:00 PM', griffinj)

oral71 = Oral(sarah, pearson, 'Oral_Sarah', '20160505 10:00:00 AM', '20160505 12:00:00 PM', griffinj)
oral72 = Oral(sarah, gruber, 'Oral_Sarah', '20160505 10:00:00 AM', '20160505 12:00:00 PM', griffinj)
oral73 = Oral(sarah, mckinney, 'Oral_Sarah', '20160505 10:00:00 AM', '20160505 12:00:00 PM', griffinj)
oral74 = Oral(sarah, simpson, 'Oral_Sarah', '20160505 10:00:00 AM', '20160505 12:00:00 PM', griffinj)

oral81 = Oral(arthur, gruber, 'Oral_Arthur', '20160505 03:00:00 PM', '20160505 05:00:00 PM', griffinj)
oral82 = Oral(arthur, pearson, 'Oral_Arthur', '20160505 03:00:00 PM', '20160505 05:00:00 PM', griffinj)
oral83 = Oral(arthur, becker, 'Oral_Arthur', '20160505 03:00:00 PM', '20160505 05:00:00 PM', griffinj)
oral84 = Oral(arthur, luker, 'Oral_Arthur', '20160505 03:00:00 PM', '20160505 05:00:00 PM', griffinj)

db.session.add(oral11)
db.session.add(oral12)
db.session.add(oral13)
db.session.add(oral14)

db.session.add(oral21)
db.session.add(oral22)
db.session.add(oral23)
db.session.add(oral24)

db.session.add(oral31)
db.session.add(oral32)
db.session.add(oral33)
db.session.add(oral34)

db.session.add(oral41)
db.session.add(oral42)
db.session.add(oral43)
db.session.add(oral44)

db.session.add(oral51)
db.session.add(oral52)
db.session.add(oral53)
db.session.add(oral54)

db.session.add(oral61)
db.session.add(oral62)
db.session.add(oral63)
db.session.add(oral64)

db.session.add(oral71)
db.session.add(oral72)
db.session.add(oral73)
db.session.add(oral74)

db.session.add(oral81)
db.session.add(oral82)
db.session.add(oral83)
db.session.add(oral84)

# Made-up Events

event1 = Event('at home', '20160502 08:00:00 AM', '20160502 10:00:00 AM', pearson)
event2 = Event('out of town', '20160506 10:00:00 AM', '20160506 10:00:00 PM', pearson, private = False)

db.session.add(event1)
db.session.add(event2)

db.session.commit()

