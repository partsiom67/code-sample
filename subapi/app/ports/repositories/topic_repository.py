from abc import ABC, abstractmethod

from app.domains.topic import Topic


class TopicRepository(ABC):
    @abstractmethod
    async def get_topics(self) -> list[Topic]:
        pass

    @abstractmethod
    async def get_topic_by_id(self, topic_id: str) -> Topic:
        pass

    @abstractmethod
    async def get_topic_by_name(self, topic_name: str) -> Topic:
        pass

    @abstractmethod
    async def create_topic(self, topic: Topic) -> Topic:
        pass

    @abstractmethod
    async def delete_topic(self, topic_name: str):
        pass
