"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt
import array


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    
    """APRS AX.25 header

Source and Destination must be length 6 (add padding spaces to fill)
Path can be up to 8 digipeaters (6 bytes each one)

The input expects a uint8 vector of ascii chars as payload to the APRS packet.
    """


    def __init__(self, source="AAAAAA", destination="BBBBBB", path="", verbose=False):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""

        gr.sync_block.__init__(
            self,
            name='APRS AX.25 header',   # will show up in GRC
            in_sig=[],
            out_sig=[]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).

        self.verbose = verbose
        self.source = source
        self.destination = destination
        self.path = path

        # Register PMT ports
        self.message_port_register_in(pmt.intern("in"))
        self.message_port_register_out(pmt.intern("out"))

        # Register callback for input messages
        self.set_msg_handler(pmt.intern("in"), self.handle_msg)


    def handle_msg(self, pmt_msg):

        # Take pmt contents
        msg = pmt.cdr(pmt_msg)

        if not pmt.is_u8vector(msg):
            print ("[ERROR] Received invalid message type. Expected u8vector")
            return

        # Check arguments
        if len(self.source) != 6 or len(self.destination) != 6:
            print ("[ERROR] Check length of source/destination (length = 6)")
            return

        if (len(self.path) > 48):
            print ("[ERROR] Check length of path (max. length 48 chars)")
            return

        if self.path != "":
            path = np.fromstring(self.path, dtype='uint8')


        # Conversion to numpy bytes array
        payload = np.array(pmt.u8vector_elements(msg), dtype = 'uint8')

        # Add ProtocolID (0xF0)
        pid = np.array(0xF0,dtype='uint8')
        payload = np.insert(payload,0,pid)

        # Add Control Field (0x03)
        cf = np.array(0x03,dtype='uint8')
        payload = np.insert(payload,0,cf)

        # Add Digipeater addresses
        if self.path:
            # Encode SSID (1 lsb due to last address field)
            path = path << 1 | 0x80
            payload = np.insert(payload,0,path)

        # Add Source Address
        # Encode SSID (0 lsb since is not the last address field)
        source = np.fromstring(self.source, dtype='uint8') << 1 | 0x60
        payload = np.insert(payload,0,source)

        # Add Destination Address
        # Encode SSID (0 lsb since is not the last address field)
        destination = np.fromstring(self.destination, dtype='uint8') << 1 | 0x60
        payload = np.insert(payload,0,destination)


        # Back to bytes array
        aprs_packet_bytes = array.array('B', payload)

        # Publish aprs packet as pmt
        self.message_port_pub(
            pmt.intern('out'),
            pmt.cons(
                pmt.car(pmt_msg),
                pmt.init_u8vector(
                    len(aprs_packet_bytes),
                    aprs_packet_bytes
                )
            )
        )

        if self.verbose:
            print ("Source: "+self.source+"  Destination: "+self.destination+"  Path: "+self.path)
            print ("APRS Packet: ")
            print (aprs_packet_bytes)
            print ("\n")


    def work(self, input_items, output_items):
        # No samples to process
        pass
