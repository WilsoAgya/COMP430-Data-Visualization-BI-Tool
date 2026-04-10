import pandas as pd
import requests
import yfinance as yf
import io


#Decided to stick with hardcoded companies for now just using 10 popular ones
#tickers = ['AMD','AAPL','MSFT','GOOG','TSLA','NVDA','JPM','HOOD','PEP','VST']
#tickers = ['IBM','CVX','AMZN','INTC','JPM','HD','KO','BA','CSCO','DIS']
#There are different lists of tickers because for each time new data was added
tickers = [
    'META', 'NFLX', 'UBER', 'V',    'MA',
    'GS',   'MS',   'BAC',  'WFC',  'C',
    'XOM',  'CRM',  'ORCL', 'ADBE', 'QCOM',
    'MU',   'TXN',  'AVGO', 'TSM',  'ARM',
    'WMT',  'TGT',  'NKE',  'MCD',  'SBUX',
    'LLY',  'JNJ',  'PFE',  'VZ',   'T'
    # Mega cap / blue chip
    'AMGN', 'MDT',  'ABT',  'TMO',  'DHR',
    'LMT',  'RTX',  'GD',   'NOC',  'CAT',
    'DE',   'MMM',  'HON',  'EMR',  'GE',
    'UPS',  'FDX',  'WM',   'RSG',  'CTAS',

    'AXP',  'BLK',  'SCHW', 'ICE',  'CME',
    'SPGI', 'MCO',  'COF',  'USB',  'PNC',
    'TFC',  'AIG',  'PRU',  'MET',  'AFL',
    'TRV',  'ALL',  'PGR',  'CB',


    'NOW',  'WDAY', 'SNOW', 'DDOG', 'NET',
    'CRWD', 'OKTA', 'ZS',   'PANW', 'FTNT',
    'AMAT', 'LRCX', 'KLAC', 'MCHP', 'ADI',
    'NXPI', 'TXN',  'MPWR', 'ON',   'STX',

 
    'COST', 'TGT',  'LOW',  'ORLY', 'AZO',
    'EBAY', 'ETSY', 'CHWY', 'BKNG', 'ABNB',
    'LYFT', 'DASH', 'UBER', 'SHOP',


    'UNH',  'CVS',  'CI',   'HUM',  'ELV',
    'ISRG', 'DXCM', 'IDXX', 'VRTX', 'REGN',


    'OXY',  'COP',  'EOG',  'SLB',  'HAL',
    'PSX',  'MPC',  'VLO',  'KMI',  'WMB',

    'BABA', 'JD',   'BIDU', 'PDD',  'NIO',

    'TTWO', 'EA',   'RBLX', 'U',    'SE',

    'SNAP', 'PINS', 'SPOT', 'MTCH', 'RDDT',  'ZM',   'DUOL',

    'PYPL', 'AFRM', 'SOFI', 'UPST', 'NU',

    'MARA', 'RIOT', 'CLSK',

    'LCID', 'XPEV', 'LI',   'CHPT', 'ENPH', 'FSLR', 'NEE', 'CEG',

    'MRNA', 'BNTX', 'BIIB', 'ALNY', 'INCY', 'NVAX',

    'NVO',  'SAP',  'TM',   'SNY',  'AZN',  'SHEL', 'VALE', 'SONY', 'RACE',
    
    'AMT',  'EQIX', 'PLD',  'O',    'VICI', 'DLR',  'PSA',

    'ODFL', 'SAIA', 'ZIM',  'DAL',  'UAL',
    # Emerging tech
    'IONQ', 'SMCI', 'APP',  'SOUN', 'RKLB', 'ASTS',

    'DELL', 'HPE',  'GDDY', 'AKAM', 'NTAP',
    'CDW',  'BAH',  'SAIC', 'LDOS', 'KEYS',
     'FIS',  'GPN',  'TOST', 'FOUR',
    'CMG',  'YUM',  'QSR',  'DRI',  'WING',
    'CAVA', 'BROS', 'ANF',  'URBN', 'RL',
    'BSX',  'EW',   'RMD',  'PODD', 'ALGN',
    'ZBH',  'HOLX', 'STE',  'GEHC', 'AXON',
    'ITW',  'PH',   'ROK',  'IR',   'FAST',
    'GWW',  'GNRC', 'TDY',  'CACI', 'HII',
    'DVN',  'FANG',  'EQT',  'APA',
    'CMCSA','CHTR', 'WBD',  'LYV',  'FOXA',
    'MAR',  'HLT',  'CCL',  'RCL',  'NCLH',
    'ADM',  'BG',   'MOS',  'CF',   'NTR',
    'CELH', 'DECK', 'ELF',  'CART', 'CSGP',
    'TWLO', 'HUBS', 'BILL', 'PCTY', 'PAYC',
    'VEEV', 'PATH', 'MDB',  'CFLT', 'GTLB',
    'ESTC', 'AI',   'CDNS', 'SNPS', 'EPAM',
    'GLOB', 'INFY', 'PTC',  'APPF', 'PEGA',
    'MANH',   'BRZE', 'DOMO', 'NCNO',
    'WOLF', 'ACLS', 'ONTO', 'AMBA', 'CRUS',
    'LSCC', 'ALGM', 'OLED', 'SITM', 'COHR',
    'LITE', 'VIAV', 'CIEN', 'FFIV', 'POWI',
    'ALLY', 'HBAN', 'RF',   'CFG',  'FITB',
    'KEY',  'MTB',  'CMA',  'ZION', 'WAL',
    'EWBC', 'OZK',  'FFIN', 'IBCP', 'SFNC',
    'ACGL', 'WRB',  'HIG',  'CINF', 'ERIE',
    'RYAN', 'RNR',  'LPLA', 'SF',   'JEF',
    'PIPR', 'MKTX', 'IBKR', 'FUTU', 'WU',
    'ABBV', 'BMY',  'MRK',  'GILD', 'ILMN',
    'IQV',  'CRL',  'RVTY', 'MEDP', 'LNTH',
    'NTRA', 'GH',   'EXAS', 'RARE', 'ACAD',
    'ARWR', 'BEAM', 'CRSP', 'NTLA', 'JAZZ',
    'LULU',   'PVH',   'CROX',
    'ONON', 'HAS',  'MAT',  'TPR',  'CPRI',
    'RH',   'WSM',  'BBWI', 'BURL', 'TJX',
    'ROST', 'FIVE', 'OLLI', 'BJ',   'SFM',
    'KR',   'SYY',  'GIS',  'CAG',  'CPB',
    'HRL',  'CLX',  'CHD',  'EL',   'COKE',
    'MKC',  'SJM',  'KHC',  'TAP',  'STZ',
    'DOV',  'XYL',  'ROP',  'VRSK', 'WAB',
    'TT',   'OTIS', 'CARR',  'HWM',
    'TDG',  'HEI',  'KTOS', 'DRS',  'CW',
    'AVAV',  'WWD',  'POWL', 'TRMB',
    'ZBRA', 'CGNX', 'NOVT',
    'AWK',  'WEC',  'ES',   'PPL',  'CMS',
    'LNT',  'ATO',  'NI',   'NRG',  'DTE',
    'ETR',  'FE',   'PNW',  'SRE',  'CNP',
    'AR',   'RRC',  'SM',   'MTDR',
    'CHRD', 'PR',   'TRGP', 'AM',   'FCX',
    'SHW',  'PPG',  'ECL',  'LYB',  'EMN',
    'OLN',  'CE',   'RPM',  'IFF',  'ALB',
    'MP',   'AA',   'FCX',  'HBM',
    'MGM',  'CZR',  'LVS',  'WYNN', 'PENN',
    'DKNG', 'RSI',
    'EXPE', 'TRIP', 'H', 'KVUE',   'WH',   'CHH',
    'CBRE', 'JLL',  'Z',    'MTG',  'RDN',
    'TNDM', 'NEOG', 'QDEL', 'HRMY', 'PTCT',
    'PRGO', 'ADMA', 'INVA', 'VRT'
]


raw_data = []

#Basic data extraction for the ticker dimension
def extract():

    raw_data.clear()

    for ticker in tickers:
        finance_data = yf.Ticker(ticker)
        #Extraction of useful data from the yfinance API
        try:
            raw_data.append({
                "ticker" : ticker,
                "info" : finance_data.info, 
                "financials" : finance_data.financials,
                "history": finance_data.history(period="6mo", interval="1h")
            })
        except Exception as e:
            print(f"Failed for {ticker}: {e}")



    return raw_data

