===================
Project maintenance
===================

Release new version
-------------------

0) (local workstation) Make sure main branches are synced with local ones, and tests pass::

    make clean -s
    test -z "$$(git status --porcelain)" && echo 'CLEAN' || echo 'DIRTY'
    git checkout master
    git push
    git checkout develop
    git push

Then wait for the
`CircleCI tests (develop) <https://circleci.com/gh/fyndata/fyndata-django-accounts/tree/develop>`_
and verify they were successful.

1) (local workstation) Update changelog.

Generate summary::

    git lg-github-pr-summary master..develop

Add new entry to changelog including the changes summary::

    nano 'HISTORY.rst'
    git add 'HISTORY.rst'
    git commit -m "HISTORY: update for new version"

2) (local workstation) Bump package version (either of the following alternatives)::

    bumpversion major|minor|patch
    bumpversion --new-version 'X.Y.Z'

Push commit ``abcd1234`` and tag ``vX.Y.Z`` automatically created by ``bumpversion``::

    git push
    git push --tags

3) (GitHub) Create pull request and new release:

- Create PR for
  `master...develop <https://github.com/fyndata/fyndata-django-accounts/compare/master...develop>`_.

  - Name: "Release".

  - Labels: ``kind: release``.

  - Description: local output of ``git lg-github-pr-summary master..develop``

- Merge PR.

- Create new release:

  - Go to the repo's
    `"Releases/tags" section <https://github.com/fyndata/fyndata-django-accounts/tags>`_.

  - Create release for the new tag just pushed.

  - Title: ``vX.Y.Z``.

  - Description: same as the PR just created.

  - Go to the CircleCI job named ``ci/circleci: dist`` corresponding to commit ``abcd1234``
    (tagged ``vX.Y.Z``), tab "Artifacts", and download the generated package files to local repo
    directory ``dist/``:

    - ``fyndata-django-accounts-X.Y.Z.tar.gz``

    - ``fyndata_django_accounts-X.Y.Z-py3-none-any.whl``

  - For the new GitHub release, add the files just downloaded.

  - "Publish release".


4) (local workstation) Publish to PyPI::

    make upload-release


5) (local workstation) Update ``develop`` from ``master``::

    git checkout master
    git pull
    git checkout develop
    git merge --ff master
    git push


Appendix
--------

Add git alias::

    git config --global alias.lg-github-pr-summary \
        '!f() { git log --date=short --merges --grep "^Merge pull request #[[:digit:]]* from" --pretty="tformat:- (%C(auto,red)<S>%s</S>%C(reset), %C(auto,green)%ad%C(reset)) %w(72,0,2)%b" "$@" | sed -E "s|<S>Merge pull request (#[0-9]+) from .+</S>|PR \1|"; }; f'
