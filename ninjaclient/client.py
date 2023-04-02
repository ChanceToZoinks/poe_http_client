from dataclasses import asdict, dataclass
from typing import Literal

from apiclient import Client, ClientConfig

from .models import *


@dataclass
class NinjaConfig(ClientConfig):
    base_url: str = "https://poe.ninja/api/data"
    league: str = "Sanctum"
    language: str = "en"
    verbose: bool = False
    timeout_seconds: int = 300


ApiPath = Literal[
    "/currencyoverview", "/itemoverview", "/0/getbuildoverview", "/0/getcharacter"
]


CurrencyOverviewType = Literal["Currency", "Fragment"]

ItemOverviewType = Literal[
    "DivinationCard",
    "Artifact",
    "Oil",
    "Incubator",
    "UniqueWeapon",
    "UniqueArmour",
    "UniqueAccessory",
    "UniqueFlask",
    "UniqueJewel",
    "SkillGem",
    "ClusterJewel",
    "Map",
    "BlightedMap",
    "BlightRavagedMap",
    "ScourgedMap",
    "UniqueMap",
    "DeliriumOrb",
    "Invitation",
    "Scarab",
    "BaseType",
    "Fossil",
    "Resonator",
    "HelmetEnchant",
    "Beast",
    "Essence",
    "Vial",
]

BuildAndCharOverviewType = Literal["exp", "depthsolo"]

EconomyRequestType = CurrencyOverviewType | ItemOverviewType

TimeMachineType = Literal[
    "",
    "day-1",
    "day-2",
    "day-3",
    "day-4",
    "day-5",
    "day-6",
    "week-1",
    "week-2",
    "week-3",
    "week-4",
    "week-5",
    "week-6",
    "week-7",
    "week-8",
    "week-9",
    "week-10",
    "week-11",
    "week-12",
    "week-13",
    "week-14",
    "week-15",
    "week-16",
]


@dataclass
class EconomyRequestParams:
    type: EconomyRequestType
    league: str
    language: str


@dataclass
class BuildsRequestParams:
    type: BuildAndCharOverviewType
    overview: str  # this is the league
    Language: str
    timemachine: TimeMachineType = ""


@dataclass
class CharacterRequestParams:
    account: str
    name: str
    type: BuildAndCharOverviewType
    overview: str  # this is the league
    Language: str
    timemachine: TimeMachineType = ""


class EconomyApi(Client[NinjaConfig]):
    def __init__(self, cfg: NinjaConfig = NinjaConfig()) -> None:
        super().__init__(cfg)

    def _build_get_currency_config(self, type: CurrencyOverviewType):
        return self.build_get_config(
            "/currencyoverview",
            CurrencyResponse,
            asdict(
                EconomyRequestParams(
                    type=type, league=self.config.league, language=self.config.language
                )
            ),
        )

    def _build_get_item_config(self, type: ItemOverviewType):
        return self.build_get_config(
            "/itemoverview",
            ItemResponse,
            asdict(
                EconomyRequestParams(
                    type=type, league=self.config.league, language=self.config.language
                )
            ),
        )

    async def get_currency(self):
        return await self.request(self._build_get_currency_config("Currency"))

    async def get_fragments(self):
        return await self.request(self._build_get_currency_config("Fragment"))

    async def get_divination_cards(self):
        return await self.request(self._build_get_item_config("DivinationCard"))

    async def get_artifacts(self):
        return await self.request(self._build_get_item_config("Artifact"))

    async def get_oils(self):
        return await self.request(self._build_get_item_config("Oil"))

    async def get_incubators(self):
        return await self.request(self._build_get_item_config("Incubator"))

    async def get_unique_weapons(self):
        return await self.request(self._build_get_item_config("UniqueWeapon"))

    async def get_unique_armours(self):
        return await self.request(self._build_get_item_config("UniqueArmour"))
    
    async def get_unique_accessories(self):
        return await self.request(self._build_get_item_config("UniqueAccessory"))

    async def get_unique_flasks(self):
        return await self.request(self._build_get_item_config("UniqueFlask"))

    async def get_unique_jewels(self):
        return await self.request(self._build_get_item_config("UniqueJewel"))

    async def get_skill_gems(self):
        return await self.request(self._build_get_item_config("SkillGem"))

    async def get_cluster_jewels(self):
        return await self.request(self._build_get_item_config("ClusterJewel"))

    async def get_maps(self):
        return await self.request(self._build_get_item_config("Map"))

    async def get_blighted_maps(self):
        return await self.request(self._build_get_item_config("BlightedMap"))

    async def get_blight_ravaged_maps(self):
        return await self.request(self._build_get_item_config("BlightRavagedMap"))

    async def get_scourged_maps(self):
        return await self.request(self._build_get_item_config("ScourgedMap"))

    async def get_unique_maps(self):
        return await self.request(self._build_get_item_config("UniqueMap"))

    async def get_delirium_orbs(self):
        return await self.request(self._build_get_item_config("DeliriumOrb"))

    async def get_invitations(self):
        return await self.request(self._build_get_item_config("Invitation"))

    async def get_scarabs(self):
        return await self.request(self._build_get_item_config("Scarab"))

    async def get_base_types(self):
        return await self.request(self._build_get_item_config("BaseType"))

    async def get_fossils(self):
        return await self.request(self._build_get_item_config("Fossil"))

    async def get_resonators(self):
        return await self.request(self._build_get_item_config("Resonator"))

    async def get_helmet_enchants(self):
        return await self.request(self._build_get_item_config("HelmetEnchant"))

    async def get_beasts(self):
        return await self.request(self._build_get_item_config("Beast"))

    async def get_essences(self):
        return await self.request(self._build_get_item_config("Essence"))

    async def get_vials(self):
        return await self.request(self._build_get_item_config("Vial"))


class BuildsApi(Client[NinjaConfig]):
    def __init__(self, cfg: NinjaConfig = NinjaConfig()) -> None:
        super().__init__(cfg)

    def _build_get_builds_config(
        self, type: BuildAndCharOverviewType, tm: TimeMachineType
    ):
        return self.build_get_config(
            "/0/getbuildoverview",
            BuildsResponse,
            asdict(
                BuildsRequestParams(
                    type=type,
                    timemachine=tm,
                    overview=self.config.league.lower(),
                    Language=self.config.language,
                )
            ),
        )

    def _build_get_character_config(
        self,
        account: str,
        name: str,
        tm: TimeMachineType,
    ):
        return self.build_get_config(
            "/0/getcharacter",
            CharacterResponse,
            asdict(
                CharacterRequestParams(
                    account=account,
                    name=name,
                    type="exp",  # doesnt matter if this is 'exp' or 'depthsolo'
                    timemachine=tm,
                    overview=self.config.league.lower(),
                    Language=self.config.language,
                )
            ),
        )

    async def get_experience_ladder(self, tm: TimeMachineType = ""):
        return await self.request(self._build_get_builds_config("exp", tm=tm))

    async def get_delve_ladder(self, tm: TimeMachineType = ""):
        return await self.request(self._build_get_builds_config("depthsolo", tm=tm))

    async def get_character(self, account: str, name: str, tm: TimeMachineType = ""):
        return await self.request(
            self._build_get_character_config(account=account, name=name, tm=tm)
        )
