from typing import KeysView, Generator

SERVICES_FOR_GROUP = {
    "all": "chialite_harvester chialite_timelord_launcher chialite_timelord chialite_farmer chialite_full_node chialite_wallet".split(),
    "node": "chialite_full_node".split(),
    "harvester": "chialite_harvester".split(),
    "farmer": "chialite_harvester chialite_farmer chialite_full_node chialite_wallet".split(),
    "farmer-no-wallet": "chialite_harvester chialite_farmer chialite_full_node".split(),
    "farmer-only": "chialite_farmer".split(),
    "timelord": "chialite_timelord_launcher chialite_timelord chialite_full_node".split(),
    "timelord-only": "chialite_timelord".split(),
    "timelord-launcher-only": "chialite_timelord_launcher".split(),
    "wallet": "chialite_wallet chialite_full_node".split(),
    "wallet-only": "chialite_wallet".split(),
    "introducer": "chialite_introducer".split(),
    "simulator": "chialite_full_node_simulator".split(),
}


def all_groups() -> KeysView[str]:
    return SERVICES_FOR_GROUP.keys()


def services_for_groups(groups) -> Generator[str, None, None]:
    for group in groups:
        for service in SERVICES_FOR_GROUP[group]:
            yield service


def validate_service(service: str) -> bool:
    return any(service in _ for _ in SERVICES_FOR_GROUP.values())
