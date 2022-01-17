from umongo import Document, fields

from telathbot.constants import METADATA_COLLECTION
from telathbot.databases.mongo import UMONGO


@UMONGO.register
class Metadata(Document):  # pylint: disable=abstract-method
    class Meta:
        collection_name = METADATA_COLLECTION

    type = fields.StrField(default="metadata")
    appVersion = fields.StrField()
    lastPostId = fields.IntegerField()
    lastPublicIp = fields.StrField()
