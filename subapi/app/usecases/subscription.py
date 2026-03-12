from app.domains.subscription import Subscription
from app.ports.repositories.subscription_repository import SubscriptionRepository


class SubscriptionActionsUsecase:
    def __init__(self, subscription_repository: SubscriptionRepository) -> None:
        self.subscription_repository = subscription_repository

    async def get_user_subscriptions(self, user_id: str) -> list[Subscription]:
        return await self.subscription_repository.get_user_subscriptions(user_id)

    async def get_subscription_by_id(
        self, subscription_id: str, user_id: str
    ) -> Subscription:
        return await self.subscription_repository.get_subscription_by_id(
            subscription_id, user_id
        )

    async def create_subscription(
        self, subscription: Subscription, user_id: str
    ) -> Subscription:
        return await self.subscription_repository.create_subscription(
            subscription, user_id
        )

    async def update_subscription(
        self, subscription_update: dict, subscription_id: str, user_id: str
    ) -> Subscription:
        return await self.subscription_repository.update_subscription(
            subscription_update, subscription_id, user_id
        )

    async def delete_subscription(self, subscription_id: str, user_id: str):
        return await self.subscription_repository.delete_subscription(
            subscription_id, user_id
        )
