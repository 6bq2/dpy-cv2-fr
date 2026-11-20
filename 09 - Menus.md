# 09 — Menus de sélection : choisir une option, un membre ou un salon

> **Objectif :** utiliser les menus de sélection dans une `ActionRow` et récupérer proprement les valeurs choisies.

## 1. Les types de menus

`discord.py` fournit plusieurs composants de sélection :

| Composant | Ce que la personne choisit | Valeur récupérée |
| --- | --- | --- |
| `ui.Select` | Options définies par le bot | `str` |
| `ui.UserSelect` | Utilisateur ou membre | `discord.User` ou `discord.Member` |
| `ui.RoleSelect` | Rôle du serveur | `discord.Role` |
| `ui.ChannelSelect` | Salon ou thread | Objet de salon résolu |
| `ui.MentionableSelect` | Utilisateur ou rôle | `Member`, `User` ou `Role` |

Une `ActionRow` contient un menu de sélection à la fois. Vous pouvez ajouter d'autres menus dans d'autres lignes.

## 2. Menu de chaînes (`ui.Select`)

Un menu classique utilise des `discord.SelectOption`. Il accepte jusqu'à 25 options :

```python
options = [
    discord.SelectOption(
        label="Général",
        value="general",
        description="Question générale",
        emoji="💬",
    ),
    discord.SelectOption(
        label="Technique",
        value="technical",
        description="Problème technique",
        emoji="🛠️",
    ),
    discord.SelectOption(
        label="Facturation",
        value="billing",
        description="Question de paiement",
        emoji="💳",
    ),
]

select = ui.Select(
    placeholder="Choisissez une catégorie",
    min_values=1,
    max_values=1,
    options=options,
    custom_id="ticket:category",
)
```

Puis associez le callback et ajoutez le menu à une ligne :

```python
select.callback = self.on_category
container.add_item(ui.ActionRow(select))
```

Dans le callback, récupérez les valeurs via l'objet Select :

```python
async def on_category(self, interaction: discord.Interaction):
    selected_values = self.category_select.values
    category = selected_values[0]

    await interaction.response.send_message(
        f"Catégorie choisie : **{category}**",
        ephemeral=True,
    )
```

Dans cet exemple, `self.category_select` doit être la référence au menu conservée dans `__init__` :

```python
self.category_select = ui.Select(
    placeholder="Choisissez une catégorie",
    options=options,
    custom_id="ticket:category",
)
self.category_select.callback = self.on_category
```

Ne lisez pas les valeurs dans `interaction.data["values"]` lorsque `discord.py` vous fournit déjà la propriété `.values` du composant.

## 3. Choisir plusieurs options

Les paramètres `min_values` et `max_values` contrôlent le nombre de sélections :

```python
select = ui.Select(
    placeholder="Choisissez jusqu'à trois rôles d'intérêt",
    min_values=1,
    max_values=3,
    options=[
        discord.SelectOption(label="Python", value="python"),
        discord.SelectOption(label="JavaScript", value="javascript"),
        discord.SelectOption(label="Design", value="design"),
        discord.SelectOption(label="Jeux vidéo", value="gaming"),
    ],
)
```

Le callback reçoit une liste :

```python
async def on_topics(self, interaction: discord.Interaction):
    topics = self.topic_select.values
    formatted = ", ".join(topics)

    await interaction.response.send_message(
        f"Tes choix : {formatted}",
        ephemeral=True,
    )
```

Pour un menu de chaînes, `values` contient les valeurs des options (`str`), pas leurs libellés visibles.

## 4. Sélectionner un utilisateur

```python
self.user_select = ui.UserSelect(
    placeholder="Choisir un membre",
    min_values=1,
    max_values=1,
    custom_id="admin:user",
)
self.user_select.callback = self.on_user

container.add_item(ui.ActionRow(self.user_select))
```

Callback :

```python
async def on_user(self, interaction: discord.Interaction):
    selected_user = self.user_select.values[0]

    await interaction.response.send_message(
        f"Utilisateur sélectionné : {selected_user.mention}",
        ephemeral=True,
    )
```

Dans un serveur, la valeur résolue est généralement un `discord.Member`. En message privé, elle peut être un `discord.User`. Si votre traitement a besoin de propriétés propres à `Member`, vérifiez le type avant de les utiliser.

## 5. Sélectionner un rôle

```python
self.role_select = ui.RoleSelect(
    placeholder="Choisir un rôle",
    custom_id="admin:role",
)
self.role_select.callback = self.on_role

container.add_item(ui.ActionRow(self.role_select))
```

```python
async def on_role(self, interaction: discord.Interaction):
    role = self.role_select.values[0]

    await interaction.response.send_message(
        f"Rôle sélectionné : {role.mention}",
        ephemeral=True,
    )
```

L'attribution ou le retrait du rôle est une opération séparée : vérifiez les permissions du bot et celles de la personne qui lance l'action avant de modifier le serveur.

## 6. Sélectionner un salon

`ui.ChannelSelect` peut être limité à certains types de salons :

```python
self.channel_select = ui.ChannelSelect(
    placeholder="Choisir un salon texte",
    channel_types=[discord.ChannelType.text],
    custom_id="admin:channel",
)
self.channel_select.callback = self.on_channel

container.add_item(ui.ActionRow(self.channel_select))
```

```python
async def on_channel(self, interaction: discord.Interaction):
    channel = self.channel_select.values[0]

    await interaction.response.send_message(
        f"Salon sélectionné : **{channel.name}** (`{channel.id}`)",
        ephemeral=True,
    )
```

Pour inclure plusieurs types, passez une liste à `channel_types`.

## 7. Sélectionner un membre ou un rôle

`ui.MentionableSelect` combine les choix de membres et de rôles :

```python
self.target_select = ui.MentionableSelect(
    placeholder="Choisir un membre ou un rôle",
    custom_id="admin:target",
)
self.target_select.callback = self.on_target

container.add_item(ui.ActionRow(self.target_select))
```

```python
async def on_target(self, interaction: discord.Interaction):
    target = self.target_select.values[0]
    await interaction.response.send_message(
        f"Élément sélectionné : {target.mention}",
        ephemeral=True,
    )
```

Le résultat peut être un `discord.Member`, un `discord.User` ou un `discord.Role`. Si le comportement diffère selon le type, utilisez `isinstance()` pour distinguer les cas.

## 8. Exemple complet : vue de sélection

```python
import discord
from discord import ui


class CategoryLayout(ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=180)

        self.category_select = ui.Select(
            placeholder="Quel est le sujet de ta demande ?",
            min_values=1,
            max_values=1,
            options=[
                discord.SelectOption(label="Général", value="general"),
                discord.SelectOption(label="Technique", value="technical"),
                discord.SelectOption(label="Facturation", value="billing"),
            ],
            custom_id="support:category",
        )
        self.category_select.callback = self.on_category

        container = ui.Container(
            ui.TextDisplay("# Centre de support"),
            ui.TextDisplay("Choisis une catégorie pour continuer."),
            ui.ActionRow(self.category_select),
        )
        self.add_item(container)

    async def on_category(self, interaction: discord.Interaction):
        category = self.category_select.values[0]
        await interaction.response.send_message(
            f"Tu as choisi : **{category}**",
            ephemeral=True,
        )
```

Envoi :

```python
await interaction.response.send_message(
    view=CategoryLayout(),
    ephemeral=True,
)
```

## Limites importantes

- `ui.Select` accepte jusqu'à 25 options.
- `min_values` peut être compris entre 0 et 25 ; `max_values` entre 1 et 25.
- Un `ActionRow` contient un seul menu de sélection.
- Un identifiant `custom_id` doit être fourni ou généré par la bibliothèque ; pour une vue persistante, définissez-le explicitement.
- Les menus spécialisés ont besoin d'un contexte adapté : les rôles et les salons sont liés aux serveurs.

**À lire ensuite :** [Exemples complets](./10%20-%20Exemples.md) · [Conseils et dépannage](./11%20-%20Conseils.md)

**Référence :** [API des menus de sélection](https://discordpy.readthedocs.io/en/stable/interactions/api.html#select-menus)

---

[← ActionRow (Boutons)](./08%20-%20ActionRow%20%28Boutons%29.md) · [Exemples →](./10%20-%20Exemples.md)
