"Allow argus-server to create tickets in Github"

import logging
from urllib.parse import urljoin

from github import Github

from argus.incident.ticket.base import TicketPlugin, TicketPluginException

LOG = logging.getLogger(__name__)


__version__ = "0.1"
__all__ = [
    "GithubPlugin",
]


class GithubPlugin(TicketPlugin):
    @classmethod
    def import_settings(cls):
        try:
            endpoint, authentication, ticket_information = super().import_settings()
        except ValueError as e:
            LOG.exception("Could not import settings for ticket plugin.")
            raise TicketPluginException(f"Github: {e}")

        if "token" not in authentication.keys():
            LOG.error(
                "Github: No token can be found in the authentication information. Please update the setting 'TICKET_AUTHENTICATION_SECRET'."
            )
            raise TicketPluginException(
                "Github: No token can be found in the authentication information. Please update the setting 'TICKET_AUTHENTICATION_SECRET'."
            )

        if "project_namespace_and_name" not in ticket_information.keys():
            LOG.error(
                "Github: No project namespace and name can be found in the ticket information. Please update the setting 'TICKET_INFORMATION'."
            )
            raise TicketPluginException(
                "Github: No project namespace and name can be found in the ticket information. Please update the setting 'TICKET_INFORMATION'."
            )

        return endpoint, authentication, ticket_information

    @staticmethod
    def create_client(endpoint, authentication):
        """Creates and returns a Github client"""
        if endpoint == "https://github.com/" or endpoint == "https://github.com":
            base_url = base_url = "https://api.github.com"
        else:
            base_url = urljoin(endpoint, "api/v3")

        try:
            client = Github(base_url=base_url, login_or_token=authentication["token"])
        except Exception as e:
            LOG.exception("Github: Client could not be created.")
            raise TicketPluginException(f"Github: {e}")
        else:
            return client

    @classmethod
    def create_ticket(cls, serialized_incident: dict):
        """
        Creates a Github ticket with the incident as template and returns the
        ticket url
        """
        endpoint, authentication, ticket_information = cls.import_settings()

        client = cls.create_client(endpoint, authentication)

        try:
            repo = client.get_repo(ticket_information["project_namespace_and_name"])
            ticket = repo.create_issue(
                title=serialized_incident["description"], body=str(serialized_incident)
            )
        except Exception as e:
            LOG.exception("Github: Ticket could not be created.")
            raise TicketPluginException(f"Github: {e}")
        else:
            return ticket.html_url
