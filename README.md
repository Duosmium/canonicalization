# Duosmium Canonicalization Tools

This repository contains resources used for canonicalization purposes by the Duosmium Results team.

The central file here is `duosmium.sqlite3`, a SQLite database containing data on school and location information as well as a list of events. This database is intended to be regularly updated as more schools are added to the website and canonicalization issues are corrected.

There are also a number of auxiliary scripts that work with the database, performing actions such as regenerating the schools list in the database and matching schools to cities. Additional dependencies are required to use these scripts; `requirements.txt` and `Pipfile` can be used with Virtualenv and Pipenv, respectively, to set up the required environments running these scripts.
