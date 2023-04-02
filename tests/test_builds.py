import json
from pathlib import Path

from pytest import fixture, mark

from apiclient import ErrorResponse, SuccessResponse
from ninjaclient import BuildsApi, NinjaConfig
from ninjaclient.models import *

WEEK13_HAVOC_JSON = "tests/week13_havoc.json"
WEEK13_EXP_LADDER_JSON = "tests/week13_exp_ladder.json"


@fixture()
def api():
    return BuildsApi(
        NinjaConfig(league="sanctum", language="en", use_vcr=True, raise_errors=True)
    )


@fixture(scope="module")
def week13_havoc() -> CharacterResponse:
    with Path(WEEK13_HAVOC_JSON).resolve().open() as f:
        return json.load(f)


@fixture(scope="module")
def week13_exp_ladder() -> BuildsResponse:
    with Path(WEEK13_EXP_LADDER_JSON).resolve().open() as f:
        return json.load(f)


@mark.asyncio
async def test_get_week13_havoc(api: BuildsApi, week13_havoc):
    account = "Havoc6"
    name = "Havoc_FocusAtlasWhen"
    tm = "week-13"
    res = await api.get_character(account=account, name=name, tm=tm)
    assert isinstance(res, SuccessResponse)
    assert res.data == week13_havoc


@mark.asyncio
async def test_get_week13_exp_ladder(api: BuildsApi, week13_exp_ladder):
    tm = "week-13"
    res = await api.get_experience_ladder(tm)
    assert isinstance(res, SuccessResponse)
    assert res.data == week13_exp_ladder
