# 05 — `Section` : associer du texte à une miniature ou un bouton

> **Objectif :** créer une ligne composée de texte à gauche et d'un accessoire à droite.

## 1. Comprendre la structure

`ui.Section` regroupe un à trois éléments textuels et leur associe un accessoire. L'accessoire est généralement :

- `ui.Thumbnail` pour afficher une miniature ;
- `ui.Button` pour proposer une action rapide.

Visuellement, cela donne :

```text
┌─────────────────────────────────────────────┐
│ Nom du membre                    [Miniature] │
│ Une courte description                      │
│ Une information supplémentaire              │
└─────────────────────────────────────────────┘
```

Une section peut être ajoutée directement à une `LayoutView` ou placée dans un `Container`.

## 2. Créer une section avec une miniature

```python
import discord
from discord import ui

layout = ui.LayoutView()

section = ui.Section(
    ui.TextDisplay("**Alex**"),
    ui.TextDisplay("Un ticket de support vient d'être ouvert."),
    accessory=ui.Thumbnail(
        media="https://example.com/avatar.png",
        description="Avatar d'Alex",
    ),
)

layout.add_item(section)
await channel.send(view=layout)
```

La miniature est placée à droite ; le texte reste à gauche.

## 3. Utiliser l'avatar d'un membre

Les objets `Member` et `User` exposent `display_avatar`, qui fournit un avatar utilisable même si la personne n'a pas d'avatar personnalisé :

```python
section = ui.Section(
    ui.TextDisplay(f"## {member.display_name}"),
    ui.TextDisplay(
        f"**ID :** `{member.id}`\n"
        f"**Compte créé :** <t:{int(member.created_at.timestamp())}:D>"
    ),
    accessory=ui.Thumbnail(
        media=member.display_avatar.url,
        description=f"Avatar de {member.display_name}",
    ),
)
container.add_item(section)
```

Pour l'icône d'un serveur, vérifiez qu'elle existe avant d'accéder à `.url`, puis construisez la section avec ou sans miniature :

```python
guild = interaction.guild

if guild is not None and guild.icon is not None:
    accessory = ui.Thumbnail(media=guild.icon.url)
else:
    accessory = ui.Button(
        label="Voir les règles",
        style=discord.ButtonStyle.link,
        url="https://example.com/rules",
    )

section = ui.Section(
    ui.TextDisplay("## Informations du serveur"),
    accessory=accessory,
)
```

Une `Thumbnail` ne s'affiche pas seule : elle doit toujours être passée comme accessoire d'une `Section`.

## 4. Ajouter un bouton comme accessoire

Une section peut afficher un bouton à droite. Il faut toujours lui associer un callback si ce bouton doit effectuer une action :

```python
class ProfileLayout(ui.LayoutView):
    def __init__(self, member: discord.Member):
        super().__init__(timeout=180)

        button = ui.Button(
            label="Voir le profil",
            style=discord.ButtonStyle.primary,
            custom_id="profile:open",
        )
        button.callback = self.open_profile

        section = ui.Section(
            ui.TextDisplay(f"## {member.display_name}"),
            ui.TextDisplay("Consultez les informations de ce membre."),
            accessory=button,
        )
        self.add_item(section)

    async def open_profile(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Profil de {interaction.user.mention}",
            ephemeral=True,
        )
```

Dans un vrai bot, adaptez le callback pour afficher les données du membre concerné. Si le message est partagé, vérifiez que la personne qui clique a le droit d'effectuer l'action.

## 5. Plusieurs éléments textuels

Une section accepte jusqu'à trois éléments de contenu textuel :

```python
section = ui.Section(
    ui.TextDisplay("## Commande #1042"),
    ui.TextDisplay("**Statut :** Préparation"),
    ui.TextDisplay("**Total :** 29,90 €"),
    accessory=ui.Thumbnail(
        media="https://example.com/product.png"
    ),
)
```

Vous pouvez aussi construire la section étape par étape :

```python
section = ui.Section(
    accessory=ui.Thumbnail(media="https://example.com/product.png")
)
section.add_item("## Produit")  # une chaîne est convertie en TextDisplay
section.add_item("Stock disponible : 12")
```

Ne placez pas une galerie entière dans une section : l'accessoire est prévu pour un seul élément tel qu'une miniature ou un bouton.

## 6. Utiliser une section dans un conteneur

Pour regrouper la section avec d'autres éléments, ajoutez-la dans un `Container` :

```python
container = ui.Container(
    accent_color=discord.Colour.blurple()
)
container.add_item(ui.TextDisplay("# Nouvelle demande"))
container.add_item(ui.Separator())
container.add_item(section)

layout = ui.LayoutView()
layout.add_item(container)
```

## Erreurs fréquentes

- Oublier le paramètre obligatoire `accessory` lors de la création.
- Ajouter plus de trois éléments textuels dans une section.
- Utiliser `ui.Thumbnail` ailleurs que comme accessoire d'une section.
- Créer un bouton sans callback alors qu'une action est attendue.
- Accéder à `guild.icon.url` sans vérifier que le serveur possède une icône.

**À lire ensuite :** [MediaGallery](./06%20-%20MediaGallery.md) · [File](./07%20-%20Composant%20File.md)

**Référence :** [API `Section`](https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.ui.Section) · [API `Thumbnail`](https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.ui.Thumbnail)

---

[← Separator](./04%20-%20Separator.md) · [MediaGallery →](./06%20-%20MediaGallery.md)
