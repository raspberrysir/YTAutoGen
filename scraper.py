import praw


#returns the story at rank rank
def scraper(rank):
    reddit = praw.Reddit(
    client_id='U6XTsiI7wFtMrxjeqwbs8Q',
    client_secret='xM2pYU9gyIjWr9Cb52F6t8EdCXvR9g',
    user_agent='YTBot',
    )

    subreddit = reddit.subreddit('stories')

    current_rank = 1

    # Iterate through the top posts in the subreddit
    for submission in subreddit.top(limit=50):
        if current_rank == rank:
            return submission.selftext
        current_rank += 1



