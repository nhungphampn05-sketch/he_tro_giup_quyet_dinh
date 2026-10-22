from pathlib import Path
from urllib.request import urlopen
from datetime import datetime, timezone, timedelta
from html import escape
import json
import math

import joblib
import pandas as pd
import streamlit as st


GOC = Path(__file__).resolve().parent

st.set_page_config(
    page_title="Tư vấn điện thoại",
    layout="wide",
)


# ==================== GIAO DIỆN ====================

st.markdown("""
<style>
:root {color-scheme: dark;}

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stHeader"] {
    background: #08141E !important;
    color: #EAF5F4 !important;
}

[data-testid="stSidebar"] {
    background: #0D202C !important;
    border-right: 1px solid #244653;
}

[data-testid="stMainBlockContainer"] {
    max-width: 1180px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

[data-testid="stHeading"] h1 {
    font-size: clamp(1.5rem, 2.5vw, 2rem);
    line-height: 1.4;
    color: #EAF5F4;
}

[data-testid="stHeading"] h2,
[data-testid="stHeading"] h3 {
    font-size: 1.2rem;
    color: #EAF5F4;
}

[data-testid="stWidgetLabel"] p {
    color: #EAF5F4 !important;
}

[data-testid="stCaptionContainer"] p {
    color: #A9C5CA !important;
    line-height: 1.7;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    color: #D8EAE9;
}

[data-testid="stSidebar"] a {
    color: #5EEAD4;
}

[data-testid="stNumberInputContainer"],
[data-baseweb="select"] > div {
    background: #102B39 !important;
    color: #EAF5F4 !important;
    border-color: #244653 !important;
    border-radius: 10px;
}

[data-testid="stNumberInputContainer"] input,
[data-baseweb="select"] input {
    color: #EAF5F4 !important;
}

[data-testid="stNumberInputContainer"] button {
    background: #102B39 !important;
    color: #D8EAE9 !important;
}

[data-baseweb="popover"] [role="listbox"] {
    background: #102B39;
    color: #EAF5F4;
}

[data-baseweb="tag"] {
    background: #134E4A !important;
    color: #CCFBF1 !important;
}

[data-testid="stSlider"] {
    background: #102532;
    border: 1px solid #244653;
    border-radius: 12px;
    padding: 15px 15px 8px;
}

[data-testid="stSlider"] [role="slider"] {
    background: #2DD4BF !important;
}

[data-testid="stSlider"] [data-testid="stTickBar"],
[data-testid="stSlider"] [data-testid="stTickBar"] * {
    color: #A9C5CA !important;
}

[data-testid="stBaseButton-primary"] {
    background: #2DD4BF !important;
    border: 1px solid #2DD4BF !important;
    color: #062A28 !important;
    border-radius: 11px;
    min-height: 46px;
    padding: 10px 22px;
}

[data-testid="stBaseButton-primary"] p {
    color: #062A28 !important;
    font-weight: 700;
}

[data-testid="stBaseButton-primary"]:hover {
    background: #5EEAD4 !important;
    border-color: #5EEAD4 !important;
}

[data-testid="stBaseButton-primary"]:focus-visible {
    outline: 2px solid #99F6E4;
    outline-offset: 3px;
}

[data-testid="stExpander"] details {
    background: #102532;
    border: 1px solid #244653;
    border-radius: 12px;
    color: #EAF5F4;
}

[data-testid="stExpander"] summary {
    color: #EAF5F4 !important;
}

.dss-header {
    background: linear-gradient(115deg, #102532, #103440, #12443F);
    color: #EAF5F4;
    border: 1px solid #28534F;
    padding: 26px;
    border-radius: 16px;
    margin: 10px 0 16px;
}

.eyebrow {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: #A9C5CA;
}

.heading {
    font-size: 25px;
    font-weight: 800;
    margin: 8px 0;
}

.muted {
    font-size: 13px;
    line-height: 1.8;
    color: #A9C5CA;
}

.best-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 18px;
    padding: 23px;
    margin-bottom: 18px;
    border-radius: 15px;
    background: #102532;
    border: 1px solid #244653;
    border-left: 3px solid #2DD4BF;
    color: #EAF5F4;
}

.best-name {
    font-size: 22px;
    font-weight: 750;
    margin: 8px 0;
}

.score-box,
.small-score {
    background: #103D3B;
    border: 1px solid #28685F;
    color: #5EEAD4;
    border-radius: 12px;
    text-align: center;
}

.score-box {
    padding: 17px 22px;
    flex-shrink: 0;
}

.score-label {
    font-size: 10px;
    color: #A7F3D0;
    letter-spacing: 1px;
}

.big-score {
    font-size: 27px;
    font-weight: 800;
    margin-top: 7px;
}

.small-score {
    padding: 10px 13px;
    font-size: 19px;
    font-weight: 800;
}

.phone-details {
    margin-bottom: 12px;
    border: 1px solid #244653;
    border-radius: 14px;
    overflow: hidden;
    background: #102532;
    color: #EAF5F4;
}

.phone-card {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 18px 21px;
    background: #102532;
    color: #EAF5F4;
    cursor: pointer;
    list-style: none;
}

.phone-card::-webkit-details-marker {
    display: none;
}

.phone-card:hover {
    background: #153746;
}

.phone-card:focus-visible {
    outline: 2px solid #5EEAD4;
    outline-offset: -3px;
}

.rank {
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 39px;
    height: 43px;
    border-radius: 10px;
    background: #0F766E;
    color: #F0FDFA;
    font-size: 17px;
    font-weight: 800;
}

.phone-info {flex: 1; min-width: 0;}

.phone-name {
    font-size: 17px;
    font-weight: 750;
    overflow-wrap: anywhere;
}

.phone-price {
    font-size: 13px;
    font-weight: 600;
    color: #D8EAE9;
    margin-top: 5px;
}

.phone-specs {
    font-size: 12px;
    color: #A9C5CA;
    margin-top: 5px;
}

.detail-hint {
    color: #5EEAD4;
    font-size: 12px;
    margin-top: 9px;
}

.hint-close {display: none;}
.phone-details[open] .hint-open {display: none;}
.phone-details[open] .hint-close {display: inline;}

.detail-body {
    padding: 20px;
    border-top: 1px solid #244653;
    background: #0B1C28;
}

.detail-title {
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 15px;
}

.detail-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
}

.detail-item {
    background: #12303C;
    padding: 13px;
    border-radius: 9px;
}

.detail-label {
    color: #A9C5CA;
    font-size: 12px;
    margin-bottom: 5px;
}

.detail-value {
    color: #EAF5F4;
    font-size: 14px;
    overflow-wrap: anywhere;
}

.detail-note {
    color: #A9C5CA;
    font-size: 12px;
    margin-top: 15px;
    line-height: 1.7;
}

.breakdown {
    background: #102532;
    border: 1px solid #244653;
    color: #EAF5F4;
    padding: 23px;
    margin-top: 20px;
    border-radius: 15px;
}

.breakdown-title {
    font-size: 16px;
    font-weight: 750;
    margin-bottom: 19px;
}

.bar-label {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 8px;
    color: #A9C5CA;
    font-size: 13px;
    margin-bottom: 8px;
}

.bar-track {
    background: #23424E;
    height: 8px;
    border-radius: 20px;
    margin-bottom: 17px;
    overflow: hidden;
}

.bar-fill {
    height: 100%;
    border-radius: 20px;
    background: linear-gradient(90deg, #0D9488, #5EEAD4);
}

@media (max-width: 600px) {
    [data-testid="stMainBlockContainer"] {
        padding: 1.25rem 1rem;
    }
    .best-card {
        flex-direction: column;
        align-items: stretch;
    }
    .dss-header, .best-card, .breakdown {padding: 18px;}
    .heading {font-size: 22px;}
    .phone-card {padding: 14px 11px; gap: 10px;}
    .phone-name {font-size: 14px;}
    .detail-grid {grid-template-columns: 1fr;}
}
</style>
""", unsafe_allow_html=True)


# ==================== HÀM HỖ TRỢ ====================

def tien_viet(value):
    return f"{value:,.0f}".replace(",", ".") + " VNĐ"


@st.cache_data(ttl=3600, show_spinner=False)
def lay_ty_gia_tu_dong():
    with urlopen(
        "https://open.er-api.com/v6/latest/INR",
        timeout=10,
    ) as response:
        du_lieu = json.load(response)

    if (
        du_lieu.get("result") != "success"
        or du_lieu.get("base_code") != "INR"
    ):
        raise ValueError("Dữ liệu tỷ giá không hợp lệ.")

    ty_gia = float(du_lieu["rates"]["VND"])

    if not math.isfinite(ty_gia) or ty_gia <= 0:
        raise ValueError("Tỷ giá không hợp lệ.")

    thoi_diem = datetime.fromtimestamp(
        du_lieu["time_last_update_unix"],
        tz=timezone.utc,
    )

    return ty_gia, thoi_diem


def diem_tieu_chi(du_lieu, cot, danh_muc):
    nho_nhat = danh_muc[cot].min()
    lon_nhat = danh_muc[cot].max()

    if lon_nhat == nho_nhat:
        return pd.Series(1.0, index=du_lieu.index)

    diem = (
        (du_lieu[cot] - nho_nhat) / (lon_nhat - nho_nhat)
    ).clip(0, 1)

    if cot == "price_inr":
        diem = 1 - diem

    return diem


def hien_thi_de_xuat(top, danh_muc, trong_so, ty_gia):
    ten_tieu_chi = {
        "price_inr": "Giá thấp",
        "battery_capacity": "Dung lượng pin",
        "ram_capacity": "RAM",
        "refresh_rate": "Tần số quét",
    }

    may_dau = top.iloc[0]

    st.markdown(
        '<div class="dss-header">'
        '<div class="eyebrow">HỆ TRỢ GIÚP QUYẾT ĐỊNH</div>'
        '<div class="heading">Điện thoại dành cho bạn</div>'
        f'<div class="muted">{len(top)} gợi ý được xếp hạng '
        'theo điều kiện và mức độ ưu tiên của bạn.</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    uu_tien = " · ".join(
        ten_tieu_chi[cot]
        for cot, w in trong_so.items()
        if w > 0
    )

    st.markdown(
        '<div class="best-card">'
        '<div>'
        '<div class="eyebrow">GỢI Ý ĐỨNG ĐẦU</div>'
        f'<div class="best-name">{escape(str(may_dau["model"]))}</div>'
        '<div class="muted">✓ Đáp ứng bộ lọc của bạn<br>'
        '✓ Có điểm cao nhất trong danh sách đủ dữ liệu<br>'
        f'Tiêu chí đang xét: {escape(uu_tien)}</div>'
        '</div>'
        '<div class="score-box">'
        '<div class="score-label">ĐIỂM PHÙ HỢP</div>'
        f'<div class="big-score">{may_dau["diem_phu_hop"] / 10:.2f} / 10</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    for thu_hang, (_, may) in enumerate(top.iterrows(), start=1):
        def gia_tri(cot, don_vi=""):
            value = may.get(cot)

            if pd.isna(value):
                return "Chưa có dữ liệu"

            if isinstance(value, str):
                return value

            return f"{value:g}{don_vi}"

        def co_khong(cot):
            value = may.get(cot)

            if pd.isna(value):
                return "Chưa có dữ liệu"

            return "Có" if value == 1 else "Không"

        ten = escape(str(may["model"]))
        gia = tien_viet(may["price_inr"] * ty_gia)

        specs = (
            f"RAM {gia_tri('ram_capacity', ' GB')}"
            f" · Bộ nhớ {gia_tri('internal_memory', ' GB')}"
            f" · Pin {gia_tri('battery_capacity', ' mAh')}"
        )

        thong_tin = [
            ("Thương hiệu", gia_tri("brand_name")),
            ("Hệ điều hành", gia_tri("os")),
            ("Giá quy đổi", gia),
            ("Điểm phù hợp", f"{may['diem_phu_hop'] / 10:.2f}/10"),
            ("RAM", gia_tri("ram_capacity", " GB")),
            ("Bộ nhớ trong", gia_tri("internal_memory", " GB")),
            ("Dung lượng pin", gia_tri("battery_capacity", " mAh")),
            ("Hỗ trợ sạc nhanh", co_khong("fast_charging_available")),
            ("Công suất sạc nhanh", gia_tri("fast_charging", " W")),
            ("Hãng bộ xử lý", gia_tri("processor_brand")),
            ("Số nhân CPU", gia_tri("num_cores")),
            ("Tốc độ CPU", gia_tri("processor_speed", " GHz")),
            ("Kích thước màn hình", gia_tri("screen_size", " inch")),
            ("Tần số quét", gia_tri("refresh_rate", " Hz")),
            ("Chiều rộng độ phân giải", gia_tri("resolution_width", " px")),
            ("Chiều cao độ phân giải", gia_tri("resolution_height", " px")),
            ("Camera chính phía sau", gia_tri("primary_camera_rear", " MP")),
            ("Camera trước", gia_tri("primary_camera_front", " MP")),
            ("Số camera sau", gia_tri("num_rear_cameras")),
            ("Hỗ trợ 5G", co_khong("5G_or_not")),
            ("Hỗ trợ thẻ nhớ", co_khong("extended_memory_available")),
            ("Điểm đánh giá trong dữ liệu", gia_tri("avg_rating")),
        ]

        cac_o = "".join(
            '<div class="detail-item">'
            f'<div class="detail-label">{escape(nhan)}</div>'
            f'<div class="detail-value">{escape(str(value))}</div>'
            '</div>'
            for nhan, value in thong_tin
        )

        st.markdown(
            '<details class="phone-details">'
            '<summary class="phone-card">'
            f'<div class="rank">{thu_hang}</div>'
            '<div class="phone-info">'
            f'<div class="phone-name">{ten}</div>'
            f'<div class="phone-price">{gia}</div>'
            f'<div class="phone-specs">{escape(specs)}</div>'
            '<div class="detail-hint">'
            '<span class="hint-open">▼ Bấm để xem thông tin chi tiết</span>'
            '<span class="hint-close">▲ Bấm để thu gọn</span>'
            '</div>'
            '</div>'
            f'<div class="small-score">{may["diem_phu_hop"] / 10:.2f}</div>'
            '</summary>'
            '<div class="detail-body">'
            f'<div class="detail-title">Thông số của {ten}</div>'
            f'<div class="detail-grid">{cac_o}</div>'
            '</div>'
            '</details>',
            unsafe_allow_html=True,
        )

    tong = sum(trong_so.values())
    cac_thanh = []

    for cot, w in trong_so.items():
        if w == 0:
            continue

        diem = float(
            diem_tieu_chi(top.iloc[[0]], cot, danh_muc).iloc[0]
        )

        ty_trong = w / tong * 100
        dong_gop = diem * w / tong * 10

        cac_thanh.append(
            '<div class="bar-label">'
            f'<span>{ten_tieu_chi[cot]} · trọng số {ty_trong:.1f}%</span>'
            f'<span>{diem * 10:.2f}/10'
            f' · đóng góp {dong_gop:.2f} điểm</span>'
            '</div>'
            '<div class="bar-track">'
            f'<div class="bar-fill" style="width:{diem * 100:.2f}%"></div>'
            '</div>'
        )

    st.markdown(
        '<div class="breakdown">'
        '<div class="breakdown-title">'
        'PHÂN TÍCH ĐIỂM CỦA MÁY ĐỨNG ĐẦU'
        '</div>'
        + "".join(cac_thanh)
        + '</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "Tổng điểm bằng tổng đóng góp của các tiêu chí "
        "(có thể chênh lệch nhỏ do làm tròn). "
        "Điểm phù hợp không phải xác suất hài lòng."
    )

    with st.expander("So sánh giá dữ liệu và giá AI dự đoán"):
        bang_ml = pd.DataFrame({
            "Điện thoại": top["model"],
            "Giá quy đổi (VNĐ)": (
                top["price_inr"] * ty_gia
            ).round(0),
            "Giá ML tham khảo (VNĐ)": (
                top["gia_ml_inr"] * ty_gia
            ).round(0),
        })

        st.dataframe(bang_ml, hide_index=True)

        st.caption(
            "Giá AI dự đoán chỉ mang tính tham khảo, không phải giá bán "
            "hiện tại và không ảnh hưởng đến thứ tự đề xuất điện thoại."
        )


# ==================== DỮ LIỆU ====================

st.title("Chọn điện thoại phù hợp với bạn")
st.caption(
    "Giá hiển thị bằng VNĐ, quy đổi từ dữ liệu Kaggle của Ấn Độ. "
    "Đây không phải giá bán thực tế tại Việt Nam."
)

file_data = GOC / "data" / "processed" / "smartphones_clean.csv"
file_model = GOC / "models" / "kaggle" / "mo_hinh_gia.joblib"

if not file_data.exists() or not file_model.exists():
    st.error(
        "Thiếu dữ liệu hoặc mô hình. "
        "Hãy chạy bước xử lý dữ liệu và huấn luyện trước."
    )
    st.stop()

df = pd.read_csv(file_data)
goi_model = joblib.load(file_model)


# ==================== TỶ GIÁ ====================

st.sidebar.header("Điều kiện lựa chọn")

try:
    with st.spinner("Đang lấy tỷ giá INR → VNĐ..."):
        ty_gia, thoi_diem_cap_nhat = lay_ty_gia_tu_dong()
except Exception:
    st.error(
        "Chưa lấy được tỷ giá. "
        "Hãy kiểm tra kết nối Internet và tải lại trang."
    )
    st.stop()

gio_viet_nam = thoi_diem_cap_nhat.astimezone(
    timezone(timedelta(hours=7))
)

st.sidebar.info(f"1 INR = {ty_gia:,.2f} VNĐ")
st.sidebar.caption(
    "Nguồn cập nhật: "
    + gio_viet_nam.strftime("%d/%m/%Y %H:%M")
    + " (giờ Việt Nam)"
)
st.sidebar.caption(
    "[Nguồn tỷ giá: ExchangeRate-API](https://www.exchangerate-api.com)"
)

if (
    datetime.now(timezone.utc) - thoi_diem_cap_nhat
    > timedelta(hours=48)
):
    st.warning(
        "Tỷ giá nguồn đã hơn 48 giờ chưa cập nhật. "
        "Giá quy đổi dùng tỷ giá tại thời điểm ghi ở thanh bên."
    )


# ==================== BỘ LỌC ====================

ngan_sach_vnd = st.sidebar.number_input(
    "Ngân sách tối đa (VNĐ)",
    min_value=0,
    value=9000000,
    step=500000,
)

st.sidebar.write(f"Ngân sách: {tien_viet(ngan_sach_vnd)}")
ngan_sach = ngan_sach_vnd / ty_gia

hang = st.sidebar.multiselect(
    "Thương hiệu — để trống nếu chọn tất cả",
    sorted(df["brand_name"].dropna().unique().tolist()),
)

he_dieu_hanh = st.sidebar.selectbox(
    "Hệ điều hành",
    ["Tất cả"] + sorted(df["os"].dropna().unique().tolist()),
)

ram = st.sidebar.selectbox(
    "RAM tối thiểu (GB)",
    [1, 2, 3, 4, 6, 8, 12, 16],
    index=3,
)

bo_nho = st.sidebar.selectbox(
    "Bộ nhớ tối thiểu (GB)",
    [8, 16, 32, 64, 128, 256, 512],
    index=3,
)

can_5g = st.sidebar.checkbox("Bắt buộc hỗ trợ 5G")

st.subheader("Mức độ ưu tiên")
st.write("Chọn mức ưu tiên từ 0 đến 5; mức 0 là bỏ qua tiêu chí.")

c1, c2, c3, c4 = st.columns(4)
w_gia = c1.slider("Giá thấp", 0, 5, 3)
w_pin = c2.slider("Dung lượng pin lớn", 0, 5, 3)
w_ram = c3.slider("RAM lớn", 0, 5, 2)
w_man_hinh = c4.slider("Tần số quét cao", 0, 5, 2)



# ==================== XẾP HẠNG ====================

if st.button("Tìm điện thoại phù hợp", type="primary"):
    trong_so = {
        "price_inr": w_gia,
        "battery_capacity": w_pin,
        "ram_capacity": w_ram,
        "refresh_rate": w_man_hinh,
    }

    tong = sum(trong_so.values())

    if tong == 0:
        st.warning("Hãy đặt ít nhất một mức ưu tiên lớn hơn 0.")
        st.stop()

    ket_qua = df.loc[
        (df["price_inr"] <= ngan_sach)
        & (df["ram_capacity"] >= ram)
        & (df["internal_memory"] >= bo_nho)
    ].copy()

    if hang:
        ket_qua = ket_qua[ket_qua["brand_name"].isin(hang)]

    if he_dieu_hanh != "Tất cả":
        ket_qua = ket_qua[ket_qua["os"] == he_dieu_hanh]

    if can_5g:
        ket_qua = ket_qua[ket_qua["5G_or_not"] == 1]

    cot_can = [cot for cot, w in trong_so.items() if w > 0]
    so_truoc = len(ket_qua)

    ket_qua = ket_qua.dropna(subset=cot_can).copy()
    so_thieu = so_truoc - len(ket_qua)

    if so_thieu:
        st.info(
            f"Có {so_thieu} máy đáp ứng bộ lọc nhưng thiếu "
            "thông số đang được ưu tiên, nên chưa được xếp hạng."
        )

    if ket_qua.empty:
        st.warning(
            "Không có điện thoại phù hợp. "
            "Hãy tăng ngân sách hoặc giảm điều kiện lọc."
        )
        st.stop()

    ket_qua["diem_phu_hop"] = 0.0

    for cot, w in trong_so.items():
        if w > 0:
            ket_qua["diem_phu_hop"] += (
                diem_tieu_chi(ket_qua, cot, df) * w / tong * 100
            )

    ket_qua = ket_qua.sort_values(
        ["diem_phu_hop", "price_inr"],
        ascending=[False, True],
    )

    top = ket_qua.head(5).copy()

    top["gia_ml_inr"] = goi_model["pipeline"].predict(
        top[goi_model["cot_dau_vao"]]
    )

    st.caption(
        f"Có {len(ket_qua)} điện thoại đủ điều kiện xếp hạng. "
        f"Đang hiển thị {len(top)} gợi ý đầu."
    )

    hien_thi_de_xuat(top, df, trong_so, ty_gia)