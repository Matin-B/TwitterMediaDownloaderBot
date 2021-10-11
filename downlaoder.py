import config
from tweepy import API, OAuthHandler, Stream


def download_tweet(tweet_id):
    try:
        tweet = api.get_status(tweet_id, tweet_mode="extended")
        tweet_text = tweet.full_text
        tweet_link = tweet_text.split(' ')[-1]
        tweet_author_username = tweet.user.screen_name
        tweet_author_name = tweet.user.name
        tweet_date = tweet.created_at.strftime("%Y/%m/%d | %H-%M") + " UTC"
    except:
        return "Not Found"
    try:
        output = {
            "tweet_author_username": tweet_author_username,
            "tweet_author_name": tweet_author_name,
            "tweet_date": tweet_date,
            "text": tweet_text,
            "link": tweet_link,
            "urls": [],
            "media": True
        }
        media = tweet.extended_entities['media']
        if len(media) != 1:
            links = []
            for item in media:
                output['urls'].append(
                    {
                        'type': 'photo',
                        'url': item['media_url_https']
                    }
                )
        else:
            media_type = media[0]['type']
            if media_type == 'photo':
                output['urls'].append(
                    {
                        'type': media_type,
                        'url': media[0]['media_url_https'],
                    }
                )
            elif media_type == 'video':
                video_info = media[0]['video_info']
                media_variants = video_info['variants']
                count = 0
                for item in media_variants:
                    if item['content_type'] == 'application/x-mpegURL':
                        media_variants.pop(count)
                    count += 1
                media_variants.sort(key=lambda x: x['bitrate'], reverse=True)
                video_urls = {}
                for url in media_variants:
                    quality = url['url'].split('/vid/')[1].split('/')[0]
                    link = url['url']
                    video_urls[quality] = link
                output['urls'].append(
                    {
                        'type': media_type,
                        'urls': video_urls,
                    }
                )
            elif media_type == 'animated_gif':
                gif_info = media[0]['video_info']
                media_variants = gif_info['variants']
                count = 0
                for item in media_variants:
                    if item['content_type'] == 'application/x-mpegURL':
                        media_variants.pop(count)
                    count += 1
                media_variants.sort(key=lambda x: x['bitrate'], reverse=True)
                output['urls'].append(
                    {
                        'type': media_type,
                        'url': media_variants[0]['url'],
                    }
                )
        return output
    except AttributeError:
        return {
            "tweet_author_username": tweet_author_username,
            "tweet_author_name": tweet_author_name,
            "tweet_date": tweet_date,
            "text": tweet_text,
            "link": tweet_link,
            "media": False
        }


auth = OAuthHandler(
    config.CONSUMER_KEY,
    config.CONSUMER_SECRET_KEY
)
auth.set_access_token(
    config.TWITTER_ACCESS_TOKEN,
    config.TWITTER_ACCESS_TOKEN_SECRET
)

api = API(
    auth,
    wait_on_rate_limit=True,
)
