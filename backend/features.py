import numpy as np
import librosa

def extract(file_path: str) -> np.ndarray:
    y, sr = librosa.load(file_path, sr=None)

    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

    mfcc_mean_2 = np.mean(mfcc[1])   
    mfcc_mean_4 = np.mean(mfcc[3])  
    mfcc_mean_7 = np.mean(mfcc[6])   

    zcr = librosa.feature.zero_crossing_rate(y)[0]
    zcr_mean = np.mean(zcr)

    onsets = librosa.onset.onset_detect(y=y, sr=sr)
    duration = librosa.get_duration(y=y, sr=sr)
    event_density_mean = len(onsets) / duration if duration > 0 else 0.0
    
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    chromagram_mean_7 = np.mean(chroma[6])  
    
    features = np.array([
        mfcc_mean_2,
        mfcc_mean_4,
        mfcc_mean_7,
        zcr_mean,
        event_density_mean,
        chromagram_mean_7
    ], dtype=float)

    return features
