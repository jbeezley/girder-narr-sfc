import pytest

from girder.plugin import loadedPlugins


@pytest.mark.plugin('sfc')
def test_import(server):
    assert 'sfc' in loadedPlugins()
