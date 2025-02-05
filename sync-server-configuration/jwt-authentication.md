---
description: How to use JSON Web Tokens (JWT) for ObjectBox Sync Authentication
---

# JWT Authentication

[JSON Web Tokens (JWT)](https://en.wikipedia.org/wiki/JSON_Web_Token) are a very common method of handling authentication. Many authentication providers support JWT out of the box. Examples include Auth0, Firebase, Clerk, and KeyCloak (an open-source solution that can be self-hosted). For this guide, we assume that you already set up JWT authentication. Since this is a process specific to the provider, please refer to the provider's documentation if you need help.

## Obtaining and Passing the JWT in the Sync Client

After setting up your JWT-based authentication service, you will obtain JWTs on the client side using the provider’s SDK. This process occurs outside of ObjectBox. Once you have the JWT, it will look like a cryptic string. Your client application must then pass this JWT to the ObjectBox SDK as a login credential, using one of the supported JWT types. For specific implementation details, refer to the [ObjectBox Sync client documentation](../sync-client.md).

## Configuring JWT on the ObjectBox Sync Server

The Sync server verifies JWTs sent by the Sync client. It primarily checks three things:

1. The [**audience** claim](https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3) (often called `aud`).
2. The [**issuer** claim](https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.1) (`iss`).
3. The **cryptographic signature**.

The audience and issuer claims are initially configured with your authentication provider. You must use the same claim values in your ObjectBox Sync Server configuration.

For signature verification, the Sync Server requires the public key from the authentication provider. This key is often provided via a URL, allowing for automatic rotation (i.e., the key may change over time). The Sync Server uses this public key to verify the signature that was created using the private key at the authentication provider.

### File based JWT configuration

The JWT configuration is part of the standard JSON configuration file used for the Sync server. All the JWT settings are done within the `auth.jwt` JSON element. Take a look at the  following example:

```json
{
  "auth": {
    "jwt": {
      "publicKeyUrl": "https://example.com/public-key",
      "claimAud": "myAUD",
      "claimIss": "myISS"
    }
  }
}
```

It uses the following configuration fields:

* **publicKeyUrl:** The URL where the Sync Server can retrieve the public key(s) from your authentication provider. Public key rotation is automatically handled by pointing to this URL, ensuring that the Sync Server always uses the correct key for signature verification. The URL must
point to a valid [JWKS](https://datatracker.ietf.org/doc/html/rfc7517) (JSON Web Key Set) resource that contains the public keys.
* **claimAud:** Must match the `aud` (audience) value that your authentication provider includes in its issued JWTs. This is used to ensure the token is intended for the correct recipient.
* **claimIss:** Must match the `iss` (issuer) value used by your authentication provider. This ensures the token is issued by a trusted source.

### CLI based JWT configuration

Starting the Sync Server with a JWT configuration using command line arguments looks like this:

`sync-server --jwt-public-key-url https://example.com/public-key --jwt-claim-aud myAUD --jwt-claim-iss myISS`

The configuration parameters match their counterparts in the JSON file, so you can refer there for details.
