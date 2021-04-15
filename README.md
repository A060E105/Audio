# Audio

# Argument
* -t, --time
>    set sound recording time, unit is second
* -f, --file-name
>    set output file name

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

# class Audio

### __init__(self, sec)
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
### __get_input_device(self)
    Description:
        get input device index
    Return type: integer
### check_device(self)
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