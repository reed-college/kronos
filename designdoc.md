## Ross's paraphrasing of Kim's ideas

> The basic problem is that finding third and fourth readers for a given thesis
> can be an enormous pain. Kim Kadas describes the current process like so:

> > The Faculty Administrative Coordinators are currently creating the
> > schedules in different applications (i.e. Word, Excel) and in a variety of
> > formats and distributing them to each other, CEP, Dean of Faculty,
> > Present's Office, our Departments, and the Registrar's Office.
>
> So that sounds rough as hell. What's needed is a centralized, and comparatively
> authoritative, way of finding third and fourth readers. That is: for all the
> people using the system, checking the system should tell you if someone is free
> or not, and should be Correct. 
>
> Kim imagines this being a database that FACs would enter data in to and query;
> I suspect we can do better, but starting there for a first pass could work.
> Eventually, if a professor has an up-to-date Google Calendar or iCalendar, they
> ought to be able to load that information in and have the System produce a
> reasonable notion of when that person is available. 
>
> One could also imagine a way for students to browse professors by availability
> and send requests to them for scheduling.

## Design Notes

* This will take in google calendars and icals for proffessors and the determine what times they are free during orals week.
* There will be an interface to see what proffessors under certain departments or other criteria are free at a certain time.
* Also it will be able to tell what times some amount of proffessors are all free. 
* There should be a way to for someone(FAC or Student, idk) to schedule a proffessor for a oral and make them no longer show up as available during that time
 
## Tenative Database layout
Professors/people
| Column Name |    Type     |
|-------------|-------------|
| Name        | varchar(50) |
| email       | varchar(80) |
Orals
| Column Name | Type |
|-------------|------|

