from langchain.agents import initialize_agent, Tool, AgentType

from tools import google_search_2, get_website_content

def lookup(requisito: str) -> str:

    from langchain.chat_models import ChatOpenAI
    from langchain import PromptTemplate
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")

    from datetime import datetime

    # Get the current date and time
    current_datetime = datetime.now()

    # Extract the date part (today's date) from the datetime object
    today_date = current_datetime.date()

    tools_for_agent =[
        Tool(
            name="Crawl Google 4 edital page", 
            func=google_search_2,
            description="usefull for when you need to search on the web",
        ),
        Tool(
            name="Checkout a Website", 
            func=get_website_content,
            description="usefull for when you need to see whats in a website",
        )
        
    ]
    
    agent = initialize_agent(
        tools=tools_for_agent, 
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
        verbose=True
        )

    summary_template = """
    Voce é um Agente autonomo que presta suporte para o time do Instituto Eldorado, seu papel é encontrar na internet oportunidades
    de negocio para o Instituto Eldorado.
    Para isso, dado o tipo de edital {requisito} Eu quero que você encontre e me traga uma lista de editais com grandes chances de sucesso para o Instituto Eldorado    
    Hoje é dia {today}
    """

    prompt_template = PromptTemplate(
        input_variables=["requisito", "today"], 
        template=summary_template,
    )

    linkedin_profile_url = agent.run(
        prompt_template.format_prompt(requisito=requisito, today=today_date))

    return linkedin_profile_url