#===========================================================
# YOUR PROJECT TITLE HERE
# YOUR NAME HERE
#-----------------------------------------------------------
# BRIEF DESCRIPTION OF YOUR PROJECT HERE
#===========================================================

from flask import Flask, render_template, request, flash, redirect
import html

from app.helpers.session import init_session
from app.helpers.db      import connect_db
from app.helpers.errors  import init_error, not_found_error
from app.helpers.logging import init_logging
from app.helpers.time    import init_datetime, utc_timestamp, utc_timestamp_now


# Create the app
app = Flask(__name__)

# Configure app
init_session(app)   # Setup a session for messages, etc.
init_logging(app)   # Log requests
init_error(app)     # Handle errors and exceptions
init_datetime(app)  # Handle UTC dates in timestamps


#-----------------------------------------------------------
# Event list page route
#-----------------------------------------------------------
@app.get("/")
def index():
    with connect_db() as client:
        sql = "SELECT * FROM events ORDER BY date ASC"
        params=[]
        result = client.execute(sql, params)
        events = result.rows
        print(events)
        
        sql = """
            SELECT 
                involved.event_id,
                people.name 
            FROM people
            JOIN involved ON people.id = involved.people_id 
            ORDER BY people.name ASC
        """
        params=[]
        result = client.execute(sql, params)
        people = result.rows
        print(people)
        
    return render_template("pages/event_list.jinja", events=events, people=people)


#-----------------------------------------------------------
# People list page route
#-----------------------------------------------------------
@app.get("/people_list")
def people():
    with connect_db() as client:
        sql = "SELECT id, name FROM people ORDER BY name ASC"
        params=[]
        result = client.execute(sql, params)
        people = result.rows
        print(people)

    return render_template("pages/people_list.jinja", people=people)


#-----------------------------------------------------------
# Event info page route
#-----------------------------------------------------------
@app.get("/event_info/<int:id>")
def e_info(id):
    with connect_db() as client:
        sql = "SELECT * FROM events WHERE id=?"
        params=[id]
        result = client.execute(sql, params)
        event = result.rows[0]
        print(event)
        
        sql = """
            SELECT 
                involved.event_id,
                people.name 
            FROM people
            JOIN involved ON people.id = involved.people_id 
            ORDER BY people.name ASC
        """
        params=[]
        result = client.execute(sql, params)
        people = result.rows
        print(people)
        
    return render_template("pages/event_info.jinja", event=event, people=people)


#-----------------------------------------------------------
# People info page route
#-----------------------------------------------------------
@app.get("/people_info/<int:id>")
def p_info(id):
    with connect_db() as client:
        sql = "SELECT * FROM people WHERE id=?"
        params=[id]
        result = client.execute(sql, params)
        person = result.rows[0]
        print(person)
        
        sql = """
            SELECT
                involved.people_id,
                events.name
            FROM events
            JOIN involved ON events.id = involved.event_id
            ORDER BY events.name ASC
        """
        params=[]
        result = client.execute(sql, params)
        events = result.rows
        print(events)
        
    return render_template("pages/people_info.jinja", person=person, events=events)


#-----------------------------------------------------------
# Event form page route
#-----------------------------------------------------------
@app.get("/event_form")
def e_form():
    return render_template("pages/event_form.jinja")


#-----------------------------------------------------------
# Person form page route
#-----------------------------------------------------------
@app.get("/people_form")
def p_form():
    return render_template("pages/people_form.jinja")