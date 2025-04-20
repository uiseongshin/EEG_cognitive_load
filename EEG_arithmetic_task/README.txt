EEG during mental arithmetic task

Igor Zyma, Sergii Tukaev, Ivan Seleznov

The data files with EEG are provided in EDF (European Data Format) format. Each folder contains two recording files per subject: 
with “_1” postfix -- the recording of the background EEG of a subject (before mental arithmetic task)
 with “_2” postfix -- the recording of EEG during the mental arithmetic task. 

In this experiment all subjects are divided into two groups: 
Group “G” (24 subjects) performing good quality count (Mean number of operations per 4 minutes = 21, SD = 7.4 ), 
Group ”B” (12 subjects) performing bad quality count (Mean number of operations per 4 minutes = 7, SD = 3.6).  
In the file “subjects_info.xlsx” the “Count quality” column provides info which subjects correspond to which group (0 - Group ”B”, 1 - Group “G”). Additionally, file “subjects_info.xlsx” provides basic information about each subject (gender, age, job, date of recording).

Both EDF and EDF+ formats are free and can be viewed using free software such as:
Polyman (for MS-Windows only; for details, please follow the link)
EDFbrowser (for Linux, Mac OS X, and MS-Windows; at www.teuniz.net)
LightWAVE and the PhysioBank ATM, platform-independent web applications from PhysioNet
WAVE and other applications for Linux, Mac OS X, and MS-Windows in the WFDB Software Package, also from PhysioNet

For using the following EDF files in Python code, we suggest using the PyEDFlib for  processing the files (https://github.com/holgern/pyedflib/tree/master/pyedflib). 

The EEGs were recorded monopolarly using Neurocom EEG 23-channel system  (Ukraine, XAI-MEDICA). The silver/silver chloride electrodes were placed on the scalp according to the International 10/20 scheme. All electrodes were referenced to the interconnected ear reference electrodes. A high-pass filter with a 30 Hz cut-off frequency and a power line notch filter (50 Hz) were used. All recordings are artifact-free EEG segments of 60 seconds duration. At the stage of data preprocessing, the Independent Component Analysis (ICA) was used to eliminate the artifacts (eyes, muscle, and cardiac overlapping of the cardiac pulsation). Arithmetic task was the serial subtraction of two numbers. Each trial started with the communication orally 4-digit (minuend) and 2-digit (subtrahend) numbers (e.g. 3141 and 42)

The participants were eligible to enroll in the study if they had normal or corrected-to-normal visual acuity, normal color vision, had no clinical manifestations of mental or cognitive impairment, verbal or non-verbal learning disabilities. Exclusion criteria were the use of psychoactive medication, drug or alcohol addiction and psychiatric or neurological complaints.

정신 산술 과제 수행 중 EEG
Igor Zyma, Sergii Tukaev, Ivan Seleznov

EEG가 포함된 데이터 파일은 EDF(European Data Format) 형식으로 제공됩니다.
각 참가자 폴더에는 두 개의 기록 파일이 있습니다:

"_1" 접미사가 붙은 파일은 정신 산술 과제 전 참가자의 기본 EEG를 기록한 것입니다.

"_2" 접미사가 붙은 파일은 정신 산술 과제 수행 중의 EEG를 기록한 것입니다.

이 실험에서 모든 참가자들은 두 그룹으로 나뉘었습니다:

그룹 “G” (24명): 질 좋은 계산을 수행한 그룹 (4분당 평균 연산 수 = 21, 표준편차 SD = 7.4)

그룹 “B” (12명): 질 낮은 계산을 수행한 그룹 (4분당 평균 연산 수 = 7, SD = 3.6)

“subjects_info.xlsx” 파일의 “Count quality” 열은 어떤 참가자가 어느 그룹에 속하는지 정보를 제공합니다.
(0 - 그룹 “B”, 1 - 그룹 “G”)
또한 “subjects_info.xlsx” 파일에는 각 참가자의 기본 정보(성별, 나이, 직업, 기록 날짜)가 포함되어 있습니다.

EDF 및 EDF+ 형식은 모두 무료이며, 다음과 같은 무료 소프트웨어를 사용하여 열어볼 수 있습니다:

Polyman (Windows 전용; 자세한 내용은 링크 참조)

EDFbrowser (Linux, Mac OS X, Windows용; www.teuniz.net)

LightWAVE 및 PhysioBank ATM (운영체제에 상관없이 웹 기반 애플리케이션)

WAVE 및 기타 애플리케이션 (Linux, Mac OS X, Windows용) - WFDB Software Package 제공 (PhysioNet 출처)

Python 코드에서 이 EDF 파일들을 사용하려면, PyEDFlib 라이브러리 사용을 권장합니다.
(https://github.com/holgern/pyedflib/tree/master/pyedflib)

EEG는 우크라이나 XAI-MEDICA사의 Neurocom EEG 23채널 시스템을 사용하여 단일극 방식(monopolar)으로 기록되었습니다.
전극은 국제 10/20 시스템에 따라 두피에 배치되었고, 모든 전극은 서로 연결된 양쪽 귀 전극을 기준으로 하여 측정되었습니다.
30Hz 컷오프의 하이패스 필터와 50Hz 전원 노치 필터가 사용되었습니다.
모든 기록은 아티팩트(잡음)가 없는 60초 길이의 EEG 세그먼트입니다.
데이터 전처리 단계에서는 ICA(독립 성분 분석)를 이용하여 눈 깜빡임, 근육, 심장 박동에 따른 아티팩트를 제거했습니다.
산수 과제는 두 숫자를 연속적으로 빼는 방식이며, 각 시도는 음성으로 전달된 네 자리 수(피감수)와 두 자리 수(감수)로 시작되었습니다 (예: 3141과 42).

참가자들은 시력 또는 색각이 정상(또는 교정 가능)이고, 정신적 또는 인지적 장애, 언어/비언어 학습장애가 없는 경우 실험에 참여할 수 있었습니다.
제외 기준으로는 향정신성 약물 복용, 약물 또는 알코올 중독, 정신과 또는 신경계 질환 병력이 포함되었습니다.