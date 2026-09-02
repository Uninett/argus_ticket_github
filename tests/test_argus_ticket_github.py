from unittest.mock import Mock

from argus.incident.ticket.base import TicketPluginException
from django.test import SimpleTestCase, override_settings

from argus_ticket_github import GithubPlugin


class GithubTicketPluginTests(SimpleTestCase):
    @override_settings(
        TICKET_ENDPOINT="https://example.com/",
        TICKET_AUTHENTICATION_SECRET={"key": "value"},
        TICKET_INFORMATION={"project_namespace_and_name": "namespace/name"},
    )
    def test_import_settings_raises_error_when_token_is_missing_from_ticket_authentication_secret(
        self,
    ):
        github_plugin = GithubPlugin()

        with self.assertRaises(TicketPluginException):
            github_plugin.import_settings()

    @override_settings(
        TICKET_ENDPOINT="https://example.com/",
        TICKET_AUTHENTICATION_SECRET={"token": "value"},
        TICKET_INFORMATION={"key": "value"},
    )
    def test_import_settings_raises_error_when_project_namespace_and_name_is_missing_from_ticket_information(
        self,
    ):
        github_plugin = GithubPlugin()

        with self.assertRaises(TicketPluginException):
            github_plugin.import_settings()


class GetTicketIdentifierTests(SimpleTestCase):
    def test_get_ticket_identifier_returns_ticket_id_for_valid_url(
        self,
    ):
        ticket_url = "https://github.com/Uninett/argus_ticket_github/issues/1"
        github_plugin = GithubPlugin()
        incident = Mock(ticket_url=ticket_url)

        ticket_identifier = github_plugin.get_ticket_identifier(incident=incident)
        self.assertEqual(ticket_identifier, "1")

    def test_get_ticket_identifier_returns_ticket_url_for_url_not_following_format(
        self,
    ):
        ticket_url = "https://example.com/1"
        github_plugin = GithubPlugin()
        incident = Mock(ticket_url=ticket_url)

        ticket_identifier = github_plugin.get_ticket_identifier(incident=incident)
        self.assertEqual(ticket_identifier, ticket_url)
