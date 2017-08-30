# Flask Simple Login Examples

In this folder there are 2 examples:

The `simple_app.py`

A simple example using a Python dictionaty as user database and storing
passwords as plain text.

Run with:

```bash
python simple_app.py
```

The `manage.py`

A complete application using Flask factories, click commands and storing
passwords encrypted in a json file `users.json` which you can easily take
as example to replace with your own database manager.

> NOTE: this example is not meant for production use as writing in a json file
> is suitable only for single access. Go with MongoDb, TinyDB or other SGDB.

Run with:

```bash
python manage.py
```

Create new user:

```bash
python manage.py adduser
```

Run the server

```bash
python manage.py runserver
```


