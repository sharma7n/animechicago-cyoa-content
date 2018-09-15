# AnimeChicago CYOA Content Manager

Content manager for the AnimeChicago CYOA application.

## Getting Started

```
bash app-bootstrap.sh
pipenv shell
python manage.py runserver $IP:$PORT
```

## Functions

1. Create, update, and delete questions
2. Provide access to the most current valid game state via a GraphQL API

## User Access Levels

1. Admin: all rights
2. Contributor: Can suggest new questions / answers, but not mutate any real game states
3. No rights