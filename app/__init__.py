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

        sql = """
                SELECT id, name
                FROM events
                
                -- Selects ids of events that are not already involved
                WHERE events.id NOT IN (
                    SELECT involved.event_id
                    FROM involved
                    JOIN people ON involved.people_id = people.id
                    WHERE people.id = ?
                )
            """
        params=[id]
        result = client.execute(sql, params)
        other_events = result.rows

        sql = """
                SELECT id, name
                FROM events
                
                -- Selects ids of events that are involved
                WHERE events.id IN (
                    SELECT involved.event_id
                    FROM involved
                    JOIN people ON involved.people_id = people.id
                    WHERE people.id = ?
                )
            """
        params=[id]
        result = client.execute(sql, params)
        connected_events = result.rows
        
    return render_template("pages/people_info.jinja", person=person, events=events, other_events=other_events, connected_events=connected_events)


#-----------------------------------------------------------
# Delete an event
#-----------------------------------------------------------
@app.get("/delete_event/<int:id>")
def delete_e(id):
    with connect_db() as client:
        sql = "DELETE FROM events WHERE id=?"
        values = [id]
        client.execute(sql, values)
        sql = "DELETE FROM involved WHERE event_id=?"
        values = [id]
        client.execute(sql, values)
        return redirect("/")
    

#-----------------------------------------------------------
# Delete a person
#-----------------------------------------------------------
@app.get("/delete_person/<int:id>")
def delete_p(id):
    with connect_db() as client:
        sql = "DELETE FROM people WHERE id=?"
        values = [id]
        client.execute(sql, values)
        sql = "DELETE FROM involved WHERE people_id=?"
        values = [id]
        client.execute(sql, values)
        return redirect("/")
    

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


#-----------------------------------------------------------
# Add a new event
#-----------------------------------------------------------
@app.post("/add_event")
def add_e():
    with connect_db() as client:
        name = request.form.get("name")
        date = request.form.get("date")
        time = request.form.get("time")
        notes = request.form.get("notes")
        info = request.form.get("info")
        sql = """
            INSERT INTO events (name, date, time, notes, info)
            VALUES (?,?,?,?,?)
        """
        values = [name, date, time, notes, info]
        result = client.execute(sql, values)
        new_event_id = result.last_insert_rowid

        return redirect(f"/event_add_people/{new_event_id}")
    

#-----------------------------------------------------------
# Add people to an event page route
#-----------------------------------------------------------
@app.get("/event_add_people/<int:id>")
def add_p_to_e(id):
    with connect_db() as client:
        sql = "SELECT id, name FROM events WHERE id = ?"
        params=[id]
        result = client.execute(sql, params)

        if result.rows:
            event = result.rows[0]
            
            sql = """
                SELECT 
                    involved.event_id,
                    people.name 
                
                FROM people
                JOIN involved ON people.id = involved.people_id 
                
                WHERE involved.event_id = ?

                ORDER BY people.name ASC
            """
            params=[id]
            result = client.execute(sql, params)
            people = result.rows
            
            sql = """
                SELECT id, name
                FROM people
                
                -- Selects ids of people who are not already involved
                WHERE people.id NOT IN (
                    SELECT involved.people_id
                    FROM involved
                    JOIN events ON involved.event_id = events.id
                    WHERE events.id = ?
                )
            """
            params=[id]
            result = client.execute(sql, params)
            other_people = result.rows
            
        return render_template("pages/event_add_people.jinja", 
                               event=event, 
                               people=people, 
                               other_people=other_people)


#-----------------------------------------------------------
# Assign people to an event
#-----------------------------------------------------------
@app.post("/assign_person/<int:id>")
def assign_p(id):
    with connect_db() as client:

        person = request.form.get("person")
        print(person)
        sql = """
            SELECT id FROM people WHERE name=?
        """
        values=[person]
        result = client.execute(sql, values)
        print(result)
        p_id = result.rows[0][0]


        sql = """
            INSERT INTO involved (event_id, people_id)
            VALUES (?,?)
        """
        values = [id, p_id]
        client.execute(sql, values)
        return redirect(f"/event_add_people/{id}")
    
#-----------------------------------------------------------
# Add a new person
#-----------------------------------------------------------
@app.post("/add_person")
def add_p():
    with connect_db() as client:
        name = request.form.get("name")
        availability = request.form.get("availability")
        sql = """
            INSERT INTO people (name, availability)
            VALUES (?,?)
        """
        values = [name, availability]
        result = client.execute(sql, values)

        return redirect("/people_list")
    
#-----------------------------------------------------------
# Assign an event to a person
#-----------------------------------------------------------
@app.post("/assign_event/<int:id>")
def assign_e(id):
    with connect_db() as client:

        event = request.form.get("event")
        print(event)
        sql = """
            SELECT id FROM events WHERE name=?
        """
        values=[event]
        result = client.execute(sql, values)
        print(result)
        e_id = result.rows[0][0]


        sql = """
            INSERT INTO involved (people_id, event_id)
            VALUES (?,?)
        """
        values = [id, e_id]
        client.execute(sql, values)
        return redirect(f"/people_info/{id}")
    
#-----------------------------------------------------------
# remove an event connection
#-----------------------------------------------------------
@app.post("/remove_event/<int:id>")
def remove_e(id):
    with connect_db() as client:

        event = request.form.get("event")
        print(event)
        sql = """
            SELECT id FROM events WHERE name=?
        """
        values=[event]
        result = client.execute(sql, values)
        print(result)
        e_id = result.rows[0][0]
        sql = "DELETE FROM involved WHERE event_id=?"
        values = [e_id]
        client.execute(sql, values)
        return redirect(f"/people_info/{id}")

#-----------------------------------------------------------
# Edit event page route
#-----------------------------------------------------------
@app.get("/event_edit/<int:id>")
def e_edit(id):
    with connect_db() as client:
        sql = "SELECT * FROM events WHERE id=?"
        params=[id]
        result = client.execute(sql, params)
        event = result.rows[0]
        print(event)
        
    return render_template("pages/event_edit.jinja", event=event)

#-----------------------------------------------------------
# Edit an event
#-----------------------------------------------------------
@app.post("/changing_event/<int:id>")
def change_e(id):
    with connect_db() as client:
        name = request.form.get("name")
        date = request.form.get("date")
        time = request.form.get("time")
        notes = request.form.get("notes")
        info = request.form.get("info")
        sql = """
            UPDATE events SET name=?, date=?, time=?, notes=?, info=? WHERE id=?
        """
        values = [name, date, time, notes, info, id]
        result = client.execute(sql, values)

        return redirect(f"/event_info/{id}")

#-----------------------------------------------------------
# Edit person page route
#-----------------------------------------------------------
@app.get("/person_edit/<int:id>")
def p_edit(id):
    with connect_db() as client:
        sql = "SELECT * FROM people WHERE id=?"
        params=[id]
        result = client.execute(sql, params)
        person = result.rows[0]
        
    return render_template("pages/people_edit.jinja", person=person)

#-----------------------------------------------------------
# Edit a person
#-----------------------------------------------------------
@app.post("/changing_person/<int:id>")
def change_p(id):
    with connect_db() as client:
        name = request.form.get("name")
        availability = request.form.get("availability")
        sql = """
            UPDATE people SET name=?, availability=? WHERE id=?
        """
        values = [name, availability, id]
        result = client.execute(sql, values)

        return redirect(f"/people_info/{id}")