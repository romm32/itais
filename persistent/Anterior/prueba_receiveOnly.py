#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#   The REQest / REPly nomenclature of the GNU Radio message blocks is from
#   the perspective of the flowgraph. So, to send a 'request' to GNU Radio, the message
#   must be sent as a 'reply' from the Python client, Likewise, a 'reply' from GNU Radio
#   must be received as a 'request' to the Python client! Therefore, send on the reply socket
#   and receive on the request socket.
#
#   The zeromq.org website says:
#   "The REQ-REP socket pair is in lockstep. The client issues zmq_send() and then zmq_recv(),
#   in a loop (or once if that's all it needs). Doing any other sequence (e.g., sending two messages in a row)
#   will result in a return code of -1 from the send or recv call." Likewise, the server "issues zmq_recv() 
#   and then zmq_send() in that order, as often as it needs to."
#
#   To conform to that requirement, a non-standard "kludge" is used (see below).

import zmq
import pmt

def main():
    zmq_context = zmq.Context()
    zmq_sock = zmq_context.socket(zmq.REQ)
    zmq_sock.connect("tcp://127.0.0.1:50247")
    while(True):
         zmq_sock.send_string("\x01\x00\x00\x00")    # this is the non-standard "kludge"
         msg = zmq_sock.recv()
         print (pmt.to_python(pmt.deserialize_str(msg)))
if __name__ == '__main__':
    main()
