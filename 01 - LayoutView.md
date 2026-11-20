# 01 — `LayoutView` : construire son premier message Components V2

> **Objectif :** comprendre le rôle de `LayoutView`, créer une mise en page et savoir comment l'envoyer, la modifier ou la rendre persistante.
>
> **Version utilisée dans ce guide :** `discord.py 2.7.1`. Components V2 est disponible à partir de `discord.py 2.6.0`.

## 1. Comprendre Components V2

Avec les messages classiques, on compose principalement avec `content`, `embed` et `view`. Components V2 propose une mise en page plus libre : le texte, les images, les fichiers et les contrôles interactifs deviennent des composants que l'on peut organiser.

`discord.ui.LayoutView` est la racine de cette mise en page. Il ne dessine rien tout seul : il contient les composants visibles.

```text
LayoutView
└── Container
    ├── TextDisplay
    ├── Separator
    ├── Section
    │   └── Thumbnail
    └── ActionRow
        ├── Button
        └── Button
```

Les anciens messages et les messages Components V2 peuvent coexister dans le même bot. En revanche, on ne mélange pas une `ui.View` classique et une `ui.LayoutView` dans le même message.

## 2. Installer la bonne version

Mettez `discord.py` à jour :

```bash
python -m pip install -U discord.py
```

Vérifiez la version réellement importée par Python :

```python
import discord

print(discord.__version__)
```

Si `discord.ui.LayoutView` n'existe pas, vérifiez que vous avez installé le bon paquet dans le bon environnement virtuel. Évitez d'installer le paquet tiers nommé `discord` à la place de `discord.py`.

## 3. Créer une vue minimale

Une `LayoutView` peut être construite dynamiquement avec `add_item()` :

```python
import discord
from discord import ui

layout = ui.LayoutView()
container = ui.Container(
    accent_color=discord.Colour.blurple()
)

container.add_item(
    ui.TextDisplay("# Bonjour !")
)
container.add_item(
    ui.TextDisplay("Ceci est mon premier message Components V2.")
)

layout.add_item(container)
```

Puis envoyez-la dans un salon :

```python
await channel.send(view=layout)
```

Ou en réponse à une interaction :

```python
await interaction.response.send_message(
    view=layout,
    ephemeral=True,
)
```

`ephemeral=True` rend la réponse visible uniquement par la personne qui a déclenché l'interaction.

## 4. Une vue complète dans une classe

Dès que la mise en page contient plusieurs composants, une classe rend le code plus simple à maintenir :

```python
import discord
from discord import ui


class WelcomeLayout(ui.LayoutView):
    def __init__(self, member: discord.Member):
        super().__init__(timeout=180)

        container = ui.Container(
            accent_color=discord.Colour.blurple()
        )
        container.add_item(ui.TextDisplay("# Bienvenue !"))
        container.add_item(
            ui.TextDisplay(
                f"Bienvenue {member.mention} sur le serveur.\n"
                "Lis les règles avant de participer."
            )
        )
        container.add_item(ui.Separator())
        container.add_item(
            ui.TextDisplay("*Amuse-toi bien parmi nous !*")
        )

        self.add_item(container)
```

Utilisation :

```python
await channel.send(view=WelcomeLayout(member))
```

Le paramètre `member` est fourni par le code qui crée la vue. La classe ne doit pas deviner le contexte dans lequel elle sera utilisée.

## 5. Déclarer les composants comme attributs de classe

Pour une interface statique, il est aussi possible de déclarer les composants directement dans la classe :

```python
class StaticLayout(ui.LayoutView):
    container = ui.Container(
        ui.TextDisplay("# Statut du bot"),
        ui.Separator(),
        ui.TextDisplay("Tous les services sont opérationnels."),
        accent_color=discord.Colour.green(),
    )
```

Cette approche est pratique quand la structure ne dépend pas de paramètres. Pour une vue qui reçoit un utilisateur, un compteur ou une liste calculée à l'exécution, préférez généralement la construction dans `__init__`.

## 6. Durée de vie d'une vue

Par défaut, `LayoutView` utilise un délai d'expiration de 180 secondes. Vous pouvez le modifier :

```python
layout = ui.LayoutView(timeout=60)   # expire après 60 secondes
layout = ui.LayoutView(timeout=None) # aucun délai d'expiration
```

Quand une vue expire, ses callbacks ne sont plus traités. Si vous souhaitez rendre l'expiration visible, vous pouvez désactiver les boutons dans `on_timeout()` ; voir [Autres astuces](./12%20-%20Autres.md).

### Vue persistante

Une vue persistante continue de recevoir les interactions après un redémarrage du bot. Deux conditions sont nécessaires :

1. `timeout=None` ;
2. chaque composant interactif doit avoir un `custom_id` défini.

Il faut ensuite réenregistrer la vue au démarrage :

```python
import discord
from discord import ui
from discord.ext import commands


class PersistentPanel(ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=None)

        button = ui.Button(
            label="Obtenir de l'aide",
            style=discord.ButtonStyle.primary,
            custom_id="support:open",
        )
        button.callback = self.open_support

        container = ui.Container(
            ui.TextDisplay("## Centre d'aide"),
            ui.TextDisplay("Clique sur le bouton pour contacter l'équipe."),
            ui.ActionRow(button),
        )
        self.add_item(container)

    async def open_support(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Explique ta demande à l'équipe.",
            ephemeral=True,
        )


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=discord.Intents.default(),
        )

    async def setup_hook(self):
        # Réassocie le callback au message déjà présent.
        self.add_view(PersistentPanel())
```

`add_view()` ne renvoie pas le message et ne le republie pas : il enregistre les callbacks pour les composants déjà envoyés. La vue enregistrée doit correspondre aux `custom_id` présents sur le message.

Vous pouvez contrôler l'état avec `view.is_persistent()`.

## 7. Retrouver un composant avec `find_item()`

Attribuez un `id` numérique à un composant que vous devrez retrouver plus tard. Dans cet exemple, on désactive un bouton après son utilisation :

```python
import discord
from discord import ui

REFRESH_BUTTON_ID = 101


class DashboardLayout(ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=180)

        button = ui.Button(
            label="Actualiser",
            style=discord.ButtonStyle.primary,
            custom_id="dashboard:refresh",
            id=REFRESH_BUTTON_ID,
        )
        button.callback = self.refresh
        self.add_item(ui.ActionRow(button))

    async def refresh(self, interaction: discord.Interaction):
        button = self.find_item(REFRESH_BUTTON_ID)

        if not isinstance(button, ui.Button):
            await interaction.response.send_message(
                "Le bouton est introuvable.",
                ephemeral=True,
            )
            return

        button.disabled = True
        await interaction.response.edit_message(view=self)
```

`find_item()` recherche un **`id` numérique** et renvoie le composant ou `None`. Il ne recherche pas le `custom_id`.

- `id` sert à retrouver un composant dans l'arbre de la mise en page.
- `custom_id` sert à identifier un bouton ou un menu dans les interactions Discord.

Pour mettre à jour un texte, le plus simple est généralement de reconstruire le `TextDisplay` avec le nouveau contenu puis d'éditer la vue. Un `TextDisplay` ne doit pas être traité comme une chaîne Python ordinaire.

## 8. Règles à connaître

| Règle | Détail |
| --- | --- |
| Composants | 40 au maximum dans une vue, y compris les composants imbriqués |
| Texte | Un `TextDisplay` accepte jusqu'à 4 000 caractères |
| Ancienne API | `ui.View` et `ui.LayoutView` ne se mélangent pas dans le même message |
| Champs classiques | N'envoyez pas `content`, `embed`, `embeds`, `poll` ou `stickers` avec une `LayoutView` |
| Pièces jointes | Elles doivent être référencées par un composant pour être visibles dans un message V2 |

`discord.py` active le flag Components V2 lorsqu'une `LayoutView` est envoyée. Vous n'avez pas besoin de définir manuellement le flag Discord.

## Pour continuer

- [Container](./02%20-%20Container.md) — organiser le contenu en blocs.
- [TextDisplay](./03%20-%20TextDisplay.md) — afficher et mettre en forme du texte.
- [Boutons et ActionRow](./08%20-%20ActionRow%20%28Boutons%29.md) — ajouter de l'interactivité.

**Références :** [API `LayoutView`](https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.ui.LayoutView) · [Référence officielle Components](https://discord.com/developers/docs/components/reference)

---

[Container →](./02%20-%20Container.md)
