import json
from local_newsletter_generator.helpers.logger_helper import get_logger
from local_newsletter_generator.event_extractor.event_extractor import extract_events
from local_newsletter_generator.event_extractor.webpage_loader import load_webpage

# Setup settings
from local_newsletter_generator.settings import Settings

settings = Settings()

# Get the configured logger
logger = get_logger()

logger.info(f"Using OpenAI API Key: {settings.OPENAI_API_KEY}")

# List of URLs to process
# TODO: Break this out into a file per city which knows how to find the latest news
urls = [
    "https://noogatoday.6amcity.com/newsletter/00000192-bf91-d0ba-a19e-ff99cd0f0022",
    "https://noogatoday.6amcity.com/newsletter/00000192-bf91-df19-a1ba-bfbba0930000",
    # Add more URLs as needed
]

# Initialize a list to store all events
all_events = []

for url in urls:
    loaded_webpage = load_webpage(url)
    events_list = extract_events(loaded_webpage)
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
