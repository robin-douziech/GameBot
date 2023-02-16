from dotenv import load_dotenv
import os

from control_commands import *

load_dotenv()

bot.run(os.getenv("TOKEN"))