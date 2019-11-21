# PyDB

NoSQL database made in Python3.

## Connection Interface

The connection to the database is made by HTTP requests over the REST protocol.

## Structure of the data

The data is stored as JSON documents grouped in lists in binary files.
Each list of JSON documents own to a collection which is independent between each other.
The inserted documents will have their JSON keys lowercased.

## Search

To search a document, you must use a POST over the URL /<collection>/search with a JSON body with the following format:
* $filter: with the filters to filter the desired documents
* $size: with the size of the desiered response
* $skip: if you want to skip a determined number of documents in the respons
* $sort: with the information about the order the results must be returned
* $map: if you want the response to be returned other than the raw inserted documents

## Filter

To search one or more documents, you can give some boolean conditions to find it. The filter is given in JSON format
with the keys being the fields of the documents you are searching and the values their values. 
Example:
1. Document in database
{'id': 1, 'first_name': 'John', 'last_name': 'Doe'}
2. Filter
{'first_name': 'John'}

This means that you will search documents which contains a field named 'first_name' with the value 'John'.

If the key-value pair is inside a document, the filter will be interpreted them as an AND condition; if the key-value pair
is inside a list, the filter will be interpreted as an OR condition.
Example:
1. {'first_name': 'John', 'last_name': 'Smith'}
Is equivalent to a SQL condition as: WHERE first_name = 'John' AND last_name = 'Smith'
2. ['first_name': 'John', 'last_name': 'Smith']
Is equivalent to a SQL condition as: WHERE first_name = 'John' OR last_name = 'Smith'

This same rule is applied for the values them selves.
Example:
1. {'id': [1, 2, 3]}
Is equivalent to a SQL condition as: WHERE id IN (1, 2, 3)

The existance of a field is checked as following.
Example:
1. {'first_name': {'$exists': True}}
Which searches for documents where the field 'first_name' exists.
2. {'first_name': {'$exists': False}}
Which searches for documents where the field 'first_name' doesn't exist.

Number comparison are made with the keywords '$gt', '$lt', '$gte' and '$lte' with the following syntax.
Example:
1. {'age': {'$te': 35}}
Which searches for documents where the field age has a value less than 35

Strings can be searched with Regular Expressions as following.
Example:
1. {'name': {'$reg': 'Jo.*'}}
Only the documents where the regex 'Jo.*' has a match on the field 'name' will be returned.

## Identification

The field 'id' will be inserted with a UUID value to each new document if it's not present.

## Indexes

Only the index over the field 'id' will be automatically created.

## How to Run

```
python3 pydb
```

## How to run the tests

```
python3 -m unittest -v
```

### PostgreSQL comparison

size of the table (without any index): 250000 elements

For PostgreSQL
time psql -h localhost -U arval -p 5432 arval -c "select * from test_sergio.test where my_id=234510;"                                                                                                                                                                        [14:38:41]
 my_id  | first_name | last_name | age |  address  |    job    | salary |        email
--------+------------+-----------+-----+-----------+-----------+--------+---------------------
 234510 | john       | doe       |  15 | somewhere | something |  12345 | my.email@google.com
(1 row)

psql -h localhost -U arval -p 5432 arval -c   0,01s user 0,01s system 27% cpu 0,060 total

For PyDB with file of 1000 lines length
time curl localhost:5000/211456                                                                                                                                                                                                                                              [14:39:16]
{
  "address": "somewhere",
  "age": 15,
  "email": "my.email@google.com",
  "first_name": "al",
  "id": 211456,
  "job": "something",
  "last_name": "jym",
  "salary": 15352
}
curl localhost:5000/211456  0,01s user 0,01s system 1% cpu 1,390 total


For PyDB with file of 10000 lines length
time curl localhost:5000/240123                                                                                                                                                                                                                                               [10:07:50]
{
  "address": "somewhere",
  "age": 15,
  "email": "my.email@google.com",
  "first_name": "al",
  "id": 240123,
  "job": "something",
  "last_name": "jym",
  "salary": 15352
}
curl localhost:5000/240123  0,01s user 0,01s system 0% cpu 1,322 total

For PyDB with file of 100000 lines length
time curl localhost:5000/240999                                                                                                                                                                                                                                              [10:10:53]
{
  "address": "somewhere",
  "age": 15,
  "email": "my.email@google.com",
  "first_name": "al",
  "id": 240999,
  "job": "something",
  "last_name": "jym",
  "salary": 15352
}
curl localhost:5000/240999  0,01s user 0,01s system 0% cpu 1,410 total
