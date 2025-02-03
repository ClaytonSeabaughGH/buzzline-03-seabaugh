# buzzline-03-seabaugh

## :rocket: Project Overview

**Buzzline-03-Seabaugh** is a project focused on processing **streaming data** using **Kafka**, which can handle different data formats such as **JSON** and **CSV**. The goal of this project is to simulate a real-time streaming environment with producers that generate data (in JSON and CSV formats) and consumers that process that data as it arrives.

In this project:
- **Producers** send data to Kafka topics in either **JSON** or **CSV** format.
- **Consumers** receive that data in real-time, process it, and trigger actions such as alerts based on certain conditions.

For example, in the **CSV example**, we simulate a **smart smoker thermometer** that sends temperature readings to the consumer, and the consumer sends alerts when the temperature is stuck (a **stall**) for too long. This project leverages **Zookeeper** and **Kafka** to manage the streaming data and interactions between producers and consumers.

---


---

## :bulb: Task 1. Manage Local Project Virtual Environment

1. **Create your `.venv`**
2. **Activate `.venv`**
3. **Install the required dependencies** using `requirements.txt`

---

## :rocket: Task 2. Start Zookeeper and Kafka (2 Terminals)

To begin, start **Zookeeper** and **Kafka** in separate terminals as instructed in your setup.

---

## :pencil: Task 3. Start a JSON Producer

In VS Code, open a terminal. Use the commands below to activate `.venv`, and start the **JSON producer**.

### Windows:

```shell
.venv\Scripts\activate
py -m producers.json_producer_seabaugh


Mac/Linux:
```zsh
source .venv/bin/activate
python3 -m producers.json_producer_seabaugh
```

## :camera: Task 4. Start a JSON Consumer
Consumers process streaming data in real time.

In VS Code, open a NEW terminal in your root project folder. Use the commands below to activate .venv and start the JSON consumer.

Windows:
```shell
.venv\Scripts\activate
py -m consumers.json_consumer_seabaugh
```

Mac/Linux:
```zsh
source .venv/bin/activate
python3 -m consumers.json_consumer_seabaugh
```

## :file_folder: Task 5. Start a CSV Producer

Follow a similar process to start the csv producer. 
You will need to:
1. Open a new terminal. 
2. Activate your .venv.
3. Know the command that works on your machine to execute python (e.g. py or python3).
4. Know how to use the -m (module flag to run your file as a module).
5. Know the full name of the module you want to run. Hint: Look in the producers folder.


## :file_folder: Task 6. Start a CSV Consumer

Follow a similar process to start the csv consumer. 
You will need to:
1. Open a new terminal. 
2. Activate your .venv.
3. Know the command that works on your machine to execute python (e.g. py or python3).
4. Know how to use the -m (module flag to run your file as a module).
5. Know the full name of the module you want to run. Hint: Look in the consumers folder.


## :hamburger: About the Smart Smoker (CSV Example)

A food stall occurs when the internal temperature of food plateaus or 
stops rising during slow cooking, typically between 150°F and 170°F. 
This happens due to evaporative cooling as moisture escapes from the 
surface of the food. The plateau can last for hours, requiring 
adjustments like wrapping the food or raising the cooking temperature to 
overcome it. Cooking should continue until the food reaches the 
appropriate internal temperature for safe and proper doneness.

The producer simulates a smart food thermometer, sending a temperature 
reading every 15 seconds. The consumer monitors these messages and 
maintains a time window of the last 5 readings. 
If the temperature varies by less than 2 degrees, the consumer alerts 
the BBQ master that a stall has been detected. This time window helps 
capture recent trends while filtering out minor fluctuations.

## :memo: Later Work Sessions
When resuming work on this project:
1. Open the folder in VS Code. 
2. Start the Zookeeper service.
3. Start the Kafka service.
4. Activate your local project virtual environment (.env).

## :floppy_disk: Save Space
To save disk space, you can delete the .venv folder when not actively working on this project.
You can always recreate it, activate it, and reinstall the necessary packages later. 
Managing Python virtual environments is a valuable skill. 

## :file_cabinet: License
This project is licensed under the MIT License as an example project. 
You are encouraged to fork, copy, explore, and modify the code as you like. 
See the [LICENSE](LICENSE.txt) file for more.
