from mongoengine import *


class Counter(DynamicEmbeddedDocument):
    value = IntField()


class Statistics(DynamicEmbeddedDocument):
    relevantPatterns = StringField()
    relevantHashtags = StringField()
    totalTweetCount = EmbeddedDocumentField(Counter)
    relevantTweetCount = EmbeddedDocumentField(Counter)
    irrelevantTweetCount = EmbeddedDocumentField(Counter)
    neutralTweetCount = EmbeddedDocumentField(Counter)
    avgRelevance = FloatField()
    maxRelevance = FloatField()
    minRelevance = FloatField()


class UStatistics(DynamicEmbeddedDocument):
    totalTweetCount = EmbeddedDocumentField(Counter)
    relevantTweetCount = EmbeddedDocumentField(Counter)
    irrelevantTweetCount = EmbeddedDocumentField(Counter)
    neutralTweetCount = EmbeddedDocumentField(Counter)
    # deltaTweetCount = EmbeddedDocumentField(Counter)
    # addedPhraseCount =EmbeddedDocumentField(Counter)
    # removedPhraseCount =EmbeddedDocumentField(Counter)
    # generalizedPhraseCount =EmbeddedDocumentField(Counter)
    # specializedPhraseCount =EmbeddedDocumentField(Counter)
    avgRelevance = FloatField()
    maxRelevance = FloatField()
    minRelevance = FloatField()
    meta = {
        'indexes': ['-relevantTweetCount']
    }


class Media(DynamicEmbeddedDocument):
    mediaURL = StringField(max_length=200)
    meta = {
        'indexes': ['mediaURL']
    }


class MediaEntities(DynamicEmbeddedDocument):
    media = ListField(EmbeddedDocumentField(Media))


class TUser(DynamicEmbeddedDocument):
    id = LongField(primary_key=True)
    screenName = StringField(max_length=200)
    name = StringField(max_length=300)
    profileImageUrl = StringField(max_length=500)
    followersCount = IntField()
    friendsCount = IntField()
    favouritesCount = IntField()
    statusesCount = IntField()
    createdAt = DateTimeField()
    description = StringField(max_length=1000)
    meta = {
        'indexes': ['$description']
    }


class User(DynamicDocument):
    id = LongField(primary_key=True)
    userInfo = EmbeddedDocumentField(TUser)
    statistics = EmbeddedDocumentField(UStatistics)
    meta = {'collection': 'user', 'strict': False}


class ST(DynamicEmbeddedDocument):
    text = StringField(max_length=500)
    createdAt = DateTimeField()
    retweetCount = IntField()
    favoriteCount = IntField()
    lang = StringField(max_length=20)
    user = EmbeddedDocumentField(TUser)
    geo = StringField()
    meta = {'allow_inheritance': True, 'strict': False}


class Status(ST):
    retweetedStatus = EmbeddedDocumentField(ST)
    meta = {'allow_inheritance': True, 'strict': False}


class Tweet(DynamicDocument):
    id = LongField(primary_key=True)
    timestamp = LongField()
    relevance = FloatField()
    status = EmbeddedDocumentField(Status)
    meta = {'strict': False}


class Query(EmbeddedDocument):
    pass


class Report(DynamicDocument):
    interestId = StringField(max_length=250)
    startTime = LongField()
    endTime = LongField()
    duration = LongField()
    # query = EmbeddedDocumentField(Query)
    statistics = EmbeddedDocumentField(Statistics)
