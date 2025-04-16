import praw
import pandas as pd
import time
from praw.exceptions import APIException

# Initialize Reddit API client with your credentials
reddit = praw.Reddit(
    client_id='1iXP2XSx1IpEBc-650U_jg',  # Replace with your client ID
    client_secret='gPIYPDKwvUEzyGyMJ4ptK9bSigfegw',  # Replace with your client secret
    user_agent='yapyd'  # Replace with your user agent
)

# Post URL
post_url = "https://www.reddit.com/r/iphone/comments/1fcwexu/apple_unveils_iphone_16_pro_new_design_longer/"

# Extract the post's ID from the URL (everything after '/comments/')
post_id = post_url.split('/')[-3]

# Get the post object using its ID
post = reddit.submission(id=post_id)

# Prepare a list to store comments
comments_data = []

# Replace "more comments" to get all comments
post.comments.replace_more(limit=None)  # Remove the limit to handle all "more" objects

# Initialize a counter to track the number of requests
request_count = 0
max_requests = 100  # After 100 requests, wait for 1 minute
sleep_time = 60  # 1 minute

# Loop through all comments and store the data in a list
for comment in post.comments.list():
    comment_data = {
        "Comment ID": comment.id,
        "Comment Body": comment.body,
        "Author": comment.author if comment.author else "Deleted",  # Handle deleted authors
        "Upvotes": comment.score,
        "Timestamp": comment.created_utc  # UTC timestamp
    }
    comments_data.append(comment_data)
    
    # Increment the request count
    request_count += 1
    
    # If 100 requests have been made, pause for 1 minute
    if request_count >= max_requests:
        print(f"Reached {max_requests} requests. Sleeping for {sleep_time} seconds...")
        time.sleep(sleep_time)  # Sleep for 1 minute
        request_count = 0  # Reset the request counter

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(comments_data)
# Export the DataFrame to a CSV file
df.to_csv('../data/iphone16pro.csv', index=False, encoding='utf-8')