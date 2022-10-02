import heroku3
import streamlit as st
st.title("Server Maintainance")
st.image("giphy.gif")
password=st.text_input("Enter Password:")
if password=="inam@hnh":
    
    if st.button("Restart Servers"):
     with st.spinner('Initating Server Restart....'):
        st.write("Please wait 5 mins")
        st.write("Restarting Image Processing Server..............")
        heroku_conn = heroku3.from_key('4367aebd-de75-480c-be55-9c9b45491092')
        app=heroku_conn.app('abo5imageapi')
        app.restart()
        st.write("Restarting Describtion Generation Server..............")
        heroku_conn = heroku3.from_key('4367aebd-de75-480c-be55-9c9b45491092')
        app=heroku_conn.app('abo5describtionapi')
        app.restart()
        st.write("Restarting Database Server..............")
        heroku_conn = heroku3.from_key('4367aebd-de75-480c-be55-9c9b45491092')
        app=heroku_conn.app('abo5productuploaddatabase')
        app.restart()
        st.write("Please Give 3 mins for the system to boot up")
