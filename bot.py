# [----------------------------------------Ключики----------------------------------------]
t = "ключ от дискорд бота"
aiapi = 'ключ от нейронки гугла'

# [----------------------------------------Импорты----------------------------------------]
import google.generativeai as genai
import discord
from discord.ext import commands
from datetime import timedelta
import requests
from io import BytesIO
from PIL import Image






# [----------------------------------------переменные----------------------------------------]

anti_spam = commands.CooldownMapping.from_cooldown(5, 15, commands.BucketType.member)
too_many_violations = commands.CooldownMapping.from_cooldown(4, 60, commands.BucketType.member)



# [----------------------------------------Конфиг ИИ----------------------------------------]
text_generation_config = {
	"temperature": 0.9,
	"top_p": 1,
	"top_k": 1,

}
safety_settings = [
	{"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
	{"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
	{"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
	{"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
]
system_instruction = "if message contains hateful speech and sluring others answer with \"hk291lzjs-k34\". And if message contains just slurs in general answer with code \"cH239jvb-82Qr\", else answer with \"ok\""
genai.configure(api_key=aiapi)



# [----------------------------------------Конфиг бота----------------------------------------]
config = {
'token': t,
'prefix': '#',
}
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=config['prefix'], intents=intents) 

# [----------------------------------------Функции----------------------------------------]
def get_gemini_response(prompt):
    model = genai.GenerativeModel(model_name="gemini-pro", generation_config=text_generation_config, safety_settings=safety_settings)
    result = model.generate_content(f"if message contains hateful speech, sluring others answer with code \"pds21L-AS\", if message contains filthy language, curse words in general (not hatespeech and saying bad things to others.) answer with \"hk291lzjs-k34\". And if message contains harmful or NSFW URLs answer with code \"cH239jvb-82Qr\", if message contains NSFW\extreme\harmful images answer with \"jakI13Lk\" answer with else answer with \"ok\". Here's the message: {prompt}" )
    print ('использовал getgeminiresponse')
    return result.text
    
def get_gemini_response_image(prompt):
    model = genai.GenerativeModel(model_name="gemini-pro-vision", generation_config=text_generation_config, safety_settings=safety_settings)
    result = model.generate_content(f"if message contains pornography/erotic content answer with \"hk291lzjs-k34\", else answer with \"ok\". Here's the message: {prompt}" )
    print ('использовал getgeminiresponsimage')
    return result.text

async def analyze_image(image_url):
    # Загрузка изображения с URL
    response = requests.get(image_url)
    if response.status_code == 200:
        image_bytes = BytesIO(response.content)
        # Обработка изображения
        image = Image.open(image_bytes)






# [----------------------------------------ивенты бота----------------------------------------]
@bot.event
async def on_message(ctx):
    if ctx.author != bot.user:
            # if ctx.attachments:
            #       for attachment in ctx.attachments:
            #            if attachment.content_type.startswith('image'):  # Проверяем, является ли прикрепленный файл изображением
            #             image_url = attachment.url  # Получаем прямую ссылку на изображение
            #             response = requests.get(image_url)
            #             if response.status_code == 200:
            #                 image_bytes = BytesIO(response.content)
            #             # Обработка изображения
            #                 image = Image.open(image_bytes)
            #             # Вызываем функцию вашего ИИ для анализа изображения
            #                 X = get_gemini_response_image(ctx)
            #                 if X.startswith("hk291lzjs-k34"):
            #                     await ctx.delete()
            #                     await ctx.channel.send(f"{ctx.author.mention}, пожалуйста, не отправляйте NSFW/экстремальный/опасный контент.")
            Z = get_gemini_response(ctx.content)
            if Z.startswith("jakI13Lk"):
                                await ctx.delete()
                                await ctx.channel.send(f"{ctx.author.mention}, пожалуйста, не отправляйте NSFW/экстремальный/опасный контент.")
            if Z.startswith("hk291lzjs-k34"):
                await ctx.delete()
                await ctx.channel.send(f"{ctx.author.mention}, пожалуйста, не используйте матерные слова")
                await ctx.author.timeout(timedelta(seconds=0), reason = 'матерится')
            if Z.startswith("pds21L-AS"):
                await ctx.delete()
                await ctx.channel.send(f"{ctx.author.mention}, не оскорбляйте других пользователей.")
                await ctx.author.timeout(timedelta(seconds=0), reason = 'оскорбляет')
            if Z.startswith("cH239jvb-82Qr"):
                await ctx.delete()
                await ctx.channel.send(f"{ctx.author.mention}, пожалуйста, не отправляйте запрещённые ссылки.")
                await ctx.author.timeout(timedelta(seconds=0), reason = 'отправляет запрещёнку')

            elif type(ctx.channel) is not discord.TextChannel or ctx.author.bot: return
            bucket = anti_spam.get_bucket(ctx)
            retry_after = bucket.update_rate_limit()
            if retry_after:
                await ctx.delete()
                await ctx.channel.send(f"{ctx.author.mention}, не спамьте.")
                violations = too_many_violations.get_bucket(ctx)
                check = violations.update_rate_limit()
                if check:
                    await ctx.author.timeout(timedelta(seconds=15), reason = 'Спаммммм')
               


@bot.event
async def on_ready():
	await bot.tree.sync()
	print("----------------------------------------")
	print(f'Gemini moderator Logged in as {bot.user}')
	print("----------------------------------------")

# [----------------------------------------Запуск бота----------------------------------------]
bot.run(config['token'])