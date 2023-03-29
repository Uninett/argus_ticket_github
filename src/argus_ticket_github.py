"Allow argus-server to create tickets in Github"

import logging
from urllib.parse import urljoin
from typing import List

from markdownify import markdownify

from argus.incident.ticket.base import TicketPlugin, TicketPluginException

LOG = logging.getLogger(__name__)


__version__ = "1.0"
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
    def convert_tags_to_dict(tag_dict: dict) -> dict:
        incident_tags_list = [entry["tag"].split("=") for entry in tag_dict]
        return {key: value for key, value in incident_tags_list}

    @staticmethod
    def get_labels(
        ticket_information: dict, serialized_incident: dict
    ) -> tuple[dict, List[str]]:
        incident_tags = GithubPlugin.convert_tags_to_dict(serialized_incident["tags"])
        labels = ticket_information.get("labels_set", [])
        labels_mapping = ticket_information.get("labels_mapping", [])
        missing_fields = []

        for field in labels_mapping:
            if type(field) is dict:
                # Information can be found in tags
                label = incident_tags.get(field["tag"], None)
                if label:
                    labels.append(label)
                else:
                    missing_fields.append(field["tag"])
            else:
                label = serialized_incident.get(field, None)
                if label:
                    labels.append(label)
                else:
                    missing_fields.append(field)

        return labels, missing_fields

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
        except Exception as e:
            error = f"Github: {e}"
            LOG.exception(error)
            raise TicketPluginException(error)

        label_contents, missing_fields = cls.get_labels(
            ticket_information=ticket_information,
            serialized_incident=serialized_incident,
        )
        repo_labels = repo.get_labels()
        labels = [label for label in repo_labels if label.name in label_contents]

        html_body = cls.create_html_body(
            serialized_incident={
                "missing_fields": missing_fields,
                **serialized_incident,
            }
        )
        markdown_body = markdownify(html=html_body)

        try:
            ticket = repo.create_issue(
                title=serialized_incident["description"],
                body=markdown_body,
                labels=labels,
            )
        except Exception as e:
            LOG.exception("Github: Ticket could not be created.")
            raise TicketPluginException(f"Github: {e}")
        else:
            return ticket.html_url
