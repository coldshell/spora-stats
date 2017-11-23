import re
from random import randint, choice, seed, random
from io import StringIO

import requests
from lxml import html


class SporaReq:
    """SopraReq request spora servers

    Attributes:
        _settings (SporaReqSettings): Request settings
    """

    def __init__(self, settings):
        """Initialization of SporaReq

        Arguments:
            _settings (SporaReqSettings): Request settings
            _reqs (list): List of requests results
        """
        self._settings = settings
        self._reqs = []

    def request(self, ID):
        """Make a request to spora website with a given ID

        Arguments:
           ID (SporaGen): Spora ID

        Returns:
            None
        """
        try:
            req = requests.post(choice(self._settings.URLs),
                                proxies=self._settings.PROXY_TOR,
                                headers=choice(self._settings.HEADERS),
                                data={'u': ID.get_id_str()})
            if req.status_code is 200:
                self.filter_request(req.content, ID)
            else:
                print("Error status code : {:d}".format(req.status_code))

        except:
            pass

    def filter_request(self, data, ID):
        """Filter the HTML content of Spora website to retrive
        the ransom prices.

        This function filters informations then stocks it in self._reqs list.

        Arguments:
            data (bytes): HTML content
            ID (SporaGen): Spora's ID used for the request

        Returns:
            None
        """
        tree = html.fromstring(data)
        names = tree.xpath(self._settings.NAME_SELECTOR)
        prices = tree.xpath(self._settings.PRICE_SELECTOR)

        # add ID information

        res = {'id': ID}
        # price information
        prices = [int(re.search(r'\d+', price).group(0)) for price in prices]
        res.update(dict(zip(names, prices)))

        print(ID.get_id_str())
        print(res)
        # add to the requests attribute
        self._reqs.append(res)

    def get_reqs(self):
        """Reqs getter"""

        return self._reqs

    def requests_to_csv(self, f=None):
        """Convert requests (self._reqs) to CSV.

        Arguments:
            f (str): file name that will receive the CSV data (default: None)

        Returns:
            None
        """
        # init
        csv = StringIO()
        delim = ';'

        # construct string
        header_csv = delim.join(["ID",
                                 "Country",
                                 "Hash",
                                 "Office",
                                 "PDF",
                                 "Autocad",
                                 "Database",
                                 "Image",
                                 "Archive",
                                 "Purchase total decrypt",
                                 "Purchase malware immune",
                                 "Purchase removal tool",
                                 "Purchase single decrypt",
                                 "Free decrypt"])
        csv.write(header_csv + '\n')

        for req in self._reqs:
            ID = req['id']
            try:
                req_csv = delim.join(list(map(str, [ID.get_id_str(),
                                                    ID.get_country(),
                                                    hex(ID.get_hash()),
                                                    ID.get_office(),
                                                    ID.get_pdf(),
                                                    ID.get_autocad(),
                                                    ID.get_db(),
                                                    ID.get_img(),
                                                    ID.get_archive(),
                                                    req['PURCHASETOTALDECRYPT'],
                                                    req['PURCHASEMALWAREIMMUNE'],
                                                    req['PURCHASEREMOVALTOOL'],
                                                    req['PURCHASESINGLEDECRYPT'],
                                                    req['FREEDECRYPT']])))
                csv.write(req_csv + '\n')
            except:
                pass

        if f:
            with open(f, "w") as text:
                text.write(csv.getvalue())
        else:
            print(csv.getvalue())

        csv.close()

class SporaGen:
    """SporaGen generates Spora's IDs

    Attributes:
        _country (str): 2 country letters
        _hash (int): 24-bit hash value
        _office (int): Number of office files
        _pdf (int): Number of pdf files
        _autocad (int): Number of autocad files
        _db (int): Number of db files
        _img (int): Number of img files
        _archive (int): Number of archive files
        _MIN_RAND (int): Minimum value for the generation of num for the ID (default: 0)
        _MAX_RAND (int): Maximum value for the generation of num for the ID (default: 200000)
    """
    _country = None
    _hash = None
    _office = None
    _pdf = None
    _autocad = None
    _db = None
    _img = None
    _archive = None
    _MIN_RAND = None
    _MAX_RAND = None

    def __init__(self, min_rand=0, max_rand=200000):
        """Initialization of SporaGen class.

        Parameters:
            _MIN_RAND (int): Minimum value for the generation of num for the ID (default: 0)
            _MAX_RAND (int): Maximum value for the generation of num for the ID (default: 200000)

        Returns:
            None
        """
        self.set_id()
        self.set_min_rand(min_rand)
        self.set_max_rand(max_rand)

    def get_country(self):
        """MIN_RAND getter

        Returns:
            str -- Returns the value of country
        """
        return self._country

    def get_hash(self):
        """Hash getter

        Returns:
            int -- Returns the value of hash
        """
        return self._hash

    def get_office(self):
        """office getter

        Returns:
            int -- Returns the value of office
        """
        return self._office

    def get_pdf(self):
        """pdf getter

        Returns:
            int -- Returns the value of pdf
        """
        return self._pdf

    def get_autocad(self):
        """autocad getter

        Returns:
            int -- Returns the value of autocad
        """
        return self._autocad

    def get_db(self):
        """db getter

        Returns:
            int -- Returns the value of db
        """
        return self._db

    def get_img(self):
        """img getter

        Returns:
            int -- Returns the value of img
        """
        return self._img

    def get_archive(self):
        """archive getter

        Returns:
            int -- Returns the value of archive
        """
        return self._archive

    def set_min_rand(self, min_rand):
        """MIN_RAND Setter

        Parameters:
            _MIN_RAND (int): Minimum value for the generation of num for the ID

        Returns:
            None
        """

        self._MIN_RAND = min_rand

    def get_min_rand(self):
        """MIN_RAND getter

        Returns:
            int -- Returns the value of MIN_RAND
        """

        return self._MIN_RAND

    def set_max_rand(self, max_rand):
        """MAX_RAND Setter

        Parameters:
            _MAX_RAND (int): Maximum value for the generation of num for the ID

        Returns:
            None
        """

        self._MAX_RAND = max_rand

    def get_max_rand(self):
        """MAX_RAND getter

        Returns:
            int -- Returns the value of MAX_RAND
        """

        return self._MAX_RAND

    def set_id(self, country="US", md5=0xF4242, office=0, pdf=0,
               autocad=0, db=0, img=0, archive=0):
        """Set the values of Spora ID

        Arguments:
            country (str): 2 country letters
            hash (int): 24-bit hash value
            office (int): Number of office files
            pdf (int): Number of pdf files
            autocad (int): Number of autocad files
            db (int): Number of db files
            img (int): Number of img files
            archive (int): Number of archive files

        Returns:
            None
        """

        self._country = country
        self._hash = md5 & 0xFFFFF
        self._office = office
        self._pdf = pdf
        self._autocad = autocad
        self._db = db
        self._img = img
        self._archive = archive

    def get_id_str(self):
        """Get the Spora's ID converted to string

        Returns:
            str -- Returns Spora's ID converted (eg.
                   RU302-15XRK-GXTFO-GZTET-KTXFF-ORTXA-AYYYY)
        """
        # Init sbox
        SBOX_OUT = "ZXROAHFGEKT"
        SBOX_IN = "0123456789|"
        TRANS = str.maketrans(SBOX_IN, SBOX_OUT)

        # Generate spora ID
        stats = "{:d}|{:d}|{:d}|{:d}|{:d}|{:d}".format(self._office, self._pdf,
                                                       self._autocad, self._db,
                                                       self._img, self._archive)

        spora_id = "{:s}{:x}{:s}".format(self._country, self._hash, stats.translate(TRANS))

        # Format spora ID
        id_sep = [spora_id[i:i + 5] for i in range(0, len(spora_id), 5)]
        spora_id = "-".join(map(lambda x: x.ljust(5, 'Y').upper(), id_sep))

        return spora_id

    def gen_id(self, country=None, md5=None, office=None, pdf=None,
               autocad=None, db=None, img=None, archive=None):
        """Generate a Spora ID.

        This method generate a spora id and fills the appropriate attribues.

        Returns:
            None
        """

        countries = ["AC", "AF", "AX", "AL", "DZ", "AD", "AO", "AI", "AQ", "AG",
                     "AR", "AM", "AW", "AU", "AT", "AZ", "BS", "BH", "BD", "BB",
                     "BY", "BE", "BZ", "BJ", "BM", "BT", "BO", "BA", "BW", "BV",
                     "BR", "IO", "VG", "BN", "BG", "BF", "BI", "KH", "CM", "CA",
                     "CV", "KY", "CF", "TD", "CL", "CN", "CX", "CC", "CO", "KM",
                     "CG", "CD", "CK", "CR", "CI", "HR", "CU", "CY", "CZ", "DK",
                     "DJ", "DM", "DO", "TP", "EC", "EG", "SV", "GQ", "EE", "ET",
                     "FK", "FO", "FJ", "FI", "FR", "FX", "GF", "PF", "TF", "GA",
                     "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GD", "GP", "GU",
                     "GT", "GN", "GW", "GY", "HT", "HM", "HN", "HK", "HU", "IS",
                     "IN", "ID", "IR", "IQ", "IE", "IM", "IL", "IT", "JM", "JP",
                     "JO", "KZ", "KE", "KI", "KP", "KR", "KW", "KG", "LA", "LV",
                     "LB", "LS", "LR", "LY", "LI", "LT", "LU", "MO", "MK", "MG",
                     "MW", "MY", "MV", "ML", "MT", "MH", "MQ", "MR", "MU", "YT",
                     "MX", "FM", "MD", "MC", "MN", "ME", "MS", "MA", "MZ", "MM",
                     "NA", "NR", "NP", "AN", "NL", "NC", "NZ", "NI", "NE", "NG",
                     "NU", "NF", "MP", "NO", "OM", "PK", "PW", "PS", "PA", "PG",
                     "PY", "PE", "PH", "PN", "PL", "PT", "PR", "QA", "RE", "RO",
                     "RU", "RW", "WS", "SM", "ST", "SA", "UK", "SN", "RS", "SC",
                     "SL", "SG", "SK", "SI", "SB", "SO", "AS", "ZA", "GS", "SU",
                     "ES", "LK", "SH", "KN", "LC", "PM", "VC", "SD", "SR", "SJ",
                     "SZ", "SE", "CH", "SY", "TW", "TJ", "TZ", "TH", "TG", "TK",
                     "TO", "TT", "TN", "TR", "TM", "TC", "TV", "UG", "UA", "AE",
                     "GB", "UK", "US", "UM", "UY", "UZ", "VU", "VA", "VE", "VN",
                     "VI", "WF", "EH", "YE", "ZM", "ZW"]

        self._country = choice(countries) if country is None else country
        self._hash = randint(0, 0xFFFFF) if md5 is None else md5 & 0xFFFFF
        self._office = randint(self._MIN_RAND, self._MAX_RAND) if office is None else office
        self._pdf = randint(self._MIN_RAND, self._MAX_RAND) if pdf is None else pdf
        self._autocad = randint(self._MIN_RAND, self._MAX_RAND) if autocad is None else autocad
        self._db = randint(self._MIN_RAND, self._MAX_RAND) if db is None else db
        self._img = randint(self._MIN_RAND, self._MAX_RAND) if img is None else img
        self._archive = randint(self._MIN_RAND, self._MAX_RAND) if archive is None else archive
