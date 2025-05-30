# BCI Game with Emotiv Epoc X

https://github.com/user-attachments/assets/6e6bce61-94d3-4159-8985-d962da73f52e


<img src="https://github.com/user-attachments/assets/02e1b40a-949b-4237-abf4-84bafcf4818c" alt="IMG_4103" width="400"/>


This project integrates the Emotiv Epoc X headset with a Pygame-based game, allowing users to control the game using Brain-Computer Interface (BCI) technology. The goal is to create games for disabled individuals that can be controlled using the Emotiv headset.

## Features

- **BCI Integration**: Connects to the Emotiv Epoc X headset to receive and process BCI signals.
- **Real-time Game Control**: Uses BCI signals to control the game character.
- **Customizable**: Easily modify the game and BCI interactions.
- **Running Animation:** Utilized sprite sheets to create fluid running animations for the player character.
- **Obstacle Generation:** Added dynamic obstacles that challenge players and require timely jumps to avoid collisions.
- **Scrolling Background:** Implemented a continuous scrolling background to enhance the immersive experience.
- **Game Modes:** Designed both Endless and Timed game modes with separate scripts, providing varied gameplay experiences.
- **Score Tracking:** Included real-time score tracking and a final score display upon game completion.


## Requirements
- Emotiv EPOC X
- Cortex Apps API 
- Python 3.8 or higher
- `dotenv`
- `websocket-client`
- `pygame`

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Daman2461/bci-game.git
    cd bci-game
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    - Create a `.env` file in the project root with your Emotiv client ID and secret:
        ```env
        CLIENT_ID=your_client_id
        CLIENT_SECRET=your_client_secret
        ```

## Usage

1. Start the backend server to connect to the Emotiv headset:
    ```bash
    python backend.py
    ```

2. Start the Pygame application:
    ```bash
    python menu.py
    ```

## Project Structure

- `backend.py`: Handles the connection to the Emotiv Epoc X headset, authorization, session creation, and data streaming.
- `game.py`: Contains the Pygame-based game logic, including player and obstacle handling, background scrolling, and BCI command processing.
CLIENT_ID=Hhdwalj8lzNtOMmk72n60wukErsKffcOPXgWGAlE
CLIENT_SECRET=7YsrsLQGRjH0cwC8bNE3iOlGgWlytxWgyNLv9ysvsDcrmy7pWjEyhn3AwZNb47G895Tim3JDh2lsHmAQSe5lkk7pgQsqS5ABAPF2YiieUlmTbVxlhdNPwJbNCQExcnz3
