# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01


import re
import os
from os import environ
from Script import script

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default
      
# Bot Information
BOT_TOKEN = "Y7832119690:AAE0h1w-Q6y1jRaASQJtawyMavKh5H-a_Lw"
bot = telebot.TeleBot(BOT_TOKEN)

# File storage folder
FILE_STORE_PATH = "files"
os.makedirs(FILE_STORE_PATH, exist_ok=True)

# JSON to track metadata
METADATA_FILE = "metadata.json"
if not os.path.exists(METADATA_FILE):
    with open(METADATA_FILE, 'w') as f:
        json.dump({}, f)


def load_metadata():
    with open(METADATA_FILE, 'r') as f:
        return json.load(f)


def save_metadata(metadata):
    with open(METADATA_FILE, 'w') as f:
        json.dump(metadata, f, indent=4)


@bot.message_handler(content_types=['document', 'photo'])
def handle_files(message):
    metadata = load_metadata()
    
    # Handle document
    if message.document:
        file_info = bot.get_file(message.document.file_id)
        file_name = message.document.file_name
        file_path = bot.download_file(file_info.file_path)
        
        # Save the file
        with open(os.path.join(FILE_STORE_PATH, file_name), 'wb') as f:
            f.write(file_path)
        
        # Save metadata
        metadata[file_name] = {
            "file_id": message.document.file_id,
            "file_name": file_name,
            "file_size": message.document.file_size,
            "uploader": message.from_user.username or message.from_user.id,
        }
    
    # Handle photos (if needed)
    # Add similar handling logic for photos if required

    save_metadata(metadata)
    bot.reply_to(message, f"File '{file_name}' stored successfully!")


@bot.message_handler(commands=['getfile'])
def send_file(message):
    metadata = load_metadata()
    file_name = message.text.split(" ", 1)[1]
    
    if file_name in metadata:
        file_path = os.path.join(FILE_STORE_PATH, file_name)
        bot.send_document(message.chat.id, open(file_path, 'rb'))
    else:
        bot.reply_to(message, "File not found!")


bot.polling()
    
