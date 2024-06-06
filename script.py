import tweepy
import requests
from PIL import Image
from io import BytesIO
import pytesseract
import africastalking

twitter_bearer_token = 'bearer-token-here'


africastalking_username = 'YOUR_AFRICASTALKING_USERNAME'
africastalking_api_key = 'YOUR_AFRICASTALKING_API_KEY'
recipient_phone_number = 'YOUR_PHONE_NUMBER'

client = tweepy.Client(bearer_token=twitter_bearer_token)

africastalking.initialize(africastalking_username, africastalking_api_key)
sms = africastalking.SMS


def fetch_latest_tweet():
    try:
        user_response = client.get_user(username='KenyaPower_Care')
        print(f"User Response: {user_response}")
        user_id = user_response.data.id
        response = client.get_users_tweets(id=user_id, max_results=5)
        print(f"Tweets Response: {response}")
        if response.data:
            for tweet in response.data:
                if 'attachments' in tweet.data and 'media_keys' in tweet.data['attachments']:
                    media_keys = tweet.data['attachments']['media_keys']
                    media_url = get_media_url(media_keys[0])
                    if media_url:
                        response = requests.get(media_url)
                        img = Image.open(BytesIO(response.content))
                        text = pytesseract.image_to_string(img)
                        return text.strip()
                return tweet.text.strip()
    except Exception as e:
        print(f"Error: {e}")
    return None


def get_media_url(media_key):
    media_response = client.get_media(media_ids=[media_key])
    if media_response.data:
        return media_response.data[0].url
    return None


def send_sms(message):
    response = sms.send(message, [recipient_phone_number])
    print(response)


if __name__ == '__main__':
    latest_tweet = fetch_latest_tweet()
    if latest_tweet:
        send_sms(latest_tweet)
