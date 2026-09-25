#!/bin/bash

# This script is used to commit changes with custom date and message.
#!/bin/bash

msg="$1"
date="$2"

if [ -z "$msg" ]; then
  echo "Error: Commit message is required."
  exit 1
fi

if [ -z "$date" ]; then
  echo "Error: Commit date is required."
  echo "Usage: ./commit.sh \"message\" \"YYYY-MM-DDTHH:MM:SS\""
  echo "Example: ./commit.sh \"Initial commit\" \"2024-06-01T12:00:00\""
  exit 1
fi

git add -A

GIT_AUTHOR_DATE="$date" \
GIT_COMMITTER_DATE="$date" \
git commit -m "$msg"

if [ $? -eq 0 ]; then
  echo "[+] Commit created with message: '$msg' and date: '$date'"
else
  echo "[-] Commit failed."
  exit 1
fi
