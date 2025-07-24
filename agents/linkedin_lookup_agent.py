import os
from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)
from langchain import hub
from tools.tools import get_profile_url_tavily

def lookup(name: str) -> str:
    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-4o-mini",
        openai_api_key=os.environ["OPENAI_API_KEY"],
    )

    # 프롬프트 템플릿 정의
    template = """given the full name {name_of_person} I want you to get it me a link to their Linkedin profile page.
Your answer should contain only a URL"""

    prompt_template = PromptTemplate(
        template=template,
        input_variables=["name_of_person"]
    )

    # 사용할 도구 등록
    tools_for_agent = [
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func=get_profile_url_tavily,
            description="useful for when you need get the Linkedin Page URL"
        )
    ]

    # ReAct 에이전트 프롬프트 불러오기 (LangChain hub 사용)
    react_prompt = hub.pull("hwchase17/react")

    # 에이전트 생성
    agent = create_react_agent(
        llm=llm,
        tools=tools_for_agent,
        prompt=react_prompt
    )

    # 실행기 구성
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools_for_agent,
        verbose=True,
        handle_parsing_errors=True
    )

    # 실행 (프롬프트 템플릿 채운 후 전달)
    result = agent_executor.invoke(
        input={"input": prompt_template.format(name_of_person=name)}
    )

    return result["output"]


if __name__ == "__main__":
    linkedin_url = lookup(name="Hyundoo(대한민국) Jeong")
    print(linkedin_url)
