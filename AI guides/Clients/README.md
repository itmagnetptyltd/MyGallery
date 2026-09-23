# Clients

One folder per client, named for the client, such as `acme/`. It holds the client profile, `acme.json`, beside the client's own style guide, Word template and logo.

`client_profile.py list "AI guides/Clients"` finds `acme/acme.json`. A logo or template path in the profile is read from the profile's own folder.

A client spans products, so this folder sits beside them rather than inside one.

A profile never lives in the skill, because the skill is reinstalled and shared.
