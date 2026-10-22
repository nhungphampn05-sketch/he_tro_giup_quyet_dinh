from pathlib import Path
import pandas as pd


# 1. Xác định đường dẫn
THU_MUC_GOC = Path(__file__).resolve().parent
FILE_GOC = THU_MUC_GOC / "data" / "raw" / "smartphones.csv"
THU_MUC_LUU = THU_MUC_GOC / "data" / "processed"


def main():
    # 2. Kiểm tra file dữ liệu gốc
    if not FILE_GOC.exists():
        print("Không tìm thấy file CSV tại:")
        print(FILE_GOC)
        print("Hãy kiểm tra vị trí và tên file smartphones.csv.")
        return

    # 3. Đọc dữ liệu và chuẩn hóa tên cột
    df = pd.read_csv(FILE_GOC)
    so_dong_ban_dau = len(df)

    df.columns = df.columns.str.strip()

    # Kiểm tra các cột cần thiết
    cot_bat_buoc = [
        "brand_name",
        "model",
        "price",
        "processor_brand",
        "os",
        "ram_capacity",
        "internal_memory",
        "battery_capacity",
    ]

    cot_con_thieu = [
        cot for cot in cot_bat_buoc
        if cot not in df.columns
    ]

    if cot_con_thieu:
        print("File CSV thiếu các cột cần thiết:")
        print(", ".join(cot_con_thieu))
        print("Hãy kiểm tra lại bộ dữ liệu đầu vào.")
        return

    # 4. Hiển thị thông tin dữ liệu trước khi làm sạch
    print("\n===== KÍCH THƯỚC DỮ LIỆU GỐC =====")
    print("Số dòng:", df.shape[0])
    print("Số cột:", df.shape[1])

    print("\n===== DANH SÁCH CỘT =====")
    print(df.columns.tolist())

    print("\n===== 5 ĐIỆN THOẠI ĐẦU TIÊN =====")

    cot_hien_thi = [
        "brand_name",
        "model",
        "price",
        "ram_capacity",
        "internal_memory",
        "battery_capacity",
    ]

    print(df[cot_hien_thi].head().to_string(index=False))

    print("\n===== DỮ LIỆU THIẾU TRƯỚC XỬ LÝ =====")

    so_o_thieu = df.isna().sum()
    cot_thieu_du_lieu = so_o_thieu[so_o_thieu > 0]

    if cot_thieu_du_lieu.empty:
        print("Không có ô thiếu được Pandas nhận diện.")
    else:
        print(cot_thieu_du_lieu.to_string())

    print(
        "\nSố dòng trùng hoàn toàn trước xử lý:",
        df.duplicated().sum(),
    )

    # 5. Chuẩn hóa các cột dạng chữ
    cot_chu = [
        "brand_name",
        "model",
        "processor_brand",
        "os",
    ]

    for cot in cot_chu:
        df[cot] = (
            df[cot]
            .astype("string")
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
        )

        df[cot] = df[cot].replace("", pd.NA)

    # Thống nhất cách viết thương hiệu, hãng chip và hệ điều hành
    for cot in ["brand_name", "processor_brand", "os"]:
        df[cot] = df[cot].str.lower()

    # 6. Chuyển các cột còn lại sang dạng số
    for cot in df.columns:
        if cot not in cot_chu:
            df[cot] = pd.to_numeric(
                df[cot],
                errors="coerce",
            )

    # 7. Xóa dòng trùng hoàn toàn sau khi chuẩn hóa
    so_dong_trung = int(df.duplicated().sum())
    df = df.drop_duplicates()

    # 8. Chỉ giữ dòng có tên máy và giá hợp lệ
    so_dong_truoc_loc = len(df)

    df = df.dropna(subset=["model", "price"])
    df = df.loc[df["price"] > 0].copy()

    so_dong_khong_hop_le = so_dong_truoc_loc - len(df)

    # 9. Đổi tên cột để ghi rõ đơn vị giá
    df = df.rename(columns={"price": "price_inr"})

    # Giữ nguyên ô thiếu ở các thông số khác.
    # Khi huấn luyện, bộ điền giá trị thiếu sẽ được
    # học từ tập train trong pipeline.

    # 10. Lưu dữ liệu đã xử lý
    THU_MUC_LUU.mkdir(parents=True, exist_ok=True)

    file_ket_qua = THU_MUC_LUU / "smartphones_clean.csv"

    df.to_csv(
        file_ket_qua,
        index=False,
        encoding="utf-8-sig",
    )

    # 11. Tạo và lưu báo cáo dữ liệu thiếu
    bao_cao = (
        df.isna()
        .sum()
        .rename("so_o_thieu")
        .to_frame()
    )

    bao_cao.index.name = "ten_cot"

    bao_cao["ty_le_thieu_phan_tram"] = (
        bao_cao["so_o_thieu"] / max(len(df), 1) * 100
    ).round(2)

    file_bao_cao = THU_MUC_LUU / "bao_cao_du_lieu_thieu.csv"

    bao_cao.to_csv(
        file_bao_cao,
        encoding="utf-8-sig",
    )

    # 12. Hiển thị kết quả xử lý
    print("\n===== KẾT QUẢ XỬ LÝ =====")
    print("Số dòng ban đầu:", so_dong_ban_dau)
    print("Số dòng trùng đã loại:", so_dong_trung)
    print(
        "Số dòng thiếu tên máy hoặc giá không hợp lệ đã loại:",
        so_dong_khong_hop_le,
    )
    print("Số dòng sau xử lý:", len(df))
    print("Tổng số dòng đã loại:", so_dong_ban_dau - len(df))
    print("Số thương hiệu:", df["brand_name"].nunique())

    print("\n===== DỮ LIỆU THIẾU SAU XỬ LÝ =====")

    bao_cao_con_thieu = bao_cao.loc[
        bao_cao["so_o_thieu"] > 0
    ]

    if bao_cao_con_thieu.empty:
        print("Không còn ô thiếu.")
    else:
        print(bao_cao_con_thieu.to_string())

    print("\nĐã lưu dữ liệu tại:")
    print(file_ket_qua)

    print("\nĐã lưu báo cáo dữ liệu thiếu tại:")
    print(file_bao_cao)

    if df.empty:
        print("\nKhông còn dòng dữ liệu hợp lệ. Hãy kiểm tra CSV gốc.")
    else:
        print("\nHoàn thành đọc, kiểm tra và làm sạch dữ liệu!")


if __name__ == "__main__":
    main()