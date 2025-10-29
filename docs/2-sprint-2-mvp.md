# Sprint 2 - A Minimum Viable Product (MVP)


## Sprint Goals

Develop a bare-bones, working web application that provides the key functionality of the system, then test and refine it so that it can serve as the basis for the final phase of development in Sprint 3.


---

## Implemented Database Schema

Replace this text with notes regarding the DB schema.

![SCREENSHOT OF DB SCHEMA](screenshots/example.png)


---

## Initial Implementation

The key functionality of the web app was implemented:


![SCREENSHOT OF A LIST OF EVENTS](screenshots/eventlist.png)
![SCREENSHOT OF A LIST OF PEOPLE](screenshots/peoplelist.png)
![SCREENSHOT OF AN INFO PAGE FOR AN EVENT](screenshots/eventinfobase.png)
![SCREENSHOT OF AN INFO PAGE FOR A EVENT](screenshots/peopleinfobase.png)

---

## Testing if the website can edit pre-existing data

I need to make sure that the form will be pre-filled with all of the current information, then updates the database depending on what you changed, and I will need to test this for both people and events. Both seem to work, but canceling the action of editing a person takes you to the wrong page

![SCREENSHOT OF A LIST OF PEOPLE](screenshots/editevent1.png)
![SCREENSHOT OF AN INFO PAGE FOR AN EVENT](screenshots/editevent2.png)
![SCREENSHOT OF AN INFO PAGE FOR A EVENT](screenshots/eventinfoedit.png)


### Changes / Improvements

Canceling editing a person now takes you back to that person's info page


---

## Testing If you can add new events/people

I need to make sure everything gets added to the table for both people and events. This worked with no visible issues.

![SCREENSHOT OF THE ADD EVENT PAGE](screenshots/addevent1.png)
![SCREENSHOT OF THE ADD EVENT PAGE](screenshots/addevent2.png)
![SCREENSHOT OF THE NEWLY ADDED EVENT](screenshots/eventlistadd.png)
![SCREENSHOT OF THE ADD PERSON PAGE](screenshots/peopleadd.png)
![SCREENSHOT OF THE NEWLY ADDED PERSON](screenshots/peoplelistadd.png)


---

## Testing the assign people feature

There should be a dropdown menu here to select people to assign to a newly created event, this worked without issue.

![SCREENSHOT OF THE ASSIGN PERSON PAGE](screenshots/assignpeople1.png)
![SCREENSHOT OF THE ASSIGN PERSON PAGE](screenshots/assignpeople2.png)


---

## Testing the add and remove event buttons on the people info page

There are two dropdown menus, one to add an event, one to remove, both function well.

![SCREENSHOT OF A PERSON'S INFO PAGE](screenshots/peopleinfobase.png)
![SCREENSHOT OF AN EVENT BEING ADDED](screenshots/peopleinfoadd.png)
![SCREENSHOT OF AN EVENT BEING REMOVED](screenshots/peopleinforemove1.png)
![SCREENSHOT OF AN EVENT BEING REMOVED](screenshots/peopleinforemove2.png)


---

## Testing if you can delete stuff

Deleting works fine, but may be done on accident



### Changes / Improvements

I added a confirmation message
![SCREENSHOT OF THE DELETION CONFIRMATION MESSAGE](screenshots/peopledelete.png)


---

## Sprint Review

I got my website up and running, and even came up with some new features along the way, unfortunately, I had to cut the calendar mode due to time constraints.

