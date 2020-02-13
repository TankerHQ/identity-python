import base64
import json

from tankersdk_identity import _hash_user_id, _deserialize_identity

TRUSTCHAIN = {
    "id": "tpoxyNzh0hU9G2i9agMvHyyd+pO6zGCjO9BfhrCLjd4=",
    "sk": "cTMoGGUKhwN47ypq4xAXAtVkNWeyUtMltQnYwJhxWYSvqjPVGmXd2wwa7y17QtPTZhn8bxb015CZC/e4ZI7+MQ==",
    "pk": "r6oz1Rpl3dsMGu8te0LT02YZ/G8W9NeQmQv3uGSO/jE=",
}
USER_ID = "b_eich"
USER_EMAIL = "brendan.eich@tanker.io"
HASHED_USER_ID = base64.b64encode(_hash_user_id(base64.b64decode(TRUSTCHAIN["id"]), USER_ID)).decode()
PERMANENT_IDENTITY = "eyJ0cnVzdGNoYWluX2lkIjoidHBveHlOemgwaFU5RzJpOWFnTXZIeXlkK3BPNnpHQ2pPOUJmaHJDTGpkND0iLCJ0YXJnZXQiOiJ1c2VyIiwidmFsdWUiOiJSRGEwZXE0WE51ajV0VjdoZGFwak94aG1oZVRoNFFCRE5weTRTdnk5WG9rPSIsImRlbGVnYXRpb25fc2lnbmF0dXJlIjoiVTlXUW9sQ3ZSeWpUOG9SMlBRbWQxV1hOQ2kwcW1MMTJoTnJ0R2FiWVJFV2lyeTUya1d4MUFnWXprTHhINmdwbzNNaUE5cisremhubW9ZZEVKMCtKQ3c9PSIsImVwaGVtZXJhbF9wdWJsaWNfc2lnbmF0dXJlX2tleSI6IlhoM2kweERUcHIzSFh0QjJRNTE3UUt2M2F6TnpYTExYTWRKRFRTSDRiZDQ9IiwiZXBoZW1lcmFsX3ByaXZhdGVfc2lnbmF0dXJlX2tleSI6ImpFRFQ0d1FDYzFERndvZFhOUEhGQ2xuZFRQbkZ1Rm1YaEJ0K2lzS1U0WnBlSGVMVEVOT212Y2RlMEhaRG5YdEFxL2RyTTNOY3N0Y3gwa05OSWZodDNnPT0iLCJ1c2VyX3NlY3JldCI6IjdGU2YvbjBlNzZRVDNzMERrdmV0UlZWSmhYWkdFak94ajVFV0FGZXh2akk9In0="
PROVISIONAL_IDENTITY = "eyJ0cnVzdGNoYWluX2lkIjoidHBveHlOemgwaFU5RzJpOWFnTXZIeXlkK3BPNnpHQ2pPOUJmaHJDTGpkND0iLCJ0YXJnZXQiOiJlbWFpbCIsInZhbHVlIjoiYnJlbmRhbi5laWNoQHRhbmtlci5pbyIsInB1YmxpY19lbmNyeXB0aW9uX2tleSI6Ii8yajRkSTNyOFBsdkNOM3VXNEhoQTV3QnRNS09jQUNkMzhLNk4wcSttRlU9IiwicHJpdmF0ZV9lbmNyeXB0aW9uX2tleSI6IjRRQjVUV212Y0JyZ2V5RERMaFVMSU5VNnRicUFPRVE4djlwakRrUGN5YkE9IiwicHVibGljX3NpZ25hdHVyZV9rZXkiOiJXN1FFUUJ1OUZYY1hJcE9ncTYydFB3Qml5RkFicFQxckFydUQwaC9OclRBPSIsInByaXZhdGVfc2lnbmF0dXJlX2tleSI6IlVtbll1dmRUYUxZRzBhK0phRHBZNm9qdzQvMkxsOHpzbXJhbVZDNGZ1cVJidEFSQUc3MFZkeGNpazZDcnJhMC9BR0xJVUJ1bFBXc0N1NFBTSDgydE1BPT0ifQ=="
PUBLIC_IDENTITY = "eyJ0YXJnZXQiOiJ1c2VyIiwidHJ1c3RjaGFpbl9pZCI6InRwb3h5TnpoMGhVOUcyaTlhZ012SHl5ZCtwTzZ6R0NqTzlCZmhyQ0xqZDQ9IiwidmFsdWUiOiJSRGEwZXE0WE51ajV0VjdoZGFwak94aG1oZVRoNFFCRE5weTRTdnk5WG9rPSJ9"


def test_parse_valid_permanent_identity():
    identity = _deserialize_identity(PERMANENT_IDENTITY)

    assert identity["trustchain_id"] == TRUSTCHAIN["id"]
    assert identity["target"] == "user"
    assert identity["value"] == HASHED_USER_ID
    assert identity["delegation_signature"] == "U9WQolCvRyjT8oR2PQmd1WXNCi0qmL12hNrtGabYREWiry52kWx1AgYzkLxH6gpo3MiA9r++zhnmoYdEJ0+JCw=="
    assert identity["ephemeral_public_signature_key"] == "Xh3i0xDTpr3HXtB2Q517QKv3azNzXLLXMdJDTSH4bd4="
    assert identity["ephemeral_private_signature_key"] == "jEDT4wQCc1DFwodXNPHFClndTPnFuFmXhBt+isKU4ZpeHeLTENOmvcde0HZDnXtAq/drM3Ncstcx0kNNIfht3g=="
    assert identity["user_secret"] == "7FSf/n0e76QT3s0DkvetRVVJhXZGEjOxj5EWAFexvjI="


def test_parse_valid_provisional_identity():
    identity = _deserialize_identity(PROVISIONAL_IDENTITY)

    assert identity["trustchain_id"] == TRUSTCHAIN["id"]
    assert identity["target"] == "email"
    assert identity["value"] == USER_EMAIL
    assert identity["public_signature_key"] == "W7QEQBu9FXcXIpOgq62tPwBiyFAbpT1rAruD0h/NrTA="
    assert identity["private_signature_key"] == "UmnYuvdTaLYG0a+JaDpY6ojw4/2Ll8zsmramVC4fuqRbtARAG70Vdxcik6Crra0/AGLIUBulPWsCu4PSH82tMA=="
    assert identity["public_encryption_key"] == "/2j4dI3r8PlvCN3uW4HhA5wBtMKOcACd38K6N0q+mFU="
    assert identity["private_encryption_key"] == "4QB5TWmvcBrgeyDDLhULINU6tbqAOEQ8v9pjDkPcybA="


def test_parse_valid_public_identity():
    identity = _deserialize_identity(PUBLIC_IDENTITY)

    assert identity["trustchain_id"] == TRUSTCHAIN["id"]
    assert identity["target"] == "user"
    assert identity["value"] == HASHED_USER_ID

