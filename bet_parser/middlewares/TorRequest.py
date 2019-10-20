import scrapy


class TorRequest(scrapy.Request):
    """
    scrapy.Request subclass which instructs Scrapy to render
    the page using Tor.

    It requires TorMiddleware to work.
    """

    def __init__(self,
                 url=None,
                 callback=None,
                 method='GET',
                 regenerate=False,
                 meta=None,
                 **kwargs):
        if url is None:
            url = 'about:blank'

        meta = meta or {}
        tor_meta = meta.setdefault('tor', {})
        tor_meta.setdefault('regenerate', regenerate)

        super(TorRequest, self).__init__(url, callback, method, dont_filter=True, meta=meta,
                                         **kwargs)
