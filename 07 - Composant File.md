# 07 — `File` : afficher une pièce jointe dans Components V2

> **Objectif :** envoyer un fichier avec une vue V2 et le rendre visible à l'intérieur de la mise en page.

## 1. Pourquoi utiliser `ui.File` ?

Dans un message Components V2, une pièce jointe envoyée n'est pas automatiquement affichée comme dans un message classique. Il faut la référencer dans la mise en page avec `ui.File` ou un composant média adapté.

La structure est la suivante :

```text
LayoutView
└── Container
    ├── TextDisplay
    └── File  ─── attachment://rapport.txt

Message envoyé avec : discord.File(...)
```

Il y a donc deux objets différents :

- `discord.File` prépare le fichier à téléverser ;
- `discord.ui.File` indique où l'afficher dans la mise en page.

## 2. Envoyer un fichier depuis le disque

```python
import discord
from discord import ui

filename = "rapport.txt"
upload = discord.File(
    "exports/rapport.txt",
    filename=filename,
)

layout = ui.LayoutView()
container = ui.Container(
    accent_color=discord.Colour.blurple()
)
container.add_item(ui.TextDisplay("# Rapport disponible"))
container.add_item(
    ui.TextDisplay("Téléchargez le fichier ci-dessous.")
)
container.add_item(
    ui.File(media=f"attachment://{filename}")
)
layout.add_item(container)

await channel.send(view=layout, file=upload)
```

Le nom après `attachment://` doit correspondre au `filename` passé à `discord.File`.

## 3. Générer un fichier en mémoire

Pour un rapport créé par le bot, `io.BytesIO` évite d'écrire un fichier temporaire sur le disque :

```python
from io import BytesIO
import discord
from discord import ui

content = "Rapport généré par le bot\nStatut : OK\n"
buffer = BytesIO(content.encode("utf-8"))

filename = "rapport.txt"
upload = discord.File(buffer, filename=filename)

layout = ui.LayoutView()
container = ui.Container()
container.add_item(ui.TextDisplay("## Rapport généré"))
container.add_item(ui.File(media=f"attachment://{filename}"))
layout.add_item(container)

await channel.send(view=layout, file=upload)
```

Si vous réutilisez un buffer qui a déjà été lu, replacez son curseur au début avant de créer ou réutiliser le fichier :

```python
buffer.seek(0)
```

## 4. Envoyer plusieurs fichiers

Chaque fichier doit avoir un nom distinct et sa propre référence :

```python
files = [
    discord.File("exports/users.csv", filename="users.csv"),
    discord.File("exports/errors.txt", filename="errors.txt"),
]

layout = ui.LayoutView()
container = ui.Container()
container.add_item(ui.TextDisplay("# Exports"))
container.add_item(ui.File(media="attachment://users.csv"))
container.add_item(ui.File(media="attachment://errors.txt"))
layout.add_item(container)

await channel.send(view=layout, files=files)
```

## 5. Marquer un fichier comme spoiler

```python
container.add_item(
    ui.File(
        media="attachment://logs.zip",
        spoiler=True,
    )
)
```

Cela marque le fichier comme spoiler côté Discord. Ce n'est pas une protection d'accès : toute personne autorisée à consulter le message peut toujours révéler le contenu.

## 6. Utiliser le composant dans une classe

```python
class TranscriptLayout(ui.LayoutView):
    def __init__(self, filename: str):
        super().__init__(timeout=180)

        container = ui.Container()
        container.add_item(ui.TextDisplay("## Transcription du ticket"))
        container.add_item(
            ui.TextDisplay("La conversation est archivée ci-dessous.")
        )
        container.add_item(
            ui.File(media=f"attachment://{filename}")
        )
        self.add_item(container)
```

Puis :

```python
filename = "ticket-0042.txt"
upload = discord.File(buffer, filename=filename)

await log_channel.send(
    view=TranscriptLayout(filename),
    file=upload,
)
```

La classe décrit uniquement la mise en page. Le code qui effectue l'envoi garde la responsabilité du fichier à téléverser.

## 7. Envoyer le fichier dans une réponse d'interaction

Le même principe fonctionne avec `InteractionResponse.send_message()` :

```python
await interaction.response.send_message(
    view=layout,
    file=upload,
    ephemeral=True,
)
```

Pour un envoi en message privé, vous pouvez utiliser `await user.send(view=layout, file=upload)`. Gérez toutefois les erreurs possibles : les messages privés peuvent être fermés ou bloqués.

## Erreurs fréquentes

| Symptôme | Vérification |
| --- | --- |
| Le composant ne trouve pas la pièce jointe | Le nom `attachment://...` correspond-il exactement au `filename` ? |
| Le fichier est vide | Le curseur du buffer est-il revenu à `0` ? |
| Le fichier n'apparaît pas | Avez-vous ajouté `ui.File` à la vue ? |
| Le bot ne peut pas envoyer le fichier | Vérifiez la taille maximale autorisée et les permissions du salon. |

**À lire ensuite :** [ActionRow et boutons](./08%20-%20ActionRow%20%28Boutons%29.md) · [Exemples](./10%20-%20Exemples.md)

**Référence :** [API `ui.File`](https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.ui.File)

---

[← MediaGallery](./06%20-%20MediaGallery.md) · [ActionRow (Boutons) →](./08%20-%20ActionRow%20%28Boutons%29.md)
