# 04 — `Separator` : aérer et séparer les sections

> **Objectif :** utiliser les séparateurs pour rendre une interface plus lisible, sans surcharger le message.

## 1. À quoi sert un séparateur ?

`ui.Separator` crée une séparation visuelle entre deux composants. Il peut afficher une ligne horizontale ou seulement ajouter de l'espace.

```python
container.add_item(ui.TextDisplay("## Informations"))
container.add_item(ui.Separator())
container.add_item(ui.TextDisplay("Voici les détails de la demande."))
```

Un séparateur ne contient pas de texte et ne déclenche aucune interaction.

## 2. Afficher ou masquer la ligne

Le paramètre s'appelle **`visible`** :

```python
# Ligne visible
ui.Separator(visible=True)

# Espace sans ligne
ui.Separator(visible=False)
```

> **Attention :** le paramètre n'est pas `divider`. Utilisez `visible`, qui est le nom attendu par l'API `discord.py`.

## 3. Modifier l'espacement

`spacing` accepte les valeurs de `discord.SeparatorSpacing` :

```python
small = ui.Separator(
    spacing=discord.SeparatorSpacing.small
)

large = ui.Separator(
    spacing=discord.SeparatorSpacing.large
)
```

Exemple complet :

```python
container = ui.Container()
container.add_item(ui.TextDisplay("# Paramètres"))
container.add_item(
    ui.Separator(spacing=discord.SeparatorSpacing.large)
)
container.add_item(ui.TextDisplay("### Notifications"))
container.add_item(ui.TextDisplay("Les notifications sont activées."))
container.add_item(
    ui.Separator(visible=False, spacing=discord.SeparatorSpacing.large)
)
container.add_item(ui.TextDisplay("### Confidentialité"))
container.add_item(ui.TextDisplay("Votre profil est privé."))
```

## 4. Quand utiliser chaque réglage ?

| Besoin | Réglage conseillé |
| --- | --- |
| Séparer deux sujets | `visible=True` |
| Ajouter de l'espace sans ligne | `visible=False` |
| Séparation discrète | `spacing=small` |
| Marquer un changement de grande section | `spacing=large` |

Les séparateurs sont des éléments de mise en page. Placez-les entre des blocs logiques, pas après chaque ligne de texte.

## 5. Ajouter un identifiant

Comme d'autres composants de mise en page, un séparateur peut recevoir un `id` numérique :

```python
SEPARATOR_ID = 30
separator = ui.Separator(
    visible=True,
    spacing=discord.SeparatorSpacing.large,
    id=SEPARATOR_ID,
)
container.add_item(separator)
```

Cet identifiant peut servir à retrouver le composant avec `layout.find_item(SEPARATOR_ID)`. Il n'est pas utilisé pour recevoir une interaction utilisateur.

## Exemple : résumé d'un ticket fermé

```python
layout = ui.LayoutView()
container = ui.Container(
    accent_color=discord.Colour.red()
)

container.add_item(ui.TextDisplay("# Ticket fermé"))
container.add_item(
    ui.TextDisplay(f"**Fermé par :** {interaction.user.mention}")
)
container.add_item(
    ui.Separator(spacing=discord.SeparatorSpacing.large)
)
container.add_item(
    ui.TextDisplay("La transcription a été archivée dans le salon des logs.")
)

layout.add_item(container)
await interaction.response.send_message(view=layout, ephemeral=True)
```

## À retenir

- `visible` contrôle l'affichage de la ligne.
- `spacing` accepte `discord.SeparatorSpacing.small` ou `.large`.
- Un séparateur n'est pas un composant interactif.
- L'API utilise `visible=`, pas `divider=`.

**À lire ensuite :** [Section](./05%20-%20Section%20%28Thumbnail%20%26%20Bouton%29.md) · [Container](./02%20-%20Container.md)

**Référence :** [API `Separator`](https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.ui.Separator)

---

[← TextDisplay](./03%20-%20TextDisplay.md) · [Section (Thumbnail & Bouton) →](./05%20-%20Section%20%28Thumbnail%20%26%20Bouton%29.md)
