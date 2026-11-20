import discord
from discord import ui
from discord.ext import commands

def disable(self):
    def disable_children(items):
        for item in items:
            if isinstance(item, (discord.ui.Button, discord.ui.Select, discord.ui.ChannelSelect, discord.ui.RoleSelect, discord.ui.UserSelect, discord.ui.MentionableSelect)):
                item.disabled = True
            children = getattr(item, "children", None)
            if children:
                disable_children(children)
    disable_children(self.children)
    
class PaginatorView(ui.LayoutView):
    def __init__(self, ctx: commands.Context, items: list, page: int = 0):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.items = items
        self.page = page
        self.chunk_base = 2

        self.build()
        self.message: discord.Message | None = None

    def build(self):
        chunk = self.items[self.page * self.chunk_base : (self.page + 1) * self.chunk_base]

        c = ui.Container()
        c.add_item(ui.TextDisplay(f"# Liste des Administrateurs sur le serveur")).add_item(ui.Separator())

        for item in chunk:
            c.add_item(ui.TextDisplay(
                f"**Mention** : {item['mention']}\n"
                f"**ID** : `{item['id']}`\n"
                f"**Rôle élevé** : `{item['highest_role_name']}`"
            ))
            c.add_item(ui.Separator())

        buttons = []
        if self.page > 0:
            btn1 = ui.Button(style=discord.ButtonStyle.secondary, emoji="◀️")
            btn1.callback = self.prev_page
            buttons.append(btn1)
        if (self.page + 1) * self.chunk_base < len(self.items):
            btn2 = ui.Button(style=discord.ButtonStyle.secondary, emoji="▶️")
            btn2.callback = self.next_page
            buttons.append(btn2)

        if buttons:
            c.add_item(ui.ActionRow(*buttons))
        
        c.add_item(ui.TextDisplay(f"-# Page **{self.page + 1}** avec un total de **{len(chunk)} administrateur{'s' if len(chunk) > 1 else ''}**"))
        self.add_item(c)

    async def on_timeout(self) -> None:
        try:
            disable(self)
            if self.message is not None:
                await self.message.edit(view=self, allowed_mentions=discord.AllowedMentions.none())
        except:
            pass

    async def interaction_check(self, i: discord.Interaction):
        if self.ctx.author.id != i.user.id:
            await i.response.send_message("❌ Tu ne peux pas gérer ce Container.", ephemeral=True)
            return False
        return True

    async def prev_page(self, i: discord.Interaction):
        if self.page == 0:
            return

        self.page -= 1
        self.clear_items()
        self.build()
        await i.response.edit_message(view=self, allowed_mentions=discord.AllowedMentions.none())
    
    async def next_page(self, i: discord.Interaction):
        if (self.page + 1) * self.chunk_base >= len(self.items):
            return

        self.page += 1
        self.clear_items()
        self.build()
        await i.response.edit_message(view=self, allowed_mentions=discord.AllowedMentions.none())

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="$",
            intents=discord.Intents.all()
        )
    
    async def on_ready(self):
        print(f"Connecté en tant que {self.user}")

bot = Bot()

@bot.command(name="admins")
async def exemple(ctx: commands.Context) -> None:
    items = [{
        "mention": admin.mention,
        "id": admin.id,
        "highest_role_name": admin.top_role.name
    } for admin in ctx.guild.members if admin.guild_permissions.administrator]
    
    view = PaginatorView(ctx, items)
    view.message = await ctx.send(view=view, allowed_mentions=discord.AllowedMentions.none())

bot.run('token')