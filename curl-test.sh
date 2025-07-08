#!/bin/bash

API_URL="http://127.0.0.1:5000/api/timeline_post"
# first post the timeline post
post_response=$(curl --silent --show-error --request POST "$API_URL" \
  -d 'name=Yixing&email=leiyixing@gmail.com&content=Just Added Database to my portfolio site!'\
  |jq '.')
echo "Post response: $post_response"

#test if the post was created
get_response=$(curl --silent --show-error --request GET "$API_URL" | jq '.')
echo "Get response: $get_response"

# check if post response is contained in get response
if echo "$get_response" | jq -e --argjson post "$post_response" '.timeline_posts[] | select(. == $post)'; then
  echo "Post created successfully."
else
  echo "Post creation failed."
fi

# delete the post
id=$(echo $post_response | jq -r '.id')
echo "Post ID: $id"
delete_response=$(curl --silent --show-error --request DELETE "$API_URL/$id")