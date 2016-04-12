#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Ofdm Rx
# Generated: Sun Feb  2 13:09:58 2014
##################################################

from PyQt4 import Qt
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import osmosdr
import sip
import sys

class ofdm_rx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Ofdm Rx")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Ofdm Rx")
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

        self.settings = Qt.QSettings("GNU Radio", "ofdm_rx")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.tune_offset = tune_offset = 500e3
        self.samp_rate = samp_rate = 500000
        self.len_tag_key = len_tag_key = "packet_len"
        self.fft_len = fft_len = 128
        self.decimation = decimation = 4

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
        	1024, #size
        	samp_rate, #samp_rate
        	"QT GUI Plot", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)
        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_TAG, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "rx_len")
        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"QT GUI Plot", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.osmosdr_source_0.set_sample_rate(samp_rate*decimation)
        self.osmosdr_source_0.set_center_freq(400e6-tune_offset, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(0, 0)
        self.osmosdr_source_0.set_gain(10, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna("", 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
          
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(decimation, (firdes.low_pass(1.0, samp_rate*decimation, 300e3, 100e3)), tune_offset, samp_rate*decimation)
        self.digital_ofdm_rx_0 = digital.ofdm_rx(
        	  fft_len=fft_len, cp_len=fft_len/4,
        	  frame_length_tag_key='frame_'+"rx_len",
        	  packet_length_tag_key="rx_len",
        	  bps_header=1,
        	  bps_payload=2,
        	  debug_log=False,
        	  scramble_bits=True
        	 )
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_tag_debug_0 = blocks.tag_debug(gr.sizeof_char*1, "Rx Packets", ""); self.blocks_tag_debug_0.set_display(True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_uchar_to_float_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.digital_ofdm_rx_0, 0))
        self.connect((self.digital_ofdm_rx_0, 0), (self.blocks_uchar_to_float_0, 0))
        self.connect((self.digital_ofdm_rx_0, 0), (self.blocks_tag_debug_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))


# QT sink close method reimplementation
    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ofdm_rx")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_tune_offset(self):
        return self.tune_offset

    def set_tune_offset(self, tune_offset):
        self.tune_offset = tune_offset
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.tune_offset)
        self.osmosdr_source_0.set_center_freq(400e6-self.tune_offset, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1.0, self.samp_rate*self.decimation, 300e3, 100e3)))
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate*self.decimation)

    def get_len_tag_key(self):
        return self.len_tag_key

    def set_len_tag_key(self, len_tag_key):
        self.len_tag_key = len_tag_key

    def get_fft_len(self):
        return self.fft_len

    def set_fft_len(self, fft_len):
        self.fft_len = fft_len

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1.0, self.samp_rate*self.decimation, 300e3, 100e3)))
        self.osmosdr_source_0.set_sample_rate(self.samp_rate*self.decimation)

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    qapp = Qt.QApplication(sys.argv)
    tb = ofdm_rx()
    tb.start()
    tb.show()
    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
    tb = None #to clean up Qt widgets

