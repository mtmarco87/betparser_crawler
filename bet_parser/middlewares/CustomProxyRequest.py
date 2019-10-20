import scrapy


class CustomProxyRequest(scrapy.Request):
    """
    scrapy.Request subclass which instructs Scrapy to render
    the page using a random Proxy.

    It requires ProxyMiddleware to work.
    """

    def __init__(self,
                 url=None,
                 callback=None,
                 method='GET',
                 do_yourself=True,
                 regenerate=False,
                 proxies=None,
                 fail_if=None,
                 accept_only_if=None,
                 meta=None,
                 **kwargs):
        if url is None:
            url = 'about:blank'

        meta = meta or {}
        proxy_meta = meta.setdefault('custom_proxy', {})
        proxy_meta.setdefault('regenerate', regenerate)
        proxy_meta.setdefault('do_yourself', do_yourself)
        proxy_meta.setdefault('proxies', proxies)
        proxy_meta.setdefault('fail_if', proxies)
        proxy_meta.setdefault('accept_only_if', proxies)

        super(CustomProxyRequest, self).__init__(url, callback, method, dont_filter=True, meta=meta,
                                                 **kwargs)
