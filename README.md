# Tutoriel Django avec API Rest

Ce repo est utilisé pour suivre le cours sur [OpenClassrooms](https://openclassrooms.com/fr/courses/7192416-mettez-en-place-une-api-avec-django-rest-framework/7422349-tirez-le-maximum-de-ce-cours).

## Sommaire

 - [Installation](Installation)

## Installation

Pour installer le projet sur PyCharm, cloner le repo dans un répertoire local avec la commande suivante :
```
git clone https://github.com/DCluseau/django-rest-ex1
```
Ouvrir le projet dans PyCharm puis, dans la console, entrer la commande suivante :
```
pip install -r requirements.txt
```

Attention, pour bien fonctionner, le projet doit être configuré avec les paramètres suivants :
- Python 3.10.11
- Django 3.2.5
- Django Rest Framework 3.12.4

Initialiser la base de données avec la commande suivante :

```
python manage.py migrate
```

Initialiser le projet pour l'environnement de développement local :

```
python manage.py init_local_dev
```

Pour lancer l'application, entrer la commande suivante dans le terminal de PyCharm :

```
python manage.py runserver
```
