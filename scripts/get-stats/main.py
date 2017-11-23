#!/usr/bin/env python
import argparse

from Settings import SporaReqSettings
from Spora import SporaGen, SporaReq
from collections import deque
from retrying import retry
import numpy as np


def main():
    # usage
    args = usage()

    # init Spora object
    sporareq = SporaReq(SporaReqSettings())
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

    ## make requests
    # known samples
    rot = deque([0, 0, 1, 0, 0, 0])
    for i in range(5):
        for i in range(18000, 120000, 5000):
            for j in range(18000, 120000, 5000):
                sporaid = SporaGen()
                sporaid.set_id(country="NO",
                        md5=0x046FC1,
                        office=j*rot[0],
                        pdf=i,
                        autocad=j*rot[2],
                        db=j*rot[3],
                        img=j*rot[4],
                        archive=j*rot[5])

                sporareq.request(sporaid)
        rot.rotate(1)
    if args.file:
        sporareq.requests_to_csv(args.file)
    else:
        sporareq.requests_to_csv()


@retry
def send_req(i, sporareq, prices):

    rot = deque([0, 1, 0, 0, 0, 0])
    sporaid = SporaGen()
    sporaid.set_id(country="US",
            md5=0x056FC8,
            office=i*rot[0],
            pdf=i*rot[1],
            autocad=i*rot[2],
            db=i*rot[3],
            img=i*rot[4],
            archive=0*rot[5])

    sporareq.request(sporaid)
    reqs = sporareq.get_reqs()
    try:
        prices[i] = reqs[-1]["PURCHASETOTALDECRYPT"]
    except:
        print("Failed RETRY")
        raise IOError("Connection problem")

    print("{:d}".format(i))


    #  for i in range(21, 21315 + 143*3 +1, 143):

    #  for i in range(20725, 20731, 1):
    #      sporaid = SporaGen()
    #      sporaid.set_id(country="IT",
    #              md5=0x046FC3,
    #              office=i*rot[0] - 1,
    #              pdf=0,
    #              autocad=0*rot[2],
    #              db=0*rot[3],
    #              img=0*rot[4],
    #              archive=0*rot[5])
    #
    #      sporareq.request(sporaid)
    # # random generation
    # for i in range(0, 100):
        # sporaid = SporaGen()
        # sporaid.set_max_rand(50000)
        # sporaid.gen_id(country="US")
        # sporareq.request(sporaid)

    # # countries tests
    # for country in countries:
        # sporaid = SporaGen()
        # sporaid.set_id(country=country,
                       # md5=0x1337F,
                       # office=4533,
                       # pdf=2326,
                       # autocad=14984,
                       # db=40801,
                       # img=953,
                       # archive=44992)
        # sporareq.request(sporaid)


def usage():
    parser = argparse.ArgumentParser(description='Spora stats')
    parser.add_argument('-f', '--file', action='store', help="Output file for the CSV")

    return parser.parse_args()


if __name__ == '__main__':
    main()
