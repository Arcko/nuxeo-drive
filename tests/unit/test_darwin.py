# coding: utf-8
from pathlib import Path

from nxdrive.osi import AbstractOSIntegration

from ..markers import mac_only


def is_folder_registered(osi: AbstractOSIntegration, name: str) -> bool:
    lst = osi._get_favorite_list()
    return osi._find_item_in_list(lst, name) is not None


@mac_only
def test_folder_registration():
    path = Path("TestCazz")

    # Unregister first; to ensure favorite bar is cleaned.
    osi = AbstractOSIntegration.get(None)
    osi.unregister_folder_link(path)
    assert not is_folder_registered(osi, path.name)

    osi.register_folder_link(path)
    assert is_folder_registered(osi, path.name)

    osi.unregister_folder_link(path)
    assert not is_folder_registered(osi, path.name)