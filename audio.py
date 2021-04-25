import wave
from pyaudio import PyAudio, paInt16
from tqdm import trange
from argparse import ArgumentParser
from os import path
from pydub import AudioSegment
import json
import re
import Settings

def command_args():
    parse = ArgumentParser(description='sound record program')
    parse.add_argument('-t', '--time', type=int, required=True, dest='time', help='set sound recording time, unit is second')
    parse.add_argument('-o', '--output-name', type=str, required=True, dest='filename', help='set output file name')
    parse.add_argument('-f', '--framerate', type=int, choices=range(1000, 100000), metavar='[1000-100000]', dest='framerate', help='set recording framerate')
    args = parse.parse_args()
    return args

class Audio():
    def __init__(self, sec):
        self.second = sec + 1
        self.init_audio_argument()
        self.init_settings()

    def init_audio_argument(self):
        self.framerate = 44100
        self.num_samples = 1024
        self.channels = 2
        self.sampwidth = 2

    def init_settings(self):
        self.__sf = Settings.Settings('audio.settings')
        if self.__sf.hasSettings():
            self.get_settings()
        else:
            self.set_settings()

    def set_settings(self):
        self.__sf.setTitle('settings')
        self.__sf.setSettings('settings', framerate=self.framerate, num_samples=self.num_samples, channels=self.channels, sampwidth=self.sampwidth)
        self.__sf.save()

    def get_settings(self):
        data = self.__sf.getSettings('settings')
        self.framerate = data['framerate']
        self.num_samples = data['num_samples']
        self.channels = data['channels']
        self.sampwidth = data['sampwidth']

    @property
    def framerate(self):
        return self.__framerate

    @framerate.setter
    def framerate(self, value):
        if value >= 4000:
            self.__framerate = value
        else:
            raise ValueError("framerate value can't below 4000")

    @property
    def num_samples(self):
        return self.__num_samples

    @num_samples.setter
    def num_samples(self, value):
        if value >= 0:
            self.__num_samples = value
        else:
            raise ValueError("number samples can't below 0")

    @property
    def channels(self):
        return self.__channels

    @channels.setter
    def channels(self, value):
        if value == 1 or value == 2:
            self.__channels = value
        else:
            raise ValueError("channels value with 1 or 2")

    @property
    def sampwidth(self):
        return self.__sampwidth

    @sampwidth.setter
    def sampwidth(self, value):
        if value > 0:
            self.__sampwidth = value
        else:
            raise ValueError("sampwidth value can't below 0")

    @property
    def time(self):
        return int( self.framerate / self.num_samples * self.second )

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
        if self.hasDevice():
            pa = PyAudio()
            stream = pa.open(format=paInt16,channels=self.channels,
            rate=self.framerate,input=True,
            input_device_index=self.__getDevice(),
            frames_per_buffer=self.num_samples)
            my_buf = []
            for _ in trange(self.time):
                string_audio_data = stream.read(self.num_samples)
                my_buf.append(string_audio_data)
            self.save_wave(my_buf)
            stream.close()

    def play(self):
        print ('play wav file')
        pass

    def __getDevice(self):
        p = PyAudio()
        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                # print ("input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0,i).get('name'))
                # print ((re.search('EZM-001', p.get_device_info_by_host_api_device_index(0, i).get('name'))) is not None)
                if ((re.search('EZM-001', p.get_device_info_by_host_api_device_index(0, i).get('name'))) is not None):
                    return i

    def hasDevice(self):
        if self.__getDevice() is None:
            print ("Error: Not find your device")
            # return False
            # develop test
            return True
        else:
            return True

    def save_wave(self, data):
        wf = wave.open(self.filename + ".wav",'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.sampwidth)
        wf.setframerate(self.framerate)
        wf.writeframes(b"".join(data))
        wf.close()

    def save_mp3(self):
        print ('save mp3')
        sound = AudioSegment.from_mp3(self.filename + '.wav')
        sound.export(self.filename + '.mp3', format='wav')

    def save_spectrogram(self):
        pass

if __name__ == '__main__':
    args = command_args()
    au = Audio(args.time)
    au.filename = args.filename
    if args.framerate is not None:
        au.framerate = args.framerate
        au.set_settings()
    au.record()
    au.save_mp3()
    au.play()