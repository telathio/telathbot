from umongo import Document, fields

from telathbot.constants import SAFETYTOOLS_COLLECTION
from telathbot.databases.mongo import UMONGO


@UMONGO.register
class SafetyToolsUse(Document):  # pylint: disable=abstract-method
    class Meta:
        collection_name = SAFETYTOOLS_COLLECTION

    postId = fields.IntegerField()
    threadId = fields.IntegerField()
    postUser = fields.StrField()
    reactionUsers = fields.StrField()
    notified = fields.BooleanField()
    dateObserved = fields.DateTimeField()
