# 12 — Autres astuces : composants avancés et bonnes pratiques

> **Objectif :** aller plus loin avec les identifiants, l'inspection d'une vue, les interactions limitées à un utilisateur et la gestion des erreurs.

## 1. Différence entre `id` et `custom_id`

Ces deux identifiants ont des rôles distincts :

| Paramètre | Type | Utilisation |
| --- | --- | --- |
| `id` | Entier | Identifier un composant dans la mise en page, notamment avec `find_item()` |
| `custom_id` | Chaîne | Identifier un bouton ou un menu lors d'une interaction Discord |

Exemple :

```python
status_text = ui.TextDisplay(
    "État : prêt",
    id=100,
)

refresh_button = ui.Button(
    label="Actualiser",
    custom_id="dashboard:refresh",
)
```

N'utilisez pas `find_item("dashboard:refresh")` : `find_item()` recherche un `id` numérique.

## 2. Parcourir tous les composants d'une vue

`walk_children()` parcourt récursivement les composants, y compris ceux qui sont imbriqués dans des conteneurs, sections ou lignes d'action :

```python
for item in layout.walk_children():
    print(type(item).__name__, item.id)
```

Pour compter les éléments imbriqués :

```python
print(layout.total_children_count)
```

Pour connaître la longueur totale du texte :

```python
print(layout.content_length())
```

Ces méthodes sont utiles pour déboguer une mise en page construite dynamiquement.

## 3. Ajouter et retirer des composants

Vous pouvez modifier une vue avant son envoi :

```python
layout = ui.LayoutView()
container = ui.Container()

status = ui.TextDisplay("État : en attente", id=10)
container.add_item(status)
layout.add_item(container)

# Retirer un composant avant l'envoi
container.remove_item(status)
container.add_item(ui.TextDisplay("État : prêt"))
```

Vous pouvez également utiliser `clear_items()` sur un conteneur ou une vue pour retirer tous ses enfants. Faites attention : vider une vue déjà envoyée ne modifie pas automatiquement le message Discord. Il faut ensuite éditer le message avec la vue mise à jour.

## 4. Modifier un message Components V2 existant

Pour récupérer les composants d'un message existant et les convertir en objet modifiable, utilisez `LayoutView.from_message()` :

```python
message = await channel.fetch_message(message_id)
layout = ui.LayoutView.from_message(message)

# Modifiez les composants récupérés ici.
await message.edit(view=layout)
```

Cette méthode retourne une `LayoutView` générique, pas une instance de votre sous-classe personnalisée. Les attributs spécifiques que vous auriez ajoutés dans votre propre classe ne sont donc pas recréés automatiquement.

Si le message initial était un message classique contenant du texte, des embeds ou des pièces jointes, consultez les paramètres d'édition de `Message.edit()` : pour passer à une `LayoutView`, les champs classiques précédents peuvent devoir être explicitement vidés (`content=None`, `embed=None`, `embeds=[]`, `attachments=[]`). Une fois le flag Components V2 posé sur un message, il ne peut plus être retiré.

## 5. Restreindre les interactions à une personne

Pour un panneau personnel, stockez l'identifiant de la personne autorisée :

```python
class PersonalPanel(ui.LayoutView):
    def __init__(self, owner_id: int):
        super().__init__(timeout=180)
        self.owner_id = owner_id

        button = ui.Button(
            label="Continuer",
            custom_id="personal:continue",
        )
        button.callback = self.continue_action
        self.add_item(ui.ActionRow(button))

    async def continue_action(self, interaction: discord.Interaction):
        if interaction.user.id != self.owner_id:
            await interaction.response.send_message(
                "Ce panneau appartient à une autre personne.",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            "Action autorisée.",
            ephemeral=True,
        )
```

Ne vous fiez pas à l'apparence de l'interface pour gérer les autorisations. Vérifiez systématiquement les droits dans le callback avant d'effectuer une opération sensible.

## 6. Désactiver les contrôles à l'expiration

Pour une vue temporaire, vous pouvez désactiver les boutons et menus quand le délai expire. Il faut conserver une référence au message envoyé :

```python
class TemporaryPanel(ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=120)
        self.message: discord.Message | None = None

        button = ui.Button(
            label="Action temporaire",
            custom_id="temporary:action",
        )
        button.callback = self.on_action
        self.add_item(ui.ActionRow(button))

    async def on_action(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Action reçue.",
            ephemeral=True,
        )

    async def on_timeout(self):
        for item in self.walk_children():
            if isinstance(
                item,
                (
                    ui.Button,
                    ui.Select,
                    ui.UserSelect,
                    ui.RoleSelect,
                    ui.ChannelSelect,
                    ui.MentionableSelect,
                ),
            ):
                item.disabled = True

        if self.message is None:
            return

        try:
            await self.message.edit(view=self)
        except discord.NotFound:
            # Le message a déjà été supprimé.
            pass
        except discord.HTTPException:
            # L'édition a échoué côté API Discord.
            pass
```

Envoi :

```python
view = TemporaryPanel()
view.message = await channel.send(view=view)
```

`self.message` n'est pas un attribut fourni automatiquement par `LayoutView` dans cet exemple : c'est une référence que nous avons ajoutée nous-mêmes.

## 7. Journaliser les erreurs des callbacks

Vous pouvez personnaliser `on_error()` pour journaliser les exceptions :

```python
import logging

logger = logging.getLogger(__name__)


class LoggedLayout(ui.LayoutView):
    async def on_error(
        self,
        interaction: discord.Interaction,
        error: Exception,
        item: ui.Item,
    ):
        logger.error(
            "Erreur dans le composant %r (custom_id=%r)",
            item,
            getattr(item, "custom_id", None),
            exc_info=(type(error), error, error.__traceback__),
        )

        if not interaction.response.is_done():
            await interaction.response.send_message(
                "Une erreur est survenue pendant cette action.",
                ephemeral=True,
            )
```

Évitez d'envoyer les détails internes d'une exception aux utilisateurs. Gardez les informations techniques dans les journaux du bot.

## 8. Savoir si une vue est persistante

```python
view = MyPersistentLayout()

if view.is_persistent():
    print("La vue respecte les critères de persistance.")
else:
    print("La vue n'est pas persistante.")
```

Une vue persistante doit utiliser `timeout=None` et avoir un `custom_id` sur chacun de ses composants interactifs. Elle doit aussi être réenregistrée avec `bot.add_view()` au démarrage du bot.

## 9. Les composants de modals ne sont pas des composants de message

`ui.Label`, `ui.TextInput`, `ui.FileUpload`, `ui.RadioGroup` et `ui.Checkbox` appartiennent à l'interface des modals/formulaires. Ils ne remplacent pas `TextDisplay`, `MediaGallery` ou `ActionRow` dans une mise en page de message.

Certains composants de formulaires ont été ajoutés dans `discord.py 2.6` ou `2.7`. Consultez la documentation de votre version avant de les utiliser et gardez leur usage dans le contexte d'un `discord.ui.Modal`.

## 10. Conseils d'architecture

- Séparez la construction de l'interface de la logique métier.
- Créez une fonction `build_*_layout()` si plusieurs commandes doivent afficher la même mise en page.
- Gardez les `custom_id` stables et préfixés par fonctionnalité, par exemple `ticket:close`.
- Vérifiez les permissions dans les callbacks.
- Enregistrez dans une base de données les états qui doivent survivre au redémarrage.
- Gérez les cas où un message ou un salon a été supprimé.
- N'enregistrez jamais un token Discord dans un fichier public.

---

Vous avez terminé le parcours principal ! Pour approfondir, gardez les références officielles à portée de main :

- [Documentation discord.py — Interactions API](https://discordpy.readthedocs.io/en/stable/interactions/api.html)
- [Référence Components Discord](https://discord.com/developers/docs/components/reference)
- [Exemples officiels discord.py](https://github.com/Rapptz/discord.py/tree/master/examples/views)

---

[← Conseils](./11%20-%20Conseils.md)
