import os
import sys
import time
import pathlib
import json
import pandas as pd
from faker import Faker
from dotenv import load_dotenv
from utils.utils_producer import verify_services, create_kafka_producer, create_kafka_topic
from utils.utils_logger import logger

# Load Environment Variables
load_dotenv()

# Getter Functions for .env Variables
def get_kafka_topic() -> str:
    topic = os.getenv("BUZZ_TOPIC", "unknown_topic")
    logger.info(f"Kafka topic: {topic}")
    return topic

def get_message_interval() -> int:
    interval = int(os.getenv("BUZZ_INTERVAL_SECONDS", 1))
    logger.info(f"Message interval: {interval} seconds")
    return interval

# Set up Paths
PROJECT_ROOT = pathlib.Path(__file__).parent.parent
DATA_FOLDER = PROJECT_ROOT.joinpath("data")
DATA_FILE = DATA_FOLDER.joinpath("buzz.json")

# Load JSON data into a DataFrame
def load_data_to_dataframe(file_path: pathlib.Path) -> pd.DataFrame:
    try:
        with open(file_path, "r") as file:
            json_data = json.load(file)
        df = pd.DataFrame(json_data)
        logger.info(f"Loaded {len(df)} records into DataFrame.")
        return df
    except Exception as e:
        logger.error(f"Error loading data into DataFrame: {e}")
        return pd.DataFrame()

# Filter messages
def filter_messages(df: pd.DataFrame) -> pd.DataFrame:
    return df[df['message'].str.len() > 20]

# Add real-time statistics
def enrich_message_with_stats(df: pd.DataFrame, message_dict: dict) -> dict:
    avg_length = df['message'].apply(len).mean()
    message_dict['avg_message_length'] = avg_length
    return message_dict

# Generate dynamic messages with Faker
faker = Faker()
def generate_fake_dataframe(num_records: int = 100) -> pd.DataFrame:
    data = [{"message": faker.sentence(), "author": faker.name(), "timestamp": time.time()} for _ in range(num_records)]
    return pd.DataFrame(data)

# Display summary statistics
def display_summary(df: pd.DataFrame):
    logger.info(f"Total messages: {len(df)}")
    logger.info(f"Unique authors: {df['author'].nunique()}")
    logger.info(f"Average message length: {df['message'].apply(len).mean()}")

# Main Function
def main():
    logger.info("START producer.")
    verify_services()
    topic = get_kafka_topic()
    interval_secs = get_message_interval()

    if not DATA_FILE.exists():
        logger.warning(f"Data file not found: {DATA_FILE}. Generating fake data.")
        df = generate_fake_dataframe()
    else:
        df = load_data_to_dataframe(DATA_FILE)

    df = filter_messages(df)

    producer = create_kafka_producer(value_serializer=lambda x: json.dumps(x).encode("utf-8"))
    create_kafka_topic(topic)

    try:
        for _, row in df.iterrows():
            enriched_message = enrich_message_with_stats(df, row.to_dict())
            producer.send(topic, value=enriched_message)
            logger.info(f"Sent message to topic '{topic}': {enriched_message}")
            time.sleep(interval_secs)
    except KeyboardInterrupt:
        logger.warning("Producer interrupted by user.")
    except Exception as e:
        logger.error(f"Error during message production: {e}")
    finally:
        producer.close()
        display_summary(df)
        logger.info("Kafka producer closed.")

if __name__ == "__main__":
    main()
