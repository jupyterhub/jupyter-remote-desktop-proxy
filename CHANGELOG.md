# Changelog

## v2.0.1

([full changelog](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/compare/v2.0.0...bec995c03f719fad2a37aa950842bc977eaae12e))

### Bugs fixed

- Retry a few times when the initial connection fails [#112](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/112) ([@sunu](https://github.com/sunu), [@yuvipanda](https://github.com/yuvipanda))

### Other merged PRs

- [pre-commit.ci] pre-commit autoupdate [#111](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/111) ([@consideRatio](https://github.com/consideRatio))

### Contributors to this release

The following people contributed discussions, new ideas, code and documentation contributions, and review.
See [our definition of contributors](https://github-activity.readthedocs.io/en/latest/#how-does-this-tool-define-contributions-in-the-reports).

([GitHub contributors page for this release](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/graphs/contributors?from=2024-04-02&to=2024-06-13&type=c))

@consideRatio ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-remote-desktop-proxy+involves%3AconsideRatio+updated%3A2024-04-02..2024-06-13&type=Issues)) | @sunu ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-remote-desktop-proxy+involves%3Asunu+updated%3A2024-04-02..2024-06-13&type=Issues)) | @yuvipanda ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-remote-desktop-proxy+involves%3Ayuvipanda+updated%3A2024-04-02..2024-06-13&type=Issues))

## v2.0

### v2.0.0 - 2024-04-02

This release removes a bundled VNC server, use of `jupyter-remote-desktop-proxy`
requires both `websockify` and a VNC server - TigerVNC and TurboVNC are
officially supported. For tested examples on how to install `websockify` and
officially supported VNC servers, see [this project's Dockerfile].

This project now publishes basic but tested images built on
[quay.io/jupyter/base-notebook] from the [jupyter/docker-stacks] to
[quay.io/jupyterhub/jupyter-remote-desktop-proxy]. Their purpose is currently
not scoped beyond use for testing and providing an example on how to install
officially supported VNC servers.

The Ctrl-Alt-Delete button is currently removed, but intended to be added back.
This is tracked by [this GitHub issue].

([full changelog](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/compare/v1.2.1...v2.0.0))

[this project's Dockerfile]: https://github.com/jupyterhub/jupyter-remote-desktop-proxy/blob/main/Dockerfile
[quay.io/jupyter/base-notebook]: https://quay.io/repository/jupyter/base-notebook?tab=tags
[quay.io/jupyterhub/jupyter-remote-desktop-proxy]: https://quay.io/repository/jupyterhub/jupyter-remote-desktop-proxy?tab=tags
[jupyter/docker-stacks]: https://github.com/jupyter/docker-stacks
[this GitHub issue]: https://github.com/jupyterhub/jupyter-remote-desktop-proxy/issues/83

#### Breaking Changes

- Require jupyter-server-proxy 4+ [#91](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/91) ([@consideRatio](https://github.com/consideRatio), [@yuvipanda](https://github.com/yuvipanda))
- Require python 3.8+, up from 3.6+ [#90](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/90) ([@consideRatio](https://github.com/consideRatio), [@manics](https://github.com/manics))
- Remove bundled VNC server [#84](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/84) ([@manics](https://github.com/manics), [@consideRatio](https://github.com/consideRatio), [@yuvipanda](https://github.com/yuvipanda))

#### New features added

- Publish TigerVNC and TurboVNC image to quay.io [#94](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/94) ([@consideRatio](https://github.com/consideRatio), [@yuvipanda](https://github.com/yuvipanda))

#### Enhancements made

- Add a "Hub Control Panel" menu item if running inside a JupyterHub [#79](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/79) ([@yuvipanda](https://github.com/yuvipanda), [@manics](https://github.com/manics), [@unode](https://github.com/unode))
- Cleanup the UI to be much nicer [#78](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/78) ([@yuvipanda](https://github.com/yuvipanda), [@manics](https://github.com/manics))

#### Bugs fixed

- MANIFEST.in: Include templates/ directory [#103](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/103) ([@zmcgrew](https://github.com/zmcgrew), [@consideRatio](https://github.com/consideRatio))
- Fix failure to specify port for TurboVNC server [#99](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/99) ([@consideRatio](https://github.com/consideRatio))
- Fix TigerVNC detection for non-apt installations [#96](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/96) ([@consideRatio](https://github.com/consideRatio), [@yuvipanda](https://github.com/yuvipanda), [@goekce](https://github.com/goekce))
- [Docker image] Install fonts-dejavu for use by terminals [#86](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/86) ([@yuvipanda](https://github.com/yuvipanda), [@manics](https://github.com/manics), [@consideRatio](https://github.com/consideRatio))
- Remove xfce4-screensaver [#76](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/76) ([@manics](https://github.com/manics), [@yuvipanda](https://github.com/yuvipanda))
- Fix container build [#70](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/70) ([@manics](https://github.com/manics), [@yuvipanda](https://github.com/yuvipanda), [@consideRatio](https://github.com/consideRatio))

#### Maintenance and upkeep improvements

- Fail early on missing websockify executable [#107](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/107) ([@consideRatio](https://github.com/consideRatio))
- refactor: small readability and consistency details [#104](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/104) ([@consideRatio](https://github.com/consideRatio))
- Bump dependency requirement a patch version [#102](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/102) ([@consideRatio](https://github.com/consideRatio))
- Fix image tests: vncserver, websockify, jupyter-remote-desktop-proxy [#101](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/101) ([@consideRatio](https://github.com/consideRatio), [@yuvipanda](https://github.com/yuvipanda))
- Fix automation to publish tigervnc and turbovnc images [#95](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/95) ([@consideRatio](https://github.com/consideRatio))
- Require jupyter-server-proxy 4+ [#91](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/91) ([@consideRatio](https://github.com/consideRatio), [@yuvipanda](https://github.com/yuvipanda))
- Require python 3.8+, up from 3.6+ [#90](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/90) ([@consideRatio](https://github.com/consideRatio), [@manics](https://github.com/manics))
- Remove bundled VNC server [#84](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/84) ([@manics](https://github.com/manics), [@consideRatio](https://github.com/consideRatio), [@yuvipanda](https://github.com/yuvipanda))
- Stop vendoring noVNC [#77](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/77) ([@yuvipanda](https://github.com/yuvipanda), [@manics](https://github.com/manics), [@consideRatio](https://github.com/consideRatio))

#### Documentation improvements

- Fix typo in README.md [#72](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/72) ([@nthiery](https://github.com/nthiery), [@yuvipanda](https://github.com/yuvipanda))

#### Contributors to this release

The following people contributed discussions, new ideas, code and documentation contributions, and review.
See [our definition of contributors](https://github-activity.readthedocs.io/en/latest/#how-does-this-tool-define-contributions-in-the-reports).

([GitHub contributors page for this release](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/graphs/contributors?from=2023-09-27&to=2024-04-02&type=c))

@benz0li ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-remote-desktop-proxy+involves%3Abenz0li+updated%3A2023-09-27..2024-04-02&type=Issues)) | @consideRatio ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-remote-desktop-proxy+involves%3AconsideRatio+updated%3A2023-09-27..2024-04-02&type=Issues)) | @goekce ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-remote-desktop-proxy+involves%3Agoekce+updated%3A2023-09-27..2024-04-02&type=Issues)) | @manics ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-remote-desktop-proxy+involves%3Amanics+updated%3A2023-09-27..2024-04-02&type=Issues)) | @nthiery ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-remote-desktop-proxy+involves%3Anthiery+updated%3A2023-09-27..2024-04-02&type=Issues)) | @unode ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-remote-desktop-proxy+involves%3Aunode+updated%3A2023-09-27..2024-04-02&type=Issues)) | @yuvipanda ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-remote-desktop-proxy+involves%3Ayuvipanda+updated%3A2023-09-27..2024-04-02&type=Issues)) | @zmcgrew ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-remote-desktop-proxy+involves%3Azmcgrew+updated%3A2023-09-27..2024-04-02&type=Issues))

## v1.2

### v1.2.1 - 2023-09-27

([full changelog](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/compare/v1.2.0...v1.2.1))

#### Bugs fixed

- Revert "Simplify xtartup command" [#64](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/64) ([@yuvipanda](https://github.com/yuvipanda), [@consideRatio](https://github.com/consideRatio))

### v1.2.0 - 2023-09-25

([full changelog](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/compare/v1.1.0...v1.2.0))

#### New features added

- Let user defines its own xstartup and geometry via ~/.vnc/xstartup [#35](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/35) ([@cmd-ntrf](https://github.com/cmd-ntrf), [@yuvipanda](https://github.com/yuvipanda), [@consideRatio](https://github.com/consideRatio))

#### Bugs fixed

- Fix module 'posixpath' has no attribute 'expand' [#61](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/61) ([@cmd-ntrf](https://github.com/cmd-ntrf), [@consideRatio](https://github.com/consideRatio))

#### Maintenance and upkeep improvements

- Simplify xtartup command [#59](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/59) ([@yuvipanda](https://github.com/yuvipanda), [@consideRatio](https://github.com/consideRatio))
- Simplify developmental dockerfile [#58](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/58) ([@yuvipanda](https://github.com/yuvipanda), [@consideRatio](https://github.com/consideRatio))

#### Documentation improvements

- Document needing seccomp=unconfined [#53](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/53) ([@yuvipanda](https://github.com/yuvipanda), [@consideRatio](https://github.com/consideRatio))

#### Contributors to this release

The following people contributed discussions, new ideas, code and documentation contributions, and review.
See [our definition of contributors](https://github-activity.readthedocs.io/en/latest/#how-does-this-tool-define-contributions-in-the-reports).

([GitHub contributors page for this release](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/graphs/contributors?from=2023-07-19&to=2023-09-25&type=c))

@benz0li ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-remote-desktop-proxy+involves%3Abenz0li+updated%3A2023-07-19..2023-09-25&type=Issues)) | @cmd-ntrf ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-remote-desktop-proxy+involves%3Acmd-ntrf+updated%3A2023-07-19..2023-09-25&type=Issues)) | @consideRatio ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-remote-desktop-proxy+involves%3AconsideRatio+updated%3A2023-07-19..2023-09-25&type=Issues)) | @domna ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-remote-desktop-proxy+involves%3Adomna+updated%3A2023-07-19..2023-09-25&type=Issues)) | @yuvipanda ([activity](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-remote-desktop-proxy+involves%3Ayuvipanda+updated%3A2023-07-19..2023-09-25&type=Issues))

## v1.1

### v1.1.0 - 2023-07-18

([full changelog](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/compare/v1.0...v1.1.0))

#### Enhancements made

- Add logic to determine if vncserver is TigerVNC [#32](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/32) ([@cmd-ntrf](https://github.com/cmd-ntrf))

#### Bugs fixed

- Fix path when using bundled tigervnc [#44](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/44) ([@pnasrat](https://github.com/pnasrat))
- Remove hardcoded display number and port, avoids multi-user conflicts [#34](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/34) ([@cmd-ntrf](https://github.com/cmd-ntrf))

#### Maintenance and upkeep improvements

- Add RELEASE.md, adopt tbump, rename release workflow for consistency [#38](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/38) ([@consideRatio](https://github.com/consideRatio))
- Remove "/usr/bin" prefix in front of dbus-launch in xstartup [#33](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/33) ([@cmd-ntrf](https://github.com/cmd-ntrf))
- Add logic to determine if vncserver is TigerVNC [#32](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/32) ([@cmd-ntrf](https://github.com/cmd-ntrf))
- dependabot: monthly updates of github actions [#30](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/30) ([@consideRatio](https://github.com/consideRatio))
- maint: add pre-commit config [#25](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/25) ([@consideRatio](https://github.com/consideRatio))
- Quieten binder-badge bot [#3](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/3) ([@manics](https://github.com/manics))

#### Documentation improvements

- Add PyPI/Issues/Forum badges for readme [#40](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/40) ([@consideRatio](https://github.com/consideRatio))
- Backfill changelog for 1.0.0 and 0.1.3 [#37](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/37) ([@consideRatio](https://github.com/consideRatio))

#### Continuous integration improvements

- Fix permissions required for trusted workflow [#48](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/48) ([@yuvipanda](https://github.com/yuvipanda))
- Use trusted publishing to push to PyPI [#46](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/46) ([@yuvipanda](https://github.com/yuvipanda))
- ci: fix typo in manics/action-binderbadge version [#39](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/39) ([@consideRatio](https://github.com/consideRatio))

#### Contributors to this release

([GitHub contributors page for this release](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/graphs/contributors?from=2023-01-19&to=2023-07-18&type=c))

[@cmd-ntrf](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-remote-desktop-proxy+involves%3Acmd-ntrf+updated%3A2023-01-19..2023-07-18&type=Issues) | [@consideRatio](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-remote-desktop-proxy+involves%3AconsideRatio+updated%3A2023-01-19..2023-07-18&type=Issues) | | [@manics](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-remote-desktop-proxy+involves%3Amanics+updated%3A2023-01-19..2023-07-18&type=Issues) | [@pnasrat](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-remote-desktop-proxy+involves%3Apnasrat+updated%3A2023-01-19..2023-07-18&type=Issues) | [@yuvipanda](https://github.com/search?q=repo%3Ajupyterhub%2Fjupyter-remote-desktop-proxy+involves%3Ayuvipanda+updated%3A2023-01-19..2023-07-18&type=Issues)

## v1.0

### v1.0.0 - 2023-01-19

With this release, the project has relocated from `jupyter-desktop-server` to
`jupyter-remote-desktop-proxy` and relocated from
[yuvipanda/jupyter-desktop-server](https://github.com/yuvipanda/jupyter-desktop-server) to
[jupyterhub/jupyter-remote-desktop-proxy](https://github.com/jupyterhub/jupyter-remote-desktop-proxy).

#### New features added

- Add a shared clipboard [#10](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/10) ([@manics](https://github.com/manics), [@yuvipanda](https://github.com/yuvipanda), [@satra](https://github.com/satra), [@fperez](https://github.com/fperez))

#### Enhancements made

- Use TurboVNC if installed [#29 (in previous github repo)](https://github.com/yuvipanda/jupyter-desktop-server/pull/29) ([@manics](https://github.com/manics), [@yuvipanda](https://github.com/yuvipanda), [@cslocum](https://github.com/cslocum))

#### Maintenance and upkeep improvements

- maint: add dependabot for github actions [#22](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/22) ([@consideRatio](https://github.com/consideRatio), [@yuvipanda](https://github.com/yuvipanda))
- Complete rename of the project - from jupyter_desktop/jupyter-desktop-server to jupyter_remote_desktop_proxy [#20](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/20) ([@yuvipanda](https://github.com/yuvipanda), [@consideRatio](https://github.com/consideRatio))
- Remove apt.txt and refactor Dockerfile [#13](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/13) ([@consideRatio](https://github.com/consideRatio), [@yuvipanda](https://github.com/yuvipanda), [@manics](https://github.com/manics))
- Update TurboVNC to 2.2.6 [#11](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/11) ([@manics](https://github.com/manics), [@consideRatio](https://github.com/consideRatio))
- Update noVNC to 1.2.0 [#6](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/6) ([@manics](https://github.com/manics))
- Add setup.py metadata [#5](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/5) ([@manics](https://github.com/manics), [@yuvipanda](https://github.com/yuvipanda))
- Add pypi publish workflow [#4](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/4) ([@manics](https://github.com/manics))
- Rename repo jupyter-desktop-server ➡️ jupyter-remote-desktop-proxy [#2](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/2) ([@manics](https://github.com/manics), [@choldgraf](https://github.com/choldgraf))
- Fix permissions on ~/.cache [#22 (in previous github repo)](https://github.com/yuvipanda/jupyter-desktop-server/pull/22) ([@manics](https://github.com/manics), [@yuvipanda](https://github.com/yuvipanda), [@djangoliv](https://github.com/djangoliv), [@nthiery](https://github.com/nthiery))
- Use conda-forge/websockify, use environment.yml in Dockerfile [#21 (in previous github repo)](https://github.com/yuvipanda/jupyter-desktop-server/pull/21) ([@manics](https://github.com/manics), [@yuvipanda](https://github.com/yuvipanda))

#### Documentation improvements

- Fix typo [#24](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/24) ([@yuvipanda](https://github.com/yuvipanda), [@consideRatio](https://github.com/consideRatio))
- Add installation instructions [#21](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/21) ([@yuvipanda](https://github.com/yuvipanda), [@consideRatio](https://github.com/consideRatio))
- Add a section on limitations - OpenGL is currently not supported [#19](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/19) ([@yuvipanda](https://github.com/yuvipanda), [@consideRatio](https://github.com/consideRatio))

#### Continuous integration improvements

- ci: update outdated github actions [#23](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/23) ([@consideRatio](https://github.com/consideRatio), [@yuvipanda](https://github.com/yuvipanda))
- binder-badge workflow needs permissions.pull-requests:write [#9](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/9) ([@manics](https://github.com/manics))
- binder-badge workflow needs permissions.issues:write [#8](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/8) ([@manics](https://github.com/manics))
- Add binder-badge.yaml [#23 (in previous github repo)](https://github.com/yuvipanda/jupyter-desktop-server/pull/23) ([@manics](https://github.com/manics), [@yuvipanda](https://github.com/yuvipanda))

## v0.1

### v0.1.3 - 2020-07-07

- add Dockerfile and adjust readme to reflect a quick start [#19 (in previous github repo)](https://github.com/yuvipanda/jupyter-desktop-server/pull/19) ([@kniec](https://github.com/kniec), [@yuvipanda](https://github.com/yuvipanda))
- Start session from $HOME [#17 (in previous github repo)](https://github.com/yuvipanda/jupyter-desktop-server/pull/17) ([@mjuric](https://github.com/mjuric), [@yuvipanda](https://github.com/yuvipanda))
- add Dockerfile and adjust readme to reflect a quick start [#19 (in previous github repo)](https://github.com/yuvipanda/jupyter-desktop-server/pull/19) ([@kniec](https://github.com/kniec), [@yuvipanda](https://github.com/yuvipanda))
- Support jupyter-server-proxy >= 1.4.0 [daecbdb](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/commit/daecbdb) ([@yuvipanda](https://github.com/yuvipanda))
- Revert "Add a jupyter server extension to render desktop/" [b6dee24](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/commit/b6dee24) ([@yuvipanda](https://github.com/yuvipanda))
- Add a jupyter server extension to render desktop/ [18d7fb7](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/commit/18d7fb7) ([@yuvipanda](https://github.com/yuvipanda))
- Fix README to point to new name [bda9a7e](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/commit/bda9a7e) ([@yuvipanda](https://github.com/yuvipanda))
- Explicitly specify version of jupyter-server-proxy needed [98b7723](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/commit/98b7723) ([@yuvipanda](https://github.com/yuvipanda))
- Set CWD of desktop environment to CWD of notebook [360f9b0](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/commit/360f9b0) ([@yuvipanda](https://github.com/yuvipanda))

### v0.1.2 - 2019-11-12

- Fix cross-origin issue in Safari (#9, thanks to @eslavich)

### v0.1.1 - 2019-11-06

- Increase default resolution to 1680x1050. The wider screen
  matches how many user displays are, and there do not seem to
  be lag issues.

### v0.1 - 2019-11-01

- Initial release
