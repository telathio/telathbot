from umongo import Document, EmbeddedDocument, fields

from telathbot.constants import SAFETYTOOLS_COLLECTION
from telathbot.databases.mongo import UMONGO


@UMONGO.register
class ToolsUser(EmbeddedDocument):  # pylint: disable=abstract-method
    reactionUser = fields.StrField(required=True)


@UMONGO.register
class SafetyToolsUse(Document):  # pylint: disable=abstract-method
    class Meta:
        collection_name = SAFETYTOOLS_COLLECTION

    postId = fields.IntegerField()
    threadId = fields.IntegerField()
    postUser = fields.StrField()
    reactionUsers = fields.ListField(values=fields.EmbeddedField(ToolsUser))
    notified = fields.BooleanField()
