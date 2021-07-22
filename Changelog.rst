3.0.0
=====

Please read the `migration guide <https://docs.tanker.io/latest/release-notes/identity/python/guide/>`_ before upgrading to this version if you use the provisional identity feature.
Refer to the `compatibility table <https://docs.tanker.io/latest/guides/manage-sdk-versions/#identity_sdk_compatibility_table>`_
for more information on compatible Core SDK versions after this upgrade.

- API break: The createProvisionalIdentity function now takes an additional argument
- It is now possible to create provisional identities targeting phone numbers
- Introduce upgrade to new deterministic identity format
- Email addresses in public provisional identities will now be hashed

2.16.1
======

* First synced release between platforms

1.3.4
=====

* Add missing ``py.typed`` file in the package

1.3.3
=====

* Add type annotations
* Format code with ``black``

1.3.2
=====

* Publish readme on pypi.org

1.3.1
=====

* Drop Python2 support
* Drop Python 3.4 support
* Drop upgrade_user_token method

1.3.0
=====

* When generating an identity, we now check that the app secret and the app ID match.

1.2.1
=====

* Add Python 3.8 support
* Bump internal dependencies

1.2
===

* Remove the concept of trustchain, use app instead
* Bump internal dependencies

1.1
===

* Update to the new identity format
* Bug fix in the user token upgrade

1.0
===

* Initial release
