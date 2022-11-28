import json
import logging
import os
from pymongo import MongoClient
import sched, time
from twelvedata import TDClient
# dev
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# logging.basicConfig(filename='/var/log/pyparser.log', level=logging.INFO)

logging.basicConfig(filename='pyparser.log', level=logging.INFO)

mg = MongoClient(os.environ['MONGO_PUBLIC_IP'], int(os.environ['MONGO_PORT']),
                 username=os.environ['MONGO_USER'],
                 password=os.environ['MONGO_PASSWORD'])
collection_ohlc_one_min = mg['stockdb']['ohlc_one_min_test']
collection_ohlc_five_min = mg['stockdb']['ohlc_five_min_test']
logging.info(collection_ohlc_one_min)
logging.info(collection_ohlc_five_min)

td = TDClient(apikey=os.environ["API_KEY"])

t = ["KOLD",
     "LABU",
     "SDS",
     "SH",
     "SOXS",
     "SPXU",
     "SQQQ",
     "SSO",
     "TZA",
     "AA",
     "AAL",
     "AAP",
     "AAPL",
     "ABBV",
     "ABEV",
     "ABNB",
     "ABT",
     "ADBE",
     "ADI",
     "ADT",
     "ADTX",
     "AEHR",
     "AFRM",
     "AGBA",
     "AGNC",
     "AHCO",
     "AKRO",
     "ALK",
     "ALT",
     "ALT",
     "AMAT",
     "AMC",
     "AMD",
     "AMGN",
     "AMLX",
     "AMV",
     "AMZN",
     "APA",
     "APE",
     "APPS",
     "APRN",
     "ARRY",
     "ASTS",
     "ASX",
     "ATVI",
     "AUY",
     "AVDL",
     "AVGO",
     "AZTA",
     "BA",
     "BABA",
     "BAC",
     "BAX",
     "BBBY",
     "BBD",
     "BBWI",
     "BCTX",
     "BEKE",
     "BHC",
     "BIAF",
     "BIDU",
     "BILI",
     "BMTX",
     "BMY",
     "BNTX",
     "BOIL",
     "BP",
     "BSX",
     "BTU",
     "BX",
     "BYND",
     "BZ",
     "CARR",
     "CASY",
     "CCJ",
     "CCL",
     "CGC",
     "CHNG",
     "CHPT",
     "CHWY",
     "CLF",
     "CLFD",
     "CLOV",
     "CMCSA",
     "CNC",
     "CNP",
     "COIN",
     "COP",
     "COUP",
     "CRM",
     "CRWD",
     "CSCO",
     "CSGP",
     "CSX",
     "CVNA",
     "CVS",
     "CVX",
     "DAL",
     "DASH",
     "DBGI",
     "DD",
     "DDOG",
     "DHI",
     "DIS",
     "DKNG",
     "DLO",
     "DNA",
     "DOCS",
     "DOCU",
     "DT",
     "DVN",
     "DWAC",
     "DXC",
     "EA",
     "EBIX",
     "ECOM",
     "EDIT",
     "EIGR",
     "ELAN",
     "ENPH",
     "EPD",
     "EQNR",
     "EQT",
     "ET",
     "ETSY",
     "EW",
     "EXC",
     "F",
     "FAST",
     "FB",
     "FCX",
     "FDX",
     "FE",
     "FIS",
     "FISV",
     "FIVN",
     "FL",
     "FRO",
     "FSLY",
     "FSR",
     "FTCH",
     "FXI",
     "GCT",
     "GE",
     "GETY",
     "GFI",
     "GGB",
     "GILD",
     "GLBL",
     "GM",
     "GME",
     "GOGO",
     "GOLD",
     "GOOG",
     "GOOGL",
     "GPS",
     "GRAB",
     "GRUB",
     "GSAT",
     "GSK",
     "GSUN",
     "GTHX",
     "GXO",
     "HA",
     "HAL",
     "HD",
     "HKD",
     "HL",
     "HOOD",
     "HPCO",
     "HPQ",
     "HUDI",
     "IBM",
     "IBN",
     "IBRX",
     "INDI",
     "INTC",
     "INVH",
     "IONQ",
     "IPAX",
     "IQ",
     "IS",
     "ISEE",
     "ISEE",
     "ISIG",
     "ITUB",
     "IWM",
     "JBHT",
     "JD",
     "JMIA",
     "JNJ",
     "JPM",
     "JWN",
     "KALA",
     "KGC",
     "KHC",
     "KNBE",
     "KO",
     "KOLD",
     "KOS",
     "KOSS",
     "KPRX",
     "KR",
     "KSS",
     "LCID",
     "LMND",
     "LNG",
     "LOW",
     "LTHM",
     "LU",
     "LULU",
     "LUMN",
     "LUV",
     "LVS",
     "LYFT",
     "M",
     "MACK",
     "MCD",
     "MDLZ",
     "MDT",
     "MEGL",
     "META",
     "MGNI",
     "MMM",
     "MMTLP",
     "MNDT",
     "MNDY",
     "MO",
     "MOS",
     "MPW",
     "MRK",
     "MRNA",
     "MRO",
     "MRVL",
     "MS",
     "MSFT",
     "MSGM",
     "MSTR",
     "MU",
     "NBRV",
     "NCR",
     "NEE",
     "NEM",
     "NET",
     "NFLX",
     "NINE",
     "NIO",
     "NKE",
     "NLOK",
     "NLSN",
     "NLY",
     "NOK",
     "NOTV",
     "NRBO",
     "NTNX",
     "NTRA",
     "NU",
     "NUTX",
     "NVAX",
     "NVDA",
     "O",
     "OKTA",
     "OLPX",
     "ON",
     "ONON",
     "OPNT",
     "ORCL",
     "ORMP",
     "OUT",
     "OXY",
     "PAA",
     "PAAS",
     "PACB",
     "PANW",
     "PARA",
     "PATH",
     "PAYO",
     "PBR",
     "PCG",
     "PDD",
     "PDSB",
     "PENN",
     "PEP",
     "PERF",
     "PFE",
     "PG",
     "PINS",
     "PIXY",
     "PLTK",
     "PLTR",
     "PLUG",
     "PM",
     "PRVB",
     "PSNY",
     "PSQ",
     "PTON",
     "PXMD",
     "PYPL",
     "QCOM",
     "QQQ",
     "QRTEB",
     "QSR",
     "RAD",
     "RBLX",
     "RCL",
     "RDFN",
     "RETA",
     "RIG",
     "RIVN",
     "RKT",
     "RLAY",
     "RLX",
     "RNG",
     "ROKU",
     "ROOT",
     "ROST",
     "RUN",
     "RXT",
     "RYCEY",
     "SAVA",
     "SBGSY",
     "SBUX",
     "SCHW",
     "SE",
     "SGFY",
     "SHAK",
     "SHLS",
     "SHOP",
     "SHPH",
     "SI",
     "SLB",
     "SLV",
     "SMAR",
     "SNAP",
     "SNOW",
     "SOFI",
     "SOXL",
     "SPCE",
     "SPWR",
     "SPXS",
     "SPY",
     "SQ",
     "SQQQ",
     "SQSP",
     "SRPT",
     "SST",
     "STNE",
     "STX",
     "SWN",
     "T",
     "TCEHY",
     "TEAM",
     "TELL",
     "TEVA",
     "TGT",
     "TGTX",
     "TINV",
     "TJX",
     "TLRY",
     "TLT",
     "TME",
     "TMUS",
     "TOST",
     "TQQQ",
     "TRIP",
     "TROW",
     "TRQ",
     "TSLA",
     "TSM",
     "TSP",
     "TTD",
     "TTWO",
     "TWLO",
     "TWST",
     "TXN",
     "U",
     "UAL",
     "UBER",
     "ULTA",
     "UNP",
     "UPS",
     "UPST",
     "UVXY",
     "V",
     "VALE",
     "VERI",
     "VERU",
     "VOD",
     "VTRS",
     "VZ",
     "W",
     "WBD",
     "WDAY",
     "WDC",
     "WELL",
     "WFC",
     "WMT",
     "WOLF",
     "WYNN",
     "XELA",
     "XOM",
     "XP",
     "XPEV",
     "YMM",
     "YOU",
     "Z",
     "ZEN",
     "ZI",
     "ZIM",
     "ZM",
     "ZS"]
s = sched.scheduler(time.time, time.sleep)


def pull_ohlc_one(sc, tickers):
    # schedule next execution
    sc.enter(60, 1, pull_ohlc_one, (sc, tickers))
    for x in tickers:
        # pull td data and convert to df
        one_min = td.time_series(
            symbol=x,
            interval="1min",
            outputsize=6,
            timezone="America/New_York",
        )
        one_df = one_min.as_pandas().reset_index()

        # add labels, calc diff
        one_df["ticker"] = x
        one_df["delta"] = one_df["close"].diff()

        # drop initial row used for calculation
        one = one_df.iloc[1:, :]

        # insert into mongo
        collection_ohlc_one_min.insert_many(json.loads(one.to_json(orient="records")))


def pull_ohlc_five(sc, tickers):
    # schedule next execution
    sc.enter(300, 1, pull_ohlc_five, (sc, tickers))
    for x in tickers:
        # pull td data and convert to df
        five_min = td.time_series(
            symbol=x,
            interval="5min",
            outputsize=2,
            timezone="America/New_York",
        )
        five_df = five_min.as_pandas().reset_index()

        # add labels, calc diff
        five_df["ticker"] = x
        five_df["delta"] = five_df["close"].diff()

        # drop initial row used for calculation
        five = five_df.iloc[1:, :]

        # insert into mongo
        collection_ohlc_five_min.insert_many(json.loads(five.to_json(orient="records")))


s.enter(0, 1, pull_ohlc_one, (s, t))
s.enter(0, 1, pull_ohlc_five, (s, t))
s.run()