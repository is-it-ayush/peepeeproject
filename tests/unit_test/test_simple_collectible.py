from lib2to3.pgen2.literals import simple_escapes
from scripts.simple_collectible.deploy import deploy
from scripts.simple_collectible.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from brownie import network
import pytest

def test_can_create_simple_collectible():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    simple_collectible = deploy()
    assert simple_collectible.ownerOf(0) == get_account()