import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns


def dcir_cal(df):
    # df = pd.read_csv(path, usecols= ['date','time', 'batVolt','batCurrent','batTemp','bmsStatus','chargeCycle','dischargeCycle', 'socPercent', 'cummulativeCharge', 'cummulativeDischarge'],parse_dates=[['date', 'time']])
    st = []
    en = []
    st.append(df.index[0])
    for i in range(1,df.shape[0]):
        if df['bmsStatus'][i] != df['bmsStatus'][i-1]:
            st.append(df.index[i])
            en.append(df.index[i-1])
    en.append(df.index[df.shape[0]-1])
    df['Index'] = df.index
    single = []
    for k in range(len(st)):
        for l in range(len(en)):
            if st[k] == en[l]:
                single.append(st[k])

    len(single)
    diff = []
    for u in range(len(st)):
        diff.append(en[u] - st[u])
    times = pd.DataFrame(st)
    times.rename(columns = {0: 'Index'}, inplace = True)
    times['End'] = en
    times['Difference'] = diff
    zero = times[(times['Difference'] <3)].index
    times.drop(zero, inplace = True)
    times.reset_index(inplace = True)
    # df['Index'] = df.index
    # z_diff = times[times['Difference'] <= 4]
    ir = []
    for t in range(times.shape[0]):
        ir.append((df['batVolt'][times['End'][t]] - df['batVolt'][times['Index'][t]])/(df['batCurrent'][times['End'][t]] - df['batCurrent'][times['Index'][t]]))
    times['DCIR'] = ir
    times
    df = pd.merge(df,times, on = 'Index', how = 'left')
    df
    infi = df[(df['DCIR'] == np.inf) | df['DCIR'] == -np.inf].index
    df=df.drop(infi, axis = 0)
    df= df.dropna()
    df
    steps = []
    for p in range(0,len(st)-1):    
        if en[p] - st[p] >= 4:
            steps.append(st[p])
            steps.append(en[p]-1)
    step = pd.DataFrame(steps)
    step.rename(columns = {0: 'Index'}, inplace = True)
   
    dcir = pd.merge(step, df, on = 'Index', how = 'left')
    
    dcir = dcir[dcir['bmsStatus']=='Charging']
    falsec = dcir[dcir['batCurrent'] == 0.0].index
    dcir = dcir.drop(falsec, axis = 0)
    dcir = dcir.reset_index(drop = True)
    charge = df[(df['bmsStatus'] == 'Charging') ]
    charge = charge.dropna()
    charge = charge.reset_index(drop = True)
    time =[]
    for p in range(charge.shape[0]):
        # time.append(df['U_time'][charge['End'][p]] - df['U_time'][charge['Index'][p]])
        time.append(charge['Difference'][p]*30)

    charge['Time'] = time
    times = charge.filter(['batVolt', 'batCurrent', 'batTemp', 'cummulativeDischarge', 'dischargeCycle', 'Time', 'DCIR'])
    df = pd.merge(df,times, on = 'Index', how = 'left')
    return df

# dcir_cal('D:\\Krutesh\\SoH ML\\Data\\Lime IoT E1.0_869630054319649.csv')