import discord
from discord.ext import commands
from urllib.parse import quote_plus

class GoogleView(discord.ui.View):
    def __init__(self, query: str):
        super().__init__()
        query = quote_plus(query)
        url = f"https://www.google.com/search?q={query}"

        self.add_item(
            discord.ui.Button(
                label=f"Rechercher sur Google {query[:20]}",
                url=url,
            )
        )


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="$",
            intents=discord.Intents.all()
        )
    
    
    async def on_ready(self):
        print(f"Connecté en tant que {self.user}")

bot = Bot()

@bot.command(name="google")
async def exemple(ctx: commands.Context, *, query: str = None):
    if query is None:
        return await ctx.reply("Tu dois donner un query. `$google chat`")
    
    view = GoogleView(query)
    view.message = await ctx.send(view=view)

bot.run('token')