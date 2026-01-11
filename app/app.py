import streamlit as st
import time
import sys
import os
import base64
import random

# ---------------------------------------------------------
# 1. YOL VE MODÜL AYARLARI
# ---------------------------------------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)

try:
    from src.predictor import HeartDiseasePredictor
    import config
except ImportError as e:
    st.error(f"Hata: Modüller bulunamadı. Lütfen klasör yapısını kontrol et.\nDetay: {e}")
    st.stop()

# ---------------------------------------------------------
# 2. SAYFA AYARLARI
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI Kalp Doktoru",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        text-align: center;
    }
    .high-risk {
        background-color: #ffcccc;
        color: #990000;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
    }
    .low-risk {
        background-color: #ccffcc;
        color: #006600;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
    }
    .centered-text {
        text-align: center;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .stMarkdown {
        caret-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. YARDIMCI FONKSİYONLAR
# ---------------------------------------------------------
@st.cache_resource
def load_prediction_engine():
    return HeartDiseasePredictor()

def get_file_path(filename):
    return os.path.join(current_dir, filename)

def get_audio_html(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        return f"""
            <audio autoplay style="display:none;">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
    except FileNotFoundError:
        return ""

def show_centered_gif(file_path, width=300):
    try:
        with open(file_path, "rb") as f:
            contents = f.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        st.markdown(
            f'<div style="display: flex; justify-content: center; margin-bottom: 20px;">'
            f'<img src="data:image/gif;base64,{data_url}" width="{width}">'
            f'</div>',
            unsafe_allow_html=True,
        )
    except FileNotFoundError:
        st.warning("Gif bulunamadı!")

def rain_emoji(emoji="💀"):
    # Emojileri yağdıran CSS/JS
    st.markdown(f"""
    <style>
    @keyframes fall {{
        0% {{ top: -10%; margin-left: 0; opacity: 1; }}
        100% {{ top: 110%; margin-left: 20px; opacity: 0; }}
    }}
    .emoji-rain {{
        position: fixed;
        top: -10%;
        font-size: 3rem;
        animation-name: fall;
        animation-timing-function: linear;
        animation-iteration-count: 1; 
        animation-fill-mode: forwards;
        z-index: 9999;
        pointer-events: none;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    html_content = ""
    
    # 40 emoji üretilir
    for i in range(40): 
        left = random.randint(0, 100)
        delay = random.uniform(0, 3) 
        duration = random.uniform(3, 6) 
        rotation = random.randint(-45, 45) 
        
        html_content += f"""
        <div class='emoji-rain' style='left: {left}%; animation-duration: {duration}s; animation-delay: {delay}s;'>
            <div style='transform: rotate({rotation}deg);'>
                {emoji}
            </div>
        </div>
        """
    
    st.markdown(html_content, unsafe_allow_html=True)

def create_input_form(key_suffix):
    # Formu 13 değişkeni kapsayacak şekilde genişlettik
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("👤 Kişisel & EKG")
        age = st.slider("Yaş", 20, 90, 50, key=f"age{key_suffix}")
        sex = st.radio("Cinsiyet", ["Erkek", "Kadın"], key=f"sex{key_suffix}")
        sex_val = 1 if sex == "Erkek" else 0
        
        # EKG (restecg)
        restecg = st.selectbox("EKG Sonucu (RestECG)", 
                               ["0: Normal", "1: ST-T Anormalliği", "2: Hipertrofi"], 
                               key=f"restecg{key_suffix}")
        
        # Egzersiz Anjinası (exang)
        exang = st.radio("Egzersiz Anjinası Var mı?", ["Hayır", "Evet"], key=f"exang{key_suffix}")
        exang_val = 1 if exang == "Evet" else 0

    with col2:
        st.subheader("🫀 Kan & Ağrı")
        cp = st.selectbox("Göğüs Ağrısı Tipi", 
                          ["Tip 1: Tipik Anjina", "Tip 2: Atipik Anjina", "Tip 3: Anjina Dışı", "Tip 4: Asemptomatik"], 
                          index=3, key=f"cp{key_suffix}")
        trestbps = st.number_input("Dinlenme Tansiyonu (mm Hg)", 90, 200, 130, key=f"trestbps{key_suffix}")
        chol = st.number_input("Kolesterol (mg/dl)", 100, 600, 250, key=f"chol{key_suffix}")
        
        # Açlık Şekeri (fbs)
        fbs = st.checkbox("Açlık Şekeri > 120 mg/dl?", key=f"fbs{key_suffix}")

    with col3:
        st.subheader("🏃 Efor & Diğer")
        thalach = st.slider("Maksimum Nabız", 60, 220, 150, key=f"thalach{key_suffix}")
        
        # ST Depresyonu (oldpeak)
        oldpeak = st.number_input("ST Depresyonu (Oldpeak)", 0.0, 6.0, 1.0, step=0.1, key=f"oldpeak{key_suffix}")
        
        # ST Eğimi (slope)
        slope = st.selectbox("ST Eğimi (Slope)", ["0: Yukarı", "1: Düz", "2: Aşağı"], key=f"slope{key_suffix}")
        
        # Damar Sayısı (ca)
        ca = st.slider("Büyük Damar Sayısı (0-3)", 0, 3, 0, key=f"ca{key_suffix}")
        
        # Talasemi (thal)
        thal = st.selectbox("Talasemi (Thal)", ["1: Normal", "2: Sabit Kusur", "3: Tersine Çevrilebilir"], index=0, key=f"thal{key_suffix}")

    # Haritalama (Mapping)
    cp_map = {"Tip 1: Tipik Anjina": 1, "Tip 2: Atipik Anjina": 2, "Tip 3: Anjina Dışı": 3, "Tip 4: Asemptomatik": 4}
    restecg_map = {"0: Normal": 0, "1: ST-T Anormalliği": 1, "2: Hipertrofi": 2}
    slope_map = {"0: Yukarı": 0, "1: Düz": 1, "2: Aşağı": 2}
    # Thal değerini string'den integer'a çeviriyoruz (Başındaki sayıyı alarak)
    thal_val = int(thal.split(":")[0]) 

    data = {
        'age': age, 
        'sex': sex_val, 
        'cp': cp_map[cp], 
        'trestbps': trestbps, 
        'chol': chol,
        'fbs': 1 if fbs else 0, 
        'restecg': restecg_map[restecg], 
        'thalach': thalach,
        'exang': exang_val, 
        'oldpeak': oldpeak, 
        'slope': slope_map[slope], 
        'ca': ca, 
        'thal': thal_val
    }
    return data

# ---------------------------------------------------------
# 4. SIDEBAR
# ---------------------------------------------------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2966/2966486.png", width=100)
st.sidebar.title("Kalp Risk Analizi")
st.sidebar.info("ℹ️ **YASAL BİLGİLENDİRME**\n\nBu uygulama istatistiksel tahmin yapar. Kesin tıbbi teşhis değildir.")

# ---------------------------------------------------------
# 5. UYGULAMA MANTIĞI
# ---------------------------------------------------------
st.title("🫀 Kalp Hastalığı Risk Analizi")

if 'stage' not in st.session_state:
    st.session_state['stage'] = 0

try:
    predictor = load_prediction_engine()
except Exception as e:
    st.error(f"Model yüklenirken hata oluştu: {e}")
    st.stop()

tab1, tab2 = st.tabs(["🎬 Senaryo Modu", "⚡ Real-Time"])

# --- TAB 1: SENARYO MODU ---
with tab1:
    music_box = st.empty()
    main_placeholder = st.empty()

    # --- DURUM 0: FORM GİRİŞİ ---
    if st.session_state['stage'] == 0:
        with main_placeholder.container():
            st.header("Hasta Veri Girişi")
            patient_data = create_input_form(key_suffix="_scenario")
            st.write("")
            col_btn, _ = st.columns([1, 4])
            
            with col_btn:
                if st.button("Analizi Başlat", type="primary", use_container_width=True):
                    st.session_state['temp_patient_data'] = patient_data
                    st.session_state['stage'] = 1 
                    main_placeholder.empty() 
                    st.rerun()

    # --- DURUM 1: YÜKLEME EKRANI ---
    elif st.session_state['stage'] == 1:
        music_html = get_audio_html(get_file_path("elevator-music.mp3"))
        music_box.markdown(music_html, unsafe_allow_html=True)
        
        gif_name = "gif-.gif" if os.path.exists(get_file_path("gif-.gif")) else "gift.gif"
        show_centered_gif(get_file_path(gif_name), width=350)
        
        col_c = st.columns([1, 2, 1])[1]
        with col_c:
            progress_bar = st.progress(0)
            status_text = st.empty()

        # DÜZELTME: 1 saniye yerine 0.1 saniye yaptık.
        time.sleep(0.1)

        messages = [
            "Değerler analiz ediliyor...",
            "EKG dalgaları analiz ediliyor...",
            "Değerler analiz ediliyor...",
            "EKG dalgaları analiz ediliyor...",
            "Değerler analiz ediliyor...",
            "EKG dalgaları analiz ediliyor...",
            "Yaşayacak mısın?",
            "Ölüm Kapıda mı?",
            "..."
        ]

        for i, msg in enumerate(messages):
            percent = int((i + 1) / len(messages) * 100)
            progress_bar.progress(percent)
            status_text.markdown(f"<p class='centered-text'>⏳ {msg}</p>", unsafe_allow_html=True)
            time.sleep(3)

        if 'temp_patient_data' in st.session_state:
            result = predictor.predict(st.session_state['temp_patient_data'])
            st.session_state['result'] = result
            st.session_state['stage'] = 2
            st.rerun()
        else:
            st.error("Veri hatası! Sayfayı yenileyin.")

    # --- DURUM 2: SONUÇ EKRANI ---
    elif st.session_state['stage'] == 2:
        music_box.empty()
        sound_html = get_audio_html(get_file_path("completion-sound.mp3"))
        st.markdown(sound_html, unsafe_allow_html=True)

        result = st.session_state['result']
        risk_score = result['risk_score']

        if result['prediction'] == 1:
            rain_emoji("💀")
        else:
            st.balloons()

        st.markdown("### 🏁 ANALİZ SONUCU")
        st.divider()
        
        col_l, col_c, col_r = st.columns([1, 2, 1])
        with col_c:
            if result['prediction'] == 1:
                st.markdown(f"<div class='metric-card high-risk'><h1>🚨 RİSKLİ</h1><h3>Hastalık İhtimali: %{risk_score}</h3></div>", unsafe_allow_html=True)
                st.write("")
                st.error("Öneri: En kısa sürede bir kardiyoloji uzmanına görünmelisiniz.")
            else:
                st.markdown(f"<div class='metric-card low-risk'><h1>✅ SAĞLIKLI</h1><h3>Risk Skoru: %{risk_score}</h3></div>", unsafe_allow_html=True)
                st.write("")
                st.success("Öneri: Değerleriniz normal görünüyor. Düzenli kontrole devam edin.")
            
            st.write("")
            if st.button("⬅️ Yeni Hasta Analizi Yap", use_container_width=True):
                st.session_state['stage'] = 0
                st.rerun()

# --- TAB 2: REAL-TIME ---
with tab2:
    st.header("Anlık Analiz")
    patient_data_2 = create_input_form(key_suffix="_realtime")
    result_rt = predictor.predict(patient_data_2)
    risk = result_rt['risk_score']
    
    st.markdown("---")
    col_res1, col_res2 = st.columns([1, 3])
    with col_res1:
        st.metric(label="Risk Skoru", value=f"%{risk}", delta="-Sağlıklı" if risk < 50 else "+Hasta", delta_color="inverse")
    with col_res2:
        if result_rt['prediction'] == 1:
            st.warning(f"⚠️ **DİKKAT:** Yüksek risk grubu. (%{risk})")
        else:
            st.success(f"✅ **DURUM İYİ:** Sağlıklı değerler. (%{risk})")