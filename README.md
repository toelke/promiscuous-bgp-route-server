A hacky script based on [ryu](https://ryu.readthedocs.io/en/latest/library_bgp_speaker.html) that connects to a BGP route server and replicates all its routes. It automatically peers with every peer connecting to it.

Run with

```
python promiscuous-rs.py <upstream-route-server-ip> <upstream-route-server-as>
```
