import discord
from discord import ui
from discord.ext import commands


class ExampleView(ui.LayoutView):
    def __init__(self) -> None:
        super().__init__(timeout=60)
        container = ui.Container()
        container.add_item(ui.TextDisplay("# Bonjour !"))
        container.add_item(ui.Separator())
        container.add_item(
            ui.TextDisplay(
                "Cliquez sur le bouton. Le premier clic gagne !\n"
                f"La LayoutView se bloque dans <t:{int(discord.utils.utcnow().timestamp() + 60)}:R>"
            )
        )

        button = ui.Button(
            label="Clique-moi",
            style=discord.ButtonStyle.primary,
            custom_id="example_button",
        )
        button.callback = self.on_click
        container.add_item(ui.ActionRow(button))

        self.add_item(container)

    async def on_click(self, interaction: discord.Interaction):
        self.stop()
        self.clear_items()
        container = ui.Container()
        container.add_item(
            ui.TextDisplay(
                f"**{interaction.user.display_name}** a appuyé en premier !"
            )
        )
        self.add_item(container)
        await interaction.response.edit_message(view=self)

    async def on_timeout(self):
        self.clear_items()
        container = ui.Container()
        container.add_item(
            ui.TextDisplay("Personne n'a appuyé à temps !")
        )
        self.add_item(container)
        if self.message is not None:
            await self.message.edit(view=self)


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="$",
            intents=discord.Intents.all()
        )
    
    
    async def on_ready(self):
        print(f"Connecté en tant que {self.user}")

bot = Bot()

@bot.command(name="click")
async def exemple(ctx: commands.Context) -> None:
    view = ExampleView()
    view.message = await ctx.send(view=view)

bot.run('token')