from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from local_newsletter_generator.helpers.logger_helper import get_logger
from langchain_core.prompts import ChatPromptTemplate

from local_newsletter_generator.settings import Settings
from local_newsletter_generator.llm.llm_setup import llm


settings = Settings()

# Get the configured logger
logger = get_logger()


class Event(BaseModel):
    """Information about an event."""

    # ^ Doc-string for the entity Event.
    # This doc-string is sent to the LLM as the description of the schema Event,
    # and it can help to improve extraction results.

    # Note that:
    # 1. Each field is an `optional` -- this allows the model to decline to extract it!
    # 2. Each field has a `description` -- this description is used by the LLM.
    # Having a good description can help improve extraction results.

    title: str = Field(description="The title of the event")
    event_type: Optional[str] = Field(
        description="The type of event, e.g. 'concert', 'workshop', 'meeting', etc."
    )
    event_series: Optional[str] = Field(
        description="The name of the event series if this event is part of a series"
    )
    date: Optional[datetime] = None
    time: Optional[str] = None
    location: Optional[str] = Field(
        description="""The location of the event, consider all your information about the event
and the city to provide an accurate location of where the event is."""
    )
    price: Optional[str] = None
    description: Optional[str] = None
    major_event: Optional[bool] = Field(
        description="Whether this event is a major event in the city"
    )
    organization: Optional[str] = Field(
        description="The organization hosting this specific event"
    )
    organizer: Optional[str] = None
    rsvp: Optional[str] = None
    source_links: Optional[List[str]] = Field(
        description="Links to the source of the event information"
    )
    image_links: Optional[List[str]] = Field(
        description="Links to images related to the event"
    )
    extra_info: Optional[str] = Field(
        description="Any additional information about the event"
    )


class EventsList(BaseModel):
    events: List[Event]


# Define a custom prompt to provide instructions and any additional context.
# 1) You can add examples into the prompt template to improve extraction quality
# 2) Introduce additional parameters to take context into account (e.g., include metadata
#    about the document from which the text was extracted.)
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert extraction algorithm. "
            "Only extract relevant information from the text. "
            "If you do not know the value of an attribute asked to extract, "
            "return null for the attribute's value.",
        ),
        # Please see the how-to about improving performance with
        # reference examples.
        # MessagesPlaceholder('examples'),
        ("human", "{text}"),
    ]
)

runnable = prompt | llm.with_structured_output(schema=EventsList)


def extract_events(
    text: str,
    original_source_url: str,
) -> EventsList:
    # Log in green text that the events are being extracted
    logger.info("\033[92mExtracting events from text\033[0m")
    extracted_data = runnable.invoke({"text": text})
    # Log in green text that the events were extracted
    logger.info(f"\033[92mExtracted {len(extracted_data.events)} events\033[0m")

    # Add the original source URL to each event
    for event in extracted_data.events:
        event.source_links = [original_source_url]

        # Convert date string to datetime object
        if event.date and isinstance(event.date, str):
            if len(event.date) == 7:  # If the date string is in 'YYYY-MM' format
                event.date += "-01"  # Add the day
            event.date = datetime.strptime(event.date, "%Y-%m-%d")

    return extracted_data
