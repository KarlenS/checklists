# Introduction

This is the repository for VERITAS **start of night** and **end of night** forms website (see VERITAS internal wiki page for the link).
The site live syncs between all users, provided the users are logged in to the same date. In addition, all responses are automatically saved to a database.

# Setup

Requirements:
* MySQL or MongoDB database
* Python packages in requirements.txt

# Website components

## Frontend

### Style
[Bootstrap](http://getbootstrap.com) is used for styling, with [custom material-design checkboxes/switches](http://bootsnipp.com/snippets/featured/material-design-switch).

### Javascript/JQuery
Progress bar shows number of items checked out of total (also updated between users).

[Toastr](https://codeseven.github.io/toastr/) is used for alerts.


## Backend

### Flask-socketio
The site uses websockets from [flask-SocketIO](https://flask-socketio.readthedocs.org), which constantly listens for specific client actions and respond by communicating certain actions to all clients.

### Database
A [Mongo] (https://www.mongodb.org/) or [MySQL] (https://www.mysql.com/) database stores form responses and is used to update all clients. 
Each entry tracks the date, user, checkbox id & state, and a comment box.
