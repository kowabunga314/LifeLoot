# LifeLoot
Life Tracker for Magic the Gathering


<h3>I don't have a lot of time to write this readme so here:</h3>

Run these commands from the app directory:
<br>
<code>
  pip install -r requirements.txt
</code>
<br>
<code>
  uvicorn app.main:app --reload
</code>

Find the docs on your local session at [this address](http://localhost:8000/docs)


<h3>How to upgrade DB</h3>
<br>
<code>alembic revision -m "<\a message about your commit>" --autogenerate</code>
<br>
<code>alembic upgrade head</code>


<h3>To launch the app, go to clone project and specify the github address, not sure if the other stuff in here will break it that way<h3>
