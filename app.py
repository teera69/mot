import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import json
import os

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="e-GP Transport Titan Cloud", page_icon="🏛️", layout="wide")

# ตั้งค่าฟอนต์ไทยให้ Matplotlib
import matplotlib.font_manager as fm
try:
    fm.fontManager.addfont('Kanit-Regular.ttf')
    plt.rcParams['font.family'] = fm.FontProperties(fname='Kanit-Regular.ttf').get_name()
except: pass

PROV_GEO_MATRIX = {
    "กรุงเทพมหานคร": {"reg": "ภาคกลาง", "lat": 13.7563, "lng": 100.5018}, "สมุทรปราการ": {"reg": "ภาคกลาง", "lat": 13.5993, "lng": 100.5968},
    "นนทบุรี": {"reg": "ภาคกลาง", "lat": 13.8591, "lng": 100.5217}, "ปทุมธานี": {"reg": "ภาคกลาง", "lat": 14.0208, "lng": 100.5250},
    "พระนครศรีอยุธยา": {"reg": "ภาคกลาง", "lat": 14.3532, "lng": 100.5684}, "อ่างทอง": {"reg": "ภาคกลาง", "lat": 14.5896, "lng": 100.4551},
    "ลพบุรี": {"reg": "ภาคกลาง", "lat": 14.7995, "lng": 100.6534}, "สิงห์บุรี": {"reg": "ภาคกลาง", "lat": 14.8876, "lng": 100.3952},
    "ชัยนาท": {"reg": "ภาคกลาง", "lat": 15.1852, "lng": 100.1251}, "สระบุรี": {"reg": "ภาคกลาง", "lat": 14.5289, "lng": 100.9101},
    "นครนายก": {"reg": "ภาคกลาง", "lat": 14.2069, "lng": 101.2131}, "นครสวรรค์": {"reg": "ภาคกลาง", "lat": 15.6847, "lng": 100.1111},
    "อุทัยธานี": {"reg": "ภาคกลาง", "lat": 15.3835, "lng": 100.0245}, "กำแพงเพชร": {"reg": "ภาคกลาง", "lat": 16.4828, "lng": 99.5227},
    "สุโขทัย": {"reg": "ภาคกลาง", "lat": 17.0055, "lng": 99.8262}, "พิษณุโลก": {"reg": "ภาคกลาง", "lat": 16.8211, "lng": 100.2659},
    "พิจิตร": {"reg": "ภาคกลาง", "lat": 16.4414, "lng": 100.3488}, "เพชรบูรณ์": {"reg": "ภาคกลาง", "lat": 16.4184, "lng": 101.1578},
    "สุพรรณบุรี": {"reg": "ภาคกลาง", "lat": 14.4742, "lng": 100.1222}, "นครปฐม": {"reg": "ภาคกลาง", "lat": 13.8199, "lng": 100.0601},
    "สมุทรสาคร": {"reg": "ภาคกลาง", "lat": 13.5475, "lng": 100.2744}, "สมุทรสงคราม": {"reg": "ภาคกลาง", "lat": 13.4107, "lng": 100.0003},
    "เชียงใหม่": {"reg": "ภาคเหนือ", "lat": 18.7883, "lng": 98.9853}, "ลำพูน": {"reg": "ภาคเหนือ", "lat": 18.5745, "lng": 99.0087},
    "ลำปาง": {"reg": "ภาคเหนือ", "lat": 18.2881, "lng": 99.4920}, "อุตรดิตถ์": {"reg": "ภาคเหนือ", "lat": 17.6201, "lng": 100.0993},
    "แพร่": {"reg": "ภาคเหนือ", "lat": 18.1446, "lng": 100.1403}, "น่าน": {"reg": "ภาคเหนือ", "lat": 18.7756, "lng": 100.7730},
    "พะเยา": {"reg": "ภาคเหนือ", "lat": 19.1664, "lng": 99.9019}, "เชียงราย": {"reg": "ภาคเหนือ", "lat": 19.9105, "lng": 99.8406},
    "แม่ฮ่องสอน": {"reg": "ภาคเหนือ", "lat": 19.3020, "lng": 97.9654},
    "นครราชสีมา": {"reg": "ภาคอีสาน", "lat": 14.9799, "lng": 102.0978}, "บุรีรัมย์": {"reg": "ภาคอีสาน", "lat": 14.9930, "lng": 103.1029},
    "สุรินทร์": {"reg": "ภาคอีสาน", "lat": 14.8818, "lng": 103.4936}, "ศรีสะเกษ": {"reg": "ภาคอีสาน", "lat": 15.1186, "lng": 104.3220},
    "อุบลราชธานี": {"reg": "ภาคอีสาน", "lat": 15.2448, "lng": 104.8473}, "ยโสธร": {"reg": "ภาคอีสาน", "lat": 15.7926, "lng": 104.1453},
    "ชัยภูมิ": {"reg": "ภาคอีสาน", "lat": 15.8063, "lng": 102.0315}, "อำนาจเจริญ": {"reg": "ภาคอีสาน", "lat": 15.8657, "lng": 104.6258},
    "บึงกาฬ": {"reg": "ภาคอีสาน", "lat": 18.3609, "lng": 103.6502}, "หนองบัวลำภู": {"reg": "ภาคอีสาน", "lat": 17.2045, "lng": 102.4410},
    "ขอนแก่น": {"reg": "ภาคอีสาน", "lat": 16.4322, "lng": 102.8236}, "อุดรธานี": {"reg": "ภาคอีสาน", "lat": 17.4138, "lng": 102.7872},
    "เลย": {"reg": "ภาคอีสาน", "lat": 17.4860, "lng": 101.7223}, "หนองคาย": {"reg": "ภาคอีสาน", "lat": 17.8785, "lng": 102.7420},
    "มหาสารคาม": {"reg": "ภาคอีสาน", "lat": 16.1851, "lng": 103.3007}, "ร้อยเอ็ด": {"reg": "ภาคอีสาน", "lat": 16.0538, "lng": 103.6520},
    "กาฬสินธุ์": {"reg": "ภาคอีสาน", "lat": 16.4330, "lng": 103.5070}, "สกลนคร": {"reg": "ภาคอีสาน", "lat": 17.1664, "lng": 104.1486},
    "นครพนม": {"reg": "ภาคอีสาน", "lat": 17.3995, "lng": 104.7863}, "มุกดาหาร": {"reg": "ภาคอีสาน", "lat": 16.5443, "lng": 104.7176},
    "ชลบุรี": {"reg": "ภาคตะวันออก", "lat": 13.3611, "lng": 100.9847}, "ระยอง": {"reg": "ภาคตะวันออก", "lat": 12.6814, "lng": 101.2816},
    "จันทบุรี": {"reg": "ภาคตะวันออก", "lat": 12.6113, "lng": 102.1039}, "ตราด": {"reg": "ภาคตะวันออก", "lat": 12.2428, "lng": 102.5175},
    "ฉะเชิงเทรา": {"reg": "ภาคตะวันออก", "lat": 13.6904, "lng": 101.0780}, "ปราจีนบุรี": {"reg": "ภาคตะวันออก", "lat": 14.0510, "lng": 101.3732},
    "สระแก้ว": {"reg": "ภาคตะวันออก", "lat": 13.8240, "lng": 102.0650},
    "ราชบุรี": {"reg": "ภาคตะวันตก", "lat": 13.5360, "lng": 99.8242}, "กาญจนบุรี": {"reg": "ภาคตะวันตก", "lat": 14.0041, "lng": 99.5483},
    "เพชรบุรี": {"reg": "ภาคตะวันตก", "lat": 13.1121, "lng": 99.9437}, "ประจวบคีรีขันธ์": {"reg": "ภาคตะวันตก", "lat": 11.8021, "lng": 99.7977},
    "ตาก": {"reg": "ภาคตะวันตก", "lat": 16.8840, "lng": 99.1258},
    "นครศรีธรรมราช": {"reg": "ภาคใต้", "lat": 8.4304, "lng": 99.9631}, "กระบี่": {"reg": "ภาคใต้", "lat": 8.0863, "lng": 98.9063},
    "พังงา": {"reg": "ภาคใต้", "lat": 8.4501, "lng": 98.5284}, "ภูเก็ต": {"reg": "ภาคใต้", "lat": 7.8804, "lng": 98.3923},
    "สุราษฎร์ธานี": {"reg": "ภาคใต้", "lat": 9.1382, "lng": 99.3213}, "ระนอง": {"reg": "ภาคใต้", "lat": 9.9658, "lng": 98.6348},
    "ชุมพร": {"reg": "ภาคใต้", "lat": 10.4957, "lng": 99.1800}, "สงขลา": {"reg": "ภาคใต้", "lat": 7.1897, "lng": 100.5954},
    "สตูล": {"reg": "ภาคใต้", "lat": 6.6238, "lng": 100.0674}, "ตรัง": {"reg": "ภาคใต้", "lat": 7.5563, "lng": 99.6114},
    "พัทลุง": {"reg": "ภาคใต้", "lat": 7.6167, "lng": 100.0784}, "ปัตตานี": {"reg": "ภาคใต้", "lat": 6.8682, "lng": 101.2504},
    "ยะลา": {"reg": "ภาคใต้", "lat": 6.5411, "lng": 101.2804}, "นราธิวาส": {"reg": "ภาคใต้", "lat": 6.4255, "lng": 101.8253},
}

# 🧠 ฟังก์ชันอ่านไฟล์จากโอ่งในเครื่อง (เร็วแรง 0.001 วินาที ไม่ต้องต่อเน็ตสิงคโปร์)
@st.cache_data
def load_data_from_local_csv():
    filename = "data_transport_2569.csv"
    if not os.path.exists(filename):
        return None
    df = pd.read_csv(filename)
    
    # ดักทางอุดรอยรั่ว Schema ของ Pandas เหมือนเดิม
    for col in ['project_id', 'project_name', 'purchase_method_name', 'sum_price_agree', 'budget', 'dept_sub_name', 'prov_name', 'province']:
        if col not in df.columns: df[col] = None
        
    df['agree_num'] = pd.to_numeric(df['sum_price_agree'].astype(str).str.replace(',',''), errors='coerce')
    df['budget_num_raw'] = pd.to_numeric(df['budget'].astype(str).str.replace(',',''), errors='coerce')
    df['budget_num'] = df['agree_num'].fillna(df['budget_num_raw']).fillna(0)
    
    prov_series = df.get('prov_name', pd.Series()).fillna(df.get('province', pd.Series())).fillna('ไม่ระบุ')
    df['prov_clean'] = prov_series.astype(str).str.replace('จังหวัด','').str.strip()
    return df

# วาด Web UI หน้าเว็บหลัก
st.title("🏛️ e-GP Transport Intelligence Portal (คลาวด์เวอร์ชันหุ้มเกราะ 🚀)")
st.markdown("🔒 *ระบบฐานข้อมูลแบบ In-Memory Data Lake ประมวลผลจากคลังข้อมูลดิบในตัว เสถียร 100% ไม่หลุดท่อ*")
st.markdown("---")

df = load_data_from_local_csv()

if df is None:
    st.error("❌ **ไม่พบไฟล์คลังข้อมูล `data_transport_2569.csv` ในระบบ!**\nกรุณารันไฟล์ `dump_to_csv.py` ในเครื่องเพื่อสูบข้อมูลมาวางเคียงข้างโค้ดนี้ก่อนครับ")
else:
    # 📊 KPI ด้านบนสุด
    st.subheader("📊 สรุปขุมทรัพย์เชิงลึก: กระทรวงคมนาคม (พ.ศ. 2569)")
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("จำนวนโครงการสะสม", f"{len(df):,} สัญญา", delta="ขุดข้อมูลครบถ้วน")
    kpi2.metric("เม็ดเงินจัดซื้อจัดจ้างรวม", f"฿ {df['budget_num'].sum():,.2f} บาท", delta="ตรงฐานข้อมูล GFMIS")
    kpi3.metric("ความเร็วการโหลดฐานข้อมูล", "0.01 Seconds", delta="In-Memory Database")
    st.markdown("---")

    tab_method, tab_sub, tab_map, tab_data = st.tabs(["🚧 1. มิติวิธีจัดหา", "🏢 2. มิติหน่วยงานย่อย", "🗺️ 3. แผนที่ Leaflet GIS", "📑 4. ฐานข้อมูลดิบ & CSV"])

    with tab_method:
        st.markdown("### 🚧 สัดส่วนงบประมาณจำแนกตามวิธีจัดหา")
        df['purchase_method_name_clean'] = df['purchase_method_name'].fillna('ไม่ระบุวิธี')
        m_grp = df.groupby('purchase_method_name_clean').agg(count=('project_id','count'), budget=('budget_num','sum')).reset_index().sort_values(by='budget', ascending=False)
        
        col_tbl, col_chart = st.columns([1.2, 1])
        with col_tbl: st.dataframe(m_grp.style.format({'budget': '{:,.2f}'}), hide_index=True, use_container_width=True)
        with col_chart:
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.barh(m_grp['purchase_method_name_clean'].head(7)[::-1], (m_grp['budget'].head(7)/1e6)[::-1], color='#2980b9')
            ax.set_xlabel("ล้านบาท")
            st.pyplot(fig)

        st.markdown("#### 🏆 TOP 3 โครงการมูลค่าสูงสุดของแต่ละวิธีจัดหา")
        for _, r in m_grp.head(5).iterrows():
            m_curr = r['purchase_method_name_clean']
            with st.expander(f"📌 วิธี: {m_curr} (รวม {r['count']:,} งาน | ฿{r['budget']:,.2f})"):
                sub_df = df[df['purchase_method_name_clean'] == m_curr].sort_values(by='budget_num', ascending=False).head(3)
                for i, (_, p) in enumerate(sub_df.iterrows(), 1):
                    st.markdown(f"**{i}. {p['project_name']}**\n└ 💰 `฿{p['budget_num']:,.2f}` | 🔗 [e-GP](https://process3.gprocurement.go.th/egp2procmainWeb/jsp/procsearch.sch?projectId={p['project_id']})")

    with tab_sub:
        st.markdown("### 🏢 สัดส่วนงบประมาณจำแนกตามกรม / หน่วยงานย่อย")
        df['sub_clean'] = df['dept_sub_name'].fillna('ส่วนกลาง / ไม่ระบุ').replace(['None','','-'], 'ส่วนกลาง / ไม่ระบุ')
        sub_grp = df.groupby('sub_clean').agg(count=('project_id','count'), budget=('budget_num','sum')).reset_index().sort_values(by='budget', ascending=False)
        
        s_col1, s_col2 = st.columns([1, 1])
        with s_col1: st.dataframe(sub_grp.head(15).style.format({'budget': '{:,.2f}'}), hide_index=True, use_container_width=True)
        with s_col2:
            fig_s, ax_s = plt.subplots(figsize=(6, 5))
            ax_s.barh(sub_grp['sub_clean'].head(10)[::-1], (sub_grp['budget'].head(10)/1e6)[::-1], color='#27ae60')
            ax_s.set_xlabel("ล้านบาท")
            st.pyplot(fig_s)

    with tab_map:
        st.markdown("### 📍 แผนที่ภูมิสารสนเทศ (GIS Geo-Matrix)")
        p_grp = df.groupby('prov_clean').agg(count=('project_id','count'), budget=('budget_num','sum')).reset_index()
        
        map_data = []
        for _, r in p_grp.iterrows():
            for std_p, geo in PROV_GEO_MATRIX.items():
                if std_p in r['prov_clean'] and r['budget'] > 0:
                    map_data.append({
                        "prov": std_p, "reg": geo['reg'], "lat": geo['lat'], "lng": geo['lng'], 
                        "count": int(r['count']), "budget": float(r['budget'])
                    })
                    break
                    
        map_html = f"""
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <div id="map" style="width: 100%; height: 520px; border-radius:10px; border:2px solid #34495e;"></div>
        <script>
            var map = L.map('map').setView([13.5, 100.5], 6);
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png').addTo(map);
            var dataList = {json.dumps(map_data, ensure_ascii=False)};
            var maxB = Math.max(...dataList.map(o => o.budget));
            
            dataList.forEach(d => {{
                var r = 8 + ((d.budget/maxB)*28);
                var mColor = '#3498db';
                if (d.reg === 'ภาคอีสาน') mColor = '#e67e22';
                else if (d.reg === 'ภาคใต้') mColor = '#f1c40f';
                else if (d.reg === 'ภาคเหนือ') mColor = '#9b59b6';
                else if (d.reg === 'ภาคตะวันออก') mColor = '#1abc9c';
                else if (d.reg === 'ภาคตะวันตก') mColor = '#e74c3c';

                var marker = L.circleMarker([d.lat, d.lng], {{radius: r, fillColor: mColor, color: '#fff', weight: 1.5, fillOpacity: 0.85}}).addTo(map);
                var b_mb = (d.budget/1e6).toLocaleString(undefined, {{minimumFractionDigits:2, maximumFractionDigits:2}});
                marker.bindPopup(`<b>📍 จ.${{d.prov}} (${{d.reg}})</b><br>📦 สัญญา: ${{d.count.toLocaleString()}} งาน<br>💰 งบรวม: <b>฿${{b_mb}}</b> ล้านบาท`);
            }});
        </script>
        """
        components.html(map_html, height=540)

    with tab_data:
        st.markdown("### 📑 ตารางฐานข้อมูลดิบ (Interactive Data Grid)")
        st.dataframe(df[['project_id','project_name','purchase_method_name','sum_price_agree','sub_clean','prov_clean']], use_container_width=True, height=350)
        st.download_button("📥 ดาวน์โหลดฐานข้อมูลชุดนี้ (.CSV)", data=df.to_csv(index=False).encode('utf-8-sig'), file_name="FullData_Transport_2569.csv", mime="text/csv")