# First
import openai
import streamlit as st
import os
from src import creat_agent, user_dict

st.title("💬 SoftDunk AIサービスセンター")
user_info_format = """
仮ユーザー
ユーザーID：{user_id}  
請求予定額：{billing_amount}  
データ使用量：{data_usage}  
データクオリティ：{data_quota}  
"""
user_info = st.code("")


if "agent" not in st.session_state:
    st.session_state["agent"] = creat_agent()
    st.session_state["messages"] = [
        {"role": "assistant", "content": "こんにちは、SoftDunk AIサービスセンターです。"},
    ]
    st.session_state["user"] = user_dict[next(iter(user_dict))]
    user_info.code(user_info_format.format(**st.session_state["user"].__dict__))

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
    user_info.code(user_info_format.format(**st.session_state["user"].__dict__))

if prompt := st.chat_input():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = st.session_state.agent.run(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
    user_info.code(user_info_format.format(**st.session_state["user"].__dict__))
