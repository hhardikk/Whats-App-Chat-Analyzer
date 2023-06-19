import streamlit as st
import Preprocessor
import Helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")
Uploaded_File = st.sidebar.file_uploader("Choose a File")
if Uploaded_File is not None:
    bytes_data = Uploaded_File.getvalue()
    data = bytes_data.decode("utf-8")
    df = Preprocessor.preprocess(data)

    #fetching unique users
    User_List = df['User'].unique().tolist()
    User_List.sort()
    User_List.insert(0, "Overall")
    Selected_user = st.sidebar.selectbox("Show analysis with respect to", User_List)

    if st.sidebar.button("Show Analysis"):
        n_messages, n_words, n_stickers, n_links = Helper.fetch_stats(Selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(n_messages)

        with col2:
            st.header("Total Words")
            st.title(n_words)

        with col3:
            st.header("Total Stickers")
            st.title(n_stickers)

        with col4:
            st.header("Total Links")
            st.title(n_links)

        #monthly timeline
        st.title("Monthly Timeline")
        month_timeline = Helper.monthly_timeline(Selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(month_timeline['time'], month_timeline['Message'], color = 'black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #Daily timeline
        st.title("Daily Timeline")
        daily_timeline = Helper.day_timeline(Selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['Only_date'], daily_timeline['Message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #Activity of group and user
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            user_day_activity = Helper.day_activity(Selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(user_day_activity.index, user_day_activity.values, color = 'red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            user_month_activity = Helper.month_activity(Selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(user_month_activity.index, user_month_activity.values, color = 'red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        #Heatmap
        st.title("Weekly Activity Map")
        Heatmap = Helper.heat_map(Selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(Heatmap)
        st.pyplot(fig)

        if Selected_user == 'Overall':
            st.title('Most Active Users')
            col1, col2 = st.columns(2)

            top5, newdf = Helper.user_status(Selected_user, df)
            fig, ax = plt.subplots()

            with col1:
                ax.bar(top5.index, top5.values, color = 'red')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(newdf)

        st.title("Most Common Words")
        coll1, coll2 = st.columns(2)
        most_common_df = Helper.most_used(Selected_user, df)

        with coll1:
            st.dataframe(most_common_df)

        fig, ax = plt.subplots()
        with coll2:
            ax.bar(most_common_df['Word'], most_common_df['Count'], color = 'red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Emoji's Analysis")
        col1, col2 = st.columns(2)

        with col1:
            emoji_df = Helper.emoji_content(Selected_user, df)
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df['Count'].head(10), labels=emoji_df['Emoji'].head(10), autopct="%0.2f")
            st.pyplot(fig)


