package com.example.riccardo.soundwifi;

import android.media.AudioFormat;
import android.media.AudioManager;
import android.media.AudioTrack;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.SocketException;
import java.net.SocketTimeoutException;

public class MainActivity extends AppCompatActivity {

    public static int bufferLength=1024*4;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //set the audio thread
        Sound player = new Sound();
        player.start();
        //give an audio output to the packets
        Packets streamAudio = new Packets(player);
        streamAudio.start();
    }

    class Sound extends Thread {
        AudioTrack audioTrack;

        public Sound() {
        }

        public void run() {
            initialize();
            while(true)
            {
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }

        public void initialize() {
            int bufferSize=bufferLength/4;
            audioTrack = new AudioTrack(AudioManager.STREAM_MUSIC,
                    48000,
                    AudioFormat.CHANNEL_OUT_STEREO,
                    AudioFormat.ENCODING_PCM_16BIT,
                    bufferSize,
                    AudioTrack.MODE_STREAM);
            audioTrack.play();
        }

        private void writeSamples(byte[] samples) {
            audioTrack.write(samples, 0, samples.length);
        }
    }

    class Packets extends Thread {
        Sound player;

        public Packets(Sound outputAudio)
        {
            player=outputAudio;
        }

        @Override
        public void run() {
            receive();
        }

        //n*4: #2 byte per channel, for two channels
        byte[] message = new byte[bufferLength];

        public void receive() {
            DatagramSocket mDataGramSocket = null;

            try {
                mDataGramSocket = new DatagramSocket(52120);
                mDataGramSocket.setReuseAddress(true);
                mDataGramSocket.setSoTimeout(100000);
            } catch (SocketException e) {
                e.printStackTrace();
            }

            DatagramPacket p = new DatagramPacket(message, message.length);

            try {

                while (true) {
                    try {
                        mDataGramSocket.receive(p);
                        player.writeSamples(message);
                    } catch (SocketTimeoutException | NullPointerException e) {

                        e.printStackTrace();
                    }
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
}
