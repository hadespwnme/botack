# botack
Botack is a powerfull tool for get message from another Telegram Bot.

<p align="center">
  <img src="img/saitama.png" alt="Botack">
</p>

## ⚠ Disclaimer
This tool is strictly for educational and ethical purposes.
The author is not responsible for any misuse or damage caused by this tool.

## 📌 Requirements
Before using Botack, ensure you have the following installed:  
- Python 3.7+  
- Required Python libraries (install using `requirements.txt`)
- An account on my.telegram.org/apps to get your Telegram API credentials (api_id, api_hash, phone_number).

## 📥 Installation & Usage
### 1️⃣ Install Dependencies
Clone the repository and install dependencies:  
```bash
git clone https://github.com/hadespwnme/botack.git
cd botack
pip install -r requirements.txt
```
### 2️⃣ Telegram Api Credential 
- Visit [this](my.telegram.org/apps) and log in with your phone number.
- Create a new application
- Copy this following to .env:
  1. **api_id**
  2. **api_hash**
  3. **phone_number**

### 3️⃣ Usage 
This tool have two option.
1. **forward**: Forward message from another bot your Telegram.
2. **attack**: Send messages to target bot as you wish.

Usage: ```python3 botack.py [option]```

