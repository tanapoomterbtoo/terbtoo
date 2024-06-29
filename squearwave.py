import numpy as np
import sounddevice as sd

def generate_square_wave(freq, duration, sampling_rate):
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    wave = np.sign(np.sin(2 * np.pi * freq * t))
    return wave

def play_sound(wave, sampling_rate):
    sd.play(wave, samplerate=sampling_rate)
    sd.wait()

if __name__ == "__main__":
    # กำหนดพารามิเตอร์
    frequency = 5  # ความถี่ของคลื่นเสียง (Hz)
    duration = 100  # ระยะเวลาของเสียง (วินาที)
    sampling_rate = 44100  # อัตราการสุ่ม (sample rate)

    while True:
        # สร้างคลื่นเสียง
        wave = generate_square_wave(frequency, duration, sampling_rate)
        print("run")
        # เล่นคลื่นเสียง
        play_sound(wave, sampling_rate)
