#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Ofdm Tx Doesntwork
# Generated: Sun Feb  2 12:49:01 2014
##################################################

from PyQt4 import Qt
from PyQt4.QtCore import QObject, pyqtSlot
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import PyQt4.Qwt5 as Qwt
import sip
import sys

class ofdm_tx_doesntwork(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Ofdm Tx Doesntwork")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Ofdm Tx Doesntwork")
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

        self.settings = Qt.QSettings("GNU Radio", "ofdm_tx_doesntwork")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1e6
        self.packet_len = packet_len = 100
        self.len_tag_key = len_tag_key = "packet_len"
        self.gain = gain = 60
        self.fft_len = fft_len = 128

        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=2,
                decimation=1,
                taps=None,
                fractional_bw=None,
        )
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
        	1024, #size
        	samp_rate, #samp_rate
        	"QT GUI Plot", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)
        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self._gain_layout = Qt.QVBoxLayout()
        self._gain_tool_bar = Qt.QToolBar(self)
        self._gain_layout.addWidget(self._gain_tool_bar)
        self._gain_tool_bar.addWidget(Qt.QLabel("gain"+": "))
        class qwt_counter_pyslot(Qwt.QwtCounter):
            def __init__(self, parent=None):
                Qwt.QwtCounter.__init__(self, parent)
            @pyqtSlot('double')
            def setValue(self, value):
                super(Qwt.QwtCounter, self).setValue(value)
        self._gain_counter = qwt_counter_pyslot()
        self._gain_counter.setRange(0, 90, 1)
        self._gain_counter.setNumButtons(2)
        self._gain_counter.setValue(self.gain)
        self._gain_tool_bar.addWidget(self._gain_counter)
        self._gain_counter.valueChanged.connect(self.set_gain)
        self._gain_slider = Qwt.QwtSlider(None, Qt.Qt.Horizontal, Qwt.QwtSlider.BottomScale, Qwt.QwtSlider.BgSlot)
        self._gain_slider.setRange(0, 90, 1)
        self._gain_slider.setValue(self.gain)
        self._gain_slider.setMinimumWidth(200)
        self._gain_slider.valueChanged.connect(self.set_gain)
        self._gain_layout.addWidget(self._gain_slider)
        self.top_layout.addLayout(self._gain_layout)
        self.digital_ofdm_tx_0 = digital.ofdm_tx(
        	  fft_len=fft_len, cp_len=fft_len/4,
        	  packet_length_tag_key=len_tag_key,
        	  bps_header=1,
        	  bps_payload=2,
        	  rolloff=0,
        	  debug_log=False,
        	  scramble_bits=True
        	 )
        self.blocks_vector_source_x_0 = blocks.vector_source_b(range(packet_len), True, 1, ())
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, packet_len, len_tag_key)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.digital_ofdm_tx_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.digital_ofdm_tx_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_time_sink_x_0, 0))


# QT sink close method reimplementation
    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ofdm_tx_doesntwork")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_packet_len(self):
        return self.packet_len

    def set_packet_len(self, packet_len):
        self.packet_len = packet_len

    def get_len_tag_key(self):
        return self.len_tag_key

    def set_len_tag_key(self, len_tag_key):
        self.len_tag_key = len_tag_key

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        Qt.QMetaObject.invokeMethod(self._gain_counter, "setValue", Qt.Q_ARG("double", self.gain))
        Qt.QMetaObject.invokeMethod(self._gain_slider, "setValue", Qt.Q_ARG("double", self.gain))

    def get_fft_len(self):
        return self.fft_len

    def set_fft_len(self, fft_len):
        self.fft_len = fft_len

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
    tb = ofdm_tx_doesntwork()
    tb.start()
    tb.show()
    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
    tb = None #to clean up Qt widgets

