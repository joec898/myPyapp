# -*- coding: utf-8 -*-
"""
Evaluation filter( underlying/vol Live, settle etc.)
(there is no list) List of MarketSymbol, Delta, Gamma, Vega,Theta of existing greeks from legacy
POST /postions/vXX/enrichedtradeevaluations?

Group EnrichedTradeEvaluations by market, underlying, portfolio, strategy (if applicable) and sum greeks

Code is adapted from RTDeltaBalance 1_5.py of Diana team
"""
import numpy as np
import pandas as pd
import requests
import json
import datetime as dt
import os

# class global variable
proxy_username = ""
proxy_password = ""
asOfDate = ""
version = ""
env = ""
portfolios = []
strategies = []
body = {}
header = {}
base_urls = {}
proxies = {}
main_url = ""

today=dt.datetime.today()
df_underTrade=pd.DataFrame()

def Initialize(settings):
    # values in self is realtime, values in settings are from properties.csv 
    global proxy_username
    global proxy_password
    global portfolios
    global strategies
    global asOfDate
    global version
    global env   
    
    global header  
    global base_urls  
    global proxies  
    global settle_date
    global body  
    global main_url
        
    proxy_username = settings.username
    proxy_password = settings.password
    asOfDate = settings.asof_date
    version = settings.version
    env = settings.env
    
    portfolios = settings.portfolios.split(",") #list(set(settings.portfolios))
    strategies = settings.strategies.split(",")
    
    if ((not portfolios[0]) or (portfolios[0]=='nan')): 
        print ('portfolio input cannot be empty!')
        exit()
        
    if ((not strategies[0]) or (strategies[0]=='nan')): strategies=[]
    
    header = {
        'Authorization' : 'Bearer ' + settings.token,
        'Content-type':'application/json', 
        'Accept':'application/json', 
        'Accept-Encoding': 'gzip'
    }
    
    base_urls = { 'dev': settings.base_url_dev,
             'qa': settings.base_url_qa,
             'uat': settings.base_url_uat,
             'production': settings.base_url_prod
             }

    # proxy_username = '' #your DS ID
    # proxy_password = '' #your DS Password
    proxy = 'http://{}:{}@{}'.format(proxy_username, proxy_password, settings.proxy_url)

    proxies = {
        'http' : proxy, 
        'https' : proxy 
    }
    
    settle_date = asOfDate #allows flexibility later, start here
    
    body = {
                "requestedSettleDate": settle_date,
                "underlyingStateRequestTypeCode": settings.price_type,
                "requestedUnderlyingSettleDate": settle_date,
                "volatilityStateRequestTypeCode": settings.vol_type,
                "requestedVolatilitySettleDate": settle_date,
                "calculateAttribution": True,
                "evaluationsOnly": False,
                "requestedValueDate": settle_date
            }

    if 'production' == env:
        main_url = base_urls[env]+'positions/' + version
    else:
        main_url = base_urls[env]+'positions/'+env + '/' + version
    
    print('main_url: ' + main_url)
    
    if not os.path.exists(settings.filepath):
        os.makedirs(settings.filepath)

    
def DownloadTrades(settings):
    Initialize(settings)
    print("strategies list: " + " ".join(strategies))
    df_detail = ApiCall(settings)
    
    return df_detail

def TestDownloadTrades(settings):
    df_detail = DownloadTrades(settings)
  
    df_main = ProcessExistingTrades(df_detail)
    file_date = today.strftime('%m%d %H%M%S')  
    file_name = 'rt_existing_db_' + file_date + '.csv'
    print('writing rt existing trades to '+ file_name)
    df_main.to_csv(settings.filepath + file_name, index=False)
    
    new_rt_trades = ProcessNewTrades(df_main, settings)
    filename = 'rt_db_'+file_date+'.csv'
    print('writing new rt trades to '+ filename)
    new_rt_trades.to_csv(settings.filepath + filename, index=False)   
    
    new_zeno_trades = ProcessZenoTrades(df_main, settings)
    filename = 'zeno_db_'+file_date+'.xlsx'
    print('writing zeno trades to ' +filename)
    new_zeno_trades.to_excel(settings.filepath + filename, index=False)
    
    
    #%% API call
def ApiCall(settings):
    
    global df_underTrade      
    try:
        if strategies:
            print("Start api call to download trades: strategies list: ".join(strategies))
            data = []
            underTrade_data = []
            hedge_data = []
            data_detail = []
            df_underTrade=pd.DataFrame()
            df_detail=pd.DataFrame()
            for pp in portfolios:
                for ss in strategies:
                    print('getting data for:',pp,' : ', ss)
                    query ='/enrichedtradesevaluation/?AcquirerCodes='+settings.acquirer+'&AsOfDate='+settings.asof_date+'&PortfolioNames='+pp+'&StrategyNames='+ss
                    url = main_url+query
                    #print("body: " + json.dumps(body))
                    diana_https_response = requests.post(
                                url,  
                                data=json.dumps(body),
                                headers=header,
                                proxies=proxies,
                                verify=True) 
                    print(diana_https_response)
                    if diana_https_response.status_code == 401:
                        print("Unauthorized access: " + url)
                        raise
                    
                    response = json.loads(diana_https_response.content)
                    # inject portfolio and strategy into the dict
                    response['tradeEvaluationSummary']['portfolio']=pp
                    response['tradeEvaluationSummary']['strategy']=ss
                    data.append(response['tradeEvaluationSummary'])
                    
                    for rr in response['enrichedTradeEvaluations']:
                        rr['portfolio']=pp 
                        rr['strategy']=ss 
                    for rr in response['underlyingTradeSummaries']:
                        rr['portfolio']=pp 
                        rr['strategy']=ss 
                    for rr in response['suggestedHedges']:
                        rr['portfolio']=pp 
                        rr['strategy']=ss
                    underTrade_data= underTrade_data + response['underlyingTradeSummaries']
                    hedge_data = hedge_data + response['suggestedHedges']
                    data_detail = data_detail + response['enrichedTradeEvaluations']
                
                    df_underTrade = pd.DataFrame(underTrade_data)
                    df_detail = pd.DataFrame(data_detail)
            
        # if user did not specify strategy then omit the strategy 
        # also want to know RT strategy names, df contains an Id
        else:
            print("Start api call to download trades: getting all strategies for each portfolio")
            data = []
            underTrade_data = []
            hedge_data = []
            data_detail = []
            #self.portfolios = list(set(settings.portfolios)) #if a portfolio is listed multiple times it will introduce duplicates.
            for pp in portfolios:
                print('getting data for:', pp)
                query ='/enrichedtradesevaluation/?AcquirerCodes='+settings.acquirer+'&AsOfDate='+asOfDate+'&PortfolioNames='+pp
                url = main_url+query
            
                diana_https_response = requests.post(
                            url,  
                            data=json.dumps(body),
                            headers=header,
                            proxies=proxies,
                            verify=True) 
                print(diana_https_response)
                if diana_https_response.status_code == 401:
                    print("Unauthorized access: " + url)
                    raise
                    
                response = json.loads(diana_https_response.content)
                # inject portfolio and strategy into the dict
                response['tradeEvaluationSummary']['portfolio']=pp
                data.append(response['tradeEvaluationSummary'])
                
                for rr in response['enrichedTradeEvaluations']:
                    rr['portfolio']=pp 
                for rr in response['underlyingTradeSummaries']:
                    rr['portfolio']=pp 
                for rr in response['suggestedHedges']:
                    rr['portfolio']=pp 
                underTrade_data= underTrade_data + response['underlyingTradeSummaries']
                hedge_data = hedge_data + response['suggestedHedges']
                data_detail = data_detail + response['enrichedTradeEvaluations']
                                                    
            df_underTrade = pd.DataFrame(underTrade_data)
            df_detail = pd.DataFrame(data_detail)
    
            # we want to have strategy names as well as id avaialble
            strategy_ids = list(set(df_detail['strategyId']))
            strategy_names = {}
            for ss in strategy_ids:
                diana_https_response = requests.get(
                            main_url+'/strategies?Ids='+str(ss),  
                            headers=header,
                            proxies=proxies,
                            verify=True) 
                print('strategy id:',str(ss),diana_https_response)
                response = json.loads(diana_https_response.content)
                strategy_names[ss]=response[0]['name']
            df_detail['strategy']=[strategy_names[id] for id in df_detail['strategyId']]
            
        print("Api call to download RT trade data completed.")    
        return df_detail

    except ValueError as ve:
        print(ve.args)
        raise


#%%  return a data frame of existing trades
def ProcessExistingTrades(df_detail):
    # make a dataframe and groupby
    # 1) flatten greek decomposition on each enriched trade evaluation and sum by underlyingsymbol, portfolio, strategy
    # we have delta and we know change in delta, to rebalance(flatten) for each trade want change in delta quantity for new hedge trade
    # create trades for RT by reversing the direction of the decmpose delta in each group (round to 1or2 decimals)

    # make columns for the greekDecompositon fields from inside the dictionary
    # must handle the cases where there is a list of items in greekDecompositions
    # this is messy to flatten the list of nested dictionaries but it is explicit and readable
    try:
        print("Started processing existing trades...") 
        df = df_detail
        rows=[] #a list of dictionaries with all the necessary fields populated
        for a,p,sid,s,q,us,ut,gd in zip(df['acquirerCode'], df['portfolioName'],df['strategyId'],
                                    df['strategy'],df['quantity'],df['underlyingSymbol'],df['underlyingType'],df['greekDecompositions']):
            for ii in gd: #iterate over the list of dicts in greekDecomposition
                rows.append({'acquirerCode':a ,'portfolioName': p,'strategyId':sid ,
                                    'strategy':s ,'quantity':q , 'full_underlyingSymbol': us,
                                    'underlyingType':ut, 'decomposed_delta': ii['delta'],
                                    'decomposed_tasDelta': ii['tasDelta'],'marketSymbol': ii['marketSymbol'],
                                    'underlyingSymbol':ii['underlyingSymbol']})
        decompose_df = pd.DataFrame(rows)
    
        # if we are using the 'detail' we want to group by underlying/portfolio/strategy       'positionDate',
        fields = ['acquirerCode','marketSymbol', 'portfolioName','strategyId','strategy',
                'quantity','underlyingSymbol','decomposed_delta','decomposed_tasDelta']
        df_main = decompose_df[fields].groupby(['acquirerCode','portfolioName','strategyId','strategy','marketSymbol'
                        ,'underlyingSymbol']).sum()
    
        df_main = df_main.reset_index()
        df_underlying=df_underTrade[['marketSymbol','symbol','ask','mid','bid','change','priceChange', 'settlePrice','settleDate']].drop_duplicates()
    
        # merge in the underlying price and change information (duplicate mid to check merge)
        df_main = pd.merge(df_main, df_underlying, 'left', left_on = ['underlyingSymbol','marketSymbol'], right_on = ['symbol','marketSymbol'])
        df_main['flipped_delta']= np.round(df_main['decomposed_delta']*-1,0) #round to whole number
        df_main['trade_quantity']=df_main['flipped_delta']
        df_main['zeno_quantity']=df_main['flipped_delta']*-1 #zeno trade is opposite of rt flattening trades
    
        # make the usual market symbols from the special CalendarSpreadFutures symbols
        df_main['zeno_market']= [rr.split('|')[0] for rr in df_main['marketSymbol']]
        mkt_mapping_dict = {'EBM':'CA','EMA':'EP','ECO':'IJ'}
        df_main['zeno_underlying']=df_main['underlyingSymbol']
        for key, value in mkt_mapping_dict.items():
            df_main['zeno_market'] = df_main['zeno_market'].replace(key, value)
            df_main['zeno_underlying'] = df_main['zeno_underlying'].replace(key, value, regex=True)
    
        df_main['zeno_strategy'] = df_main['zeno_market']+'DELTA'
    
        df_main['tradeDate']=str(today.date())        
                
        print("Processing existing trades completed.")  
        return df_main

    except ValueError as ve:
        print(ve.args)
        raise


def cleanDF(df_main, settings):
    #remove zero quantity rows
    df_main = df_main[df_main['trade_quantity']!=0]
    
    df_main['Counterparty']='CGCRMPD'
    df_main['settleType'] = 'F'
    df_main['comment'] = 'ZENOBAL'
    df_main['legal entity'] = 'CGCRMPD'
    df_main['sec cpty']='NONE'
    df_main['Acquirer']= settings.acquirer

    def Port_Team(portfolio):
        switcher = {
                'Corn NA':"Origination",
                'Soybean NA': "Origination",
                'Chicago Wheat NA':"Origination",
                'Kansas Wheat NA':"Origination",
                'Minneapolis Wheat NA':"Origination",
                'Grains OTC Orig':"Origination",
                'Veg Oil OTC Orig':"Origination",
                'Grains OTC PANGEA':"PANGEA",
                'Softs OTC PANGEA':"PANGEA",
                'Veg Oil OTC PANGEA':"PANGEA",
                'Livestock OTC PANGEA':"PANGEA",
                'Grains OTC NORAM': "NORAM",
                'Veg Oil OTC NORAM': "NORAM",
                'Softs OTC NORAM': "NORAM",
                'Livestock OTC NORAM': "NORAM",
                'Grains Trading':"Trading",
                'Livestock Trading':"Trading",
                'Softs Trading':"Trading",
                'Veg Oil Trading':"Trading",
                'Grains OTC APAC': "APAC",
                'Veg Oil OTC APAC': "APAC",
                'Softs OTC APAC': "APAC",
                'Livestock OTC APAC': "APAC",
                }
        return switcher.get(portfolio,'No Team Found')

    df_main['Team']= df_main['portfolioName'].apply(Port_Team)

    return df_main

#%%  RT deltaBalance Trades
def ProcessNewTrades(df_main, settings):    
    try:
        df_main = cleanDF(df_main, settings)
        
        print("Started processing new trades...") 
        rt_fields = ['trade_quantity','underlyingSymbol','mid','portfolioName','Acquirer',
                    'Counterparty','strategy','tradeDate','Team']    #,'settleType','comment',,'underlyingSymbol'
        new_rt_trades = df_main[rt_fields].copy()
        #new_rt_trades = new_rt_trades.loc[abs(new_rt_trades['trade_quantity'])>=0.0001]
        #new_rt_trades['Delta']=0
    
        new_rt_trades['ID']=''
        new_rt_trades['Customer Order ID']=''
        new_rt_trades['Risk Price']=new_rt_trades['mid']
    
        #new_rt_trades['Direction']=np.sign(new_rt_trades['trade_quantity'])
    
        rt_names = {'trade_quantity':'Quantity',  'underlyingSymbol':'Symbol', 'mid':'Price', 
                    'portfolioName':'Portfolio', 'strategy':'Strategy'}
        new_rt_trades = new_rt_trades.rename(columns=rt_names)
                
        print("Processing new trades completed.")     
        return new_rt_trades

    except ValueError as ve:
        print(ve.args)
        raise

    #%%  zeno trades
def ProcessZenoTrades(df_main, settings):
    # create trades for zeno (format tbd) that reverse the direction of the total sum by underlying trades in 2)
    #form of fields in zeno file
    #Trade ID	Inst ID	B/S	Inst Symbol	Inst Type	Trade Date	Quantity	Price	Strategy	Cpty	Legal Entity	Settle Type	Settle Date	Sec Cpty	Contact	Trade Type	Comment
    def direction(zeno_qty):
        if zeno_qty > 0 :
            dir = 'B'
        else:
            dir = 'S'
        return dir
        
    try:
        print("Started processing zeno trades...") 
        df_main = cleanDF(df_main,settings)
        
        # settings.asof_date is in yyyy-mm-dd formate
        # convert to a format of dd/mm/yyyy
        asOfDate = dt.datetime.strptime(settings.asof_date,'%Y-%m-%d') 
        #df_main['tradeDate']=asOfDate.strftime('%m/%d/%Y')
        df_main.loc[:,'tradeDate']=asOfDate.strftime('%m/%d/%Y')
    
        zeno_fields = ['portfolioName','strategy','zeno_underlying', 'tradeDate', 'zeno_quantity','mid', 'zeno_strategy',
                    'Counterparty','legal entity', 'settleType','settleDate','sec cpty']
        new_zeno_trades = df_main[zeno_fields].copy()
        new_zeno_trades['B/S']=new_zeno_trades['zeno_quantity'].apply(direction)
        new_zeno_trades['zeno_quantity']=abs(new_zeno_trades['zeno_quantity'])
        new_zeno_trades['Trade ID']=''
        new_zeno_trades['Inst Type']='FuturesContract'
        new_zeno_trades['Inst ID']=''
        new_zeno_trades['Contact']=''
        new_zeno_trades['Trade Type']=''
        new_zeno_trades['Comment']='BAL'
    
        zeno_names = {'zeno_underlying': 'Inst Symbol', 'tradeDate':'Trade Date', 'zeno_quantity':'Quantity', 
                    'mid':'Price', 'zeno_strategy':'Strategy', 'Counterparty':'Cpty', 
                    'legal entity':'Legal Entity', 'settleType':'Settle Type',
                    'settleDate':'', 'sec cpty':'Sec Cpty'}
        new_zeno_trades = new_zeno_trades.rename(columns=zeno_names)
        #new_zeno_trades = new_zeno_trades.loc[abs(new_zeno_trades['Quantity'])>0.000001]
            
        print("Processing zeno trades completed.") 
        return new_zeno_trades
    
    except ValueError as ve:
        print(ve.args)
        raise
