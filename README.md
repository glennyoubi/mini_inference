## PROJET DE MINI-INFÉRENCE

## EXPLICATIONS DES FICHIERS PYTHON

**main.py :** Contrôle l'execution totale du programme et éxecute la fonction de détection d'inférence.
**reqs.py :** Permet de faire des requêtes sur le site de jeuxDeMots et de passer de la page web à des ficheirs json
            contenant les relations entrantes et sortantes pour ***term*** téléchargé.
**json_converter.py :** Ce fichier contient les fonctions transformant des fichiers textes en fichier.
**relation_links_id_name.py :** Ce fichier retourne les id des relations présentes dans jeuxDeMots.
**files_cleaning.py :** Supprime tous les fichiers .txt et json des termes déjà téléchargés.

## EXPLICATIONS DES AUTRES FICHIERS

Dans ***./words/*** les fichiers ***words_base.txt** et **words_base_rels.txt** enregistrent les termes déjà téléchargés sur lesquels on a effectué une inférence.

Dans ***./words/relations/*** le fichier **keep.txt** permet juste d'éviter la suppression du répertoire ***/relations/***.

Les fichiers json, contenant les relations entrantes et sortantes, sont enregistrés dans  ***./words/relations/***

## POUR NETTOYER

Use this command :
```
make propre
```
