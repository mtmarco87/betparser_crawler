from typing import List


class SeleniumExecParams:
    url: str = None
    cookies: any = None
    kill_timeouts: bool = False
    wait_time: float = None
    wait_until = None
    script: str = None
    scroll_to_element: str = None
    scroll_wait_time: float = None
    render_js: bool = False
    extract_sub_links_by_class: List[str] = None
    extract_proxies: bool = False

    def __init__(self, url: str = None, cookies: any = None, kill_timeouts: bool = False, wait_time: float = None,
                 wait_until=None, script: str = None, scroll_to_element: str = None, scroll_wait_time: float = None,
                 render_js: bool = False, extract_sub_links_by_class: List[str] = None, extract_proxies: bool = False):
        self.url = url
        self.cookies = cookies
        self.kill_timeouts = kill_timeouts
        self.wait_time = wait_time
        self.wait_until = wait_until
        self.script = script
        self.scroll_to_element = scroll_to_element
        self.scroll_wait_time = scroll_wait_time
        self.render_js = render_js
        self.extract_sub_links_by_class = extract_sub_links_by_class
        self.extract_proxies = extract_proxies

    def clone(self):
        return SeleniumExecParams(self.url, self.cookies, self.kill_timeouts, self.wait_time, self.wait_until,
                                  self.script, self.scroll_to_element, self.scroll_wait_time, self.render_js,
                                  self.extract_sub_links_by_class, self.extract_proxies)

    def simplified_clone(self):
        return SeleniumExecParams(None, None, self.kill_timeouts, self.wait_time, None, None, self.scroll_to_element,
                                  self.scroll_wait_time, self.render_js, None, False)
