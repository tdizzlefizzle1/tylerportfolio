#!/bin/bash

echo "Beginning timeline post"
curl http://localhost:5000/api/timeline_post
echo "POST Requests:"
curl -X POST http://localhost:5000/api/timeline_post -d 'name=Tyler&email=tylerhols@yahoo.com&content=Just Added Database to my portfolio site!'
curl -X POST http://localhost:5000/api/timeline_post -d 'name=Tyler&email=tylerhols@yahoo.com&content=Testing my endpoints with postman and curl.'
echo "DELETE Request:"
curl -X DELETE http://localhost:5000/api/timeline_post
