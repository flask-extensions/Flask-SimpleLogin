Simple Login Extension for Flask
================================

The simplest way to add login to Flask!

So why Flask Simple Login?
==========================

Sometimes you need something simple for that small project or for prototyping.

Flask Simple Login
==================

What it provides:

   * Login and Logout forms and pages
   * Function to check if user is logged-in
   * Decorator for views
   * Easy and customizable ``login_checker``
   * Basic auth for API endpoints

What it does not provide:

   * Database Integration
   * Password management
   * API authentication with Token or JWT
   * Role or user based access control

Of course you can easily implement all above by your own. Take a look at `example`_.

   .. _example: https://github.com/flask-extensions/flask_simplelogin/tree/main/example

Install
=======

First install it from `PyPI`_:

    .. _PyPI: https://pypi.org/project/flask_simplelogin/

::

    pip install flask_simplelogin


Flask Simple Login depends on Flask-WTF and WTForms, as well as on a `SECRET_KEY` set in your `app.config`.

Quick start
===========

::

    from flask import Flask
    from flask_simplelogin import SimpleLogin

    app = Flask(__name__)
    SimpleLogin(app)

**That's it!**

Now you have ``/login`` and ``/logout`` routes in your application.

The user name defaults to ``admin`` and the password defaults to ``secret`` — yeah that's not clever, let's see how to change it!


.. toctree::
   :maxdepth: 2
   :caption: Index:

   configuring.md
   usage.md
   customizing.md
   extras.md


References:
===========

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
