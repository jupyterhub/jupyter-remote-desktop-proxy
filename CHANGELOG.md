# Changelog

## v1.0.0 - 2023-01-19

With this release, the project has relocated from `jupyter-desktop-server` to
`jupyter-remote-desktop-proxy` and relocated from
[yuvipanda/jupyter-desktop-server](https://github.com/yuvipanda/jupyter-desktop-server) to
[jupyterhub/jupyter-remote-desktop-proxy](https://github.com/jupyterhub/jupyter-remote-desktop-proxy).

### New features added

- Add a shared clipboard [#10](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/10) ([@manics](https://github.com/manics), [@yuvipanda](https://github.com/yuvipanda), [@satra](https://github.com/satra), [@fperez](https://github.com/fperez))

### Enhancements made

- Use TurboVNC if installed [#29 (in previous github repo)](https://github.com/yuvipanda/jupyter-desktop-server/pull/29) ([@manics](https://github.com/manics), [@yuvipanda](https://github.com/yuvipanda), [@cslocum](https://github.com/cslocum))

### Maintenance and upkeep improvements

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

### Documentation improvements

- Fix typo [#24](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/24) ([@yuvipanda](https://github.com/yuvipanda), [@consideRatio](https://github.com/consideRatio))
- Add installation instructions [#21](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/21) ([@yuvipanda](https://github.com/yuvipanda), [@consideRatio](https://github.com/consideRatio))
- Add a section on limitations - OpenGL is currently not supported [#19](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/19) ([@yuvipanda](https://github.com/yuvipanda), [@consideRatio](https://github.com/consideRatio))

### Continuous integration improvements

- ci: update outdated github actions [#23](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/23) ([@consideRatio](https://github.com/consideRatio), [@yuvipanda](https://github.com/yuvipanda))
- binder-badge workflow needs permissions.pull-requests:write [#9](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/9) ([@manics](https://github.com/manics))
- binder-badge workflow needs permissions.issues:write [#8](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/pull/8) ([@manics](https://github.com/manics))
- Add binder-badge.yaml [#23 (in previous github repo)](https://github.com/yuvipanda/jupyter-desktop-server/pull/23) ([@manics](https://github.com/manics), [@yuvipanda](https://github.com/yuvipanda))

## v0.1.3 - 2020-07-07

- add Dockerfile and adjust readme to reflect a quick start [#19 (in previous github repo)](https://github.com/yuvipanda/jupyter-desktop-server/pull/19) ([@kniec](https://github.com/kniec), [@yuvipanda](https://github.com/yuvipanda))
- Start session from $HOME [#17 (in previous github repo)](https://github.com/yuvipanda/jupyter-desktop-server/pull/17) ([@mjuric](https://github.com/mjuric), [@yuvipanda](https://github.com/yuvipanda))
- add Dockerfile and adjust readme to reflect a quick start [#19 (in previous github repo)](https://github.com/yuvipanda/jupyter-desktop-server/pull/19) ([@kniec](https://github.com/kniec), [@yuvipanda](https://github.com/yuvipanda))
- Support jupyter-server-proxy >= 1.4.0 [daecbdb](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/commit/daecbdb) ([@yuvipanda](https://github.com/yuvipanda))
- Revert "Add a jupyter server extension to render desktop/" [b6dee24](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/commit/b6dee24) ([@yuvipanda](https://github.com/yuvipanda))
- Add a jupyter server extension to render desktop/ [18d7fb7](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/commit/18d7fb7) ([@yuvipanda](https://github.com/yuvipanda))
- Fix README to point to new name [bda9a7e](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/commit/bda9a7e) ([@yuvipanda](https://github.com/yuvipanda))
- Explicitly specify version of jupyter-server-proxy needed [98b7723](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/commit/98b7723) ([@yuvipanda](https://github.com/yuvipanda))
- Set CWD of desktop environment to CWD of notebook [360f9b0](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/commit/360f9b0) ([@yuvipanda](https://github.com/yuvipanda))

## v0.1.2 - 2019-11-12

- Fix cross-origin issue in Safari (#9, thanks to @eslavich)

## v0.1.1 - 2019-11-06

- Increase default resolution to 1680x1050. The wider screen
  matches how many user displays are, and there do not seem to
  be lag issues.

## v0.1 - 2019-11-01

- Initial release
