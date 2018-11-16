from girder import events
from girder import plugin
from girder.models.assetstore import Assetstore
from girder.utility import assetstore_utilities
from girder_worker_utils.transforms.girder_io import GirderFileId, GirderItemMetadata
from girder_worker import GirderWorkerPluginABC

from .rest import add_routes
from .tasks import extract_narr_metadata


class GirderItemNarrMetadata(GirderItemMetadata):
    def transform(self, data):
        self.gc.put('item/%s/narr' % self.item_id, json=data)
        return data


class GWPlugin(GirderWorkerPluginABC):
    def __init__(self, app, *args, **kwargs):
        self.app = app

    def task_imports(self):
        return ['girder_narr_sfc.tasks']


def _get_girder_path(girder_file):
    assetstore = Assetstore().load(girder_file['assetstoreId'])
    adapter = assetstore_utilities.getAssetstoreAdapter(assetstore)
    return adapter.fullPath(girder_file)


def _file_upload_handler(event):
    file = event.info['file']
    if file.get('exts') and 'nc' == file['exts'][-1]:
        extract_narr_metadata.delay(
            GirderFileId(str(file['_id'])),
            girder_result_hooks=[GirderItemNarrMetadata(str(file['itemId']))]
        )


class GirderPlugin(plugin.GirderPlugin):
    DISPLAY_NAME = 'Surface Temperature Processor'

    def load(self, info):
        plugin.getPlugin('worker').load(info)
        events.bind('model.file.finalizeUpload.after',
                    'narr-sfc', _file_upload_handler)
        add_routes(info['apiRoot'])
