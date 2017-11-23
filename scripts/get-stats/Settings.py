class SporaReqSettings:
    """SporaReqSettings is the configuration class for SporaReq"""

    def __init__(self):
        """Initialization of SporaReqSettings"""
        # Requests configuration
        self.PROXY_TOR = {'http': "socks5://127.0.0.1:9050"}
        self.HEADERS = [{'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0'},
                        {'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'},
                        {'USER_AGENT': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36'},
                        {'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'},
                        {'USER_AGENT': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1'},
                        {'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}]
        self.URLs = ["http://torifyme.com"]

        # Parsing rules
        self.NAME_SELECTOR = '//input[@name="p"]/@value'
        self.PRICE_SELECTOR = '//span[@class="price"]/text()'

