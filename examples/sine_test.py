#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Sine test
# GNU Radio version: 3.8.1.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
import soapy

from gnuradio import qtgui

class sine_test(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Sine test")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Sine test")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "sine_test")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.hostname = hostname = "10.42.0.100"
        self.soapy_dev = soapy_dev = "driver=totem" + (f",hostname={hostname}" if hostname else "")
        self.samp_rate = samp_rate = 100e3
        self.freq_range = freq_range = 10000

        ##################################################
        # Blocks
        ##################################################
        self._freq_range_range = Range(-60000, 60000, 500, 10000, 200)
        self._freq_range_win = RangeWidget(self._freq_range_range, self.set_freq_range, 'Freq', "counter_slider", int)
        self.top_grid_layout.addWidget(self._freq_range_win)
        self.soapy_sink_0 = None
        if "custom" == 'custom':
            dev = soapy_dev
            devname = dev.split("=", 1)[1]
        else:
            dev = 'driver=' + "custom"
            devname = "custom"

        self.soapy_sink_0 = soapy.sink(1, dev, '', samp_rate, "fc32", '')

        self.soapy_sink_0.set_gain_mode(0,False)
        self.soapy_sink_0.set_gain_mode(1,False)

        self.soapy_sink_0.set_frequency(0, 408.0e6)
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
            self.soapy_sink_0.set_gain(0,76)
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
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            2048, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "TX", #name
            1
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, freq_range, 0.7, 0, 0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.soapy_sink_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "sine_test")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_hostname(self):
        return self.hostname

    def set_hostname(self, hostname):
        self.hostname = hostname
        self.set_soapy_dev("driver=totem" + (f",hostname={hostname}" if self.hostname else ""))

    def get_soapy_dev(self):
        return self.soapy_dev

    def set_soapy_dev(self, soapy_dev):
        self.soapy_dev = soapy_dev

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_freq_range(self):
        return self.freq_range

    def set_freq_range(self, freq_range):
        self.freq_range = freq_range
        self.analog_sig_source_x_0.set_frequency(self.freq_range)





def main(top_block_cls=sine_test, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
