# Discord Bot

This is a Discord bot that performs various functions, such as joining voice channels, playing music from YouTube, and checking for updates on League of Legends.

## 🛠 Installation

To install the necessary dependencies for this project, you must have Python and pip already installed on your system. Then, run the following command at the root of the project:

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration
### Environment Variables
Before running the bot, you need to configure some environment variables that the bot will use for its operation. You must create a .env file at the root of the project with the following variables:

```bash
DISCORD_TOKEN=YourDiscordToken
GUILD_ID=YourServerID
CHANNEL_ID=YourChannelID
```

Replace YourDiscordToken, YourServerID, and YourChannelID with your actual values:

 - DISCORD_TOKEN: The token for your Discord bot.
 - GUILD_ID: The ID of the Discord server where your bot will be active.
 - CHANNEL_ID: The ID of the Discord channel where the bot will send messages and updates.

## 🚀 Execution
To run the bot, use the following command from the command line at the root of your project:

```bash
python main.py
```

This command will start the bot, and it should be ready to respond to commands on Discord.

*Leer este documento en otros idiomas: [Español](README.es.md).*
