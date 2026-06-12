# collab-group

collab-group is a service to query [Gafaelfawr](https://gafaelfawr.lsst.io) for group information, and then to create directories on a shared collaboration volume corresponding to each user group.
It then sets ownership and permissions appropriately on those directories: they will be group-writeable and have set-group-id turned on so that subdirectories will be owned by the same group.

The purpose of this is to provide users of the Rubin Science Platform with file space where they can do ad-hoc collaborative work by creating groups and adding other users to those groups.

Eventually it will be absorbed into [Nublado](https://nublado.lsst.io).
