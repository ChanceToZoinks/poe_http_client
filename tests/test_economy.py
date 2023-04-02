from typing import Type

from pytest import fixture, mark

from apiclient import ErrorResponse, SuccessResponse
from ninjaclient import EconomyApi, NinjaConfig
from ninjaclient.models import *

from . import has_all_keys


@fixture()
def api():
    return EconomyApi(
        NinjaConfig(league="sanctum", language="en", use_vcr=True, raise_errors=True)
    )


def check_res(res: SuccessResponse | ErrorResponse, res_type: Type):
    assert isinstance(res, SuccessResponse)
    assert has_all_keys(res.data, list(res_type.__required_keys__))


def check_currency(res: SuccessResponse | ErrorResponse):
    check_res(res, CurrencyResponse)


def check_item(res: SuccessResponse | ErrorResponse):
    check_res(res, ItemResponse)


def build_test(func_name, checker=check_item):
    @mark.asyncio
    async def inner(api):
        func = getattr(api, func_name)
        checker(await func())

    return inner


test_get_currency = build_test("get_currency", checker=check_currency)
test_get_fragments = build_test("get_fragments", checker=check_currency)
test_get_div_cards = build_test("get_divination_cards")
test_get_artifacts = build_test("get_artifacts")
test_get_oils = build_test("get_oils")
test_get_incubators = build_test("get_incubators")
test_get_u_weaps = build_test("get_unique_weapons")
test_get_u_armours = build_test("get_unique_armours")
test_get_u_access = build_test("get_unique_accessories")
test_get_u_flasks = build_test("get_unique_flasks")
test_get_u_jewels = build_test("get_unique_jewels")
test_get_skills = build_test("get_skill_gems")
test_get_cluster_jewels = build_test("get_cluster_jewels")
test_get_maps = build_test("get_maps")
test_get_b_maps = build_test("get_blighted_maps")
test_get_br_maps = build_test("get_blight_ravaged_maps")
test_get_s_maps = build_test("get_scourged_maps")
test_get_u_maps = build_test("get_unique_maps")
test_get_d_orbs = build_test("get_delirium_orbs")
test_get_invites = build_test("get_invitations")
test_get_scarabs = build_test("get_scarabs")
test_get_bases = build_test("get_base_types")
test_get_fossils = build_test("get_fossils")
test_get_res = build_test("get_resonators")
test_get_enchs = build_test("get_helmet_enchants")
test_get_beasts = build_test("get_beasts")
test_get_ess = build_test("get_essences")
test_get_vials = build_test("get_vials")
