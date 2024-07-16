# Math Quiz Telegram Bot

> Project is a Telegram bot for conducting math quizzes with various difficulty levels. The bot is built using the `telebot` library, saves data using the `pickle` library and work with images using the `pillow`.

## Installation

1. Clone the repository or download the project files.
2. Install the required dependencies:

   ```bash
   pip install pyTelegramBotAPI
   pip install pillow
   ```
3. Create a database.py file and add your API token:
   ```bash
   # database.py
   API_TOKEN = 'YOUR_API_TOKEN'
   ```
## Usage
1. Run the bot
   ```bash
    python bot.py
   ```
2. Start a conversation with the bot on Telegram by searching for the bot's username and sending the /start command.
## Features
  - The bot provides math equations for users to solve.
  - Users can take a test with different levels of difficulty.
  - The bot saves users' progress and levels using the pickle library.
## File Structure
  - `bot.py`: The main bot script.
  - `database.py`: Contains the API token.
  - `pract.py`: Contains the function create_equation to generate math equations.
  - `data.pkl`: File used to save user progress and other data.
## Example
When the bot is started, it sends a welcome message and prompts the user to take a test:
```bash
Hello [username], I am created to help you learn math. I will give you examples and equations, and you need to just write the answers to these examples or equations. Let's immediately proceed to the test. You have 10 equation, the more levels you pass, the more you can go through. Good luck!
```
## Contributing
Feel free to submit issues, fork the repository, and send pull requests. For major changes, please open an issue first to discuss what you would like to change.
