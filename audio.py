import wave
from pyaudio import PyAudio, paInt16
from tqdm import trange
from argparse import ArgumentParser
from os import path
import json
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
        self.init_settings_argument()
        self.get_settings_arguments()

    def init_settings_argument(self):
        self._argument = {}
        self._argument['settings'] = {}
        self._argument['settings']['framerate'] = 44100
        self._argument['settings']['num_samples'] = 1024
        self._argument['settings']['channels'] = 2
        self._argument['settings']['sampwidth'] = 2

    def get_settings_arguments(self):
        if path.isfile('audio.settings'):
            with open('audio.settings', 'r+') as file:
                self._argument = json.load(file)
        else:
            with open('audio.settings', 'w+') as file:
                json.dump(self._argument, file, indent=4)

    def save_settings(self):
        with open('audio.settings', 'w+') as file:
            json.dump(self._argument, file, indent=4)

    @property
    def time(self):
        return int( self._argument['settings']['framerate'] / self._argument['settings']['num_samples'] * self.second )

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
            stream = pa.open(format=paInt16,channels=self._argument['settings']['channels'],
            rate=self._argument['settings']['framerate'],input=True,
            input_device_index=self.__get_input_device(),
            frames_per_buffer=self._argument['settings']['num_samples'])
            my_buf = []
            for _ in trange(self.time):
                string_audio_data = stream.read(self._argument['settings']['num_samples'])
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
        wf.setnchannels(self._argument['settings']['channels'])
        wf.setsampwidth(self._argument['settings']['sampwidth'])
        wf.setframerate(self._argument['settings']['framerate'])
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