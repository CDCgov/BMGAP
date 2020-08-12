#!/usr/bin/env bash
while read line; do
    token_response=$(./example-impersonation.sh "$line")
    token=$(jq '.access_token' <<< "$token_response")
    stripped_token=${token%\"}
    final_token=${stripped_token#\"}
    echo "$final_token"
    id_info=$(curl -k --silent "https://amdportal-sams.cdc.gov/id/validate/$final_token")
    status_code=$(jq '.status' <<< id_info)
    if [[ status_code == 200 ]]; then
        
    fi
done << EOF
s1jb
noc0
ncbs-b
EOF
