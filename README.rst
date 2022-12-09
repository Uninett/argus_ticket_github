argus_ticket_github
===================

This is a plugin to create tickets in Github from
`Argus <https://github.com/Uninett/argus-server>`_

Settings
--------

* ``TICKET_ENDPOINT``: ``"https://github.com/"`` or link to self-hosted instance, absolute URL
* ``TICKET_AUTHENTICATION_SECRET``: create a `personal access token <https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token>`_ with the scope "``repo``"

  ::

    {
        "token": token,
    }

* ``TICKET_INFORMATION``:

  To know which project to create the ticket in the Github API needs to know
  the owner and name of it. The owner is the user or organization the Github
  repository belongs to and the name is the name of the Github project.

  ::

    {
       "project_namespace_and_name": project_namespace_and_name,
    }

  For the Github project 
  `Hello Git World <https://github.com/githubtraining/hellogitworld>`_ the
  dictionary would look like this:

  ::

    {
       "project_namespace_and_name": "githubtraining/hellogitworld",
    }