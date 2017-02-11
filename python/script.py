import pyaudio
import sys
import wave
import time
import timeit
import socket

CHUNK_SIZE =1024    #n sample, each sample is 32 bit: 2 (stereo) 16 bit (format)
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 48000
INPUT_DEVICE = 3


audio = pyaudio.PyAudio()

info = audio.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
for i in range(0, numdevices):
        if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            for value in audio.get_device_info_by_host_api_device_index(0, i).items():
                print (value)
            print ("\n####################\n")

stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=False, frames_per_buffer=CHUNK_SIZE, input_device_index=INPUT_DEVICE)

print ("* recording")
 
HOST='192.168.1.14'
PORT = 52120              # Arbitrary non-privileged port
addr = (HOST, PORT)

pkts_sent=0
interval_measure=0.5

while True:
    pkt_time_stats = timeit.default_timer()

    try:
        time.sleep(3)
        print ("RETRY")
        transmit = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        transmit.connect((HOST, PORT))

        while True:
            data = stream.read(CHUNK_SIZE)

            transmit.sendto(data, addr)
            pkts_sent=pkts_sent+1

            if((timeit.default_timer()-pkt_time_stats)>interval_measure):
                sys.stdout.write("PKTpSec: "+str(int((pkts_sent/interval_measure)/2))+"\t| KByte/s: "+str(((len(data)*pkts_sent/interval_measure)/1000))+"\r")
                sys.stdout.flush()

                pkt_time_stats = timeit.default_timer()
                pkts_sent=0
    
        transmit.close()

        print ("* done")

        stream.stop_stream()
        stream.close()
        audio.terminate()
    except ConnectionRefusedError:        
        print ("ERROR")
