from typing import Tuple

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from output_parsers import summary_parser, Summary
from third_party.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent

def ice_break(name: str) -> Tuple[Summary, str]:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)

    summary_template = """
    given the Linkedin {information} about a person I want you to create:
    1. a short summary
    2. two interesting facts about them

    \n{formal_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={"formal_instructions": summary_parser.get_format_instructions()}
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")

    # LangChain Expression Language 구성
    chain = summary_prompt_template | llm | summary_parser
    res: Summary = chain.invoke(input={"information": linkedin_data})

    return res, linkedin_data.get("photoUrl")


if __name__ == "__main__":
    load_dotenv()
    print("Ice Breaker Start!")
    result, photo_url = ice_break(name="Hyundoo(대한민국) Jeong")
