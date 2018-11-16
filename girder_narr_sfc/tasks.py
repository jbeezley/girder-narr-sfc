from girder_worker.app import app
from girder_worker.utils import girder_job

from .processing import extract_file_metadata


@girder_job(title='Extract NARR metadata')
@app.task(bind=True)
def extract_narr_metadata(self, file):
    return extract_file_metadata(file)
