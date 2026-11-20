# 10 — Exemples complets : assembler une vraie interface

> **Objectif :** passer des composants isolés à des interfaces cohérentes que vous pouvez adapter à votre bot.

Les exemples utilisent `discord.py 2.7.1`. Les variables comme `channel`, `member` ou `interaction` sont précisées dans le contexte de chaque extrait.

## 1. Réponse Components V2 éphémère

Une réponse éphémère est visible uniquement par l'utilisateur qui a lancé la commande :

```python
import discord
from discord import ui


async def send_private_notice(interaction: discord.Interaction):
    layout = ui.LayoutView()
    container = ui.Container(
        accent_color=discord.Colour.orange()
    )
    container.add_item(ui.TextDisplay("# Action indisponible"))
    container.add_item(
        ui.TextDisplay(
            "Tu dois vérifier les règles du serveur avant de continuer."
        )
    )
    layout.add_item(container)

    await interaction.response.send_message(
        view=layout,
        ephemeral=True,
    )
```

## 2. Fiche de profil avec avatar

```python
import discord
from discord import ui


def build_profile(member: discord.Member) -> ui.LayoutView:
    layout = ui.LayoutView()
    container = ui.Container(
        accent_color=discord.Colour.blurple()
    )

    container.add_item(
        ui.Section(
            ui.TextDisplay(f"# {member.display_name}"),
            ui.TextDisplay(f"Identifiant : `{member.id}`"),
            accessory=ui.Thumbnail(
                media=member.display_avatar.url,
                description=f"Avatar de {member.display_name}",
            ),
        )
    )
    container.add_item(ui.Separator())
    container.add_item(
        ui.TextDisplay(
            f"**A rejoint le serveur :** "
            f"<t:{int(member.joined_at.timestamp())}:D>"
            if member.joined_at
            else "**Date d'arrivée :** inconnue"
        )
    )

    layout.add_item(container)
    return layout
```

Envoi :

```python
await channel.send(view=build_profile(member))
```

## 3. Compteur interactif qui met à jour le message

Le compteur reste dans l'instance de la vue. Après chaque clic, une nouvelle vue est construite avec la valeur à jour :

```python
import discord
from discord import ui


class CounterLayout(ui.LayoutView):
    def __init__(self, count: int = 0):
        super().__init__(timeout=180)
        self.count = count

        button = ui.Button(
            label="Ajouter 1",
            style=discord.ButtonStyle.primary,
            custom_id="counter:add",
        )
        button.callback = self.increment

        container = ui.Container(
            ui.TextDisplay("# Compteur"),
            ui.TextDisplay(f"Valeur : **{self.count}**"),
            ui.ActionRow(button),
        )
        self.add_item(container)

    async def increment(self, interaction: discord.Interaction):
        updated_view = CounterLayout(self.count + 1)
        await interaction.response.edit_message(view=updated_view)
```

Envoi depuis une commande :

```python
await interaction.response.send_message(view=CounterLayout())
```

Cet exemple stocke le compteur en mémoire dans l'instance. Il revient à zéro si le bot redémarre ou si une nouvelle vue est créée. Pour des données durables ou partagées entre plusieurs processus, enregistrez l'état dans une base de données.

## 4. Panneau de ticket avec prise en charge et fermeture

L'extrait suivant montre la structure d'un panneau et la vérification des permissions. Le code métier de création/suppression du salon est volontairement séparé : adaptez-le à votre système de tickets.

```python
import discord
from discord import ui


class TicketPanel(ui.LayoutView):
    def __init__(self, owner_id: int):
        super().__init__(timeout=1800)
        self.owner_id = owner_id
        self.claimed_by: int | None = None

        claim = ui.Button(
            label="Prendre en charge",
            style=discord.ButtonStyle.primary,
            custom_id="ticket:claim",
        )
        close = ui.Button(
            label="Fermer",
            style=discord.ButtonStyle.danger,
            custom_id="ticket:close",
        )
        claim.callback = self.claim_ticket
        close.callback = self.close_ticket

        container = ui.Container(
            accent_color=discord.Colour.blurple()
        )
        container.add_item(ui.TextDisplay("# Ticket de support"))
        container.add_item(
            ui.TextDisplay(f"**Ouvert par :** <@{owner_id}>")
        )
        container.add_item(ui.Separator())
        container.add_item(
            ui.TextDisplay("Un membre de l'équipe peut prendre ce ticket en charge.")
        )
        container.add_item(ui.ActionRow(claim, close))
        self.add_item(container)

    async def claim_ticket(self, interaction: discord.Interaction):
        if not isinstance(interaction.user, discord.Member):
            await interaction.response.send_message(
                "Cette action est disponible uniquement sur un serveur.",
                ephemeral=True,
            )
            return

        if not interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message(
                "Tu n'as pas la permission de prendre ce ticket en charge.",
                ephemeral=True,
            )
            return

        if self.claimed_by is not None:
            await interaction.response.send_message(
                "Ce ticket est déjà pris en charge.",
                ephemeral=True,
            )
            return

        self.claimed_by = interaction.user.id
        await interaction.response.send_message(
            f"Ticket pris en charge par {interaction.user.mention}."
        )

    async def close_ticket(self, interaction: discord.Interaction):
        is_owner = interaction.user.id == self.owner_id
        can_manage = (
            isinstance(interaction.user, discord.Member)
            and interaction.user.guild_permissions.manage_channels
        )

        if not (is_owner or can_manage):
            await interaction.response.send_message(
                "Tu ne peux pas fermer ce ticket.",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            "Demande de fermeture validée. Branche ici ta logique d'archivage.",
            ephemeral=True,
        )
```

**À adapter avant production :** les permissions ci-dessus sont un exemple simple. Dans un système réel, vérifiez aussi que l'interaction se déroule dans le salon du ticket, utilisez les rôles de votre équipe et empêchez les doubles opérations en base de données.

## 5. Galerie d'images depuis le dossier du projet

```python
from pathlib import Path
import discord
from discord import ui


async def send_gallery(channel: discord.abc.Messageable):
    base = Path(__file__).resolve().parent
    names = ["home.png", "profile.png", "settings.png"]

    files = [
        discord.File(base / "assets" / name, filename=name)
        for name in names
    ]

    gallery = ui.MediaGallery()
    for name in names:
        gallery.add_item(
            media=f"attachment://{name}",
            description=f"Capture : {name}",
        )

    layout = ui.LayoutView()
    container = ui.Container()
    container.add_item(ui.TextDisplay("# Galerie du projet"))
    container.add_item(gallery)
    layout.add_item(container)

    await channel.send(view=layout, files=files)
```

Les chemins doivent exister dans le dossier `assets`. Le nom de chaque URL `attachment://` correspond au `filename` du fichier associé.

## 6. Menu de catégorie pour les tickets

```python
import discord
from discord import ui


class TicketCategoryLayout(ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=300)

        self.category_select = ui.Select(
            placeholder="Sélectionne le sujet de ta demande",
            min_values=1,
            max_values=1,
            options=[
                discord.SelectOption(label="Assistance", value="support"),
                discord.SelectOption(label="Signalement", value="report"),
                discord.SelectOption(label="Partenariat", value="partner"),
            ],
            custom_id="ticket:choose-category",
        )
        self.category_select.callback = self.on_category

        container = ui.Container(
            ui.TextDisplay("# Créer un ticket"),
            ui.TextDisplay("Choisis une catégorie pour continuer."),
            ui.ActionRow(self.category_select),
        )
        self.add_item(container)

    async def on_category(self, interaction: discord.Interaction):
        category = self.category_select.values[0]
        await interaction.response.send_message(
            f"Catégorie sélectionnée : **{category}**.\n"
            "La création du ticket peut maintenant commencer.",
            ephemeral=True,
        )
```

Ce code ne crée pas encore de salon : il montre comment récupérer et valider le choix. Ajoutez votre fonction de création de ticket après la sélection.

## 7. Exemple de bot minimal pour tester une commande

Ce script permet d'envoyer une vue via une commande slash. Créez une application dans le [Discord Developer Portal](https://discord.com/developers/applications), invitez-la avec les scopes `bot` et `applications.commands`, puis définissez la variable d'environnement `DISCORD_TOKEN`.

```python
import os
import discord
from discord import ui
from discord.ext import commands


class DemoBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=discord.Intents.default(),
        )

    async def setup_hook(self):
        await self.tree.sync()


bot = DemoBot()


@bot.tree.command(name="cv2", description="Afficher une démonstration Components V2")
async def cv2(interaction: discord.Interaction):
    layout = ui.LayoutView()
    container = ui.Container(
        accent_color=discord.Colour.blurple()
    )
    container.add_item(ui.TextDisplay("# Components V2 fonctionne !"))
    container.add_item(
        ui.TextDisplay("Cette interface a été envoyée avec `discord.py`. ")
    )
    layout.add_item(container)

    await interaction.response.send_message(
        view=layout,
        ephemeral=True,
    )


token = os.getenv("DISCORD_TOKEN")
if not token:
    raise RuntimeError("La variable d'environnement DISCORD_TOKEN est absente.")

bot.run(token)
```

N'écrivez jamais votre token directement dans un dépôt public. Utilisez une variable d'environnement ou un gestionnaire de secrets. Sous PowerShell, vous pouvez définir la variable pour la session avec `$env:DISCORD_TOKEN = "votre_token"` avant de lancer le script.

## Conseils pour adapter les exemples

- Remplacez les textes et couleurs par ceux de votre projet.
- Vérifiez les permissions avant les actions sensibles.
- Répondez à chaque interaction ou utilisez `defer()` si le traitement est long.
- Enregistrez les données importantes en base plutôt que seulement dans les attributs d'une vue.
- Pour un panneau qui doit survivre au redémarrage, consultez le chapitre [LayoutView](./01%20-%20LayoutView.md) sur les vues persistantes.

**Références :** [API `discord.ui`](https://discordpy.readthedocs.io/en/stable/interactions/api.html) · [Guide des interactions](https://discordpy.readthedocs.io/en/stable/interactions/index.html)

---

[← Menus](./09%20-%20Menus.md) · [Conseils →](./11%20-%20Conseils.md)
