# argus_ticket_github

This is a plugin to create tickets in Github from [Argus](https://github.com/Uninett/argus-server)

## Settings

* `TICKET_ENDPOINT`: `"https://github.com/"` or link to self-hosted instance, absolute URL
* `TICKET_AUTHENTICATION_SECRET`: Create a [personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) with the scope `repo`:

    ```
    {
        "token": token
    }
    ```

    It is recommended to create a Github API user and to ensure that that user
    has the necessary authorization for creating issues in the relevant
    repository.

* `TICKET_INFORMATION`:

    Project namespace and name (obligatory)

    ```
    {
        "project_namespace_and_name": project_namespace_and_name
    }
    ```

    To know which project to create the ticket in the Github API needs to know
    the owner and name of it. The owner is the user or organization the Github
    repository belongs to and the name is the name of the Github project.

    For the Github project
    [Hello Git World](https://github.com/githubtraining/hellogitworld) the
    dictionary would look like this:

    ```
    {
       "project_namespace_and_name": "githubtraining/hellogitworld",
    }
    ```

    Labels (optional)

    There are two ways of automatically filling labels:

    1. Labels that are always the same, independent of the incident.
    These will be set in `labels_set`.


        ```
        {
            "labels_set" : [
                label1,
                label2,
                label3,
            ]
        }
        ```

    2. Labels that are filled by attributes of the Argus incident.
    These are set in `labels_mapping` which is a list of the names of the
    attributes as they are returned by the API (e.g. `start_time`). If the
    information can be found in the tags the it has to be a dictionary with
    `tag` as the key and the name of the tag as the value (e.g.
    {"tag": "host"}).

        ```
        {
            "custom_fields_mapping" : [
                attribute_of_incident,
                {"tag": name_of_tag},
            ]
        }
        ```

## Code style

argus_ticket_github uses black as a source code formatter. Black can be installed
by running

```console
$ pip install black
```

A pre-commit hook will format new code automatically before committing.
To enable this pre-commit hook, run

```console
$ pre-commit install
```
