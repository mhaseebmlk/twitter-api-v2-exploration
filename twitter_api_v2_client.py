import os
import argparse

import tweepy


REQUIRED_ENV_VARS = [
        "CONSUMER_KEY",
        "CONSUMER_SECRET",
        "ACCESS_TOKEN",
        "ACCESS_TOKEN_SECRET",
        "BEARER_TOKEN",
]
consumer_key = os.environ["CONSUMER_KEY"]
consumer_secret = os.environ["CONSUMER_SECRET"]
access_token = os.environ["ACCESS_TOKEN"]
access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]
bearer_token = os.environ["BEARER_TOKEN"]


def delete_tweets(parser):
    if parser.username is None:
        raise ValueError("The delete_tweets action requires the username value.")

    client_bearer_token = tweepy.Client(bearer_token=bearer_token)
    user_id = client_bearer_token.get_user(username=parser.username).data.id

    client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    # Get all the tweets by this user and confirm with the user if they would
    # like to delete the tweet
    while True:
        response = client_bearer_token.get_users_tweets(
                id=user_id,
                max_results=100
        )

        tweets = response.data
        for tweet in tweets:
            delete_tweet = input("Would you like to delete the following tweet? [y/N] \n{}\n> ".format(tweet.text) )
            if delete_tweet == 'y':
                response = client.delete_tweet(id=tweet.id)

                if response.data["deleted"] is not True:
                    print("[WARN] Could not delete that tweet!")

        if "next_token" not in responses.meta:
            break

    print("DONE.")


ACTIONS = {
        "delete_tweets": delete_tweets,
}


def parse_args():
    parser = argparse.ArgumentParser(
            description="""Client to interact with the Twitter API v2. 
            This is done using the tweepy library. The following environment 
            variables must be set in order to use this tool: {}""".format(REQUIRED_ENV_VARS)
    )
    parser.add_argument(
            "--action",
            required=True,
            help="""The set of actions that can be perfomed with the API. 
            An action might require further input arguments. Supported 
            actions: {}""".format(list(ACTIONS.keys())),
            type=str,
    )
    parser.add_argument(
            "--username",
            required=False,
            help="The Twitter username of a user.",
            type=str,
    )

    return parser.parse_args()


def run():
    parser = parse_args()
    if parser.action not in ACTIONS:
        raise ValueError("The action {} is not supported.".format(parser.action))

    ACTIONS[parser.action](parser)


if __name__=="__main__":
    run()
