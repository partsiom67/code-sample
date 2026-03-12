from abc import ABC, abstractmethod

from app.domains.subscription import Subscription


class SubscriptionRepository(ABC):
    @abstractmethod
    async def get_user_subscriptions(self, user_id: str) -> list[Subscription]:
        pass

    @abstractmethod
    async def get_subscription_by_id(
        self, subscription_id: str, user_id: str
    ) -> Subscription:
        pass

    @abstractmethod
    async def create_subscription(
        self, subscription: Subscription, user_id: str
    ) -> Subscription:
        pass

    @abstractmethod
    async def update_subscription(
    self, subscription_update: Subscription, subscription_id: str, user_id: str
) -> Subscription:
        pass
    
    @abstractmethod
    async def delete_subscription(self, subscription_id: str, user_id: str):
        pass
