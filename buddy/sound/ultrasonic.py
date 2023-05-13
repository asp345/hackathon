import scipy
import numpy as np
import wave
import math
from scipy.io.wavfile import write
from scipy.io.wavfile import read

def int_to_bin(n):
    n = int(n)
    bit = []
    for i in range(16):
        bit.append(n % 2)
        n //= 2
    return bit[::-1]

def bin_to_int(bit):
    tmp = 1
    res = 0
    for i in range(15, -1, -1):
        res += tmp * bit[i]
        tmp *= 2
    return res

def send_ultrasonic(n, bit_freq, path, rate = 44100, bps = 60, margin_time = 0.2):
    bit = int_to_bin(n)
    # bit with start, end signal
    bit_with_signal = [1, 0] + bit + [0, 1]
    bit_block_size = int(rate / bps)
    data = [0] * int(margin_time * rate)
    # sin wave * bit 데이터 생성
    for i in range(20):
        for j in range(bit_block_size):
            data.append(int(bit_with_signal[i] * math.sin((2 * math.pi) * (bit_freq / rate) * j) * 2147483640))
    data += [0] * int(margin_time * rate)
    data = np.array(data)
    wav = write(path, rate, data)

def receive_ultrasonic(bit_freq, path, bps = 60, sampling_num = 5):
    # wav 읽기
    raw = read(path)
    raw_data = wave.open(path)
    mx = (256 ** raw_data.getsampwidth()) // 2
    raw_data.close()
    rate = raw[0]
    wav = np.array(raw[1], dtype = float)
    wav /= mx
    # 채널 개수 줄이기
    if len(wav.shape) == 2:
        temp = wav.shape[1]
        wav = wav.sum(axis = 1)
        wav /= temp
    wav_len = wav.shape[0]
    # 블럭 크기 계산
    block_size = (rate // (bps * sampling_num))
    block_num = wav_len // block_size
    # 블럭 단위로 분할
    block = []
    for i in range(block_num):
        tmp_block = []
        for j in range(block_size):
            tmp_block.append(wav[i * block_size + j])
        block.append(np.array(tmp_block))
    # 블럭 단위로 fft
    data = []
    for b in block:
        amp = np.fft.fft(b)
        tmp_sum = 0
        data.append(abs(amp[int(block_size / (rate / bit_freq))]))
    # 비트 추출
    data_mx = max(data)
    bit_raw = list(map(lambda x: 1 if (x > (data_mx / 2)) else 0, data))

    start_t, end_t, bit_t = 0, 0, 0
    for i in range(len(bit_raw) - 1):
        if bit_raw[i] == 0 and bit_raw[i + 1] == 1:
            start_t = i + 1
            break
    for i in range(len(bit_raw) - 1, 1, -1):
        if bit_raw[i] == 0 and bit_raw[i - 1] == 1:
            end_t = i
            break
    bit_t = end_t - start_t
    bit = []
    if (20 * sampling_num - 3 <= bit_t <= 20 * sampling_num + 3):
        if bit_t < 20 * sampling_num:
            start_t -= 1
        elif bit_t > 20 * sampling_num:
            start_t += 1
        end_t = start_t + 20 * sampling_num
        # bit_raw의 개수가 20 * sampling_num 되도록 조정
        for i in range(16):
            bit.append(0)
            for j in range(5):
                bit[i] += bit_raw[start_t + (i + 2) * sampling_num + j]
            if bit[i] > sampling_num / 2:
                bit[i] = 1
            else:
                bit[i] = 0
    return bin_to_int(bit)

