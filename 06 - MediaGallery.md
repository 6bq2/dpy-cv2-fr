# 06 — `MediaGallery` : afficher plusieurs médias

> **Objectif :** présenter des images ou des médias dans une galerie, depuis une URL ou des fichiers envoyés avec le message.

## 1. À quoi sert une galerie ?

`ui.MediaGallery` affiche un ensemble de médias dans un même bloc. C'est utile pour :

- une série de captures d'écran ;
- des aperçus de produits ;
- des images d'un événement ;
- un tutoriel illustré ;
- plusieurs rendus d'une interface.

Une galerie contient **de 1 à 10 éléments**. Elle peut être ajoutée directement à une `LayoutView` ou à un `Container`.

## 2. Afficher une seule image

```python
import discord
from discord import ui

layout = ui.LayoutView()
container = ui.Container()

container.add_item(ui.TextDisplay("# Aperçu du projet"))

gallery = ui.MediaGallery()
gallery.add_item(
    media="https://example.com/screenshot.png",
    description="Capture de l'écran principal",
)

container.add_item(gallery)
layout.add_item(container)
await channel.send(view=layout)
```

`media` peut être une URL accessible ou une référence de pièce jointe telle que `attachment://capture.png`.

## 3. Ajouter plusieurs images

Ajoutez les éléments un par un :

```python
gallery = ui.MediaGallery()

gallery.add_item(
    media="https://example.com/home.png",
    description="Page d'accueil",
)
gallery.add_item(
    media="https://example.com/settings.png",
    description="Paramètres",
)
gallery.add_item(
    media="https://example.com/profile.png",
    description="Profil utilisateur",
)

container.add_item(gallery)
```

Vous pouvez également créer explicitement les objets `discord.MediaGalleryItem` :

```python
items = [
    discord.MediaGalleryItem(
        media="https://example.com/one.png",
        description="Première image",
    ),
    discord.MediaGalleryItem(
        media="https://example.com/two.png",
        description="Deuxième image",
    ),
]

gallery = ui.MediaGallery(*items)
```

L'utilisation de `add_item()` est généralement plus facile à lire pour commencer.

## 4. Afficher des images locales

Pour envoyer un fichier situé sur le disque, il faut :

1. créer un objet `discord.File` ;
2. référencer son nom avec `attachment://...` dans la galerie ;
3. envoyer le fichier dans le même appel que la vue.

Exemple avec `pathlib` :

```python
from pathlib import Path
import discord
from discord import ui

BASE_DIR = Path(__file__).resolve().parent
image_path = BASE_DIR / "assets" / "interface.png"

file = discord.File(
    image_path,
    filename="interface.png",
)

gallery = ui.MediaGallery()
gallery.add_item(
    media="attachment://interface.png",
    description="Capture de l'interface",
)

layout = ui.LayoutView()
container = ui.Container()
container.add_item(ui.TextDisplay("# Capture locale"))
container.add_item(gallery)
layout.add_item(container)

await channel.send(view=layout, file=file)
```

Le nom de `attachment://interface.png` doit correspondre exactement au `filename` de `discord.File`, extension et casse comprises.

## 5. Envoyer plusieurs fichiers locaux

```python
files = [
    discord.File("assets/home.png", filename="home.png"),
    discord.File("assets/settings.png", filename="settings.png"),
]

gallery = ui.MediaGallery()
gallery.add_item(media="attachment://home.png", description="Accueil")
gallery.add_item(media="attachment://settings.png", description="Paramètres")

layout = ui.LayoutView()
layout.add_item(gallery)

await channel.send(view=layout, files=files)
```

N'envoyez pas les mêmes objets `discord.File` plusieurs fois sans les recréer ou repositionner correctement leurs flux. Le plus simple est de créer de nouveaux objets pour chaque envoi.

## 6. Ajouter un avertissement spoiler

Un élément de galerie peut être marqué comme spoiler :

```python
gallery.add_item(
    media="https://example.com/reveal.png",
    description="Aperçu masqué",
    spoiler=True,
)
```

Le paramètre `spoiler` s'applique à l'élément de média concerné.

## 7. Ajouter ou retirer des images

Quelques méthodes utiles :

```python
gallery.add_item(media="https://example.com/one.png")
gallery.clear_items()  # retire tous les éléments
```

`MediaGallery` expose également `append_item()`, `insert_item_at()` et `remove_item()` pour gérer une galerie construite dynamiquement.

## Limites et conseils

- 10 éléments maximum par galerie.
- Le média doit être une URL ou une pièce jointe correctement envoyée.
- La description d'un élément peut contenir jusqu'à 256 caractères.
- Pour une seule petite image associée à un profil, préférez `Section` + `Thumbnail`.
- Vérifiez que les URL sont accessibles par Discord et ne nécessitent pas une session privée.

**À lire ensuite :** [Composant File](./07%20-%20Composant%20File.md) · [Exemples complets](./10%20-%20Exemples.md)

**Référence :** [API `MediaGallery`](https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.ui.MediaGallery)

---

[← Section (Thumbnail & Bouton)](./05%20-%20Section%20%28Thumbnail%20%26%20Bouton%29.md) · [Composant File →](./07%20-%20Composant%20File.md)
