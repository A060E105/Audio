import wave
from pyaudio import PyAudio, paInt16
import re
import abc

class BaseAudio(abc.ABC):
    @abc.abstractclassmethod
    def save_wave_file(self):
        pass

    @abc.abstractclassmethod
    def save_mp3_file(self):
        pass

    @abc.abstractclassmethod
    def record(self):
        pass

    @abc.abstractclassmethod
    def play(self):
        pass

    @abc.abstractclassmethod
    def __get_input_device(self):
        pass

    @abc.abstractclassmethod
    @property
    def time(self):
        pass

    @abc.abstractclassmethod
    @time.setter
    def time(self, record_time):
        pass

    @abc.abstractclassmethod
    @property
    def filename(self):
        pass

    @abc.abstractclassmethod
    @filename.setter
    def filename(self, name):
        pass

framerate = 8000
NUM_SAMPLES = 1024
channels = 1
sampwidth = 2
TIME = 2

def save_wave_file(filename,data):
    '''save the date to the wavfile'''
    wf = wave.open(filename,'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(data))
    wf.close()

def getDeviceIndex():
    p = PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print ("input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0,i).get('name'))
            print ((re.search('EZM-001', p.get_device_info_by_host_api_device_index(0, i).get('name'))) is not None)
            if ((re.search('EZM-001', p.get_device_info_by_host_api_device_index(0, i).get('name'))) is not None):
                print ('select this device')
                return i

def my_record():
    pa = PyAudio()
    stream = pa.open(format=paInt16,channels=1,
    rate = framerate,input = True,
    input_device_index=getDeviceIndex(),
    frames_per_buffer=NUM_SAMPLES)
    my_buf = []
    count = 0
    while count < TIME * 10: #控制錄音時間
        string_audio_data = stream.read(NUM_SAMPLES)
        my_buf.append(string_audio_data)
        count += 1
        print('.')
    save_wave_file('01.wav',my_buf)
    stream.close()

chunk = 1024
def play():
    wf = wave.open(r"01.wav",'rb')
    p = PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=
    wf.getnchannels(),rate=wf.getframerate(),output=True)
    while True:
        # print('.', end='')
        data = wf.readframes(chunk)
        # print(data)
        if data == b"":
            break
        stream.write(data)
    stream.close()
    p.terminate()

if __name__ == '__main__':
    my_record()
    print('Over!') 
    play()
    # getDeviceIndex()