# Contribuer

Merci de prendre le temps d’améliorer cette documentation. Les petites corrections sont aussi utiles que les nouveaux tutoriels.

## Avant de modifier

- Vérifiez que le sujet n’est pas déjà expliqué dans l’un des 12 chapitres.
- Pour un changement important, ouvrez d’abord une Issue afin d’éviter un travail en double.
- Confirmez le comportement d’une API dans la [documentation officielle de discord.py](https://discordpy.readthedocs.io/en/stable/interactions/api.html).
- Ne publiez jamais de token, de mot de passe, de fichier `.env` ou de donnée personnelle.

## Règles pour les tutoriels

1. Rédigez en français ; conservez les noms des classes, méthodes et paramètres en anglais.
2. Indiquez la version minimale de `discord.py` lorsqu’un exemple dépend d’une version précise.
3. Fournissez les imports et le contexte nécessaires pour comprendre l’extrait.
4. Préférez un exemple court qui fonctionne à un extrait incomplet.
5. Expliquez les limites ou cas particuliers lorsqu’ils peuvent provoquer une erreur.
6. Ajoutez des liens vers les références officielles plutôt que de recopier leur documentation.

## Envoyer une contribution

1. Forkez le dépôt.
2. Créez une branche descriptive, par exemple `docs/corrige-menu-select`.
3. Modifiez uniquement les fichiers nécessaires.
4. Lancez le contrôle local : `python .github/scripts/check_docs.py`.
5. Ouvrez une Pull Request en expliquant le problème et la solution.

## Avant d’envoyer la Pull Request

- [ ] Le changement apporte une information nouvelle ou corrige une erreur.
- [ ] Les liens internes fonctionnent.
- [ ] Les blocs de code sont correctement ouverts et fermés.
- [ ] Les versions mentionnées sont précises.
- [ ] Aucun secret ni donnée privée n’a été ajouté.
