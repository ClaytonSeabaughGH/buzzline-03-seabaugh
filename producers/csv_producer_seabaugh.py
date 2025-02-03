#####################################
# Import Modules
#####################################

# Import packages from Python Standard Library
import os
import sys
import time  # control message intervals
import pathlib  # work with file paths
import json  # work with JSON data
from datetime import datetime  # work with timestamps

# Import external packages
import polars as pl  # Fast DataFrame library
from dotenv import load_dotenv

# Import functions from local modules
from utils.utils_producer import (
    verify_services,
    create_kafka_producer,
    create_kafka_topic,
)
from utils.utils_logger import logger

#####################################
# Load Environment Variables
#####################################

load_dotenv()

#####################################
# Getter Functions for .env Variables
#####################################

def get_kafka_topic() -> str:
    topic = os.getenv("SMOKER_TOPIC", "unknown_topic")
    logger.info(f"Kafka topic: {topic}")
    return topic

def get_message_interval() -> int:
    interval = int(os.getenv("SMOKER_INTERVAL_SECONDS", 1))
    logger.info(f"Message interval: {interval} seconds")
    return interval

#####################################
# Set up Paths
#####################################

PROJECT_ROOT = pathlib.Path(__file__).parent.parent
DATA_FOLDER = PROJECT_ROOT.joinpath("data")
DATA_FILE = DATA_FOLDER.joinpath("smoker_temps.csv")

logger.info(f"Data file: {DATA_FILE}")

#####################################
# Message Generator with Polars
#####################################

def generate_messages_with_stats(file_path: pathlib.Path):
    try:
        logger.info(f"Reading data from file: {file_path}")
        df = pl.read_csv(file_path)

        if "temperature" not in df.columns:
            logger.error("Missing 'temperature' column in CSV.")
            sys.exit(1)

        for row in df.iter_rows(named=True):
            current_timestamp = datetime.utcnow().isoformat()
            temperature = float(row["temperature"])

            # Real-time statistics
            temp_series = df.select("temperature").to_series()
            stats = {
                "mean_temperature": temp_series.mean(),
                "max_temperature": temp_series.max(),
                "min_temperature": temp_series.min(),
            }

            message = {
                "timestamp": current_timestamp,
                "temperature": temperature,
                "stats": stats,
            }
            logger.debug(f"Generated message: {message}")
            yield message

    except FileNotFoundError:
        logger.error(f"File not found: {file_path}. Exiting.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error in message generation: {e}")
        sys.exit(3)

#####################################
# Main Function
#####################################

def main():
    logger.info("START producer.")
    verify_services()

    topic = get_kafka_topic()
    interval_secs = get_message_interval()

    if not DATA_FILE.exists():
        logger.error(f"Data file not found: {DATA_FILE}. Exiting.")
        sys.exit(1)

    producer = create_kafka_producer(value_serializer=lambda x: json.dumps(x).encode("utf-8"))

    try:
        create_kafka_topic(topic)
        logger.info(f"Kafka topic '{topic}' is ready.")
    except Exception as e:
        logger.error(f"Failed to create or verify topic '{topic}': {e}")
        sys.exit(1)

    try:
        for message in generate_messages_with_stats(DATA_FILE):
            producer.send(topic, value=message)
            logger.info(f"Sent message to topic '{topic}': {message}")
            time.sleep(interval_secs)
    except KeyboardInterrupt:
        logger.warning("Producer interrupted by user.")
    except Exception as e:
        logger.error(f"Error during message production: {e}")
    finally:
        producer.close()
        logger.info("Kafka producer closed.")

    logger.info("END producer.")

#####################################
# Conditional Execution
#####################################

if __name__ == "__main__":
    main()
