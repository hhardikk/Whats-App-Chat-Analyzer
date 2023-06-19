from urlextract import URLExtract
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()
def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    num_messages = df.shape[0]
    words = []
    for message in df['Message']:
        words.extend(message.split())

    n_sticker = 0
    n_image = 0

    for message in df['Message']:
        message = message.replace('\u200e', '')
        message = message.replace('\n', '')
        if message == 'sticker omitted':
            n_sticker += 1
        elif message == 'image omitted':
            n_image += 1

    links = []
    for message in df['Message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), n_sticker, len(links)

def user_status(selected_user, df):
    for message in df['Message']:
        message = message.replace('\u200e', '')

    x = df['User'].value_counts().head()
    dataset = round((df['User'].value_counts()/df.shape[0])*100, 2).reset_index().rename(columns={'User': 'Name', 'count': 'percent'})
    return x, dataset

def most_used(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    f = open("stop_hinglish.txt", 'r')
    stop_words = f.read()
    temp = df[df['Message'] != '\u200esticker omitted\n']
    temp = temp[temp['Message'] != '\u200eimage omitted\n']

    words = []
    for message in df['Message']:
        message = message.replace('\u200e', '')
        for word in message.lower().split():
            if word[0] == '@':
                break
            if word not in stop_words:
                words.append(word)

    most_used_df = pd.DataFrame(Counter(words).most_common(20))
    most_used_df = most_used_df.rename(columns={0: 'Word', 1: 'Count'})
    return most_used_df

def emoji_content(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    emojis = []
    for message in df['Message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    most_emoji_used_df = pd.DataFrame(Counter(emojis).most_common(20))
    most_emoji_used_df = most_emoji_used_df.rename(columns={0: 'Emoji', 1: 'Count'})
    return most_emoji_used_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    timeline = df.groupby(['Year', 'Month_Num', 'Month']).count()['Message'].reset_index()

    time = []

    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + "-" + str(timeline['Year'][i]))

    timeline['time'] = time
    return timeline

def day_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    daily_timeline = df.groupby(['Only_date']).count()['Message'].reset_index()

    return daily_timeline

def day_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    df['day_name'] = df['Date'].dt.day_name()
    return df['day_name'].value_counts()

def month_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    return df['Month'].value_counts()

def heat_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    df['day_name'] = df['Date'].dt.day_name()

    activity_heatmap = df.pivot_table(index = 'day_name', columns = 'period', values = 'Message', aggfunc= 'count').fillna(0)
    return activity_heatmap

