<a href="#readme"><img src="https://tanker.io/images/github-logo.png" alt="Tanker logo" width="175" /></a>

[![Actions status](https://github.com/TankerHQ/identity-python/workflows/tests/badge.svg)](https://github.com/TankerHQ/identity-python/actions)
[![PyPi package](https://img.shields.io/pypi/v/tankersdk-identity.svg)](https://pypi.org/project/tankersdk-identity)
[![Coverage](https://img.shields.io/codecov/c/github/TankerHQ/identity-python.svg?label=Coverage)](https://codecov.io/gh/TankerHQ/identity-python)
[![Deps scanning](https://img.shields.io/badge/deps%20scanning-pyup.io-brightgreen)](https://github.com/TankerHQ/identity-python/actions/workflows/safety.yml)

# Identity SDK

Tanker identity generation in Python for the [Tanker SDK](https://docs.tanker.io/latest/).

## Installation

With `pip`:

```sh
$ pip install tankersdk-identity
```

## API

```python
tankersdk_identity.create_identity(app_id, app_secret, user_id)
```

Create a new Tanker identity. This identity is secret and must only be given to a user who has been authenticated by your application. This identity is used by the Tanker client SDK to open a Tanker session

**app_id**<br>
The app ID, must match the one used in the constructor of the Core SDK.

**app_secret**<br>
The app secret, secret that you have saved right after the creation of your app.

**user_id**<br>
The ID of a user in your application.
<br><br>

```python
tankersdk_identity.create_provisional_identity(app_id, "email", email)
```

Create a Tanker provisional identity. It allows you to share a resource with a user who does not have an account in your application yet.

**app_id**<br>
The app ID, must match the one used in the constructor of the Core SDK.

**email**<br>
The email of the potential recipient of the resource.
<br><br>

```python
tankersdk_identity.get_public_identity(identity)
```

Return the public identity from an identity. This public identity can be used by the Tanker client SDK to share encrypted resource.

**identity**<br>
A secret identity.
<br><br>

## Going further

Read more about identities in the [Tanker guide](https://docs.tanker.io/latest/guides/identity-management/).

Check the [examples](https://github.com/TankerHQ/identity-python/tree/master/examples) folder for usage examples.
