from __future__ import annotations

from abc import ABC, abstractmethod

from channels.runtime import ChannelMessage


class ChannelAdapter(ABC):
    @abstractmethod
    def receive(self, payload: dict) -> ChannelMessage:
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
