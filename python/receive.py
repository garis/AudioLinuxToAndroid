import socket
import wave
import pyaudio

CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt8
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
INPUT_DEVICE = 3

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 52120              # Arbitrary non-privileged port
receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive.bind((HOST, PORT))
receive.listen(1)

conn, addr = receive.accept()
print ('Connected by', addr)
data = conn.recv(1024)

i=1

frames = []
while data != '':
    data = conn.recv(1024)
    i=i+1
    print (i)
    frames.append(data)
    if not data: break

WAVE_OUTPUT_FILENAME ="fileRecorded.wav"

audio = pyaudio.PyAudio()
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

conn.close()