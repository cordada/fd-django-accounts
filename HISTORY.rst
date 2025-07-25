.. :changelog:

History
-------

unreleased (YYYY-MM-DD)
+++++++++++++++++++++++

0.15.0 (2025-07-25)
+++++++++++++++++++

- (PR #354, 2025-05-20) chore(deps): Bump setuptools from 75.8.2 to 78.1.1
- (PR #353, 2025-06-09) chore: Bump the production-dependencies group with 6 updates
- (PR #350, 2025-06-26) chore(deps): Bump flake8 from 7.1.1 to 7.2.0
- (PR #355, 2025-06-26) chore(deps): Bump tox from 4.23.2 to 4.26.0
- (PR #356, 2025-06-26) chore(deps): Bump setuptools from 78.1.1 to 80.9.0
- (PR #359, 2025-07-09) chore(deps): Bump coverage from 7.6.12 to 7.9.1
- (PR #360, 2025-07-25) Remove upper bound on Python version
- (PR #357, 2025-07-25) chore(deps): Bump mypy from 1.15.0 to 1.16.1
- (PR #358, 2025-07-25) chore(deps): Bump flake8 from 7.2.0 to 7.3.0
- (PR #361, 2025-07-25) Fix Python package license metadata deprecations

0.14.0 (2025-03-25)
+++++++++++++++++++

- (PR #339, 2025-03-24) chore(deps): Bump setuptools from 71.1.0 to 75.8.2
- (PR #340, 2025-03-24) chore(deps): Bump mypy from 1.13.0 to 1.15.0
- (PR #341, 2025-03-24) chore(deps): Bump coverage from 7.4.1 to 7.6.12
- (PR #345, 2025-03-24) Improve test coverage exclusions
- (PR #344, 2025-03-24) Require Python ≥3.9

0.13.0 (2025-03-12)
+++++++++++++++++++

- (PR #328, 2024-12-03) chore: Bump codecov/codecov-action from 5.0.6 to 5.0.7 in the production-dependencies group
- (PR #327, 2024-12-03) chore(deps): Bump mypy from 1.8.0 to 1.13.0
- (PR #326, 2024-12-09) chore(deps): Bump wheel from 0.45.0 to 0.45.1
- (PR #325, 2024-12-09) chore(deps): Bump psycopg2 from 2.9.9 to 2.9.10
- (PR #329, 2025-01-03) chore: Bump the production-dependencies group with 3 updates
- (PR #331, 2025-01-28) chore(deps): Bump twine from 5.1.1 to 6.0.1
- (PR #336, 2025-02-28) chore: Drop support for Python 3.8
- (PR #337, 2025-02-28) chore: Bump the production-dependencies group across 1 directory with 5 updates
- (PR #338, 2025-02-28) Use most recent patch version of Python in CI/CD configuration
- (PR #335, 2025-02-28) chore(deps): Bump twine from 6.0.1 to 6.1.0

0.12.0 (2024-11-25)
+++++++++++++++++++

- (PR #321, 2024-11-25) Improve Make task `clean`
- (PR #322, 2024-11-25) deps: Update `twine` from 4.0.2 to 5.1.1

0.11.0 (2024-11-25)
+++++++++++++++++++

- (PR #311, 2024-11-22) Move Mypy, Flake8, Coverage.py configurations to separate configuration files
- (PR #312, 2024-11-22) deps: Update `setuptools` from ≤69.1.0 to 71.1.0
- (PR #313, 2024-11-22) deps: Update `wheel` from ≤0.42.0 to 0.45.0
- (PR #314, 2024-11-22) deps: Update `pip` from 22.3.1 to 24.2
- (PR #315, 2024-11-22) Replace `setup.py sdist` and `bdist_wheel` with `build`
- (PR #316, 2024-11-22) When running `twine check`, fail on warnings
- (PR #318, 2024-11-25) Update Bumpversion configuration to be compliant with Commitlint
- (PR #317, 2024-11-25) Replace Setuptools Configuration with Python Project Configuration

0.10.0 (2024-11-22)
+++++++++++++++++++

- (PR #299, 2024-11-20) deps: Update PostgreSQL from version ≥12.3 to 15.5
- (PR #300, 2024-11-20) chore(deps): Bump the production-dependencies group with 7 updates
- (PR #303, 2024-11-20) chore(deps): Bump flake8 from 6.0.0 to 7.1.1
- (PR #304, 2024-11-20) chore(deps): Bump tox from 4.11.3 to 4.23.2
- (PR #305, 2024-11-21) deps: Update `Django` from ≥2.1 to ≥4.2
- (PR #306, 2024-11-21) Improve type annotations
- (PR #307, 2024-11-22) Update for Django 4.2. ⚠️ Contains breaking changes.
- (PR #308, 2024-11-22) Add methods required by Django Admin to `.models.User`

0.9.0 (2024-02-26)
++++++++++++++++++

- (PR #279, 2024-01-10) chore(deps): Bump mypy from 1.4.1 to 1.8.0
- (PR #281, 2024-01-29) chore: Bump the production-dependencies group with 7 updates
- (PR #284, 2024-02-13) Change Python project structure from Flat layout to Src layout
- (PR #285, 2024-02-13) chore: Bump the production-dependencies group with 3 updates
- (PR #286, 2024-02-14) Add Python project configuration
- (PR #275, 2024-02-15) chore(deps): Bump wheel from 0.41.2 to 0.42.0
- (PR #282, 2024-02-16) chore: Bump coverage from 7.2.7 to 7.4.1
- (PR #287, 2024-02-16) chore: Bump setuptools from 68.0.0 to 69.1.0

0.8.0 (2023-10-23)
++++++++++++++++++

- (PR #258, 2023-09-07) Add Codecov repository upload token; update Codecov status badge
- (PR #261, 2023-09-27) Add dependency groups to Dependabot configuration
- (PR #264, 2023-09-27) Allow GitHub Actions to pass secrets from CI/CD to CI workflow
- (PR #262, 2023-09-27) chore: Bump the production-dependencies group with 4 updates
- (PR #266, 2023-10-17) Add missing tests for `commands.createsuperuser`
- (PR #263, 2023-10-23) chore(deps): Bump tox from 3.26.0 to 4.11.3
- (PR #253, 2023-10-23) chore(deps): Bump wheel from 0.40.0 to 0.41.2
- (PR #267, 2023-10-23) chore(deps): Bump psycopg2 from 2.9.3 to 2.9.9

0.7.0 (2023-06-09)
++++++++++++++++++

- (PR #242, 2023-07-10) Add improved `__repr__()` to `User` model
- (PR #243, 2023-07-10) Fix broken Make task `docker-compose-run-test`
- (PR #241, 2023-07-10) chore: Bump codecov/codecov-action from 3.1.2 to 3.1.4
- (PR #244, 2023-07-14) chore: Bump actions/setup-python from 4.5.0 to 4.7.0
- (PR #231, 2023-07-14) chore(deps): Bump flake8 from 3.8.4 to 6.0.0
- (PR #240, 2023-07-14) chore: Bump actions/checkout from 3.3.0 to 3.5.3
- (PR #237, 2023-07-14) chore: Bump actions/dependency-review-action from 3.0.4 to 3.0.6
- (PR #235, 2023-07-14) chore(deps): Bump coverage from 7.2.1 to 7.2.7
- (PR #247, 2023-07-25) chore(deps): Bump mypy from 1.1.1 to 1.4.1
- (PR #246, 2023-07-25) chore(deps): Bump setuptools from 67.6.0 to 68.0.0
- (PR #245, 2023-07-25) chore(deps): Bump twine from 4.0.1 to 4.0.2

0.6.1 (2023-06-09)
++++++++++++++++++

- (PR #228, 2023-04-04) Add Git commit linter
- (PR #225, 2023-04-05) Bump wheel from 0.38.4 to 0.40.0
- (PR #227, 2023-05-23) chore(deps): Bump actions/dependency-review-action from 3.0.3 to 3.0.4
- (PR #234, 2023-06-05) Add Codecov to CI workflow

0.6.0 (2023-03-14)
++++++++++++++++++

- (PR #218, 2023-03-08) Drop support for Python 3.7
- (PR #209, 2023-03-14) chore(deps): bump coverage from 7.1.0 to 7.2.1
- (PR #219, 2023-03-14) chore(deps): bump setuptools from 67.1.0 to 67.6.0
- (PR #220, 2023-03-14) chore: bump actions/cache from 3.2.5 to 3.3.1

0.5.0 (2023-03-07)
++++++++++++++++++

- (PR #204, 2023-01-26) Add GitHub Dependency Review
- (PR #206, 2023-02-06) chore(deps): bump coverage from 6.4.4 to 7.1.0
- (PR #195, 2023-02-06) chore(deps): bump mypy from 0.971 to 0.991
- (PR #201, 2023-02-06) chore(deps): bump wheel from 0.37.1 to 0.38.4
- (PR #207, 2023-02-06) chore(deps): bump setuptools from 65.3.0 to 67.1.0
- (PR #212, 2023-03-07) Switch CI/CD to GitHub actions
- (PR #215, 2023-03-07) chore(deps): bump mypy from 0.991 to 1.1.1

0.4.0 (2023-01-05)
++++++++++++++++++

- (PR #197, 2022-12-20) chore: Update `last_login` field on User model
- (PR #199, 2023-01-04) chore: Add support for Python 3.10

0.3.0 (2022-11-11)
++++++++++++++++++

- (PR #191, 2022-11-10) fix(requirements): Pin importlib-metadata dependency for python 3.7
- (PR #190, 2022-11-11) feat: Add Python 3.9 support

0.2.0 (2022-09-22)
++++++++++++++++++

- (PR #174, 2022-08-19) chore(management): Improve management command `createsuperuser`
- (PR #176, 2022-08-29) chore: Add Make tasks for installation
- (PR #138, 2022-08-31) build(deps): bump wheel from 0.36.2 to 0.37.1
- (PR #178, 2022-09-05) Add testing with Docker Compose
- (PR #177, 2022-09-05) build(deps): bump tox from 3.24.5 to 3.25.1
- (PR #179, 2022-09-06) chore: Drop support for Python 3.6
- (PR #167, 2022-09-06) chore(deps): bump coverage from 5.4 to 6.4.4
- (PR #180, 2022-09-06) build(deps): bump mypy from 0.910 to 0.971
- (PR #175, 2022-09-08) chore(deps): bump setuptools from 53.0.0 to 65.3.0
- (PR #182, 2022-09-22) build(deps): bump twine from 3.3.0 to 4.0.1
- (PR #181, 2022-09-22) chore(deps): bump psycopg2 from 2.8.6 to 2.9.3
- (PR #183, 2022-09-22) chore(deps): bump tox from 3.25.1 to 3.26.0

0.1.4 (2022-08-19)
++++++++++++++++++

- (PR #44, 2020-09-16) build(deps): bump codecov from 2.1.7 to 2.1.9
- (PR #42, 2020-09-16) build(deps): bump coverage from 5.2 to 5.3
- (PR #43, 2020-09-17) build(deps): bump psycopg2 from 2.8.5 to 2.8.6
- (PR #45, 2020-09-17) build(deps): bump wheel from 0.34.2 to 0.35.1
- (PR #47, 2020-10-19) build(deps): bump tox from 3.20.0 to 3.20.1
- (PR #46, 2020-10-19) build(deps): bump flake8 from 3.8.3 to 3.8.4
- (PR #48, 2020-10-19) build(deps): bump mypy from 0.782 to 0.790
- (PR #50, 2020-11-12) build(deps): bump codecov from 2.1.9 to 2.1.10
- (PR #49, 2020-11-12) build(deps): bump setuptools from 50.3.0 to 50.3.2
- (PR #53, 2020-12-15) build(deps): bump setuptools from 50.3.2 to 51.0.0
- (PR #54, 2020-12-15) build(deps): bump wheel from 0.35.1 to 0.36.2
- (PR #55, 2020-12-15) Update Python 3.6, 3.7, and 3.8 versions
- (PR #56, 2020-12-15) config: Make CI 'dist' job depend on 'test' jobs
- (PR #58, 2020-12-22) build(deps): bump coverage from 5.3 to 5.3.1
- (PR #61, 2020-12-30) build(deps): bump twine from 3.2.0 to 3.3.0
- (PR #57, 2020-12-30) build(deps): bump codecov from 2.1.10 to 2.1.11
- (PR #73, 2021-02-16) build(deps): bump tox from 3.20.1 to 3.22.0
- (PR #71, 2021-02-16) build(deps): bump setuptools from 51.0.0 to 53.0.0
- (PR #69, 2021-02-16) build(deps): bump mypy from 0.790 to 0.800
- (PR #74, 2021-02-16) build(deps): bump coverage from 5.3.1 to 5.4
- (PR #88, 2021-10-13) build(deps): bump mypy from 0.800 to 0.910
- (PR #119, 2022-03-25) build(deps): bump tox from 3.22.0 to 3.24.5
- (PR #169, 2022-08-18) chore: Change Dependabot schedule interval from `daily` to `monthly`
- (PR #172, 2022-08-19) feat(management): Add management command `createsuperuser`
- (PR #171, 2022-08-19) chore: Remove dependabot `time` and `timezone` params

0.1.3 (2020-09-15)
++++++++++++++++++

- (PR #40, 2020-09-15) config: Add PyPI package uploading to CI
- (PR #36, 2020-09-15) build(deps): bump tox from 3.7.0 to 3.20.0
- (PR #24, 2020-09-15) build(deps): bump twine from 1.13.0 to 3.2.0
- (PR #39, 2020-09-15) build(deps): bump setuptools from 40.8.0 to 50.3.0
- (PR #23, 2020-07-15) build(deps): bump flake8 from 3.7.6 to 3.8.3
- (PR #21, 2020-07-13) build(deps): bump mypy from 0.780 to 0.782
- (PR #18, 2020-07-13) build(deps): bump wheel from 0.33.1 to 0.34.2
- (PR #22, 2020-07-09) config: Verify Python dependency compatibility in CI
- (PR #19, 2020-07-08) build(deps): bump codecov from 2.0.15 to 2.1.7
- (PR #17, 2020-07-07) build(deps): bump coverage from 4.5.2 to 5.2
- (PR #16, 2020-07-07) config: Add configuration for GitHub Dependabot
- (PR #15, 2020-06-18) config: Upgrade PostgreSQL to v12.3

0.1.2 (2020-06-08)
++++++++++++++++++

* (PR #10, 2020-04-13) Update readme
* (PR #11, 2020-06-08) config: Improve support for multiple Python versions to CircleCI
* (PR #12, 2020-06-08) Update test dependencies 'mypy' and 'psycopg2'
* (PR #13, 2020-06-08) Add Python 3.8 support

0.1.1 (2019-02-21)
++++++++++++++++++

* setup: fix missing package data files

0.1.0 (2019-02-21)
++++++++++++++++++

* First implementation.
* First release on PyPI.
