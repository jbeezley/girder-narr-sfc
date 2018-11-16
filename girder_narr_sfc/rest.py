from girder.api import access
from girder.api.describe import autoDescribeRoute, Description
from girder.api.rest import boundHandler
from girder.constants import AccessType
from girder.models.item import Item


def add_routes(api):
    api.item.route('PUT', (':id', 'narr'), add_narr_metadata)


@access.user
@boundHandler
@autoDescribeRoute(
    Description('Add NARR specific metadata to an item.')
    .modelParam('id', model=Item, level=AccessType.ADMIN)
    .jsonParam('metadata', 'A JSON object containing the NARR metadata',
               paramType='body', requireObject=True)
)
def add_narr_metadata(self, item, metadata):
    item['narr'] = metadata
    Item().save(item)
