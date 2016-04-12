#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Test Rx Time
# Generated: Sat Feb  1 15:40:15 2014
##################################################

from PyQt4 import Qt
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import pmt
import sys
import time

class test_rx_time(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Test Rx Time")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Test Rx Time")
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

        self.settings = Qt.QSettings("GNU Radio", "test_rx_time")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 500e3

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	device_addr="",
        	stream_args=uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(400e6, 0)
        self.uhd_usrp_source_0.set_gain(0, 0)
        self.digital_header_payload_demux_0 = digital.header_payload_demux(
        	  5,
        	  1,
        	  0,
        	  "frame_len",
        	  "",
        	  False,
        	  gr.sizeof_gr_complex,
        	  "rx_time",
                  int(samp_rate),
                  (),
            )
        self.blocks_vector_source_x_0 = blocks.vector_source_b((0, 0, 0, 1,) + (0,) * 9999, True, 1, [])
        self.blocks_tag_debug_0 = blocks.tag_debug(gr.sizeof_gr_complex*1, "Header Info", ""); self.blocks_tag_debug_0.set_display(True)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.from_long(100), 10)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.uhd_usrp_source_0, 0), (self.digital_header_payload_demux_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.digital_header_payload_demux_0, 1))
        self.connect((self.digital_header_payload_demux_0, 0), (self.blocks_tag_debug_0, 0))
        self.connect((self.digital_header_payload_demux_0, 1), (self.blocks_null_sink_0, 0))

        ##################################################
        # Asynch Message Connections
        ##################################################
        self.msg_connect(self.blocks_message_strobe_0, "strobe", self.digital_header_payload_demux_0, "header_data")

# QT sink close method reimplementation
    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "test_rx_time")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

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
    tb = test_rx_time()
    tb.start()
    tb.show()
    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
    tb = None #to clean up Qt widgets

