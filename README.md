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
* $size: with the size of the desiered response (default size is 10, unbounded is -1)
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

A field or a filter can be negate with the keyword '$not'.
Example:
1. {'$filter': {'first_name': {'$not': 'John'}}}
Won't return the documents where the field 'first_name' is 'John'
2. {'$filter': {'$not': {'first_name': 'John'}}}
Has the same result as the previous, but this way we negate the comparison 'first_name' == 'John'. Which can also be a more complexe filter

## Mapper

The results can be mapped to a desired structure. In the '$map' field, you have to specify each field you want to map
(inner documents are reachable with dots notation) to a new field name (if the new field contains dots a new inner
document will be created). Not specified fields will be ignored
Example:
1. Database document
{'user': {'first_name': 'John', 'last_name': 'Smith'}}
2. Mapper
{'user.first_name': 'customer.name'}
3. Result
{'customer': {'name': 'John'}}

The keyword '$itself' can be used for a field or an inner document if you want the field or inner document to be maintained
as before.
Example:
1. Database document
{'user': {'first_name': 'John', 'last_name': 'Smith'}}
2. Mapper
{'user': '$itself'}
3. Result
{'user': {'first_name': 'John', 'last_name': 'Smith'}}

You can also only specify the excluded fields or inner documents of the mapping with the keyword '$exclude' followed by the list of fields (with
dot notation) you want to exclude.
Example:
1. Database document
{'user': {'first_name': 'John', 'last_name': 'Smith'}}
2. Mapper
{'$exclude': ['user.first_name']}
3. Result
{'user': {'last_name': 'Smith'}}

## Sorting

The outputs can be sorted on multiple fields in two orders (ASC or DESC). The sorting will be applied in the order of the fields are selected.
The sort operation will be done before the mapping.
Example:
1. Sort
{'$sort': {'first_name': 'ASC', 'last_name': 'DESC'}}
2. Description
The results will be first sorted by the field 'first_name' in alphabetical order, then by the field 'last_name' in reverse alphabetical order.

## Identification

The field 'id' will be inserted with a UUID value to each new document if it's not present.

## Indexes

Only the index over the field 'id' will be automatically created.

## Authorization

The /auth/login endpoint will return a token which must be send back to each HTTP request in the Authorization Bearer header.

## CRUD

Here are the commands to create, read, update and delete a document (create and update are managed as upsert):
* POST /<collection> : the body will be inserted in the collection. If the body already contains an id, it will update the existing document with that id, otherwise it will create a document with that id.
* PUT /<collection>/<id> : the body will replace the document with the id of the URL path in the colleciton
* PATCH /<collection>/<id> : the body will be inserted in the collection document with the id of the URL path in the collection
* DELETE /<collection>/<id> : the collection document with the id of the URL will be deleted

## How to Run

```
python3 pydb
```

## How to run the tests

```
python3 -m unittest -v
```

### TODO

* correct bulk insert
* bulk update
* bulk delete
* handle nested documents at filters
* Sort by inner documents
* Sort nested documents
* At queries status, add source request to detect deadlocks
* Replication auth
* Master/Slave complete sync
* Master/Master replication
* Sharding

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
