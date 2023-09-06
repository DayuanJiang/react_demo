class UserInfo:
    def __init__(self, user_id, billing_amount, data_usage, data_quota):
        self.user_id = user_id
        self.billing_amount = billing_amount
        self.data_usage = data_usage
        self.data_quota = data_quota

    def data_quota_charge(self, amount):
        self.data_quota += amount

    def __repr__(self) -> str:
        return f"UserInfo(user_id={self.user_id}, billing_amount={self.billing_amount}, data_usage={self.data_usage}, data_quota={self.data_quota})"


import random


def generate_user_info_randomly():
    # data_quota = random.choice([1, 3, 7, 10, 20])
    # return UserInfo(
    #     user_id=random.randint(1, 100),
    #     billing_amount=random.randint(10, 10000),
    #     data_usage=data_quota + 10,
    #     data_quota=data_quota,
    # )
    return UserInfo(
        user_id=10,
        billing_amount=1000,
        data_usage=7,
        data_quota=3,
    )


from langchain.agents import tool
from dotenv import load_dotenv

load_dotenv()


@tool
def get_user_data_usage(user_id) -> int:
    """Returns the amount of data used by the user. if user_id is not in user_dict, return -1"""
    try:
        return user_dict[user_id].data_usage
    except KeyError:
        return -1


@tool
def get_user_data_quota(user_id) -> int:
    """Returns the data quota of the user. if user_id is not in user_dict, return -1"""
    try:
        return user_dict[user_id].data_quota
    except KeyError:
        return -1


@tool
def charge_user_data_quota(user_id: int, amount: int) -> int:
    """Charges the data quota of the user. if user_id is not in user_dict, return -1"""
    try:
        user_dict[user_id].data_quota_charge(amount)
        return 1
    except KeyError:
        return -1


tools = [get_user_data_usage, get_user_data_quota, charge_user_data_quota]

from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent
from langchain.prompts import MessagesPlaceholder
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor
from langchain.memory import ConversationBufferMemory


llm = ChatOpenAI(temperature=0)
sys_content = """
あなたは通信会社SoftDunkのAIアシスタントです。ユーザから質問に対して回答することが得意です。
常識：
1. 話を開始する前にユーザーIDを聞いてください。
2. 通信量がクォータを超えるとスピードが遅くなる。
"""
system_message = SystemMessage(content=sys_content)
MEMORY_KEY = "チャット履歴"
prompt = OpenAIFunctionsAgent.create_prompt(
    system_message=system_message,
    extra_prompt_messages=[MessagesPlaceholder(variable_name=MEMORY_KEY)],
)

user_dict = {}


def creat_agent():
    user = generate_user_info_randomly()
    user_dict[user.user_id] = user
    memory = ConversationBufferMemory(memory_key=MEMORY_KEY, return_messages=True)
    agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(
        agent=agent, tools=tools, memory=memory, verbose=True
    )
    return agent_executor
