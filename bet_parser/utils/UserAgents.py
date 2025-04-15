class UserAgents:
    """
    A static class to hold a list of common user agents.
    """

    sorted = [
        {
            "percent": "19.8%",
            "useragent": "Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/134.0.0.0 Safari\/537.36",
            "system": "Chrome 134.0 Win10",
        },
        {
            "percent": "11.2%",
            "useragent": "Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/134.0.0.0 Safari\/537.36",
            "system": "Chrome 134.0 macOS",
        },
        {
            "percent": "6.6%",
            "useragent": "Mozilla\/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko\/20100101 Firefox\/136.0",
            "system": "Firefox 136.0 Win10",
        },
        {
            "percent": "6.1%",
            "useragent": "Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/135.0.0.0 Safari\/537.36",
            "system": "Chrome 135.0 Win10",
        },
        {
            "percent": "4.0%",
            "useragent": "Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/134.0.0.0 Safari\/537.36 Edg\/134.0.0.0",
            "system": "Edge 134.0 Win10",
        },
        {
            "percent": "3.3%",
            "useragent": "Mozilla\/5.0 (X11; Linux x86_64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/134.0.0.0 Safari\/537.36",
            "system": "Chrome 134.0 Linux",
        },
        {
            "percent": "2.6%",
            "useragent": "Mozilla\/5.0 (Macintosh; Intel Mac OS X 10.15; rv:136.0) Gecko\/20100101 Firefox\/136.0",
            "system": "Firefox 136.0 macOS",
        },
        {
            "percent": "2.5%",
            "useragent": "Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/135.0.0.0 Safari\/537.36",
            "system": "Chrome 135.0 macOS",
        },
        {
            "percent": "2.5%",
            "useragent": "Mozilla\/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko\/20100101 Firefox\/137.0",
            "system": "Firefox 137.0 Win10",
        },
        {
            "percent": "2.4%",
            "useragent": "Mozilla\/5.0 (X11; Linux x86_64; rv:136.0) Gecko\/20100101 Firefox\/136.0",
            "system": "Firefox 136.0 Linux",
        },
        {
            "percent": "2.2%",
            "useragent": "Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit\/605.1.15 (KHTML, like Gecko) Version\/18.3.1 Safari\/605.1.15",
            "system": "Safari Generic macOS",
        },
        {
            "percent": "1.8%",
            "useragent": "Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/133.0.0.0 Safari\/537.36",
            "system": "Chrome 133.0 macOS",
        },
        {
            "percent": "1.7%",
            "useragent": "Mozilla\/5.0 (X11; Linux x86_64; rv:128.0) Gecko\/20100101 Firefox\/128.0",
            "system": "Firefox 128.0 Linux",
        },
        {
            "percent": "1.7%",
            "useragent": "Mozilla\/5.0 (X11; Linux x86_64; rv:137.0) Gecko\/20100101 Firefox\/137.0",
            "system": "Firefox 137.0 Linux",
        },
        {
            "percent": "1.5%",
            "useragent": "Mozilla\/5.0 (X11; Ubuntu; Linux x86_64; rv:136.0) Gecko\/20100101 Firefox\/136.0",
            "system": "Firefox 136.0 Linux",
        },
        {
            "percent": "1.4%",
            "useragent": "Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/135.0.0.0 Safari\/537.36 Edg\/135.0.0.0",
            "system": "Edge 135.0 Win10",
        },
        {
            "percent": "1.4%",
            "useragent": "Mozilla\/5.0 (X11; Linux x86_64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/135.0.0.0 Safari\/537.36",
            "system": "Chrome 135.0 Linux",
        },
        {
            "percent": "1.1%",
            "useragent": "Mozilla\/5.0 (Macintosh; Intel Mac OS X 10.15; rv:137.0) Gecko\/20100101 Firefox\/137.0",
            "system": "Firefox 137.0 macOS",
        },
        {
            "percent": "1.1%",
            "useragent": "Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/133.0.0.0 Safari\/537.36",
            "system": "Chrome 133.0 Win10",
        },
        {
            "percent": "0.8%",
            "useragent": "Mozilla\/5.0 (X11; Linux x86_64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/133.0.0.0 Safari\/537.36",
            "system": "Chrome 133.0 Linux",
        },
        {
            "percent": "0.8%",
            "useragent": "Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit\/605.1.15 (KHTML, like Gecko) Version\/18.4 Safari\/605.1.15",
            "system": "Safari Generic macOS",
        },
        {
            "percent": "0.7%",
            "useragent": "Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/132.0.0.0 Safari\/537.36",
            "system": "Chrome 132.0 Win10",
        },
        {
            "percent": "0.7%",
            "useragent": "Mozilla\/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko\/20100101 Firefox\/135.0",
            "system": "Firefox 135.0 Win10",
        },
        {
            "percent": "0.7%",
            "useragent": "Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/132.0.0.0 Safari\/537.36 OPR\/117.0.0.0",
            "system": "Chrome 132.0 Win10",
        },
        {
            "percent": "0.7%",
            "useragent": "Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/132.0.0.0 YaBrowser\/25.2.0.0 Safari\/537.36",
            "system": "Yandex Browser Generic Win10",
        },
        {
            "percent": "0.5%",
            "useragent": "Mozilla\/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko\/20100101 Firefox\/128.0",
            "system": "Firefox 128.0 Win10",
        },
        {
            "percent": "0.4%",
            "useragent": "Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/131.0.0.0 Safari\/537.36",
            "system": "Chrome 131.0 Win10",
        },
        {
            "percent": "0.4%",
            "useragent": "Mozilla\/5.0 (X11; Linux x86_64; rv:135.0) Gecko\/20100101 Firefox\/135.0",
            "system": "Firefox 135.0 Linux",
        },
        {
            "percent": "0.3%",
            "useragent": "Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/132.0.0.0 Safari\/537.36",
            "system": "Chrome 132.0 macOS",
        },
        {
            "percent": "0.3%",
            "useragent": "Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit\/605.1.15 (KHTML, like Gecko) Version\/18.3 Safari\/605.1.15",
            "system": "Safari Generic macOS",
        },
        {
            "percent": "0.3%",
            "useragent": "Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/125.0.0.0 Safari\/537.36 GLS\/100.10.9939.100",
            "system": "Chrome 125.0 Win10",
        },
        {
            "percent": "0.3%",
            "useragent": "Mozilla\/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko\/20100101 Firefox\/115.0",
            "system": "Firefox 115.0 Win7",
        },
        {
            "percent": "0.3%",
            "useragent": "Mozilla\/5.0 (X11; Linux x86_64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/132.0.0.0 Safari\/537.36",
            "system": "Chrome 132.0 Linux",
        },
        {
            "percent": "0.3%",
            "useragent": "Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit\/605.1.15 (KHTML, like Gecko)",
            "system": "Apple Mail for OSX macOS",
        },
        {
            "percent": "0.3%",
            "useragent": "Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/109.0.0.0 Safari\/537.36",
            "system": "Chrome 109.0 Win10",
        },
        {
            "percent": "0.3%",
            "useragent": "Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/131.0.0.0 Safari\/537.36",
            "system": "Chrome 131.0 macOS",
        },
        {
            "percent": "0.3%",
            "useragent": "Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/134.0.0.0 Safari\/537.36 Edg\/134.0.0.0",
            "system": "Edge 134.0 macOS",
        },
        {
            "percent": "0.3%",
            "useragent": "Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit\/605.1.15 (KHTML, like Gecko) Version\/18.1 Safari\/605.1.15",
            "system": "Safari Generic macOS",
        },
        {
            "percent": "0.3%",
            "useragent": "Mozilla\/5.0 (X11; Linux x86_64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/131.0.0.0 Safari\/537.36",
            "system": "Chrome 131.0 Linux",
        },
        {
            "percent": "0.3%",
            "useragent": "Mozilla\/5.0 (X11; Ubuntu; Linux x86_64; rv:137.0) Gecko\/20100101 Firefox\/137.0",
            "system": "Firefox 137.0 Linux",
        },
        {
            "percent": "0.2%",
            "useragent": "Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/116.0.0.0 Safari\/537.36",
            "system": "Chrome 116.0 macOS",
        },
        {
            "percent": "0.2%",
            "useragent": "Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit\/605.1.15 (KHTML, like Gecko) Version\/17.6 Safari\/605.1.15",
            "system": "Safari Generic macOS",
        },
        {
            "percent": "0.2%",
            "useragent": "Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/133.0.0.0 Safari\/537.36 Edg\/133.0.0.0",
            "system": "Edge 133.0 Win10",
        },
        {
            "percent": "0.2%",
            "useragent": "Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit\/605.1.15 (KHTML, like Gecko) Version\/17.5 Safari\/605.1.15",
            "system": "Safari Generic macOS",
        },
        {
            "percent": "0.2%",
            "useragent": "Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit\/605.1.15 (KHTML, like Gecko) Version\/18.2 Safari\/605.1.15",
            "system": "Safari Generic macOS",
        },
        {
            "percent": "0.2%",
            "useragent": "Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/132.0.0.0 Safari\/537.36 OPR\/117.0.0.0 (Edition std-2)",
            "system": "Chrome 132.0 Win10",
        },
        {
            "percent": "0.2%",
            "useragent": "Mozilla\/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/134.0.0.0 Safari\/537.36",
            "system": "Chrome 134.0 ChromeOS",
        },
        {
            "percent": "0.2%",
            "useragent": "Mozilla\/5.0 (X11; Linux x86_64; rv:138.0) Gecko\/20100101 Firefox\/138.0",
            "system": "Firefox 138.0 Linux",
        },
        {
            "percent": "0.2%",
            "useragent": "Mozilla\/5.0 (X11; Ubuntu; Linux x86_64; rv:135.0) Gecko\/20100101 Firefox\/135.0",
            "system": "Firefox 135.0 Linux",
        },
        {
            "percent": "0.2%",
            "useragent": "Mozilla\/5.0 (iPhone; CPU iPhone OS 18_3_2 like Mac OS X) AppleWebKit\/605.1.15 (KHTML, like Gecko) Version\/18.3.1 Mobile\/15E148 Safari\/604.1",
            "system": "Mobile Safari Generic iOS",
        },
        {
            "percent": "0.2%",
            "useragent": "Mozilla\/5.0 (Linux; Android 10; K) AppleWebKit\/537.36 (KHTML, like Gecko) SamsungBrowser\/27.0 Chrome\/125.0.0.0 Safari\/537.36",
            "system": "Samsung Browser Generic Android",
        },
        {
            "percent": "0.2%",
            "useragent": "Mozilla\/5.0 (Macintosh; Intel Mac OS X 10.15; rv:128.0) Gecko\/20100101 Firefox\/128.0",
            "system": "Firefox 128.0 macOS",
        },
        {
            "percent": "0.2%",
            "useragent": "Mozilla\/5.0 (Macintosh; Intel Mac OS X 10.15; rv:135.0) Gecko\/20100101 Firefox\/135.0",
            "system": "Firefox 135.0 macOS",
        },
        {
            "percent": "0.2%",
            "useragent": "Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/128.0.0.0 Safari\/537.36",
            "system": "Chrome 128.0 macOS",
        },
        {
            "percent": "0.2%",
            "useragent": "Mozilla\/5.0 (Windows NT 10.0; rv:109.0) Gecko\/20100101 Firefox\/115.0",
            "system": "Firefox 115.0 Win10",
        },
        {
            "percent": "0.2%",
            "useragent": "Mozilla\/5.0 (Windows NT 10.0; rv:128.0) Gecko\/20100101 Firefox\/128.0",
            "system": "Firefox 128.0 Win10",
        },
        {
            "percent": "0.2%",
            "useragent": "Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/126.0.0.0 Safari\/537.36",
            "system": "Chrome 126.0 Win10",
        },
        {
            "percent": "0.2%",
            "useragent": "Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/128.0.0.0 Safari\/537.36",
            "system": "Chrome 128.0 Win10",
        },
        {
            "percent": "0.2%",
            "useragent": "Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/129.0.0.0 Safari\/537.36",
            "system": "Chrome 129.0 Win10",
        },
        {
            "percent": "0.2%",
            "useragent": "Mozilla\/5.0 (X11; Linux x86_64) AppleWebKit\/537.36 (KHTML, like Gecko) SamsungBrowser\/27.0 Chrome\/125.0.0.0 Safari\/537.36",
            "system": "Chrome Generic Linux",
        },
        {
            "percent": "0.2%",
            "useragent": "Mozilla\/5.0 (X11; Linux x86_64; rv:109.0) Gecko\/20100101 Firefox\/119.0",
            "system": "Firefox 119.0 Linux",
        },
        {
            "percent": "0.2%",
            "useragent": "Mozilla\/5.0 (X11; Linux x86_64; rv:109.0) Gecko\/20100101 Firefox\/119.0",
            "system": "Firefox 119.0 Linux",
        },
    ]
