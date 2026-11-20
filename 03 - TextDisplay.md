# 03 — `TextDisplay` : écrire et mettre en forme le contenu

> **Objectif :** construire un message lisible avec du Markdown Discord, des mentions, des horodatages et du texte dynamique.

## 1. Le rôle de `TextDisplay`

`ui.TextDisplay` affiche du texte dans une mise en page Components V2. C'est l'équivalent pratique du contenu textuel d'un message ou d'une partie d'un embed, mais sous forme de composant.

Il peut être placé directement dans une `LayoutView`, dans un `Container`, dans une `Section` ou dans certains contextes de modals.

```python
from discord import ui

text = ui.TextDisplay("Bonjour depuis Components V2 !")
```

Puis ajoutez-le à un conteneur ou à la vue :

```python
container.add_item(text)
# ou : layout.add_item(text)
```

## 2. Le Markdown pris en charge

Le texte accepte la mise en forme Markdown habituelle de Discord :

```python
container.add_item(
    ui.TextDisplay(
        "# Titre principal\n"
        "## Sous-titre\n"
        "Texte normal, **important**, *italique* ou ~~barré~~.\n"
        "> Une citation\n"
        "`du code` ou un bloc de code.\n"
        "[Documentation Discord](https://discord.com/developers/docs)"
    )
)
```

Pour les messages longs, séparez les sections en plusieurs `TextDisplay`. C'est plus simple à relire et vous pouvez modifier une partie sans reconstruire tout le texte.

```python
container.add_item(ui.TextDisplay("# État du bot"))
container.add_item(ui.TextDisplay("**État :** En ligne"))
container.add_item(ui.TextDisplay("**Latence :** `42 ms`"))
```

## 3. Construire du texte dynamique

Utilisez les f-strings pour injecter des valeurs calculées :

```python
import discord
from discord import ui


async def send_profile(channel, member: discord.Member):
    layout = ui.LayoutView()
    container = ui.Container()

    container.add_item(
        ui.TextDisplay(
            f"# Profil de {member.display_name}\n"
            f"**Identifiant :** `{member.id}`\n"
            f"**Compte créé :** <t:{int(member.created_at.timestamp())}:D>"
        )
    )

    layout.add_item(container)
    await channel.send(view=layout)
```

N'oubliez pas que les données dynamiques peuvent contenir des caractères spéciaux ou du texte fourni par les utilisateurs. Validez les entrées selon votre besoin métier avant de les intégrer au message.

## 4. Horodatages Discord

Discord transforme une balise de temps en date localisée pour chaque lecteur :

```python
import discord

now = int(discord.utils.utcnow().timestamp())
text = ui.TextDisplay(f"Dernière mise à jour : <t:{now}:R>")
```

Quelques formats utiles :

| Format | Affichage |
| --- | --- |
| `<t:TIMESTAMP:t>` | Heure courte |
| `<t:TIMESTAMP:T>` | Heure avec secondes |
| `<t:TIMESTAMP:d>` | Date courte |
| `<t:TIMESTAMP:D>` | Date longue |
| `<t:TIMESTAMP:f>` | Date et heure |
| `<t:TIMESTAMP:F>` | Date complète |
| `<t:TIMESTAMP:R>` | Temps relatif |

Remplacez `TIMESTAMP` par un timestamp Unix en secondes, pas en millisecondes.

## 5. Mentions et notifications

Les mentions fonctionnent dans un `TextDisplay` :

```python
container.add_item(
    ui.TextDisplay(
        f"Ticket ouvert par {member.mention} dans {channel.mention}."
    )
)
```

Attention : afficher une mention et déclencher une notification sont deux choses différentes. Le paramètre `allowed_mentions` contrôle quelles mentions Discord doit réellement traiter.

Pour désactiver toutes les notifications de mention dans un message contenant du texte dynamique :

```python
await channel.send(
    view=layout,
    allowed_mentions=discord.AllowedMentions.none(),
)
```

Si vous souhaitez autoriser uniquement certaines catégories de mentions, configurez explicitement `discord.AllowedMentions` au lieu d'accepter toutes les mentions par défaut.

## 6. Limite de longueur

Un `TextDisplay` accepte jusqu'à **4 000 caractères**. Gardez donc les textes courts et répartissez les informations entre plusieurs composants lorsque c'est pertinent. La vue possède également une limite globale de composants.

Vous pouvez inspecter le texte total de la vue avec :

```python
print(layout.content_length())
```

La méthode `content_length()` aide à contrôler le volume de texte, mais elle ne remplace pas les limites propres à Discord.

## 7. Mettre à jour un texte après une interaction

Pour afficher une nouvelle valeur, reconstruisez le bloc contenant le texte puis éditez le message. Cette approche garde l'interface simple et évite de dépendre d'un attribut interne du composant :

```python
import discord
from discord import ui


def build_status_layout(status: str) -> ui.LayoutView:
    layout = ui.LayoutView()
    container = ui.Container()
    container.add_item(ui.TextDisplay("# État du service"))
    container.add_item(ui.TextDisplay(f"État : **{status}**"))
    layout.add_item(container)
    return layout


async def update_status(interaction: discord.Interaction, status: str):
    await interaction.response.edit_message(
        view=build_status_layout(status)
    )
```

`edit_message()` remplace les composants du message déclencheur par ceux de la nouvelle vue. Conservez la même logique pour reconstruire également les boutons ou menus qui doivent rester disponibles.

## Bonnes pratiques

- Une seule idée principale par bloc de texte.
- Utilisez les titres Markdown pour créer une hiérarchie.
- Évitez de placer tout le message dans un unique composant géant.
- Désactivez les mentions non souhaitées avec `allowed_mentions`.
- Ne construisez pas un message avec des données utilisateur non validées.

**À lire ensuite :** [Separator](./04%20-%20Separator.md) · [Section](./05%20-%20Section%20%28Thumbnail%20%26%20Bouton%29.md)

**Références :** [API `TextDisplay`](https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.ui.TextDisplay) · [Styles Markdown et horodatages Discord](https://discord.com/developers/docs/reference#message-formatting)

---

[← Container](./02%20-%20Container.md) · [Separator →](./04%20-%20Separator.md)
