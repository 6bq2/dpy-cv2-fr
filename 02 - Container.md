# 02 — `Container` : structurer une interface en blocs

> **Objectif :** utiliser les conteneurs pour regrouper visuellement du texte, des séparateurs, des galeries, des fichiers et des contrôles.

## 1. À quoi sert un conteneur ?

`ui.Container` est un bloc de mise en page. Il rassemble des composants qui appartiennent à la même zone et peut afficher une bande de couleur sur son bord.

Utilisez un conteneur pour créer, par exemple :

- un panneau d'information ;
- une fiche de profil ;
- un résumé de ticket ;
- une carte de statut ;
- une zone qui regroupe texte et boutons.

Un `Container` doit être ajouté à une `ui.LayoutView`. Il peut contenir des `TextDisplay`, `Separator`, `Section`, `MediaGallery`, `File` et `ActionRow`.

## 2. Créer son premier conteneur

```python
import discord
from discord import ui

layout = ui.LayoutView()

container = ui.Container()
container.add_item(
    ui.TextDisplay("# Informations du serveur")
)
container.add_item(
    ui.TextDisplay("Bienvenue dans notre communauté.")
)

layout.add_item(container)
await channel.send(view=layout)
```

Vous pouvez également passer les enfants directement au constructeur :

```python
container = ui.Container(
    ui.TextDisplay("## Maintenance"),
    ui.Separator(),
    ui.TextDisplay("Le service sera indisponible à 22 h."),
)
```

Les deux styles sont valides. `add_item()` est pratique pour construire une vue progressivement ; le constructeur est agréable lorsque la structure est déjà connue.

## 3. Ajouter une couleur d'accent

Le paramètre `accent_color` accepte une couleur `discord.Colour`, un entier RGB Discord ou `None` :

```python
blue = ui.Container(
    accent_color=discord.Colour.blurple()
)

green = ui.Container(
    accent_color=discord.Colour.green()
)

red = ui.Container(
    accent_color=discord.Colour.red()
)

custom = ui.Container(
    accent_color=discord.Colour.from_rgb(220, 70, 70)
)

without_accent = ui.Container(accent_color=None)
```

`accent_colour` (orthographe britannique) est également accepté par `discord.py`. Choisissez une seule orthographe dans un projet pour garder un code cohérent.

La couleur sert à distinguer des zones. Évitez d'en utiliser une différente pour chaque ligne : gardez une hiérarchie visuelle simple.

## 4. Organiser plusieurs éléments

Un conteneur peut mélanger les types de composants autorisés :

```python
container = ui.Container(
    accent_color=discord.Colour.blurple()
)

container.add_item(ui.TextDisplay("# Centre de support"))
container.add_item(
    ui.TextDisplay("Choisissez une action ci-dessous.")
)
container.add_item(ui.Separator())

section = ui.Section(
    ui.TextDisplay("**Disponibilité**"),
    ui.TextDisplay("L'équipe répond actuellement aux demandes."),
    accessory=ui.Thumbnail(
        media="https://example.com/support.png",
        description="Icône du support",
    ),
)
container.add_item(section)

button = ui.Button(
    label="Ouvrir un ticket",
    style=discord.ButtonStyle.primary,
    custom_id="support:open",
)
container.add_item(ui.ActionRow(button))

layout = ui.LayoutView()
layout.add_item(container)
```

Ce bloc montre la structure. Pour que le bouton fasse quelque chose, vous devez lui associer un callback, comme expliqué dans [ActionRow](./08%20-%20ActionRow%20%28Boutons%29.md).

## 5. Créer plusieurs conteneurs

Une même `LayoutView` peut contenir plusieurs conteneurs indépendants :

```python
layout = ui.LayoutView()

status = ui.Container(
    ui.TextDisplay("## API"),
    ui.TextDisplay("<:online:123456789012345678> Opérationnelle"),
    accent_color=discord.Colour.green(),
)

database = ui.Container(
    ui.TextDisplay("## Base de données"),
    ui.TextDisplay("<:offline:123456789012345678> Maintenance"),
    accent_color=discord.Colour.orange(),
)

layout.add_item(status)
layout.add_item(database)
```

Chaque bloc peut ainsi avoir son propre accent et son propre contenu.

## 6. Limites et erreurs fréquentes

### Ne pas imbriquer les conteneurs

Un `Container` ne peut pas contenir un autre `Container`. Ajoutez les deux conteneurs directement à la `LayoutView` :

```text
LayoutView
├── Container
│   ├── TextDisplay
│   └── Separator
└── Container
    ├── TextDisplay
    └── ActionRow
```

### Respecter la limite globale

La limite de 40 composants s'applique à toute la vue, y compris les composants placés dans les conteneurs, sections et lignes d'action. Utilisez `layout.total_children_count` pour inspecter le nombre total d'éléments imbriqués.

### Ne pas envoyer de contenu classique à côté

Avec une `LayoutView`, le texte doit être dans un composant. Utilisez `TextDisplay` au lieu de `content=` et choisissez Components V2 ou les embeds classiques pour un message donné.

## 7. Le paramètre `spoiler`

Le constructeur accepte aussi `spoiler=True` :

```python
hidden_block = ui.Container(
    ui.TextDisplay("Ce bloc est marqué comme spoiler."),
    spoiler=True,
)
```

Cette option marque le conteneur comme spoiler côté Discord. Elle ne remplace pas une vérification d'accès : ne placez jamais des informations confidentielles dans un message visible par des personnes non autorisées.

## À retenir

- `Container` regroupe les éléments d'une même zone.
- `accent_color` ajoute une couleur de bordure.
- Plusieurs conteneurs peuvent être ajoutés à une même `LayoutView`.
- Les conteneurs ne peuvent pas être imbriqués.
- La limite de composants est calculée sur toute la vue.

**À lire ensuite :** [TextDisplay](./03%20-%20TextDisplay.md) · [Separator](./04%20-%20Separator.md) · [Section](./05%20-%20Section%20%28Thumbnail%20%26%20Bouton%29.md)

**Référence :** [API `Container`](https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.ui.Container)

---

[← LayoutView](./01%20-%20LayoutView.md) · [TextDisplay →](./03%20-%20TextDisplay.md)
