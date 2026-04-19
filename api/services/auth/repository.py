from datetime import UTC, datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database.models import RefreshToken


class RefreshTokenRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(
        self,
        user_id: int,
        token_hash: str,
        expires_at: datetime,
        user_agent: str | None = None,
    ) -> RefreshToken:
        token = RefreshToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
            user_agent=user_agent,
        )
        self._session.add(token)
        await self._session.flush()
        return token

    async def find_by_hash(self, token_hash: str) -> RefreshToken | None:
        query = select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        if self._session.bind is not None and self._session.bind.dialect.name == "postgresql":
            query = query.with_for_update()
        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def revoke(self, token: RefreshToken, replaced_by: str | None = None) -> None:
        token.revoked_at = datetime.now(UTC)
        if replaced_by is not None:
            token.replaced_by = replaced_by
        await self._session.flush()

    async def revoke_all_for_user(self, user_id: int) -> None:
        await self._session.execute(
            update(RefreshToken)
            .where(RefreshToken.user_id == user_id)
            .where(RefreshToken.revoked_at.is_(None))
            .values(revoked_at=datetime.now(UTC))
        )
        await self._session.flush()
