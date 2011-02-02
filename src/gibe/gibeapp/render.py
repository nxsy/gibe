import markdown

from gibe.syntaxhighlighter_markdown import SyntaxHighlighterExtension
from gibe.excerpt_markdown import ExcerptExtension
from gibe.gibeapp import models
from gibe.gibeapp.urlify_tweet import urlify_tweet

syntaxhighlighterextension = SyntaxHighlighterExtension({})
excerpt_extension = ExcerptExtension({})

class PostRenderer(object):
    def __init__(self, post):
        self.post = post

    @property
    def show_delicious(self):
        if isinstance(self.post, models.DeliciousPost):
            return False

        if isinstance(self.post, models.TweetPost):
            return False

        return True

    @property
    def show_disqus(self):
        if isinstance(self.post, models.DeliciousPost):
            return False

        if isinstance(self.post, models.TweetPost):
            return False

        return True

    @property
    def content_html(self):
        if isinstance(self.post, models.DeliciousPost):
            md = markdown.Markdown(extensions=[syntaxhighlighterextension, excerpt_extension, 'footnotes'])
            content = md.convert(self.post.comment)
            return content

        content = self.post.content

        if isinstance(self.post, models.TweetPost):
            content = urlify_tweet(content)

        if isinstance(self.post, models.MarkupPost):
            md = markdown.Markdown(extensions=[syntaxhighlighterextension, excerpt_extension, 'footnotes'])
            content = md.convert(content)

        if isinstance(self.post.content, models.GibeMarkdownContent):
            md = markdown.Markdown(extensions=[syntaxhighlighterextension, excerpt_extension, 'footnotes'])
            content = md.convert(self.post.content.markdown)

        return content

    @property
    def excerpt_html(self):
        if isinstance(self.post, models.DeliciousPost):
            md = markdown.Markdown(extensions=[syntaxhighlighterextension, excerpt_extension, 'footnotes'])
            content = md.convert(self.post.comment)
            return content

        content = self.post.content

        if isinstance(self.post, models.TweetPost):
            content = urlify_tweet(content)

        if isinstance(self.post, models.MarkupPost):
            md = markdown.Markdown(extensions=[syntaxhighlighterextension, excerpt_extension, 'footnotes'])
            content = md.convert(content)
            if md.excerpt:
                content = markdown.etree.tostring(md.excerpt)


        return content

    @property
    def source(self):
        if isinstance(self.post, models.TweetPost):
            return 'twitter'

        if isinstance(self.post, models.MarkupPost):
            return 'website'

        if isinstance(self.post, models.DeliciousPost):
            return 'delicious'

    @property
    def link(self):
        if self.post.content.canonical_url:
            return self.post.content.canonical_url

        return

    @property
    def canonical_link(self):
        if self.post.content.canonical_url:
            return self.post.content.canonical_url

        return

    def __getattr__(self, attr):
        return getattr(self.post, attr)

    def template(self):
        if isinstance(self.post, models.TweetPost):
            return "content-tweet.xhtml.template"

        if isinstance(self.post, models.MarkupPost):
            return "content-post.xhtml.template"

        if isinstance(self.post.content, models.GibeMarkdownContent):
            return "content-gibemarkdowncontent.xhtml.template"

        if isinstance(self.post, models.DeliciousPost):
            return "content-delicious.xhtml.template"

    def excerpt_template(self):
        if isinstance(self.post, models.TweetPost):
            return "excerpt-tweet.xhtml.template"

        if isinstance(self.post, models.MarkupPost):
            return "excerpt-post.xhtml.template"

        if isinstance(self.post, models.DeliciousPost):
            return "excerpt-delicious.xhtml.template"

    @property
    def author(self):
        return "nxsy"

    @property
    def author_html(self):
        return urlify_tweet("@" + self.author)
