Findings:
- Listens to either localhost or public by default
- Different flags needs to be used
  - Tiger's default from local can be changed with "-localhost no --I-KNOW-THIS-IS-INSECURE"
  - Turbo's default from public can be changed with "-localhost"
- Connecting from inside a container is to connect from 127.0.0.1, but outside
  is to connect from 172 at least on my computer's docker network, which means
  that we can be influenced by this when testing.
- When websockify is involved, it intercepts an old_port to be bound to
  localhost:new_port, making initially listening to 0.0.0.0 irrelevant.
- Connecting via jupyter-server-proxy often require a second attempt, likely due
  to https://github.com/jupyterhub/jupyter-server-proxy/issues/459 and letting a
  websocket handshake finalize before its finalized against the proxied backend.
