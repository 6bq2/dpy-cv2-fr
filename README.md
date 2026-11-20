# discord.py — Components V2 en français

<p align="center">
  <strong>Apprendre à construire des interfaces Discord modernes avec Python.</strong><br>
  Des explications progressives, des exemples pratiques et des repères pour éviter les erreurs courantes.
</p>

> Documentation communautaire non officielle. Ce projet n'est pas affilié à Discord ni aux mainteneurs de `discord.py`.

## Avant de commencer

- **Python :** 3.8 ou plus récent (selon les prérequis de `discord.py`).
- **Bibliothèque :** `discord.py 2.6.0` minimum pour Components V2.
- **Version de référence des exemples :** `discord.py 2.7.1`.

Installez ou mettez à jour la bibliothèque :

```bash
python -m pip install -U discord.py
```

Vérifiez la version chargée par Python :

```python
import discord
print(discord.__version__)
```

Utilisez un environnement virtuel et évitez d'appeler votre fichier `discord.py` : il masquerait le vrai module.

## Parcours conseillé

| # | Guide | Contenu |
| ---: | --- | --- |
| 01 | [LayoutView](./01%20-%20LayoutView.md) | Créer, envoyer, modifier et rendre une vue persistante |
| 02 | [Container](./02%20-%20Container.md) | Regrouper les éléments et appliquer une couleur d'accent |
| 03 | [TextDisplay](./03%20-%20TextDisplay.md) | Markdown, texte dynamique, mentions et horodatages |
| 04 | [Separator](./04%20-%20Separator.md) | Ajouter des séparations et maîtriser l'espacement |
| 05 | [Section, Thumbnail et bouton](./05%20-%20Section%20%28Thumbnail%20%26%20Bouton%29.md) | Associer un texte à une miniature ou une action |
| 06 | [MediaGallery](./06%20-%20MediaGallery.md) | Afficher des médias et des images locales |
| 07 | [Composant File](./07%20-%20Composant%20File.md) | Afficher une pièce jointe dans la mise en page |
| 08 | [ActionRow et boutons](./08%20-%20ActionRow%20%28Boutons%29.md) | Ajouter des boutons et traiter les interactions |
| 09 | [Menus](./09%20-%20Menus.md) | Choisir une option, un utilisateur, un rôle ou un salon |
| 10 | [Exemples complets](./10%20-%20Exemples.md) | Assembler des interfaces de bot réutilisables |
| 11 | [Conseils et dépannage](./11%20-%20Conseils.md) | Limites, erreurs fréquentes et vérifications |
| 12 | [Autres astuces](./12%20-%20Autres.md) | Inspection, édition, persistance et architecture |

## Les trois règles à comprendre en premier

1. **`LayoutView` est la racine** de la mise en page Components V2.
2. **Le contenu s'ajoute sous forme de composants** (`TextDisplay`, `Container`, `Section`, `MediaGallery`, `File`, etc.).
3. **Chaque interaction doit être acquittée une seule fois** via `interaction.response`. Pour un traitement long, utilisez `defer()` puis `followup` ou une édition adaptée.

Une `LayoutView` ne se combine pas avec `content`, `embed`/`embeds`, `poll` ou `stickers` dans le même message. Le flag Components V2 est permanent une fois appliqué à un message.

## Références officielles

- [Documentation discord.py](https://discordpy.readthedocs.io/en/stable/)
- [API Interactions et composants de discord.py](https://discordpy.readthedocs.io/en/stable/interactions/api.html)
- [Référence Components de Discord](https://discord.com/developers/docs/components/reference)
- [Dépôt officiel discord.py et exemples](https://github.com/Rapptz/discord.py)

## Contribuer

Les corrections, améliorations pédagogiques et nouveaux exemples sont les bienvenus. Consultez [CONTRIBUTING.md](./CONTRIBUTING.md) avant de proposer une modification. Pour signaler une vulnérabilité, suivez [SECURITY.md](./SECURITY.md).

## Licence

Ce projet conserve sa licence MIT. Consultez le fichier [LICENSE](./LICENSE).
