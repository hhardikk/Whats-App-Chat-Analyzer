import re
import pandas as pd

def preprocess(data):
    pattern = '\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}:\d{1,2}\]\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    for i in range((len(dates))):
        dates[i] = dates[i].replace(']', '')
        dates[i] = dates[i].replace('[', '')
        dates[i] = dates[i].replace(' ', '')

    df = pd.DataFrame({'User_messages': messages, 'Message_date': dates})
    df['Message_date'] = pd.to_datetime(df['Message_date'], format='%d/%m/%y,%H:%M:%S')
    df.rename(columns={'Message_date': 'Date'}, inplace=True)

    Messages = []
    Users = []
    for msg in df['User_messages']:
        text = re.split('([\w\W]+?):\s', msg)
        Users.append(text[1])
        Messages.append(text[2])

    df['User'] = Users
    df['Message'] = Messages
    df.drop(columns=['User_messages'], inplace=True)

    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month_name()
    df['Day'] = df['Date'].dt.day
    df['Hour'] = df['Date'].dt.hour
    df['Minute'] = df['Date'].dt.minute
    df['Month_Num'] = df['Date'].dt.month
    df['Only_date'] = df['Date'].dt.date

    period = []
    for hour in df['Hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str(hour) + "-" + str('01'))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df