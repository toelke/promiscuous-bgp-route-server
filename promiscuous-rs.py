import eventlet

eventlet.monkey_patch()

import logging
import sys

if len(sys.argv) != 3:
    print(f"Please call as {sys.argv[0]} <peer-ip> <peer-as>")
    sys.exit(1)

log = logging.getLogger()
log.addHandler(logging.StreamHandler(sys.stderr))
log.setLevel(logging.DEBUG)

import ryu.services.protocols.bgp.bgpspeaker
from ryu.services.protocols.bgp.info_base.base import PrefixFilter
from ryu.lib.packet.bgp import BGP_CAP_FOUR_OCTET_AS_NUMBER

start_protocol_orig = ryu.services.protocols.bgp.core.CoreService.start_protocol


def start_protocol_patched(coreservice, socket):
    """When a neighbor connects that does not exist, quickly add it."""
    peer_addr, peer_port = coreservice.get_remotename(socket)
    peer = coreservice._peer_manager.get_by_addr(peer_addr)
    if not peer:
        # Use AS 1 for the peer, it will be fixed in validate_open_msg
        log.info(f'Adding peer {peer_addr}')
        s.neighbor_add(peer_addr, 1, is_route_server_client=True)
        s.in_filter_set(peer_addr, [PrefixFilter('0.0.0.0/0', PrefixFilter.POLICY_DENY)])
    start_protocol_orig(coreservice, socket)


ryu.services.protocols.bgp.core.CoreService.start_protocol = start_protocol_patched

validate_open_msg_orig = ryu.services.protocols.bgp.speaker.BgpProtocol._validate_open_msg


def validate_open_msg_patched(bgpprotocol, open_msg):
    """When the OPEN message is received, quickly change the peer AS."""
    opt_param_cap_map = open_msg.opt_param_cap_map
    cap4as = opt_param_cap_map.get(BGP_CAP_FOUR_OCTET_AS_NUMBER, None)
    if cap4as is None:
        log.info(f'fixing peer from {bgpprotocol._peer.remote_as} to {open_msg.my_as}')
        bgpprotocol._peer._neigh_conf._settings['remote_as'] = open_msg.my_as
    else:
        log.info(f'fixing peer from {bgpprotocol._peer.remote_as} to {cap4as.as_number}')
        bgpprotocol._peer._neigh_conf._settings['remote_as'] = cap4as.as_number
    validate_open_msg_orig(bgpprotocol, open_msg)


ryu.services.protocols.bgp.speaker.BgpProtocol._validate_open_msg = validate_open_msg_patched

s = ryu.services.protocols.bgp.bgpspeaker.BGPSpeaker(as_number=131072, router_id='10.0.0.3')
s.neighbor_add(sys.argv[1], sys.argv[2])
s.out_filter_set(sys.argv[1], [PrefixFilter('0.0.0.0/0', PrefixFilter.POLICY_DENY)])
while 1:
    eventlet.sleep(30)
