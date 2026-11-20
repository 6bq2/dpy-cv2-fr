import discord
from discord import ui
from discord.ext import commands

class PersistentView(ui.LayoutView):
    def __init__(self) -> None:
        super().__init__(timeout=None)

        container = ui.Container()
        container.add_item(ui.TextDisplay("# Vue persistante"))

        button = ui.Button(
            label="Clique-moi",
            style=discord.ButtonStyle.primary,
            custom_id="persistent:example",
        )
        button.callback = self.on_click
        container.add_item(ui.ActionRow(button))
        self.add_item(container)

    async def on_click(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("Le bouton persistant fonctionne !", ephemeral=True)

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="$",
            intents=discord.Intents.all()
        )

    async def setup_hook(self):
        self.add_view(PersistentView())   
         
    async def on_ready(self):
        print(f"Connecté en tant que {self.user}")

bot = Bot()

@bot.command(name="persistent")
async def exemple(ctx: commands.Context) -> None:
    view = PersistentView()
    view.message = await ctx.send(view=view)

bot.run('token')