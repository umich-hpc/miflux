
# Updating create-dmg

[create-dmg](https://github.com/umich-flux/create-dmg) is a git subtree.  See

https://blogs.atlassian.com/2013/05/alternatives-to-git-submodule-git-subtree/

To update the subtree with changes made in the upstream project:

```bash
git fetch create-dmg master
git subtree pull --prefix client/util/create-dmg create-dmg master
```

To contribute local changes to the subtree upstream:

```bash
git subtree push --prefix=client/util/create-dmg create-dmg master
```
