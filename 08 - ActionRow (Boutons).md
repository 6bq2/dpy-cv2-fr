# 08 — `ActionRow` : ajouter des boutons interactifs

> **Objectif :** placer des boutons dans une interface V2, traiter les clics et comprendre les identifiants d'interaction.

## 1. Le rôle d'une `ActionRow`

`ui.ActionRow` organise les composants interactifs sur une ligne.

Dans un message Components V2, une ligne peut contenir :

- jusqu'à **5 boutons** ; ou
- **un seul menu de sélection**.

On ne mélange pas plusieurs boutons et un menu dans la même `ActionRow`.

## 2. Ajouter plusieurs boutons

```python
import discord
from discord import ui

row = ui.ActionRow(
    ui.Button(
        label="Confirmer",
        style=discord.ButtonStyle.success,
        custom_id="order:confirm",
    ),
    ui.Button(
        label="Annuler",
        style=discord.ButtonStyle.danger,
        custom_id="order:cancel",
    ),
)

container.add_item(row)
```

Les styles courants :

| Style | Usage |
| --- | --- |
| `primary` | Action principale |
| `secondary` | Action neutre ou secondaire |
| `success` | Confirmation ou réussite |
| `danger` | Suppression ou action risquée |
| `link` | Ouvrir une URL |

## 3. Associer un callback à un bouton

Un bouton avec un `custom_id` peut déclencher un callback. Avec une vue construite dynamiquement, créez le bouton puis affectez sa méthode :

```python
class ConfirmLayout(ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=180)

        confirm = ui.Button(
            label="Confirmer",
            style=discord.ButtonStyle.success,
            custom_id="confirm:yes",
        )
        confirm.callback = self.on_confirm

        container = ui.Container(
            ui.TextDisplay("## Valider cette opération ?"),
            ui.ActionRow(confirm),
        )
        self.add_item(container)

    async def on_confirm(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Opération confirmée.",
            ephemeral=True,
        )
```

Le callback reçoit l'objet `Interaction`. Vous pouvez notamment lire `interaction.user`, `interaction.guild`, `interaction.channel` et `interaction.message` selon le contexte.

## 4. Répondre à une interaction

Une interaction doit être acquittée une seule fois via `interaction.response`.

Pour répondre immédiatement :

```python
await interaction.response.send_message(
    "Action reçue !",
    ephemeral=True,
)
```

Pour modifier le message qui contient le bouton :

```python
await interaction.response.edit_message(view=self)
```

Pour une opération qui prend du temps :

```python
await interaction.response.defer(ephemeral=True)

# Traitement long ici...

await interaction.followup.send(
    "Traitement terminé.",
    ephemeral=True,
)
```

Après `defer()`, n'appelez pas une deuxième fois `interaction.response.send_message()`. Utilisez `followup` ou la méthode d'édition adaptée.

## 5. Vérifier qui peut utiliser un bouton

Un bouton visible dans un salon peut être cliqué par plusieurs personnes. Ne supposez pas que seule la personne qui a lancé la commande pourra l'utiliser.

Exemple : réserver l'action à l'auteur du panneau :

```python
class PrivatePanel(ui.LayoutView):
    def __init__(self, owner_id: int):
        super().__init__(timeout=180)
        self.owner_id = owner_id

        button = ui.Button(
            label="Continuer",
            style=discord.ButtonStyle.primary,
            custom_id="panel:continue",
        )
        button.callback = self.continue_action

        self.add_item(ui.ActionRow(button))

    async def continue_action(self, interaction: discord.Interaction):
        if interaction.user.id != self.owner_id:
            await interaction.response.send_message(
                "Ce panneau ne t'appartient pas.",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            "Tu peux continuer.",
            ephemeral=True,
        )
```

Une vérification côté callback est importante même si le bouton semble privé visuellement.

## 6. Créer un bouton lien

Un bouton de style `link` ouvre une adresse et ne déclenche pas de callback :

```python
link_button = ui.Button(
    label="Documentation",
    style=discord.ButtonStyle.link,
    url="https://discordpy.readthedocs.io/",
)

container.add_item(ui.ActionRow(link_button))
```

N'ajoutez pas de `custom_id` ni de callback à un bouton lien : il n'en a pas besoin.

## 7. Plusieurs lignes de boutons

Si vous avez plus de cinq boutons, créez plusieurs `ActionRow` :

```python
buttons = [
    ui.Button(
        label=f"Option {index + 1}",
        custom_id=f"option:{index + 1}",
    )
    for index in range(8)
]

for start in range(0, len(buttons), 5):
    container.add_item(
        ui.ActionRow(*buttons[start:start + 5])
    )
```

Le nombre global de composants de la vue reste limité à 40.

## 8. Utiliser les décorateurs d'une `ActionRow`

`discord.py` permet aussi de déclarer les callbacks avec un décorateur attaché à une ligne d'action :

```python
class DecoratedLayout(ui.LayoutView):
    actions = ui.ActionRow()

    @actions.button(
        label="Dire bonjour",
        style=discord.ButtonStyle.primary,
        custom_id="hello:greet",
    )
    async def greet(
        self,
        interaction: discord.Interaction,
        button: ui.Button,
    ):
        await interaction.response.send_message(
            "Bonjour !",
            ephemeral=True,
        )
```

Cette syntaxe est utile pour les layouts statiques. La méthode `button` attend `self`, l'interaction et le bouton.

## 9. `id` et `custom_id`

- `custom_id` est l'identifiant transmis avec l'interaction Discord. Il doit être stable pour une vue persistante.
- `id` est l'identifiant numérique du composant dans la mise en page ; il sert notamment à le retrouver avec `find_item()`.

Ne confondez pas ces deux paramètres.

**À lire ensuite :** [Menus de sélection](./09%20-%20Menus.md) · [LayoutView et vues persistantes](./01%20-%20LayoutView.md)

**Référence :** [API `ActionRow`](https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.ui.ActionRow) · [API `Button`](https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.ui.Button)

---

[← Composant File](./07%20-%20Composant%20File.md) · [Menus →](./09%20-%20Menus.md)
