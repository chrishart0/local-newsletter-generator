import json
from local_newsletter_generator.helpers.logger_helper import get_logger
from local_newsletter_generator.event_extractor.event_extractor import extract_events
from local_newsletter_generator.event_extractor.webpage_loader import load_webpage
from local_newsletter_generator.llm.llm_setup import llm

# Setup settings
from local_newsletter_generator.settings import Settings

settings = Settings()

# Get the configured logger
logger = get_logger()

# List of URLs to process
# TODO: Break this out into a file per city which knows how to find the latest news
chattanooga_urls = [
    "https://noogatoday.6amcity.com/newsletter/00000192-bf91-d0ba-a19e-ff99cd0f0022",  # TODO: This must be updated daily
    "https://www.chattanoogan.com/Leisuretime/Around-Town.aspx",
    "https://www.visitchattanooga.com/blog/post/weekend-top-5/",
    # "https://www.eventbrite.com/d/tn--chattanooga/all-events/", The web scraper isn't getting dates for events from this page
    "https://www.cha.guide/events",
    # Add more URLs as needed
]

san_antonio_urls = [
    "https://www.thesanantonioriverwalk.com/events/",
    "https://www.visitsanantonio.com/events/",
    # Add more URLs as needed
]


def generate_events_data():
    # Initialize a list to store all events
    all_events = []

    for url in san_antonio_urls:
        loaded_webpage = load_webpage(url)
        events_list = extract_events(loaded_webpage, url)
        all_events.extend(events_list.events)  # Add individual events to the list

    # Convert events to a serializable format using Pydantic
    serializable_events = [event.dict() for event in all_events]

    # Store events in a JSON file
    with open("events.json", "w") as f:
        json.dump(serializable_events, f, indent=4, default=str)

    logger.info(f"Stored {len(all_events)} events in events.json")

    # Print length of all_events
    logger.info(f"Extracted {len(all_events)} events")

    # Print each event
    for event in all_events:
        logger.info("--------------------------------")
        for field_name, field_value in event.dict().items():
            logger.info(f"{field_name.capitalize()}: {field_value}")


def generate_events_markdown():
    logger.info("Generating events markdown")
    # Load events from the JSON file
    with open("events.json", "r") as f:
        events_data = json.load(f)

    # Sort events by date, handling None values by using a default date far in the past
    events_data.sort(key=lambda x: x.get("date") or "0000-01-01")

    # Produce a markdown file with the events and all the details
    with open("events.md", "w") as f:
        f.write("# San Antonio Events\n\n")
        for event in events_data:
            # Use the event title as a larger header
            f.write(f"## {event.get('title', 'Untitled Event')}\n\n")
            for field_name, field_value in event.items():
                if field_name != "title" and field_value not in [
                    None,
                    "None",
                ]:  # Skip the title and None values
                    f.write(f"**{field_name.capitalize()}:** {field_value}\n\n")
            f.write("\n\n")


def generate_newsletter_markdown():
    logger.info("Generating newsletter markdown")

    # Load events from the JSON file
    with open("events.json", "r") as f:
        events_data = json.load(f)

    # Sort events by date, handling None values by using a default date far in the past
    events_data.sort(key=lambda x: x.get("date") or "0000-01-01")

    # Format event details into one string by reading from events.md
    with open("events.md", "r") as f:
        events_string = f.read()

    # Assign the formatted string to the message
    messages = [
        (
            "system",
            """You are a newsletter writer.
Generate a newsletter for the following event details I provide.
The newsletter should be written like a newsletter written by a local.
If you don't know a date but are confident in an approximate date, use that but make it clear it's an approximation, use some syntax to tell the editor to go fill the real date in.""",
        ),
        ("human", events_string),
    ]

    # Pass the message to the LLM
    newsletter_author_response = llm.invoke(messages)

    # Write the newsletter content to a markdown file
    with open("newsletter.md", "w") as f:
        f.write(newsletter_author_response.content)


def translate_newsletter_to_spanish():
    logger.info("Translating newsletter to Spanish")

    # Read the newsletter content from the markdown file
    with open("newsletter.md", "r") as f:
        newsletter_content = f.read()

    messages = [
        (
            "system",
            """You are a newsletter writer born and living in San Antonio, TX.
            Translate the following newsletter content to Spanish.""",
        ),
        ("human", newsletter_content),
    ]

    # Pass the message to the LLM
    translated_newsletter_content = llm.invoke(messages)

    # Write the translated newsletter content to a markdown file
    with open("translated_newsletter.md", "w") as f:
        f.write(translated_newsletter_content.content)


if __name__ == "__main__":
    generate_events_data()
    generate_events_markdown()
    generate_newsletter_markdown()
    translate_newsletter_to_spanish()
