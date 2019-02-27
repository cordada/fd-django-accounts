===================
Project maintenance
===================

Release new version
-------------------

0) (local workstation) Make sure local branch ``develop`` is up to date and tests pass::

    git checkout develop
    git push

Then wait for the CircleCI tests and verify they were successful.
https://circleci.com/gh/fyndata/fyndata-django-accounts/tree/develop

1) (local workstation) Bump package version (either of the following alternatives)::

    bumpversion major|minor|patch
    bumpversion --new-version 'X.Y.Z'

Push commit ``abcd1234`` and tag ``vX.Y.Z`` automatically created by ``bumpversion``::

    git push
    git push --tags

2) (GitHub) Create pull request and release:

- Create PR for ``master..develop`` named "Release", with label ``kind: release``.
  https://github.com/fyndata/fyndata-django-accounts/compare/master...develop

- Merge PR.

- Create new release:

    - Go to the repo's "Releases/tags" section
      https://github.com/fyndata/fyndata-django-accounts/tags

    - Create release for the new tag just pushed.

    - Go to the CircleCI job named ``ci/circleci: dist`` corresponding to commit ``abcd1234``
      (tagged ``vX.Y.Z``), tab "Artifacts", and download the generated package files:

        - `fyndata-django-accounts-X.Y.Z.tar.gz`

        - `fyndata_django_accounts-X.Y.Z-py3-none-any.whl`

    - For the new GitHub release, add the files just downloaded.

    - "Create".


3) (local workstation) Update ``develop`` from ``master``::

    git checkout master
    git pull
    git checkout develop
    git merge --ff master
    git push
