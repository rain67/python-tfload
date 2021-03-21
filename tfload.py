# loading transfer function provided by HRAK (.mat file)
from icecream import ic
import numpy as np 
import struct
from more_itertools import chunked

def decimalize(datalist: list):
    return datalist[3] + datalist[2] * 256 + datalist[1] * (256**2) + datalist[0] * (256**3) 

def bin_to_float(b):
    q = int(b, 0)                    # binary to int.
    b8 = struct.pack("I", q)         # "I" means int. int to binary.
    return struct.unpack("f", b8)[0] # "f" means float type. binary to float.

def read_mat(path):
    data = open(path, 'rb').read()

    int_data =[] 
    for i in range(64,len(data)):                       # 最初の64bitはchar
        int_data.append(data[i])                        # 65番目(index=64)から1bit intをリストに格納

    int_data=np.array(int_data)
    int_data = int_data.reshape([int(len(int_data)/4),4])       # 4byteなので4つで1ペア
    int_data = np.fliplr(int_data)                              # 逆順に入っているのでflip
    decimal = [ decimalize(datalist) for datalist in int_data ] # 4byteをまとめて32bitのint(十進数)に変換
    binary = [bin(x) for x in decimal]                          # できたintを32bit binaryデータに 

    dim = decimal[0] # 2
    row = decimal[1] # 8(マイク数)
    col = decimal[2] # 257(周波数次元)

    float_data = [bin_to_float(x) for x in binary[3:]]      # 32bit-binaryデータを、単精度浮動小数点数に変換
    float_data = list(chunked(float_data, 2))               # 長さ2のリストに変換。各要素(リスト)の0番には実部、1番には虚部が入る。
    complex_data = [complex(x[0],x[1]) for x in float_data] 
    tf_matlix = np.array(complex_data).reshape(col,row)
    return tf_matlix

ic(read_mat('transferFunction/localization/tf00003.mat'))
