from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import (
    GroupKFold,
    GroupShuffleSplit,
    cross_val_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# 1. Đường dẫn
GOC = Path(__file__).resolve().parent
FILE_DATA = GOC / "data" / "processed" / "smartphones_clean.csv"
THU_MUC_LUU = GOC / "models" / "kaggle"
THU_MUC_LUU.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(FILE_DATA)

# 2. Chọn các thông số đầu vào
cot_so = [
    "5G_or_not",
    "num_cores",
    "processor_speed",
    "battery_capacity",
    "fast_charging_available",
    "fast_charging",
    "ram_capacity",
    "internal_memory",
    "screen_size",
    "refresh_rate",
    "num_rear_cameras",
    "primary_camera_rear",
    "primary_camera_front",
    "extended_memory_available",
    "resolution_height",
    "resolution_width",
]

cot_chu = ["brand_name", "processor_brand", "os"]

X = df[cot_so + cot_chu]
y = df["price_inr"]

# 3. Tạo nhóm dòng máy bằng cách bỏ phần RAM/bộ nhớ trong ngoặc.
# Đây là quy tắc ban đầu; cần rà soát nhóm trước báo cáo cuối cùng.
ten_nhom = (
    df["model"]
    .str.lower()
    .str.replace(r"\([^)]*(?:gb|tb)[^)]*\)", "", regex=True)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

nhom = df["brand_name"].fillna("unknown") + "|" + ten_nhom

# Tách khoảng 20% số nhóm làm tập kiểm tra
bo_chia = GroupShuffleSplit(
    n_splits=1,
    test_size=0.2,
    random_state=42,
)

idx_train, idx_test = next(bo_chia.split(X, y, groups=nhom))

X_train = X.iloc[idx_train]
X_test = X.iloc[idx_test]
y_train = y.iloc[idx_train]
y_test = y.iloc[idx_test]
nhom_train = nhom.iloc[idx_train]

assert set(nhom_train).isdisjoint(set(nhom.iloc[idx_test]))

print("Số điện thoại huấn luyện:", len(X_train))
print("Số điện thoại kiểm tra:", len(X_test))

# Lưu cách chia để kiểm tra và giải thích trong báo cáo
phan_chia = df[["model", "price_inr"]].copy()
phan_chia["nhom_dong_may"] = nhom
phan_chia["tap_du_lieu"] = "train"
phan_chia.loc[idx_test, "tap_du_lieu"] = "test"
phan_chia.to_csv(
    THU_MUC_LUU / "phan_chia_du_lieu.csv",
    index=False,
    encoding="utf-8-sig",
)

# 4. Quy trình xử lý dữ liệu số
xu_ly_so = Pipeline([
    ("dien_thieu", SimpleImputer(strategy="median")),
    ("chuan_hoa", StandardScaler()),
])

# 5. Quy trình xử lý dữ liệu chữ
xu_ly_chu = Pipeline([
    (
        "dien_thieu",
        SimpleImputer(strategy="constant", fill_value="unknown"),
    ),
    (
        "ma_hoa",
        OneHotEncoder(handle_unknown="ignore"),
    ),
])

tien_xu_ly = ColumnTransformer(
    [
        ("so", xu_ly_so, cot_so),
        ("chu", xu_ly_chu, cot_chu),
    ],
    sparse_threshold=1.0,
)

# 6. Các mô hình cần so sánh
cac_mo_hinh = {
    "Co_so_trung_vi": DummyRegressor(strategy="median"),
    "Linear_Regression": LinearRegression(),
    "Random_Forest": RandomForestRegressor(
        n_estimators=200,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
    ),
}

# 7. Chọn mô hình bằng đánh giá chéo trên tập train
# Tập test chưa được dùng trong bước lựa chọn.
cv = GroupKFold(n_splits=5)
ket_qua_cv = []
cac_pipeline = {}

for ten, thuat_toan in cac_mo_hinh.items():
    print(f"\nĐang đánh giá: {ten} ...")

    pipeline = Pipeline([
        ("tien_xu_ly", clone(tien_xu_ly)),
        ("mo_hinh", thuat_toan),
    ])

    diem = cross_val_score(
        pipeline,
        X_train,
        y_train,
        groups=nhom_train,
        cv=cv,
        scoring="neg_mean_absolute_error",
        n_jobs=1,
        error_score="raise",
    )

    ket_qua_cv.append({
        "mo_hinh": ten,
        "MAE_CV_INR": -diem.mean(),
        "do_lech_chuan_MAE": diem.std(),
    })
    cac_pipeline[ten] = pipeline

bang_cv = pd.DataFrame(ket_qua_cv).sort_values("MAE_CV_INR")
bang_cv.to_csv(
    THU_MUC_LUU / "so_sanh_mo_hinh.csv",
    index=False,
    encoding="utf-8-sig",
)

print("\n===== SO SÁNH TRÊN TẬP TRAIN =====")
print(bang_cv.round(2).to_string(index=False))

# 8. Huấn luyện mô hình được chọn và đánh giá trên test
ten_tot_nhat = bang_cv.iloc[0]["mo_hinh"]
mo_hinh_tot_nhat = cac_pipeline[ten_tot_nhat]

mo_hinh_tot_nhat.fit(X_train, y_train)
du_doan = mo_hinh_tot_nhat.predict(X_test)

mae = mean_absolute_error(y_test, du_doan)
rmse = np.sqrt(mean_squared_error(y_test, du_doan))
r2 = r2_score(y_test, du_doan)

print("\n===== KẾT QUẢ TRÊN TẬP TEST =====")
print("Mô hình được chọn:", ten_tot_nhat)
print(f"MAE:  {mae:,.2f} INR")
print(f"RMSE: {rmse:,.2f} INR")
print(f"R²:   {r2:.4f}")

pd.DataFrame([{
    "mo_hinh": ten_tot_nhat,
    "MAE_INR": mae,
    "RMSE_INR": rmse,
    "R2": r2,
}]).to_csv(
    THU_MUC_LUU / "danh_gia_test.csv",
    index=False,
    encoding="utf-8-sig",
)

# 9. Lưu dự đoán cho những điện thoại thuộc tập test
ket_qua_test = df.iloc[idx_test][["model", "price_inr"]].copy()
ket_qua_test["gia_du_doan_inr"] = du_doan
ket_qua_test["sai_so_tuyet_doi_inr"] = np.abs(
    y_test.to_numpy() - du_doan
)

ket_qua_test.to_csv(
    THU_MUC_LUU / "du_doan_test.csv",
    index=False,
    encoding="utf-8-sig",
)

# 10. Lưu mô hình và danh sách cột đầu vào
joblib.dump(
    {
        "pipeline": mo_hinh_tot_nhat,
        "ten_mo_hinh": ten_tot_nhat,
        "cot_dau_vao": cot_so + cot_chu,
        "don_vi_gia": "INR",
    },
    THU_MUC_LUU / "mo_hinh_gia.joblib",
)

if ten_tot_nhat == "Co_so_trung_vi":
    print("\nML chưa vượt mô hình cơ sở trong đánh giá chéo.")
    print("Cần xem lại dữ liệu và đặc trưng trước khi sử dụng.")

print("\nĐã lưu kết quả tại:", THU_MUC_LUU)
print("Hoàn thành huấn luyện!")