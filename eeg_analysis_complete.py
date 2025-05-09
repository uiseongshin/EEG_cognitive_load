import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.colors import TwoSlopeNorm
import mne
from mne.stats import permutation_cluster_1samp_test as pcluster_test
import os

# 그래프 설정
sns.set_style('whitegrid')  # seaborn 스타일 설정
sns.set_context('talk')     # 글자 크기 등 컨텍스트 설정

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def load_subject_data(subject_num):
    """주어진 피험자 번호에 대한 휴식 상태와 과제 상태의 EEG 데이터를 로드합니다.
    
    Parameters
    ----------
    subject_num : int
        피험자 번호 (0-35)
        
    Returns
    -------
    raw_rest : mne.io.Raw
        휴식 상태 EEG 데이터
    raw_task : mne.io.Raw
        과제 수행 중 EEG 데이터
    """
    # 파일 경로 설정
    subject = f"{subject_num:02d}"  # 두 자리 숫자로 변환
    rest_path = f"./EEG_arithmetic_task/Subject{subject}_1.edf"
    task_path = f"./EEG_arithmetic_task/Subject{subject}_2.edf"
    
    # 데이터 로드
    raw_rest = mne.io.read_raw_edf(rest_path, preload=True)
    raw_task = mne.io.read_raw_edf(task_path, preload=True)
    
    # 채널 이름에서 점(.) 제거
    raw_rest.rename_channels(lambda x: x.strip("."))
    raw_task.rename_channels(lambda x: x.strip("."))
    
    return raw_rest, raw_task

def preprocess_raw(raw):
    """Raw EEG 데이터를 전처리합니다.
    
    Parameters
    ----------
    raw : mne.io.Raw
        전처리할 Raw EEG 데이터
        
    Returns
    -------
    raw : mne.io.Raw
        전처리된 EEG 데이터
    """
    # EEG 채널만 선택
    raw.pick_types(eeg=True)
    
    # 필터 적용
    raw.filter(l_freq=0.5, h_freq=45.0)
    
    return raw

def create_epochs(raw_data, duration=60, overlap=0):
    """연속된 EEG 데이터를 에포크로 분할합니다.
    
    Parameters
    ----------
    raw_data : mne.io.Raw
        에포크로 분할할 Raw EEG 데이터
    duration : float
        각 에포크의 길이(초)
    overlap : float
        에포크 간 중복되는 시간(초)
        
    Returns
    -------
    epochs : mne.Epochs
        분할된 에포크 데이터
    """
    # 데이터 길이 계산
    data_duration = raw_data.times[-1]
    
    # 에포크 시작 시간 계산
    step = duration - overlap
    starts = np.arange(0, data_duration - duration, step)
    
    # 이벤트 배열 생성
    events = np.array([
        [int(start * raw_data.info['sfreq']), 0, 1]
        for start in starts
    ])
    
    # 에포크 생성
    epochs = mne.Epochs(
        raw_data,
        events,
        tmin=0,
        tmax=duration,
        baseline=None,
        preload=True
    )
    
    return epochs

def compute_tfr(epochs, freqs=np.arange(4, 41, 1), n_cycles=None):
    """에포크 데이터에 대해 시간-주파수 분석을 수행합니다.
    
    Parameters
    ----------
    epochs : mne.Epochs
        분석할 에포크 데이터
    freqs : array
        분석할 주파수 범위
    n_cycles : array or None
        각 주파수별 사이클 수. None이면 freqs/2 사용
        
    Returns
    -------
    tfr : mne.time_frequency.AverageTFR
        시간-주파수 분석 결과
    """
    if n_cycles is None:
        n_cycles = freqs / 2.
    
    tfr = epochs.compute_tfr(
        method="multitaper",
        freqs=freqs,
        n_cycles=n_cycles,
        use_fft=True,
        return_itc=False,
        average=True,
        decim=2
    )
    
    return tfr

def compute_erds(tfr_task, tfr_rest):
    """과제 중과 휴식 상태의 TFR 데이터로부터 ERDS를 계산합니다.
    
    Parameters
    ----------
    tfr_task : mne.time_frequency.AverageTFR
        과제 수행 중의 TFR 데이터
    tfr_rest : mne.time_frequency.AverageTFR
        휴식 상태의 TFR 데이터
        
    Returns
    -------
    erds : array
        ERDS 값 (채널 x 주파수 x 시간)
    """
    # 휴식 상태 평균 파워 계산
    rest_power = tfr_rest.data.mean(axis=-1, keepdims=True)  # 시간에 대해 평균
    
    # ERDS 계산: (task - rest) / rest * 100
    erds = (tfr_task.data - rest_power) / rest_power * 100
    
    return erds

def plot_erds_map(erds, times, freqs, ch_names, vmin=-100, vmax=100):
    """ERDS 맵을 시각화합니다.
    
    Parameters
    ----------
    erds : array
        ERDS 값 (채널 x 주파수 x 시간)
    times : array
        시간 축 값
    freqs : array
        주파수 축 값
    ch_names : list
        채널 이름 목록
    vmin, vmax : float
        컬러맵의 최소/최대값
    """
    n_channels = len(ch_names)
    fig, axes = plt.subplots(n_channels, 1, figsize=(12, 4*n_channels))
    if n_channels == 1:
        axes = [axes]
    
    for ax, data, name in zip(axes, erds, ch_names):
        im = ax.pcolormesh(
            times, freqs, data,
            cmap='RdBu_r',
            norm=TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)
        )
        ax.set_title(f'채널: {name}')
        ax.set_xlabel('시간 (초)')
        ax.set_ylabel('주파수 (Hz)')
        plt.colorbar(im, ax=ax, label='ERDS (%)')
    
    plt.tight_layout()
    return fig

def analyze_single_subject(subject_num, channels_of_interest=['F3', 'F4', 'F7', 'F8']):
    """단일 피험자의 데이터를 분석합니다.
    
    Parameters
    ----------
    subject_num : int
        피험자 번호
    channels_of_interest : list
        분석할 채널 목록
    """
    # 데이터 로드 및 전처리
    raw_rest, raw_task = load_subject_data(subject_num)
    
    # 채널 이름 출력
    print("사용 가능한 채널 목록:")
    print(raw_rest.ch_names)
    
    raw_rest = preprocess_raw(raw_rest)
    raw_task = preprocess_raw(raw_task)
    
    # 채널 선택
    available_channels = [ch for ch in channels_of_interest if ch in raw_rest.ch_names]
    if not available_channels:
        raise ValueError("지정한 채널 중 데이터에 존재하는 채널이 없습니다.")
    
    raw_rest.pick_channels(available_channels)
    raw_task.pick_channels(available_channels)
    
    # 에포크 생성
    epochs_rest = create_epochs(raw_rest, duration=30, overlap=15)
    epochs_task = create_epochs(raw_task, duration=30, overlap=15)
    
    # 시간-주파수 분석
    freqs = np.arange(4, 41, 1)
    tfr_rest = compute_tfr(epochs_rest, freqs=freqs)
    tfr_task = compute_tfr(epochs_task, freqs=freqs)
    
    # ERDS 계산
    erds = compute_erds(tfr_task, tfr_rest)
    
    # ERDS 맵 시각화
    fig = plot_erds_map(
        erds,
        tfr_task.times,
        tfr_task.freqs,
        tfr_task.ch_names,
        vmin=-50,
        vmax=50
    )
    plt.suptitle(f'피험자 {subject_num:02d}의 ERDS 맵')
    
    return fig, erds


def main():
    """메인 실행 함수"""
    # 결과 저장할 디렉토리 생성
    os.makedirs('results', exist_ok=True)
    
    # 분석할 채널 설정
    channels_of_interest = ['F3', 'F4', 'F7', 'F8']
    
    # 단일 피험자 분석 예시 (피험자 0)
    fig, _ = analyze_single_subject(0, channels_of_interest)
    fig.savefig('results/subject00_erds.png')
    plt.close(fig)
    
    # 그룹 분석
    mean_erds = analyze_groups(channels_of_interest)
    
    # 그룹별 ERDS 맵 시각화 및 저장
    for group, erds_data in mean_erds.items():
        fig = plot_erds_map(
            erds_data,
            np.linspace(0, 30, erds_data.shape[-1]),  # 30초 구간
            np.arange(4, 41, 1),  # 4-40 Hz
            channels_of_interest,
            vmin=-50,
            vmax=50
        )
        plt.suptitle(f'그룹 {group}의 평균 ERDS 맵')
        fig.savefig(f'results/group_{group}_erds.png')
        plt.close(fig)

if __name__ == "__main__":
    main() 