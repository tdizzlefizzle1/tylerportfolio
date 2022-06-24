#!/bin/bash

echo "Beginning timeline posts"
curl http://localhost:5000/api/timeline_post

echo ""
echo -e "POST Requests: \n"
id1=$((curl -X POST http://localhost:5000/api/timeline_post -d 'name=&email=&content=') | jq ".id")
id2=$((curl -X POST http://localhost:5000/api/timeline_post -d 'name=&email=&content=') | jq ".id")

echo ""
echo -e "DELETE Request: \n"

curl -X DELETE http://localhost:5000/api/timeline_post -d "id=$id1"
curl -X DELETE http://localhost:5000/api/timeline_post -d "id=$id2"

echo ""
echo -e "Test successful! \n"