import autogen
import os

openai_key = os.environ['OPENAI_KEY']
openai_endpoint = os.environ['OPENAI_ENDPOINT']

assert openai_key
assert openai_endpoint

# config_list = [
#     {
#         'model': 'gpt-4-plugins',
#         'api_key': openai_key
#     }
# ]

# https://microsoft.github.io/autogen/blog/2023/12/01/AutoGenAssistant/#configuring-an-llm-provider
config_list = [
    {
        "model": "gpt-4-plugins",
        "api_key": openai_key,
        "base_url": openai_endpoint,
        "api_type": "azure",
        "api_version": "2023-06-01-preview",
    }
]
llm_config = {
    # "request_timeout": 600,
    # agent uses cache if there is the same prompt so that it saves money
    "seed": 42,
    "config_list": config_list,
    "temperature": 0,
    "top_p": 0
}

assistant = autogen.AssistantAgent(
    name="Psychologist",
    llm_config=llm_config,
    system_message="Psychologist specialised about people relationship"
)

mathematician_assistant = autogen.AssistantAgent(
    name="Mathematician",
    llm_config=llm_config,
    system_message="Mathematician"
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    #  not to high to avoid infinite loop
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get(
        "content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "web"},
    llm_config=llm_config,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
    Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)

task1 = """
Give me a summary of this article: https://epiotrkow.pl/news/50-lat-malzenstwa-minelo-jak-jeden-dzien--nbsp;,53297
"""

example_task_2 = """
Generate numbers from 0 to 10 and write them on disk
"""

user_proxy.initiate_chat(
    mathematician_assistant,
    message=example_task_2
)
