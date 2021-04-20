# Audio

# Argument
* -t, --time
>   set sound recording time, unit is second
* -o, --output-name
>   set output file name
* -f, --framerate
>   set recording framerate

# using plugin
* pyaudio
> * Pip  
> pip install pyaudio  
> * Anaconda  
> conda install pyaudio
* tqdm
> * Pip  
> pip install tqdm  
> * Anaconda  
> conda install tqdm
* pydub  
> * Pip  
> pip install pydub  
> * Ubuntu/Debian Linux:  
>  > apt-get install ffmpeg  
> * Anaconda  
> conda install -c conda-forge pydub  

# class Audio

### __init__(self, sec)
### init_settings_argument(self)
    Description:
        initialization settings arguments
### get_settings_arguments(self)
    Description:
        read settings file, if settings file does not exist, create new settings file
### save_settings(self)
    Description:
        save settings arguments in settings file
### framerate(self)
    Description:
        get framerate
    Return type: integer
### framerate(self, value)
    Description:
        set framerate
### num_samples(self)
    Description:
        get number samples
    Return type: integer
### num_samples(self, value)
    Description:
        set number samples
### channels(self)
    Description:
        get channels
    Return type: integer
### channels(self, value)
    Description:
        set channels
### sampwidth(self)
    Description:
        get sampwidth
    Return type: integer
### sampwidth(self, value)
    Description:
        set sampwidth
### time(self)
    Description:
        get recording time count
    Return type: integer
### second(self)
    Description:
        Return record second
    Return type: integer
### second(self, sec)
    Description:
        set record second
    Parameters: sec -- record second
### filename(self)
    Description:
        Return filename
    Return type: string
### filename(self, name)
    Description:
        set output file name
    Parameters: name -- output file name
### record(self)
    Description:
        sound recording
### play(self)
    Description:
        play audio file
### __getDevice(self)
    Description:
        get input device index
    Return type: integer
### hasDevice(self)
    Description:
        check have input device
    Return type: boolean
### save_wave(self, data)
    Description:
        save wave file
    Parameters: data -- sound record data list
### save_mp3(self)
    Description:
        save mp3 file
### save_spectrogram(self)
    Description:
        save spectrogram file

# other methods
### command_args()
    Description:
        get command line arguments
    Return type: argparse.Namespace