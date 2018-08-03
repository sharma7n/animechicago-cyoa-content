# Architecture

## Components

- Game Service: REST API that provides the full game state to an authorized client.
    - Has one POST route that accepts some config options, and is returned either one full and valid game state or an error response
    - Different urls on animechicago.com can use different versions of the game:
    - `/cyoa/` (current), `/cyoa/summer18/`, `/cyoa/spring18/` etc.
    - Request must have come from either the animechicago domain/subdomain, the mobile app, or a testing domain (allowed hosts)
    - As a second layer of authentication, the request should provide a secret key
    - Has a caching layer over it
- Content Administration: Web UI to update questions, choices, or series. Can also visualize the entire game, and generate versions of the game.
    - Requires both authentication (users log in to manage content) and authorization (users must have the right permission level)
- Live Models: Contain the Questions, Choices, and Series in a normalized relational form
    - Can be updated at any time by a user
- Archived Games: Contains the entire game state as a "document"
    - Can be created and deleted, but not modified
- Archiving Batch: Each (night? week?), automatically generate a version of the game. Keep one canonical version in storage for each quarter.

## Technologies

- Web framework: `Django`. Has great built-in user functionality, including permissions.
- Web UI front end: `Vue.js`.
- REST API: `Django REST API`. Since we're already working with django...
- Database: `Postgresql`. Solid relational database. I think postgres can also store some document-y kind of stuff.
- Caching: `Memcached` or `Redis`. Don't yet know which to choose.

## Priorities / Steps

1. Get Django and Postgres up and running. Define all the core models, create user groups, put in test content.
2. Get Django REST API up and running. Create the endpoint to get the game. (for now, each request immediately assembles the entire game)
3. Make a test client for the API, and ensure that I can obtain the game state.
4. Inject a caching service between the client and the API.
5. Create CLI tool for generating the game.
6. Create an archive model, and configure the system to regularly archive the game
7. The route to get the game should now first search the archives, and then try to construct the game (by adding it to the archives, and then reading from them).
8. The response on this route should be delegated as some kind of Task that can execute outside of the request-response cycle (not sure how to do this in a way that adds value)
9. Make the web client and the mobile client, and connect all of the components correctly.
10. Make a nicer web UI for contributors than the django-admin site.
11. Testing and logging/monitoring
12. Contribute content regularly!

# Data Model

3 models:
- `Question`
- `Choice`
- `Series`

Because our data has an inherent structure, and Questions/Series are repeated, a relational data storage model makes sense for actually maintaining the content.

We can and should also put a caching service in front of the database, from the perspective of the API at least.

The emitted "game" data will be in more of a JSON format.

# Emitted Game Example

```
{
    "version": "date-time",
    "serverTime": "date-time",
    "data": {
        "_root": {
            "type": "question",
            "text": "Do you want to watch anime?",
            "choices": [
                {
                    "text": "No",
                    "node": {
                        "type": "series",
                        "name": "CNN"
                    }
                },
                {
                    "text": "Yes",
                    "node": {
                        "type": "question",
                        "text": "Do you have bad taste?",
                        "choices": [
                            {
                                "text": "No",
                                "node": {
                                    "type": "series",
                                    "name": "Kaiji"
                                }
                            },
                            {
                                "text": "Yes",
                                "node": {
                                    "type": "series",
                                    "name": "Oreimo"
                                }
                            }
                        ]
                    }
                }
            ]
        }
    }
}
```