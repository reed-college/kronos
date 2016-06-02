from kronos import db
from kronos.models import FAC, Stu, Prof, Oral, Event

db.create_all()


# FACs

gonyerk = FAC('gonyerk', 'Kristy', 'asdf', 'gonyerk@reed.edu')
griffinj = FAC('griffinj', 'Jolie', 'asdf', 'griffinj@reed.edu')


# Linguistic Seniors

emma = Stu('erennie', 'Emma Rennie', '123', 'erennie@reed.edu', 'Linguistics', 'Philosophy, Religion, Psychology and Linguistics')
richard = Stu('adcockr', 'Richard Adcock', 'asd', 'adcockr@reed.edu', 'Linguistics', 'Philosophy, Religion, Psychology and Linguistics')
manon = Stu('gilmorem', 'Manon Gilmore', 'sdf', 'gilmorem@reed.edu', 'Linguistics', 'Philosophy, Religion, Psychology and Linguistics')
knar = Stu('knhovakim', 'Knar', 'asdf', 'knhovakim@reed.edu', 'Linguistics', 'Philosophy, Religion, Psychology and Linguistics')
syd = Stu('lows', 'Syd', 'asdf', 'lows@reed.edu', 'Linguistics', 'Philosophy, Religion, Psychology and Linguistics')
miriam = Stu('golzm', 'Miriam', 'asdf', 'golzm@reed.edu', 'Linguistics', 'Philosophy, Religion, Psychology and Linguistics')
sarah = Stu('allens', 'Sarah', 'asdf', 'allens@reed.edu', 'Linguistics', 'Philosophy, Religion, Psychology and Linguistics')
arthur = Stu('sillersa', 'Arthur', 'asdf', 'sillersa@reed.edu', 'Linguistics', 'Philosophy, Religion, Psychology and Linguistics')


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


# Orals

oral1 = Oral(emma, [pearson, becker, hovda, somda], 'Oral_Emma', '20160502 10:00:00 AM', '20160502 12:00:00 PM', griffinj)
oral2 = Oral(richard, [becker, gruber, minardi, kroll], 'Oral_Richard', '20160502 03:00:00 PM', '20160502 05:00:00 PM', griffinj)
oral3 = Oral(manon, [pearson, gruber, becker, witt], 'Oral_Manon', '20160503 10:00:00 AM', '20160503 12:00:00 PM', griffinj)
oral4 = Oral(knar, [gruber, pearson, khan, bershtein], 'Oral_Knar', '20160503 01:00:00 PM', '20160503 03:00:00 PM', griffinj)
oral5 = Oral(syd, [becker, pearson, ditter, makley], 'Oral_Syd', '20160503 03:00:00 PM', '20160503 05:00:00 PM', griffinj)
oral6 = Oral(miriam, [gruber, becker, hancock, faletra], 'Oral_Miriam', '20160504 01:00:00 PM', '20160504 03:00:00 PM', griffinj)
oral7 = Oral(sarah, [pearson, gruber, mckinney, simpson], 'Oral_Sarah', '20160505 10:00:00 AM', '20160505 12:00:00 PM', griffinj)
oral8 = Oral(arthur, [gruber, pearson, becker, luker], 'Oral_Arthur', '20160505 03:00:00 PM', '20160505 05:00:00 PM', griffinj) 


# Made-up Events
# self, summary, dtstart, dtend, user, private = True

event1 = Event('at home', '20160502 08:00:00 AM', '20160502 10:00:00 AM', pearson)
event2 = Event('out of town', '20160506 10:00:00 AM', '20160506 10:00:00 PM', pearson, private = False)


