from mongoengine import *


class Header(EmbeddedDocument):
    interests = ListField(StringField())
    tweet_time = LongField()
    org_tweet_time = LongField()


class TUser(EmbeddedDocument):
    id = StringField(max_length=200)
    profile_image_url = StringField(max_length=300)
    screen_name = StringField(max_length=200)
    name = StringField(max_length=300)


class Media(EmbeddedDocument):
    media_url = StringField(max_length=200)


class Entities(EmbeddedDocument):
    media = ListField(EmbeddedDocumentField(Media))


class ReTweetObj(EmbeddedDocument):
    id = StringField(max_length=200)
    text = StringField(max_length=500)
    created_at = DateTimeField()
    retweet_count = IntField()
    favorite_count = IntField()
    geo = StringField()
    user = EmbeddedDocumentField(TUser)
    entities = EmbeddedDocumentField(Entities)
    time = DateTimeField()


class TweetObj(EmbeddedDocument):
    id = StringField(max_length=200)
    text = StringField(max_length=500)
    created_at = DateTimeField()
    retweet_count = IntField()
    favorite_count = IntField()
    geo = StringField()
    user = EmbeddedDocumentField(TUser)
    retweeted_status = EmbeddedDocumentField(ReTweetObj)
    entities = EmbeddedDocumentField(Entities)
    time = DateTimeField()


class Tweet(Document):
    header = EmbeddedDocumentField(Header)
    tweet = EmbeddedDocumentField(TweetObj)


class Report(Document):
    interest_id = StringField(max_length=250)
    start_time = LongField()
    end_time = LongField()
    terms = StringField()
    itemsets = StringField()
    tweet_count = IntField()

