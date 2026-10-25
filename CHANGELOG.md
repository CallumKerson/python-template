# Changelog

## [0.6.1](https://github.com/CallumKerson/python-template/compare/v0.6.0...v0.6.1) (2026-10-25)


### 🐛 Bug Fixes

* lock tools limited by os only for their platforms ([#32](https://github.com/CallumKerson/python-template/issues/32)) ([731efd4](https://github.com/CallumKerson/python-template/commit/731efd43a4b96f61682164e132e625506a38c085))

## [0.6.0](https://github.com/CallumKerson/python-template/compare/v0.5.0...v0.6.0) (2026-10-25)


### ✨ Features

* attach each release's sdist and wheel ([#30](https://github.com/CallumKerson/python-template/issues/30)) ([40922d8](https://github.com/CallumKerson/python-template/commit/40922d881c823670d7a170ff8819ec967e0a7010))

## [0.5.0](https://github.com/CallumKerson/python-template/compare/v0.4.0...v0.5.0) (2026-10-25)


### ✨ Features

* lint generated projects' workflows with jactionlint ([07bc0ae](https://github.com/CallumKerson/python-template/commit/07bc0aebd5853241cc0e9c1a39e476ca696a89d2))

## [0.4.0](https://github.com/CallumKerson/python-template/compare/v0.3.0...v0.4.0) (2026-10-13)


### ⚠ BREAKING CHANGES

* the config files move, so updating an existing project conflicts wherever it changed them. Move them into .config/ before updating.

### ✨ Features

* cache uv's Python install in generated projects' workflows ([#22](https://github.com/CallumKerson/python-template/issues/22)) ([9444dce](https://github.com/CallumKerson/python-template/commit/9444dce35ddd16b978989fc307a6511685e7f6c3))
* keep generated projects' tool config in .config ([#26](https://github.com/CallumKerson/python-template/issues/26)) ([6cf6bf1](https://github.com/CallumKerson/python-template/commit/6cf6bf12960d0d150c16e15cf4f345ab4c80e5e0))


### 🐛 Bug Fixes

* default the project name to the directory's name when copying into . ([#27](https://github.com/CallumKerson/python-template/issues/27)) ([9f2d7f8](https://github.com/CallumKerson/python-template/commit/9f2d7f8274f4659cecf2b327297d9eab1f768723))

## [0.3.0](https://github.com/CallumKerson/python-template/compare/v0.2.0...v0.3.0) (2026-10-13)


### ⚠ BREAKING CHANGES

* the template is rewritten. Its questions, layout and answers file all change, so existing projects need to be copied again.

### ✨ Features

* add a cyclopts CLI project type ([#12](https://github.com/CallumKerson/python-template/issues/12)) ([f9a0423](https://github.com/CallumKerson/python-template/commit/f9a042365586e5aa401bcd0af0e3e97c05cce6a0))
* add optional GitHub CI, Renovate and release-please ([#13](https://github.com/CallumKerson/python-template/issues/13)) ([252f36a](https://github.com/CallumKerson/python-template/commit/252f36a819c769d5d9115e4666adb55d5bb63309))
* extend the shared Renovate preset in generated projects ([#17](https://github.com/CallumKerson/python-template/issues/17)) ([ddfe7fd](https://github.com/CallumKerson/python-template/commit/ddfe7fd6318628d39fefb601abb8a44a23f934cf))
* rebuild the template around uv, mise and hk ([#11](https://github.com/CallumKerson/python-template/issues/11)) ([150706f](https://github.com/CallumKerson/python-template/commit/150706fc9f1a0780b85a7d84ba5f62f560a1d95c))
* run CI before release-please in generated projects ([#18](https://github.com/CallumKerson/python-template/issues/18)) ([225f0de](https://github.com/CallumKerson/python-template/commit/225f0de3b5073a0ab39cf33c616177f953fec6b1))
* use the GitHub CLI's token when pinning, and show failed commands' output ([#21](https://github.com/CallumKerson/python-template/issues/21)) ([1aedd02](https://github.com/CallumKerson/python-template/commit/1aedd02745261795ff96b2f0981371bbb1706f7d))

## [0.2.0](https://github.com/CallumKerson/python-template/compare/v0.1.0...v0.2.0) (2025-08-25)


### Features

* add description to template ([deff97d](https://github.com/CallumKerson/python-template/commit/deff97d83ec35e768c49086b96792916d0ebb42e))


### Documentation

* add README ([7029426](https://github.com/CallumKerson/python-template/commit/70294263c573ee4d29c34d9304f97994d0317dd4))

## 0.1.0 (2025-08-25)


### Features

* add initial template ([96f96ab](https://github.com/CallumKerson/python-template/commit/96f96aba550f903a842b73f886fb5e965d374294))
