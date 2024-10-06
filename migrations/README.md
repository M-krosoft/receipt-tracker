Single-database configuration for Flask.

## Before using:

In the main project directory:
- create ``` .env ``` file and set ``` FLASK_APP=run.py```

 ## After changes in database, run:
```
$ flask db migrate -m "Some message"
$ flask db upgrade
```

It is critical to note that autogenerate is not intended to be perfect.
It is always necessary to manually review and correct the candidate migrations that autogenerate produces.

### Autogenerate will detect:
- Table additions, removals.

- Column additions, removals.

- Change of nullable status on columns.

- Basic changes in indexes and explicitly-named unique constraints

- Basic changes in foreign key constraints

