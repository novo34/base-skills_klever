from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from channels.runtime import ChannelMessage


@dataclass(frozen=True)
class ChannelAuthenticationResult:
    verified: bool
    identity_verified: bool
    method: str
    external_actor_id: str | None = None


class ChannelAdapter(ABC):
    @abstractmethod
    def authenticate(
        self,
        *,
        payload: dict,
        headers: dict[str, str],
    ) -> ChannelAuthenticationResult:
        """Verify provider webhook/session authenticity before message normalization."""
        raise NotImplementedError

    @abstractmethod
    def receive(
        self,
        payload: dict,
        *,
        authentication: ChannelAuthenticationResult,
    ) -> ChannelMessage:
        """Build a ChannelMessage only from previously verified authentication evidence."""
        raise NotImplementedError

    @abstractmethod
    def send_reply(
        self,
        *,
        channel_message_id: str,
        text: str,
        action_url: str | None = None,
    ) -> dict:
        raise NotImplementedError
