

# PostgreSQL comparison

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
