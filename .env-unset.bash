#!/bin/bash

# Set the path to your .env file
env_file=".env"

# Read each line from the .env file
while IFS= read -r line; do
  # Extract the environment variable name by cutting at the '=' character
  var_name=$(echo "$line" | cut -d '=' -f 1)
  
  # Check if the line is not empty and does not start with a '#' (comment)
  if [[ ! -z "$var_name" && ! "$var_name" =~ ^# ]]; then
    # Unset the environment variable
    unset $var_name
    echo "Unset: $var_name"
  fi
done < "$env_file"
