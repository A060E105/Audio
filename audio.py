import wave
from pyaudio import PyAudio, paInt16
from tqdm import trange
from argparse import ArgumentParser
import re

def command_args():
    parse = ArgumentParser(description='sound record program')
    parse.add_argument('-t', '--time', type=int, required=True, dest='time', help='set sound recording time, unit is second')
    parse.add_argument('-f', '--file-name', type=str, required=True, dest='filename', help='set output file name')
    args = parse.parse_args()
    return args

class Audio():
    def __init__(self, sec):
        self.second = sec + 1
        self._framerate = 44100
        self._NUM_SAMPLES = 1024
        self._channels = 1
        self._sampwidth = 2

    @property
    def time(self):
        return int( self._framerate / self._NUM_SAMPLES * self.second )

    @property
    def second(self):
        return self._second

    @second.setter
    def second(self, sec):
        self._second = sec

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, name):
        self._filename = name

    def record(self):
        if self.check_device():
            pa = PyAudio()
            stream = pa.open(format=paInt16,channels=self._channels,
            rate=self._framerate,input=True,
            input_device_index=self.__get_input_device(),
            frames_per_buffer=self._NUM_SAMPLES)
            my_buf = []
            for _ in trange(self.time):
                string_audio_data = stream.read(self._NUM_SAMPLES)
                my_buf.append(string_audio_data)
            self.save_wave(my_buf)
            stream.close()

    def play(self):
        print ('play wav file')
        pass

    def __get_input_device(self):
        p = PyAudio()
        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                # print ("input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0,i).get('name'))
                # print ((re.search('EZM-001', p.get_device_info_by_host_api_device_index(0, i).get('name'))) is not None)
                if ((re.search('EZM-001', p.get_device_info_by_host_api_device_index(0, i).get('name'))) is not None):
                    return i

    def check_device(self):
        if self.__get_input_device() is None:
            print ("Error: Not find your device")
            # return False
            # develop test
            return True
        else:
            return True

    def save_wave(self, data):
        wf = wave.open(self.filename + ".wav",'wb')
        wf.setnchannels(self._channels)
        wf.setsampwidth(self._sampwidth)
        wf.setframerate(self._framerate)
        wf.writeframes(b"".join(data))
        wf.close()

    def save_mp3(self):
        print ('save mp3')
        pass

    def save_spectrogram(self):
        pass

if __name__ == '__main__':
    args = command_args()
    au = Audio(args.time)
    au.filename = args.filename
    au.record()
    au.play()