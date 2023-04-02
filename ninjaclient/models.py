from typing import Generic, Literal, TypedDict, TypeVar


class SparkLine(TypedDict):
    """Seems to contains 6 data points at most to render the trend line."""

    data: list[float]
    totalChange: float


class Language(TypedDict):
    name: str
    translations: object


class NamedObject(TypedDict):
    name: str


class CurrencyLineTransaction(TypedDict):
    """For showing how much you get for selling or spend when buying. Value in chaos orbs."""

    id: int
    league_id: int
    pay_currency_id: int
    get_currency_id: int
    sample_time_utc: str
    count: int
    value: float
    data_point_count: int
    includes_secondary: bool
    listing_count: int


class CurrencyLine(TypedDict):
    currencyTypeName: str
    pay: CurrencyLineTransaction
    receive: CurrencyLineTransaction
    paySparkLine: SparkLine
    receiveSparkLine: SparkLine
    chaosEquivalent: float
    lowConfidencePaySparkLine: SparkLine
    lowConfidenceReceiveSparkLine: SparkLine
    detailsId: str


class CurrencyDetail(TypedDict):
    id: int
    icon: str
    name: str
    tradeId: str


class CurrencyResponse(TypedDict):
    lines: list[CurrencyLine]
    currencyDetails: list[CurrencyDetail]
    language: Language


class ItemModifier(TypedDict):
    text: str
    optional: bool


class ItemLine(TypedDict):
    id: int
    name: str
    icon: str
    stackSize: int
    artFilename: str
    itemClass: int
    sparkline: SparkLine
    lowConfidenceSparkLine: SparkLine
    implicitModifiers: list[ItemModifier]
    explicitModifiers: list[ItemModifier]
    flavourText: str
    chaosValue: float
    exaltedValue: float
    divineValue: float
    count: int
    detailsId: str
    listingCount: int


class ItemResponse(TypedDict):
    lines: list[ItemLine]
    language: Language


class DefensiveStat(TypedDict):
    strength: int
    dexterity: int
    intelligence: int
    enduranceCharges: int
    frenzyCharges: int
    powerCharges: int
    itemSetType: int
    weaponConfigurationType: int
    life: int
    energyShield: int
    mana: int
    evasionRating: int
    armour: int


class ItemDataProperty(TypedDict):
    name: str
    values: list[list[str]]
    displayMode: int


class ItemDataHybrid(TypedDict):
    baseTypeName: str
    isVaalGem: bool
    secDescrText: str


class ItemData(TypedDict):
    id: str
    identified: bool
    corrupted: bool
    fractured: bool
    synthesized: bool
    name: str
    ilvl: int
    icon: str
    w: int
    h: int
    x: int
    y: int
    typeLine: str
    baseType: str
    explicitMods: list[str]
    properties: list[ItemDataProperty]
    requirements: list[ItemDataProperty]
    league: str
    descrText: str
    frameType: int
    replica: bool


class HybridItemData(ItemData):
    hybrid: ItemDataHybrid


class SocketedItemData(ItemData):
    socket: int
    colour: Literal["G", "I", "S", "D"]


class Socket(TypedDict):
    group: int
    attr: Literal["D", "S", "I", "G"]  # Dex = Green, Str = Red, Int = Blue, G = White
    sColour: Literal["G", "R", "B", "W"]


class EquippableItemData(ItemData):
    inventoryId: str
    implicitMods: list[str]
    craftedMods: list[str]
    enchantMods: list[str]
    sockets: list[Socket]
    socketedItems: list[SocketedItemData]
    league: str
    frameType: int
    replica: bool


AnyItemData = ItemData | HybridItemData | SocketedItemData | EquippableItemData


_TItemData = TypeVar("_TItemData", ItemData, HybridItemData)


class Gem(TypedDict):
    name: str
    level: int
    quality: int


class GemItem(Gem, Generic[_TItemData]):  # requires python >= 3.11 for this to work
    itemData: _TItemData


class SkillDps(TypedDict):
    name: str
    dps: float
    dotDps: float
    # [phys, lightning, cold, fire, chaos] as percentages e.g. [0, 0, 100, 0, 0]
    damageTypes: list[int]
    dotDamageTypes: list[int]
    # [dps, phys, lightning, cold, fire, chaos, ?]
    damage: list[int]


SkillGem = GemItem[HybridItemData]
SupportGem = GemItem[ItemData]


class Skill(TypedDict):
    gem: SkillGem
    supportGems: list[SupportGem]
    itemSlot: int
    allGems: list[GemItem[AnyItemData]]
    dps: list[SkillDps]


class CharacterItem(TypedDict):
    itemData: EquippableItemData
    itemSlot: int
    itemClass: int


class Keystone(TypedDict):
    name: str
    icon: str
    stats: list[str]


class ItemProvidedGem(TypedDict):
    slot: int
    gems: list[Gem]


class Mastery(TypedDict):
    name: str


# 'class' is a reserved word so this has to be created like this
CharacterResponse = TypedDict(
    "CharacterResponse",
    {
        "account": str,
        "name": str,
        "league": str,
        "defensiveStats": DefensiveStat,
        "skills": list[Skill],
        "level": int,
        "class": str,
        "pathOfBuildingExport": str,
        "items": list[CharacterItem],
        "passiveTreeUrl": str,
        "keyStones": list[Keystone],
        "flasks": list[CharacterItem],
        "jewels": list[CharacterItem],
        "passiveSelection": list[int],
        "lastSeenUtc": str,
        "updatedUtc": str,
        "lastCheckedUtc": str,
        "status": int,
        "language": Language,
        "itemProvidedGems": list[ItemProvidedGem],
        "masteries": list[Mastery],
        "baseClass": int,
        "ascendancyClass": int,
    },
)


class BuildsUniqueItem(TypedDict):
    name: str
    type: str


class BuildsAllSkills(TypedDict):
    name: str
    icon: str


class BuildsActiveSkill(BuildsAllSkills):
    dpsName: str


class BuildsPassiveNode(TypedDict):
    name: str
    icon: str
    isKeystone: bool
    type: str


class SkillDetailSupportGems(TypedDict):
    names: list[NamedObject]
    # keys cast to int and index names
    # the first entry of the list is a user id and all subsequent are deltas. see BuildsResponse.uniqueItemsUse for more
    use: dict[str, list[int]]
    # reverse dict of names. find a support gem's position in names via this dict
    dictionary: dict[str, int]


class BuildsSkillDetail(TypedDict):
    name: str
    supportGems: SkillDetailSupportGems
    # keys are user id and values follow this format [dps, phys, lightning, cold, fire, chaos, ?] where phys, light, ... chaos are whole numbers representing percentages e.g. 75
    dps: dict[str, list[int]]


class BuildsResponse(TypedDict):
    # list of ascendancies/base class names
    classNames: list[str]
    # the position of the entry in this list corresponds to the character on the ladder in that same position. the entry in the list indexes 'classNames'
    classes: list[int]
    uniqueItems: list[BuildsUniqueItem]
    # the keys of the dict are '0', '1', '2', ... and when cast to int correspond to items in 'uniqueItems'
    # the first entry of the inner list is a user's id which can be used to lookup in 'names'
    # all subsequent elements in that list are deltas from the value of the previous entry in the list
    # e.g. if I have BuildsResponse['uniqueItemUse']['0'] = [0, 1, 5, 22, 100] then the user ids of the people using unique '0' are [0, 0+1, 0+1+5, 0+1+5+22, 0+1+5+22+100] = [0, 1, 6, 28, 128]
    # see this thread for more discussion: https://www.reddit.com/r/pathofexiledev/comments/u60oxv/iterating_over_poeninja_builds_to_gather_uniques/i6qyd23/
    uniqueItemUse: dict[str, list[int]]
    activeSkills: list[BuildsActiveSkill]
    # the discussion above regarding unique items applies to this as well
    activeSkillUse: dict[str, list[int]]
    allSkills: list[BuildsAllSkills]
    # the discussion above regarding unique items applies to this as well
    allSkillUse: dict[str, list[int]]
    keystones: list[BuildsPassiveNode]
    # the discussion above regarding unique items applies to this as well
    keystoneUse: dict[str, list[int]]
    # index corresponds to user id, value used to lookup in 'fetchModes'
    fetchModeUse: list[int]
    fetchModes: list[NamedObject]
    # index corresponds to user id
    levels: list[int]
    # index corresponds to user id
    life: list[int]
    # index corresponds to user id
    energyShield: list[int]
    # index corresponds to user id, value used to lookup in 'weaponConfigurationTypes'
    weaponConfigurationTypeUse: list[int]
    weaponConfigurationTypes: list[NamedObject]
    # the index of this list is "user id"
    names: list[str]
    # the index of this list is "user id"
    accounts: list[str]
    # the index of this list is "user id" and the value corresponds to their ladder position
    ladderRanks: list[int]
    updatedUtc: str
    skillModes: list[NamedObject]
    # the index of this list is "user id"
    skillModeUse: dict[str, list[int]]
    # find a player's dps with a skill using this also their ranking
    skillDetails: list[BuildsSkillDetail]
    # index is user id
    delveSolo: list[int]
    language: Language
    intervals: list[object]
    intervalNames: list[str]
    leagues: list[str]
    leagueNames: list[str]
    twitchAccounts: list[str]
    twitchNames: list[str]
    online: list[str]
    uniqueItemTooltips: list[bool]
    keystoneTooltips: list[bool]
    masteries: list[NamedObject]
    # the discussion above regarding unique items applies to this as well
    masteryUse: dict[str, list[int]]
