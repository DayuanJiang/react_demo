# First
import openai
import streamlit as st
import os
from src import creat_agent, user_dict

user_info_format = """
仮ユーザー
ユーザーID：{user_id}  
請求予定額：{billing_amount}  
データ使用量：{data_usage}  
データクォータ：{data_quota}  
"""


st.title("💬 SoftDunk AIサービスセンター")


if "agent" not in st.session_state:
    st.session_state["agent"] = creat_agent()
    st.session_state["messages"] = [
        {"role": "assistant", "content": "こんにちは、SoftDunk AIサービスセンターです。"},
    ]
    st.session_state["user"] = user_dict[next(iter(user_dict))]


with st.sidebar:
    st.markdown(
        """
    **AIアシスタントを持つツール**：
    1. データの使用量を調べるAPI
    2. データのクォータを調べるAPI
    3. データのクォータを上げるAPI
    
    **会話の流れ**：  
    データ使用量を知りたいです。 
    IDは10です。 
    最近通信スピードがめちゃくちゃ遅くなったんですが、どうすればよろしいでしょうか。    
    データクォータを10チャージしたい。  
    """
    )
    user_info = st.code("")
    user_info.code(user_info_format.format(**st.session_state["user"].__dict__))
    handler = st.session_state["agent"].callbacks[0]
    log_block = st.markdown("**システムログ**\n" + "\n\n".join(handler.log))


for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
    user_info.code(user_info_format.format(**st.session_state["user"].__dict__))

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = st.session_state.agent.run(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
    user_info.code(user_info_format.format(**st.session_state["user"].__dict__))
    log_block.markdown("**システムログ**  \n" + "\n\n".join(handler.log))
