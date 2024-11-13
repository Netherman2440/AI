import sys
sys.path.append("../../")  # Go up two directories to reach project root

from src import httpRequest

image_url = 'https://openart.ai/share/aEhPbkNZRElYZjBQOE9PbnVHUkI7aHR0cHM6Ly9jZG4ub3BlbmFydC5haS91cGxvYWRzL2ltYWdlX0VxWVdTUExYXzE3MzE1MTU4ODUwNTlfNTEyLndlYnA'
verify_response = httpRequest.verify('robotid', image_url)
print(verify_response)
