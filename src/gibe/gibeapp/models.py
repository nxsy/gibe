from mongoengine import Document, EmbeddedDocument, fields

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
    pass

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
    base_url = fields.StringField()



class CachedTweet(Document):
    status_id = fields.StringField(required=True)
    text = fields.StringField(required=True)
    created_at = fields.DateTimeField(required=True)
    author_screen_name = fields.StringField(required=True)



# Keeps per-page data of some sort, as opposed to data associated with the
# particular version of the content in question.  This might be something like
# "views", tracking search terms used to arrive on the page, or something like
# that.
class PageAnnotation(EmbeddedDocument):
    pass

# Keeps data about the particular version of the content in question.  This
# might be something like "tags", categories.
class ContentAnnotation(EmbeddedDocument):
    pass

class Content(EmbeddedDocument):
    title = fields.StringField(max_length=120)
    author = fields.ReferenceField(User)
    published_date = fields.DateTimeField()
    creation_date = fields.DateTimeField()
    all_urls = fields.ListField(fields.StringField())
    canonical_url = fields.StringField()

    annotations = fields.ListField(fields.EmbeddedDocumentField(ContentAnnotation))

class GibeMarkdownContent(Content):
    markdown = fields.StringField()

class Page(Document):
    content = fields.EmbeddedDocumentField(Content)
    drafts = fields.ListField(fields.EmbeddedDocumentField(Content))

    annotations = fields.ListField(fields.EmbeddedDocumentField(PageAnnotation))

    meta = {
        'indexes': [
            'content.published_date',
            'content.all_urls',
        ],
    }

