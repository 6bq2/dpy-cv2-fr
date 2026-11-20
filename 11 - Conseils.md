# 11 — Conseils, limites et dépannage

> **Objectif :** identifier rapidement les erreurs courantes et éviter les problèmes avant la mise en production.

## 1. Vérifier la version de `discord.py`

Components V2 nécessite `discord.py 2.6.0` ou une version ultérieure. Ce guide est écrit pour `2.7.1`.

```bash
python -m pip install -U discord.py
```

Puis :

```python
import discord
print(discord.__version__)
```

Si vous obtenez :

```text
AttributeError: module 'discord.ui' has no attribute 'LayoutView'
```

vérifiez la version, l'environnement virtuel actif et le paquet installé. Si votre projet contient un fichier nommé `discord.py`, renommez-le : il peut masquer la vraie bibliothèque.

## 2. Ne pas mélanger les champs classiques et Components V2

Une `LayoutView` active le mode Components V2 pour le message. Les champs classiques suivants ne peuvent pas accompagner cette vue :

- `content` ;
- `embed` ou `embeds` ;
- `poll` ;
- `stickers`.

À éviter :

```python
await channel.send(
    content="Bonjour",
    embed=discord.Embed(title="Titre"),
    view=layout,
)
```

À utiliser :

```python
layout = ui.LayoutView()
container = ui.Container()
container.add_item(ui.TextDisplay("# Bonjour"))
container.add_item(ui.TextDisplay("Le texte est dans la mise en page."))
layout.add_item(container)

await channel.send(view=layout)
```

Les embeds et les vues classiques restent disponibles pour les messages qui n'utilisent pas Components V2.

## 3. Ne pas confondre `ui.View` et `ui.LayoutView`

`discord.ui.View` est l'API classique des composants. `discord.ui.LayoutView` est la racine utilisée pour les composants V2.

Un même bot peut utiliser les deux systèmes dans des messages différents. Ne passez pas une `ui.View` classique à un message qui utilise une `LayoutView`, et inversement.

## 4. Ne pas imbriquer deux conteneurs

Incorrect :

```python
outer = ui.Container()
inner = ui.Container()
outer.add_item(inner)
```

Correct :

```python
layout = ui.LayoutView()
layout.add_item(ui.Container(ui.TextDisplay("Bloc 1")))
layout.add_item(ui.Container(ui.TextDisplay("Bloc 2")))
```

## 5. Respecter les limites des composants

| Élément | Limite |
| --- | ---: |
| Composants dans une `LayoutView` | 40 au total, y compris les éléments imbriqués |
| Contenu d'un `TextDisplay` | 4 000 caractères |
| Éléments d'une `Section` | 3 éléments textuels maximum |
| Boutons dans une `ActionRow` | 5 maximum |
| Menus dans une `ActionRow` | 1 maximum, sans boutons sur la même ligne |
| Options d'un `ui.Select` | 25 maximum |
| Éléments d'une `MediaGallery` | 10 maximum |

Le nombre total de composants est accessible avec `layout.total_children_count`.

## 6. Erreur sur `Separator`

Le paramètre pour afficher ou masquer la ligne est `visible`, pas `divider`.

```python
# Correct
ui.Separator(visible=False)

# Incorrect : le paramètre divider n'existe pas
ui.Separator(divider=False)
```

## 7. Une interaction qui affiche « Cette interaction a échoué »

Chaque callback doit répondre à l'interaction dans le délai prévu par Discord. Utilisez l'une de ces approches :

Réponse immédiate :

```python
await interaction.response.send_message(
    "Action reçue.",
    ephemeral=True,
)
```

Modification du message qui contient le composant :

```python
await interaction.response.edit_message(view=self)
```

Traitement long :

```python
await interaction.response.defer(ephemeral=True)

# Effectuer le traitement...

await interaction.followup.send(
    "Terminé.",
    ephemeral=True,
)
```

N'utilisez pas plusieurs méthodes `interaction.response` pour la même interaction. Après une réponse ou un defer, utilisez `interaction.followup` ou les méthodes d'édition adaptées.

## 8. Un bouton cesse de fonctionner après un redémarrage

Pour une vue persistante, vérifiez les trois points suivants :

1. la vue utilise `timeout=None` ;
2. tous les boutons et menus ont un `custom_id` stable ;
3. la vue est enregistrée avec `bot.add_view()` au démarrage du bot.

Exemple dans `setup_hook()` :

```python
async def setup_hook(self):
    self.add_view(MyPersistentLayout())
```

`timeout=None` seul ne suffit pas. La méthode `is_persistent()` peut servir à vérifier que la vue respecte les critères de persistance.

## 9. `find_item()` ne trouve pas le composant

`find_item()` cherche l'`id` numérique du composant, pas son `custom_id`.

```python
TEXT_ID = 42

container.add_item(
    ui.TextDisplay("Texte initial", id=TEXT_ID)
)

item = layout.find_item(TEXT_ID)
```

Un `custom_id` est un identifiant d'interaction et sert aux boutons ou menus. Les deux ne sont pas interchangeables.

## 10. Une pièce jointe n'apparaît pas

Dans un message V2, le fichier doit être référencé par un composant. Vérifiez le nom :

```python
upload = discord.File("report.pdf", filename="report.pdf")
container.add_item(ui.File(media="attachment://report.pdf"))
await channel.send(view=layout, file=upload)
```

Le nom après `attachment://` doit correspondre au `filename` envoyé. Pour une image, vous pouvez utiliser `MediaGallery` ou une `Thumbnail` lorsque le contexte le permet.

## 11. Vérifier les permissions et le contexte

Avant de modifier un salon, un rôle ou un message :

- contrôlez que l'utilisateur a le droit d'effectuer l'action ;
- contrôlez les permissions du bot ;
- vérifiez que `interaction.guild` n'est pas `None` si l'action exige un serveur ;
- gérez `discord.Forbidden`, `discord.NotFound` et `discord.HTTPException` quand c'est pertinent.

Un composant visible ne constitue pas une autorisation. Les contrôles doivent être appliqués côté serveur dans le callback.

## 12. Faire des tests avant publication

Testez au minimum :

- une interaction avec l'utilisateur autorisé et un utilisateur non autorisé ;
- un clic après l'expiration de la vue ;
- un redémarrage pour les vues persistantes ;
- les noms de fichiers avec majuscules/minuscules ;
- les menus sans valeur, à une valeur et à plusieurs valeurs ;
- la limite de composants lorsque la vue est générée dynamiquement.

**À lire ensuite :** [Autres astuces](./12%20-%20Autres.md) · [Exemples](./10%20-%20Exemples.md)

**Références :** [API discord.py](https://discordpy.readthedocs.io/en/stable/interactions/api.html) · [Référence Components Discord](https://discord.com/developers/docs/components/reference)

---

[← Exemples](./10%20-%20Exemples.md) · [Autres →](./12%20-%20Autres.md)
