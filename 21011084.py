

import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write,read
from scipy import fftpack
from math import pi
from math import floor
# DTMF TABLE
dtmfTable = {
    "1" : np.array([1209,697]),
    "2" : np.array([1366,697]),
    "3" : np.array([1477,697]),
    "4" : np.array([1209,770]),
    "5" : np.array([1366,770]),
    "6" : np.array([1477,770]),
    "7" : np.array([1209,852]),
    "8" : np.array([1366,852]),
    "9" : np.array([1447,852]),
    "0" : np.array([1366,941]),
}

def numberToDTMF(phoneNum):
    Fs = 8000 # Sampling Rate
    Ts = 1/Fs # Sampling Interval
    A = 10 # Amplitude
    T = 0.1 # Time
    Time = np.arange(0,T,Ts) # Time Vector  
    Delay = 0.1 # Delay Time
    delayTime = np.arange(0,Delay,Ts) # Delay Time Vector
    mainSound = np.array([],dtype=np.float32) # Main Sound Array

    #Recording
    for i in phoneNum:
        values = dtmfTable[i]
        fHigh = values[0]
        fLow = values[1]
        sound = A*np.sin(2*np.pi*fLow*Time) + A*np.sin(2*np.pi*fHigh*Time)
        sound = np.array(sound,dtype=np.float32)
        delaySound = np.sin(2*pi*0*delayTime)
        delaySound = np.array(delaySound,dtype=np.float32)
        mainSound = np.append(mainSound,sound)
        mainSound = np.append(mainSound,delaySound)

    #Saving The Sound File
    fileName = phoneNum + ".wav"
    write(fileName,Fs,mainSound)

def analyzeNewFile(phoneNumber): 
    Fs = 8000
    fileName = phoneNumber+".wav"
    samplerate,audio = read(fileName)
    N = audio.shape[0] #Length Of File
    d = int(N / samplerate) #Duration Of Audio File
    n = 11 #Lenght Of Phone Number
    length = floor(len(audio)/n)
    # Plotting The Audio File
    plt.plot(np.arange(N)/samplerate,audio)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.title("Phone Number: "+phoneNumber)
    plt.show()
    
    plt.stem(np.arange(N)/samplerate,audio)
    plt.show()
    M = int(N / n)
    plt.clf()
    #Plotting Every Numbers Frequency
    fourierArray =[]
    for i in range(0,N,M):
        fourier = fftpack.fft(audio[i:i+M])
        fourier = fourier.real
        plt.xlim(500,1700)
        plt.title(phoneNumber[i//M])
        plt.xlabel('Frequency (kHz)')
        plt.ylabel('Frequency Magnitude')
        plt.title
        freqs = np.arange(length) * (samplerate/length)
        plt.plot(freqs,np.abs(fourier))
        plt.show()
        plt.xlim(500,1700)
        plt.stem(freqs,np.abs(fourier))
        plt.show()
        plt.clf()
#-------------------------------------------------------
#Analysing The DTMF File

def analyzeDTMF(fileName):
    Fs = 8000
    fileName = fileName+".wav"
    samplerate,audio = read(fileName)
    N = audio.shape[0] #Length Of File
    n = 11 #Lenght Of Phone Number
    length = floor(len(audio)/n)
    # Plotting The Audio File
    plt.plot(np.arange(N)/samplerate,audio)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.show()
    plt.clf()
    M = int(N / n)

    #Plotting Every Numbers Frequency
    fourierArray =[]
    for i in range(0,N,M):
        fourier2 = fftpack.fft(audio[i:i+M],Fs)
        fourier = fftpack.fft(audio[i:i+M])
        fourier = fourier.real
        fourier2 = fourier2.real
        plt.xlim(500,1700)
        plt.ylim(0,20000)
        plt.xlabel('Frequency (kHz)')
        plt.ylabel('Frequency Magnitude')
        plt.title
        freqs = np.arange(length) * (samplerate/length)
        plt.plot(freqs,np.abs(fourier))
        plt.show()
        fourier2 = fourier2[10:2000:]
        max1 = np.argmax(fourier2)
        fourier2[max1] = 0
        max2 = np.argmax(fourier2)
        plt.clf()
        fourierArray.append([max1,max2])

    for i in fourierArray:
        if i[0] > i[1]:
            i[0],i[1] = i[1],i[0]
    #-------------------------------------------------------
    highValues = [1209,1366,1477]
    lowValues = [697,770,852,941]
    phoneNumber=[]
    for i in fourierArray:
        low = min(lowValues,key= lambda x:abs(x-i[0]))
        high = min(highValues,key= lambda x:abs(x-i[1]))
        total = low + high
        for key,value in dtmfTable.items():
            if total == (value[0] + value[1]):
                phoneNumber.append(key)
                break
    print("Phone Number : {} {}{}{} {}{}{} {}{} {}{}".format(phoneNumber[0],phoneNumber[1],phoneNumber[2],phoneNumber[3],phoneNumber[4],phoneNumber[5],phoneNumber[6],phoneNumber[7],phoneNumber[8],phoneNumber[9],phoneNumber[10]))

def main():
    print("*************************\n")
    phoneNum = input("Enter A Phone Number:")
    print("\n*************************")
    numberToDTMF(phoneNum)
    analyzeNewFile(phoneNum)
    fileName = input("Enter The File Name:")
    print("\n*************************\n")
    analyzeDTMF(fileName)
    print("\n*************************\n")

if __name__ == '__main__':
    main()
   
    

    
