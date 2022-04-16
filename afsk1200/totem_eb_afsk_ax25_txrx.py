#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: TOTEM Emb. AFSK1200 TX/RX
# Author: José Miguel Lago, Diego Hurtado de Mendoza
# Copyright: Alén Space S.L. (2021)
# Description: AX.25 AFSK1200
# GNU Radio version: 3.8.1.0

from gnuradio import analog
import math
from gnuradio import blocks
import pmt
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import ax25_aprs
import epy_block_1
import epy_block_1_0
import soapy
import distutils
from distutils import util
import string_to_uint8_0


class totem_eb_afsk_ax25_txrx(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "TOTEM Emb. AFSK1200 TX/RX")

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 32
        self.baudrate = baudrate = 1200
        self.samp_rate = samp_rate = sps*baudrate
        self.preamble_len = preamble_len = 50
        self.postamble_len = postamble_len = 3
        self.hostname = hostname = ""
        self.variable_low_pass_filter_taps_0 = variable_low_pass_filter_taps_0 = firdes.low_pass(1.0, samp_rate, 500,1.5e3, firdes.WIN_KAISER, 6.76)
        self.tag_preamble = tag_preamble = gr.tag_utils.python_to_tag((0, pmt.intern("packet_len"), pmt.from_long(preamble_len*8), pmt.from_bool(False)))
        self.tag_postamble = tag_postamble = gr.tag_utils.python_to_tag((0, pmt.intern("packet_len"), pmt.from_long(postamble_len*8), pmt.from_bool(False)))
        self.soapy_dev = soapy_dev = "driver=totem" + (f",hostname={hostname}" if hostname else "")
        self.freq = freq = 434e6
        self.channel_rate = channel_rate = 4*samp_rate

        ##################################################
        # Blocks
        ##################################################
        self.xlating_fire = filter.freq_xlating_fir_filter_fcf(1, variable_low_pass_filter_taps_0, 1700, samp_rate)
        self.string_to_uint8_0 = string_to_uint8_0.blk()
        self.soapy_source_0 = None
        # Make sure that the gain mode is valid
        if('Overall' not in ['Overall', 'Specific', 'Settings Field']):
            raise ValueError("Wrong gain mode on channel 0. Allowed gain modes: "
                  "['Overall', 'Specific', 'Settings Field']")

        dev = soapy_dev

        # Stream arguments for every activated stream
        tune_args = ['']
        settings = ['']

        # Setup the device arguments
        dev_args = ''

        self.soapy_source_0 = soapy.source(1, dev, dev_args, 'bufflen=10000',
                                  tune_args, settings, channel_rate, "fc32")



        self.soapy_source_0.set_dc_removal(0,bool(distutils.util.strtobool('True')))

        # Set up DC offset. If set to (0, 0) internally the source block
        # will handle the case if no DC offset correction is supported
        self.soapy_source_0.set_dc_offset(0,0)

        # Setup IQ Balance. If set to (0, 0) internally the source block
        # will handle the case if no IQ balance correction is supported
        self.soapy_source_0.set_iq_balance(0,0)

        self.soapy_source_0.set_agc(0,False)

        # generic frequency setting should be specified first
        self.soapy_source_0.set_frequency(0, freq)

        self.soapy_source_0.set_frequency(0,"BB",0)

        # Setup Frequency correction. If set to 0 internally the source block
        # will handle the case if no frequency correction is supported
        self.soapy_source_0.set_frequency_correction(0,0)

        self.soapy_source_0.set_antenna(0,'A_BALANCED')

        self.soapy_source_0.set_bandwidth(0,200e3)

        if('Overall' != 'Settings Field'):
            # pass is needed, in case the template does not evaluare anything
            pass
            self.soapy_source_0.set_gain(0,50)
        self.soapy_sink_0 = None
        if "custom" == 'custom':
            dev = soapy_dev
            devname = dev.split("=", 1)[1]
        else:
            dev = 'driver=' + "custom"
            devname = "custom"

        self.soapy_sink_0 = soapy.sink(1, dev, 'bufflen=100000', channel_rate, "fc32", 'packet_len')

        self.soapy_sink_0.set_gain_mode(0,False)
        self.soapy_sink_0.set_gain_mode(1,False)

        self.soapy_sink_0.set_frequency(0, freq)
        self.soapy_sink_0.set_frequency(1, 100.0e6)

        # Made antenna sanity check more generic
        antList = self.soapy_sink_0.listAntennas(0)

        if len(antList) > 1:
            # If we have more than 1 possible antenna
            if len('A') == 0 or 'A' not in antList:
                print("ERROR: Please define ant0 to an allowed antenna name.")
                strAntList = str(antList).lstrip('(').rstrip(')').rstrip(',')
                print("Allowed antennas: " + strAntList)
                exit(0)

            self.soapy_sink_0.set_antenna(0,'A')

        if 1 > 1:
            antList = self.soapy_sink_0.listAntennas(1)
            # If we have more than 1 possible antenna
            if len(antList) > 1:
                if len('TX') == 0 or 'TX' not in antList:
                    print("ERROR: Please define ant1 to an allowed antenna name.")
                    strAntList = str(antList).lstrip('(').rstrip(')').rstrip(',')
                    print("Allowed antennas: " + strAntList)
                    exit(0)

                self.soapy_sink_0.set_antenna(1,'TX')

        # Setup IQ Balance
        if devname != 'uhd' and devname != 'lime':
            if (self.soapy_sink_0.IQ_balance_support(0)):
                self.soapy_sink_0.set_iq_balance(0,0)

            if (self.soapy_sink_0.IQ_balance_support(1)):
                self.soapy_sink_0.set_iq_balance(1,0)

        # Setup Frequency correction
        if (self.soapy_sink_0.freq_correction_support(0)):
            self.soapy_sink_0.set_frequency_correction(0,0)

        if (self.soapy_sink_0.freq_correction_support(1)):
            self.soapy_sink_0.set_frequency_correction(1,0)

        if devname == 'sidekiq' or "False" == 'False':
            self.soapy_sink_0.set_gain(0,89)
            self.soapy_sink_0.set_gain(1,0)
        else:
            if devname == 'bladerf':
                 self.soapy_sink_0.set_gain(0,"txvga1", -35)
                 self.soapy_sink_0.set_gain(0,"txvga2", 0)
            elif devname == 'uhd':
                self.soapy_sink_0.set_gain(0,"PGA", 24)
                self.soapy_sink_0.set_gain(1,"PGA", 0)
            else:
                 self.soapy_sink_0.set_gain(0,"PGA", 24)
                 self.soapy_sink_0.set_gain(1,"PGA", 0)
                 self.soapy_sink_0.set_gain(0,"PAD", 0)
                 self.soapy_sink_0.set_gain(1,"PAD", 0)
                 self.soapy_sink_0.set_gain(0,"IAMP", 0)
                 self.soapy_sink_0.set_gain(1,"IAMP", 0)
                 self.soapy_sink_0.set_gain(0,"txvga1", -35)
                 self.soapy_sink_0.set_gain(0,"txvga2", 0)
                 # Only hackrf uses VGA name, so just ch0
                 self.soapy_sink_0.set_gain(0,"VGA", 10)
        self.low_pass_filter_1 = filter.interp_fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                baudrate,
                baudrate/2,
                firdes.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                channel_rate,
                15000,
                30000,
                firdes.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                channel_rate,
                15e3,
                30e3,
                firdes.WIN_HAMMING,
                6.76))
        self.epy_block_1_0 = epy_block_1_0.blk()
        self.epy_block_1 = epy_block_1.blk()
        self.digital_symbol_sync_xx_0 = digital.symbol_sync_ff(
            digital.TED_SIGNAL_TIMES_SLOPE_ML,
            sps,
            6*0.045,
            1.0,
            1.0,
            0.01,
            1,
            digital.constellation_bpsk().base(),
            digital.IR_MMSE_8TAP,
            128,
            [])
        self.digital_hdlc_framer_pb_0 = digital.hdlc_framer_pb('packet_len')
        self.digital_hdlc_deframer_bp_0 = digital.hdlc_deframer_bp(10, 500)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bf((1200, 2200), 1)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_vector_source_x_0_0 = blocks.vector_source_b(postamble_len*[1,0,1,0,1,0,1,0], True, 1, [tag_postamble])
        self.blocks_vector_source_x_0 = blocks.vector_source_b(preamble_len*[1,0,1,0,1,0,1,0], True, 1, [ tag_preamble ])
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_char*1, 'packet_len', 0)
        self.blocks_tagged_stream_multiply_length_0 = blocks.tagged_stream_multiply_length(gr.sizeof_gr_complex*1, 'packet_len', channel_rate/baudrate)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_float*1, sps)
        self.blocks_message_strobe_1_0 = blocks.message_strobe(pmt.intern("Hello World"), 2000)
        self.blocks_message_debug_1 = blocks.message_debug()
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.ax25_aprs = ax25_aprs.blk(source="ZZZZZZ", destination="ZZZZZZ", path="ZZZZZZ", verbose=0)
        self.analog_rail_ff_0 = analog.rail_ff(-1, 1)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(2*sps / (2*math.pi))
        self.analog_nbfm_tx_0 = analog.nbfm_tx(
        	audio_rate=sps*baudrate,
        	quad_rate=channel_rate,
        	tau=75e-6,
        	max_dev=3e3,
        	fh=-1.0,
                )
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=int(samp_rate),
        	quad_rate=channel_rate,
        	tau=75e-6,
        	max_dev=3e3,
          )
        self.analog_frequency_modulator_fc_0 = analog.frequency_modulator_fc(2*math.pi/(baudrate * sps))



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.ax25_aprs, 'out'), (self.digital_hdlc_framer_pb_0, 'in'))
        self.msg_connect((self.blocks_message_strobe_1_0, 'strobe'), (self.string_to_uint8_0, 'message_in'))
        self.msg_connect((self.digital_hdlc_deframer_bp_0, 'out'), (self.blocks_message_debug_1, 'print_pdu'))
        self.msg_connect((self.string_to_uint8_0, 'message_out'), (self.ax25_aprs, 'in'))
        self.connect((self.analog_frequency_modulator_fc_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.analog_nbfm_rx_0, 0), (self.xlating_fire, 0))
        self.connect((self.analog_nbfm_tx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.low_pass_filter_1, 0))
        self.connect((self.analog_rail_ff_0, 0), (self.digital_symbol_sync_xx_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.analog_nbfm_tx_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.analog_frequency_modulator_fc_0, 0))
        self.connect((self.blocks_tagged_stream_multiply_length_0, 0), (self.soapy_sink_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_tagged_stream_mux_0, 0))
        self.connect((self.blocks_vector_source_x_0_0, 0), (self.blocks_tagged_stream_mux_0, 2))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.epy_block_1_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.digital_hdlc_framer_pb_0, 0), (self.epy_block_1, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.epy_block_1, 0), (self.blocks_tagged_stream_mux_0, 1))
        self.connect((self.epy_block_1_0, 0), (self.digital_hdlc_deframer_bp_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_tagged_stream_multiply_length_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.analog_nbfm_rx_0, 0))
        self.connect((self.low_pass_filter_1, 0), (self.analog_rail_ff_0, 0))
        self.connect((self.soapy_source_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.xlating_fire, 0), (self.analog_quadrature_demod_cf_0, 0))


    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_samp_rate(self.sps*self.baudrate)
        self.analog_frequency_modulator_fc_0.set_sensitivity(2*math.pi/(self.baudrate * self.sps))
        self.analog_quadrature_demod_cf_0.set_gain(2*self.sps / (2*math.pi))
        self.blocks_repeat_0.set_interpolation(self.sps)

    def get_baudrate(self):
        return self.baudrate

    def set_baudrate(self, baudrate):
        self.baudrate = baudrate
        self.set_samp_rate(self.sps*self.baudrate)
        self.analog_frequency_modulator_fc_0.set_sensitivity(2*math.pi/(self.baudrate * self.sps))
        self.blocks_tagged_stream_multiply_length_0.set_scalar(self.channel_rate/self.baudrate)
        self.low_pass_filter_1.set_taps(firdes.low_pass(1, self.samp_rate, self.baudrate, self.baudrate/2, firdes.WIN_HAMMING, 6.76))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_channel_rate(4*self.samp_rate)
        self.low_pass_filter_1.set_taps(firdes.low_pass(1, self.samp_rate, self.baudrate, self.baudrate/2, firdes.WIN_HAMMING, 6.76))

    def get_preamble_len(self):
        return self.preamble_len

    def set_preamble_len(self, preamble_len):
        self.preamble_len = preamble_len
        self.set_tag_preamble(gr.tag_utils.python_to_tag((0, pmt.intern("packet_len"), pmt.from_long(self.preamble_len*8), pmt.from_bool(False))))
        self.blocks_vector_source_x_0.set_data(self.preamble_len*[1,0,1,0,1,0,1,0], [ self.tag_preamble ])

    def get_postamble_len(self):
        return self.postamble_len

    def set_postamble_len(self, postamble_len):
        self.postamble_len = postamble_len
        self.set_tag_postamble(gr.tag_utils.python_to_tag((0, pmt.intern("packet_len"), pmt.from_long(self.postamble_len*8), pmt.from_bool(False))))
        self.blocks_vector_source_x_0_0.set_data(self.postamble_len*[1,0,1,0,1,0,1,0], [self.tag_postamble])

    def get_hostname(self):
        return self.hostname

    def set_hostname(self, hostname):
        self.hostname = hostname
        self.set_soapy_dev("driver=totem" + (f",hostname={hostname}" if self.hostname else ""))

    def get_variable_low_pass_filter_taps_0(self):
        return self.variable_low_pass_filter_taps_0

    def set_variable_low_pass_filter_taps_0(self, variable_low_pass_filter_taps_0):
        self.variable_low_pass_filter_taps_0 = variable_low_pass_filter_taps_0
        self.xlating_fire.set_taps(self.variable_low_pass_filter_taps_0)

    def get_tag_preamble(self):
        return self.tag_preamble

    def set_tag_preamble(self, tag_preamble):
        self.tag_preamble = tag_preamble
        self.blocks_vector_source_x_0.set_data(self.preamble_len*[1,0,1,0,1,0,1,0], [ self.tag_preamble ])

    def get_tag_postamble(self):
        return self.tag_postamble

    def set_tag_postamble(self, tag_postamble):
        self.tag_postamble = tag_postamble
        self.blocks_vector_source_x_0_0.set_data(self.postamble_len*[1,0,1,0,1,0,1,0], [self.tag_postamble])

    def get_soapy_dev(self):
        return self.soapy_dev

    def set_soapy_dev(self, soapy_dev):
        self.soapy_dev = soapy_dev

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.soapy_sink_0.set_frequency(0, self.freq)
        self.soapy_source_0.set_frequency(0, self.freq)

    def get_channel_rate(self):
        return self.channel_rate

    def set_channel_rate(self, channel_rate):
        self.channel_rate = channel_rate
        self.blocks_tagged_stream_multiply_length_0.set_scalar(self.channel_rate/self.baudrate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.channel_rate, 15e3, 30e3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.channel_rate, 15000, 30000, firdes.WIN_HAMMING, 6.76))





def main(top_block_cls=totem_eb_afsk_ax25_txrx, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
