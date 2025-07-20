# SteamBot - Automatic Steam News by Email

SteamBot is a Python project that automatically collects news from the games in your Steam library and wishlist, organizes the information, and sends a summary in HTML format by email. It's the ideal solution for anyone who wants to keep up with updates and news about their favorite games without having to manually access Steam.
Steam keeps a news history only for games played in the last six months, which can cause you to miss important information about older titles. SteamBot solves this problem, ensuring that no news goes unnoticed, even for games you haven't accessed in a long time.

## Features

- Automatic retrieval of games from the library and wishlist of multiple users via the Steam API.
- Fetches the latest news for each game.
- Stores news and games in a SQLite database, avoiding duplicates.
- Generates personalized HTML emails for each user, grouping news by library and wishlist.
- Automatic email sending via Gmail.
- Validates game images for display in cards.
- Automatically cleans old news, keeping only the 10 most recent per game.
- Automatically corrects game names that were not fetched correctly.

## Requirements

- Python 3.7 or higher
- Packages: `requests`, `smtplib`, `email`
- SQLite database (created automatically)
- Gmail account for sending emails (app password recommended)
- Steam API key
- Configuration file `utils/secrets.json` with user and email data

## How to run

1. Clone or download the repository.
2. Install Python dependencies:
   ```bash
   pip install requests
   ```
3. Configure the `utils/secrets.json` file with your Steam key, user emails, and Gmail credentials.
4. Run the main script:
   ```bash
   python SteamBot.py
   ```
5. The program will fetch games, collect news, generate the HTML, and send the email to the configured recipients.
6. The generated HTML will also be saved in `utils/card.html`.

> **Notes**
> - Email sending uses Gmail SMTP. Make sure to allow access or use an app password.
> - The database is created automatically and stores only the last 10 news items for each game.
> - The system avoids sending duplicate news and corrects game names with fetch errors.

## File Structure

- `SteamBot.py`: Main script, orchestrates all logic for fetching, storing, and sending.
- `utils/utilsAPI.py`: Functions for accessing Steam APIs.
- `utils/utilsSQL.py`: Functions for manipulating the SQLite database.
- `utils/utilsEmail.py`: Functions for building HTML and sending email.
- `utils/secrets.json`: User and credential configuration (not included in the repository).
- `utils/card.html`: File generated with the email content in HTML.

## Example

When running the script, each registered user will receive an email similar to this:

![HTML Card Example]()

## License

This project is distributed for educational and personal purposes. Check with Steam for commercial use of their APIs.

---

Developed with dedication and Python by [AzumaNoDoragon](https://steamcommunity.com/id/AzumaNoDoragon/), a  developer and gamer.