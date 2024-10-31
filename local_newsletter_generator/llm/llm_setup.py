from local_newsletter_generator.settings import Settings
from local_newsletter_generator.helpers.logger_helper import get_logger
from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI

# Get the configured logger
logger = get_logger()

settings = Settings()

# Conditionally set the LLM based on the environment variables
if settings.AZURE_OPENAI_API_KEY:
    logger.info("Using Azure OpenAI")
    llm = AzureChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=settings.AZURE_OPENAI_API_KEY,
        azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        deployment_name=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
        openai_api_version="2024-02-01",
    )
else:
    logger.info("Using OpenAI")
    llm = ChatOpenAI(
        model="gpt-4o-mini", temperature=0, max_tokens=None, timeout=None, max_retries=2
    )
