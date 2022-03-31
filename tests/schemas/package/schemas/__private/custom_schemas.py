from typing import Any, Dict

from schemas.predefined import *
from schemas.__private.fundamental_schemas import Schema


class AssetHbd(Schema):
    def __init__(self, **options: Any):
        super().__init__(options)

    def _create_schema(self) -> Dict[str, Any]:
        return Map({
            'amount': String()._create_schema(),
            'precision': Int(enum=[3])._create_schema(),
            'nai': String(pattern='@@000000013')._create_schema(),
        })._create_schema()


class AssetHive(Schema):
    def __init__(self, **options: Any):
        super().__init__(options)

    def _create_schema(self) -> Dict[str, Any]:
        return Map({
            'amount': String()._create_schema(),
            'precision': Int(enum=[3])._create_schema(),
            'nai': String(pattern='@@000000021')._create_schema(),
        })._create_schema()


class AssetVests(Schema):
    def __init__(self, **options: Any):
        super().__init__(options)

    def _create_schema(self) -> Dict[str, Any]:
        return Map({
            'amount': String()._create_schema(),
            'precision': Int(enum=[6])._create_schema(),
            'nai': String(pattern='@@000000037')._create_schema(),
        })._create_schema()


class Authority(Schema):
    def __init__(self, **options: Any):
        super().__init__(options)

    def _create_schema(self) -> Dict[str, Any]:
        return Map({
            'weight_threshold': Int()._create_schema(),
            'account_auths': Array(
                ArrayStrict(
                    String(),
                    Int()._create_schema(),
                )._create_schema()
            )._create_schema(),
            'key_auths': Array(
                ArrayStrict(
                    Key(),
                    Int()._create_schema(),
                )
            )._create_schema(),
        })._create_schema()


class Key(Schema):
    def __init__(self, **options: Any):
        super().__init__(options)

    def _create_schema(self) -> Dict[str, Any]:
        return String(pattern=r'^(?:STM|TST)[A-Za-z0-9]{50}$')._create_schema()


class Manabar(Schema):
    def __init__(self, **options: Any):
        super().__init__(options)

    def _create_schema(self) -> Dict[str, Any]:
        return Map({
            "current_mana": Int()._create_schema(),
            "last_update_time": Int()._create_schema(),
        })._create_schema()


class Proposal(Schema):
    def __init__(self, **options: Any):
        super().__init__(options)

    def _create_schema(self) -> Dict[str, Any]:
        return Map({
            'id': Int()._create_schema(),
            'proposal_id': Int()._create_schema(),
            'creator': String()._create_schema(),
            'receiver': String()._create_schema(),
            'start_date': Date()._create_schema(),
            'end_date': Date()._create_schema(),
            'daily_pay': AssetHbd(),
            'subject': String()._create_schema(),
            'permlink': String()._create_schema(),
            'total_votes': Int()._create_schema(),
            'status': String()._create_schema(),
        })._create_schema()


class Version(Schema):
    def __init__(self, **options: Any):
        super().__init__(options)

    def _create_schema(self) -> Dict[str, Any]:
        return String(pattern=r'^(\d+\.)?(\d+\.)?(\*|\d+)$')._create_schema()
