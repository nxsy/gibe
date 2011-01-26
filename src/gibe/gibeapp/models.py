from mongoengine import Document, fields

class User(Document):
    email = fields.StringField(required=True)
    first_name = fields.StringField(max_length=50)
    last_name = fields.StringField(max_length=50)

class Post(Document):
    title = fields.StringField(max_length=120, required=True)
    author = fields.ReferenceField(User)
    published_date = fields.DateTimeField()
    creation_date = fields.DateTimeField(required=True)
    canonical_url = fields.StringField(required=True)
    all_urls = fields.ListField(fields.StringField())
    meta = {
        'indexes': ['published_date'],
    }

class TextPost(Post):
    content = fields.StringField()

class MarkupPost(Post):
    content = fields.StringField()
    markup = fields.StringField()

class TweetPost(Post):
    content = fields.StringField(required=True)
    tweet_id = fields.StringField(required=True)
    tweet_url = fields.StringField(required=True)
    retweeting = fields.StringField()
    meta = {
        'indexes': ['tweet_id'],
    }

class DeliciousPost(Post):
    link_url = fields.StringField()
    comment = fields.StringField()

class ImagePost(Post):
    image_path = fields.StringField()

class LinkPost(Post):
    link_url = fields.StringField()

class Settings(Document):
    key = fields.StringField(required=True, unique=True)

class TwitterSettings(Settings):
    oauth_token = fields.StringField()
    oauth_token_secret = fields.StringField()
    consumer_key = fields.StringField()
    consumer_secret = fields.StringField()

class BitlySettings(Settings):
    username = fields.StringField()
    api_key = fields.StringField()

class BlogSettings(Settings):
    title = fields.StringField()
    subtitle = fields.StringField()
    description = fields.StringField()
    feed_title = fields.StringField()
    feed_subtitle = fields.StringField()
    feed_description = fields.StringField()

class CachedTweet(Document):
    status_id = fields.StringField(required=True)
    text = fields.StringField(required=True)
    created_at = fields.DateTimeField(required=True)
    author_screen_name = fields.StringField(required=True)

