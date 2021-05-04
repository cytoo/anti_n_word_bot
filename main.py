from telethon import TelegramClient
from telethon.events import NewMessage
from telethon.sessions import StringSession
import re
import time
import config

N_WORD_TIME = time.time()
client = TelegramClient(StringSession(config.session), config.api_id, config.api_hash)


async def format_time(seconds: int) -> str:
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    string = (
        ((str(days) + " day(s), ") if days else "") +
        ((str(hours) + " hour(s), ") if hours else "") +
        ((str(minutes) + " minute(s), ") if minutes else "") +
        ((str(seconds) + " second(s), ") if seconds else "")
    )
    return string[:-2]


@client.on(NewMessage(outgoing=True))
async def scanner(event: NewMessage.Event):
    global N_WORD_TIME
    text = event.message.text
    if re.findall(r"(n|i|e){1,32}((g{2,32}|q){1,32}|[rgq]{2,32})[aoe3r]{1,32}", text):
        n_time = await format_time(int(time.time() - N_WORD_TIME))
        await event.reply("`ANTI-N-WORD BOT`\n**restting the timer because you said the N-word.**\n you've been "
                          "going on without saying the N-word for %s" % n_time)
        N_WORD_TIME = time.time()


@client.on(NewMessage(outgoing=True, pattern=r"^\.status$"))
async def stats(event: NewMessage.Event):
    n_time = await format_time(int(time.time() - N_WORD_TIME))
    await event.edit(f"`ANTI-N-WORD BOT` **good job! you've been going on without saying the N-word for {n_time}**")

client.start()
print("N_WORD_BOT online")
client.run_until_disconnected()