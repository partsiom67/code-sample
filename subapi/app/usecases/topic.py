from app.domains.topic import Topic
from app.ports.repositories.topic_repository import TopicRepository


class TopicActionsUsecase:
    def __init__(self, topic_repository: TopicRepository) -> None:
        self.topic_repository = topic_repository

    async def get_topics(self) -> list[Topic]:
        return await self.topic_repository.get_topics()

    async def get_topic_by_id(self, topic_id: str) -> Topic:
        return await self.topic_repository.get_topic_by_id(topic_id)

    async def get_topic_by_name(self, topic_name: str) -> Topic:
        return await self.topic_repository.get_topic_by_name(topic_name)

    async def create_topic(self, topic: Topic) -> Topic:
        return await self.topic_repository.create_topic(topic)

    async def delete_topic(self, topic_id: str):
        return await self.topic_repository.delete_topic(topic_id)
