#!/usr/bin/env bash

script=$(basename "${BASH_SOURCE[0]}")

USAGE="
Usage: $script <web-server> 

Args: 
    web-server: connection string to the webserver. E.g.: localhost:8080
"

if (( $# != 1 )); then
    echo "$USAGE"
    exit 1
fi

webserver="$1"
tmpfile="$(mktemp /tmp/media-register-users.XXXXXX)"
tmperror="$(mktemp /tmp/media-register-users-error.XXXXXX)"

for i in {1..1000}; do
    echo "register user $i"
    httpcode=$(
        curl -o "$tmpfile" -w '%{http_code}\n' -d "first_name=first_name_"$i"&last_name=last_name_"$i"&username=username_"$i"&password=password_"$i \
            http://"$webserver"/wrk2-api/user/register 2>"$tmperror"
    )
    if [[ $? -ne 0 ]]; then
        echo "non-zero curl return:"
        echo "'''"
        cat "$tmperror"
        echo "'''"
        break
    else
        if ! [[ $httpcode =~ '2\d\d' ]]; then
            echo "request failed:" 
            echo "'''"
            cat "$tmpfile"
            echo "'''"
            break
        fi
    fi
done

rm "$tmpfile"
