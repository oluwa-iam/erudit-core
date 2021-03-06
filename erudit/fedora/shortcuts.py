# -*- coding: utf-8 -*-

from django.core.cache import caches

from .serializers import get_datastream_cache_serializer
from ..conf import settings as erudit_settings


def get_datastream_file_cache():
    return caches[erudit_settings.FEDORA_FILEBASED_CACHE_NAME]


def get_cached_datastream_content(fedora_object, datastream_name, cache=None):
    """ Given a Fedora object and a datastream name, returns the content of the datastream.

    Note that this content can be cached in a file-based cache!
    """
    cache = cache or get_datastream_file_cache()
    serializer, deserializer = get_datastream_cache_serializer(datastream_name)
    content_key = 'erudit-fedora-file-{pid}-{datastream_name}'.format(
        pid=fedora_object.pid,
        datastream_name=datastream_name,
    )

    content = deserializer(cache.get(content_key))
    try:
        assert content is None
        content = getattr(fedora_object, datastream_name).content
    except AssertionError:
        # We've just retrieved the content of the file from the file-based cache!
        pass
    else:
        # Puts the content of the file in the file-based cache!
        cache.set(
            content_key,
            serializer(content),
            erudit_settings.FEDORA_FILEBASED_CACHE_DEFAULT_TIMEOUT
        )

    return content
