import random
import json
import requests
import discord
from discord.ext import commands, tasks
from pd import pd


abc = 'abcdefghijklmnopqrstuvwxyz'
eabc0 = '🅰 🅱 x x x x x x x x x x x x 🅾 x x x x x x x x x x x'.replace(' ', '')
eabc1 = '🇦 🇧 🇨 🇩 🇪 🇫 🇬 🇭 🇮 🇯 🇰 🇱 🇲 🇳 🇴 🇵 🇶 🇷 🇸 🇹 🇺 🇻 🇼 🇽 🇾 🇿'.replace(' ', '')
eabc2 = '🅐 🅑 🅒 🅓 🅔 🅕 🅖 🅗 🅘 🅙 🅚 🅛 🅜 🅝 🅞 🅟 🅠 🅡 🅢 🅣 🅤 🅥 🅦 🅧 🅨 🅩'.replace(' ', '')
emodic = {x[0]: x[1:] for x in zip(abc, eabc0, eabc1)}
slicenames = ['ab', 'cl', 'sos', 'ng', 'ok', 'up', 'cool', 'new', 'free', 'vs', 'x', '!!', '!?', 'm', 'id', 'p', 'wc', 'atm', 'abc', 'll', 'tm', 'c', 'r', 'end', 'back', 'on', 'top', 'soon', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', '!', '!', '?', '?', 'v', 'x', 'zzz', 'x', ]
slices = list(zip(
    slicenames, 
    ['🆎', '🆑', '🆘', '🆖', '🆗', '🆙', '🆒', '🆕', '🆓', '🆚', '❌', '‼️', '⁉️', '〽️', '🆔', '🅿️', '🚾', '🏧', '🔤', '⏸️', '™️', '©️', '®️', '🔚', '🔙', '🔛', '🔝', '🔜', '🔘', '⚪', '⚫', '🔴', '🔵', '🟤', '🟣', '🟢', '🟡', '🟠', '☮️', '⭕', '🔅', '🔆', '⏺️', '❗', '❕', '❓', '❔', '✅', '❎', '💤', '✖️', ]
))
#'0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟', '#️⃣', '*️⃣', 
async def setup(bot):
    l = tenor_cog(bot)
    await bot.add_cog(l)
    print(''.join(slicenames))
    print(slices)

class tenor_cog(commands.Cog):
    def __init__(self, bot):
        print('tenor module loaded')
        self.pd = pd('tenor.json')
        if 'score' not in self.pd:
            self.pd['score'] = {}
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        return
        a = message.author
        if a.bot:
            return
        c = message.channel
        txt = message.content
        if txt[0] in ['.', ':']:
            return
        if message.guild.id != 871762312208474133:
            return
        words = txt.split()
        if txt.startswith(str(self.bot.user.mention) + ' frp'):
            if c.id != 1085160288178941973:
                return
            alarm = 'alarm'
            with open('tenor', 'r') as f:
                key = f.read().replace('\n', '')
            n = 10
            query = f"https://g.tenor.com/v2/search?q={alarm}&key={key}&limit={n}"
            response = requests.get(query)
            data = response.json()
            url = random.choice(data['results'])
            await c.send(f'<@{451839413836840980}>\n' + url['url'])
        elif len(words) == 1:
            if len(message.mentions) == 0 and not message.reference:
                if txt.startswith('http'):
                    return
                sid = str(a.id)
                if sid not in self.pd['score']:
                    self.pd['score'][sid] = 0
                self.pd['score'][sid] += 1
                self.pd.sync()
                alarm = words[0]
                with open('tenor', 'r') as f:
                    key = f.read().replace('\n', '')
                n = 10
                query = f"https://g.tenor.com/v2/search?q={alarm}&key={key}&limit={n}"
                response = requests.get(query)
                data = response.json()
                url = random.choice(data['results'])
                await c.send(f'your score: {self.pd["score"][sid]}\n' + url['url'])
            else:
                if message.reference:
                    ref_message = await c.fetch_message(message.reference.message_id)
                    l = get_emoji(txt.lower())
                    if l:
                        for i in l:
                            await ref_message.add_reaction(i)
                        await message.delete()
        else:
            for i in words:
                try:
                    if i[0] == '#':
                        alarm = i[1:]
                        with open('tenor', 'r') as f:
                            key = f.read().replace('\n', '')
                        n = 10
                        query = f"https://g.tenor.com/v2/search?q={alarm}&key={key}&limit={n}"
                        response = requests.get(query)
                        data = response.json()
                        url = random.choice(data['results'])
                        await c.send(url['url'])
                except:
                    pass

def get_emoji(txt, carry = ''):
    if not txt:
        return carry
    for i in slices:
        if i[1][0] not in carry:
            if txt.startswith(i[0]):
                return get_emoji(txt[len(i[0]):], carry + i[1][0])
    for j in emodic[txt[0]]:
        if j == 'x':
            continue
        if j not in carry:
            return get_emoji(txt[1:], carry + j)
    return []
