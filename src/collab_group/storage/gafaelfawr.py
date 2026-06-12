"""Gafaelfawr storage driver for collab-group."""

from urllib.parse import urljoin

from httpx import AsyncClient
from rubin.repertoire import DiscoveryClient
from structlog.stdlib import BoundLogger

from ..models.domain.group import Group

__all__ = ["GafaelfawrStorage"]


class GafaelfawrStorage:
    "Gafaelfawr storage driver for collab-group."

    def __init__(
        self, token: str, exclude_groups: list[str], logger: BoundLogger
    ) -> None:
        self._logger = logger
        self._token = token
        self._exclude_groups = exclude_groups
        self._disco_client = DiscoveryClient()  # uses REPERTOIRE_BASE_URL
        self._g_api: str | None = None
        self._http_client: AsyncClient | None = None

    async def get_groups(self) -> list[Group]:
        """Get list of groups to check for directory existence/permissions.

        Returns
        -------
            list of groups to check
        """
        await self._ensure_gafaelfawr_client()
        if self._http_client is None:
            raise RuntimeError("Failed to acquire HTTP client")
        all_groups = (await self._http_client.get("groups")).json()
        user_groups = all_groups.get("user", [])
        check_groups: list[Group] = []
        for gr in user_groups:
            if gr["name"] not in self._exclude_groups:
                self._logger.info(f"Checking group {gr['name']}")
                check_groups.append(Group(name=gr["name"], gid=gr["id"]))
            else:
                self._logger.info(f"Skipping group {gr['name']}")
        return check_groups

    async def _ensure_gafaelfawr_client(self) -> None:
        if self._http_client:
            return
        if not self._g_api:
            self._logger.info("Creating URL for Gafaelfawr API")
            g_url = await self._disco_client.url_for_internal("gafaelfawr")
            if g_url is None:
                raise RuntimeError("Failed to get URL for Gafaelfawr service")
            self._g_api = urljoin(
                g_url,
                "/api/v1",
            )
        self._logger.info("Creating HTTP client for Gafaelfawr")
        self._http_client = AsyncClient(
            base_url=self._g_api,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._token}",
            },
        )
