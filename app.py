import streamlit as st

# ==============================
# CẤU HÌNH TRANG
# ==============================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# ==============================
# TIÊU ĐỀ
# ==============================
st.title("💰 TÍNH LÃI TIỀN GỬI TIẾT KIỆM")
st.write("Tính toán tiền lãi theo **lãi đơn** hoặc **lãi kép**.")

st.divider()

# ==============================
# HÀM ĐỊNH DẠNG TIỀN
# ==============================
def format_money(value):
    return f"{value:,.0f} VNĐ".replace(",", ".")


# ==============================
# NHẬP THÔNG TIN
# ==============================

st.subheader("📋 Thông tin tiền gửi")

so_tien = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=100_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)

ky_han = st.selectbox(
    "Kỳ hạn",
    [
        "1 tháng",
        "3 tháng",
        "6 tháng",
        "9 tháng",
        "12 tháng",
        "18 tháng",
        "24 tháng",
        "36 tháng"
    ]
)

hinh_thuc_lai = st.radio(
    "Phương pháp tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ],
    horizontal=True
)

hinh_thuc_lanh_lai = st.selectbox(
    "Hình thức lãnh lãi",
    [
        "Lãnh lãi hàng tháng",
        "Lãnh lãi hàng quý",
        "Lãnh lãi cuối kỳ"
    ]
)

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=5.0,
    step=0.1,
    format="%.2f"
)

# ==============================
# CHUYỂN KỲ HẠN SANG THÁNG
# ==============================

ky_han_thang = {
    "1 tháng": 1,
    "3 tháng": 3,
    "6 tháng": 6,
    "9 tháng": 9,
    "12 tháng": 12,
    "18 tháng": 18,
    "24 tháng": 24,
    "36 tháng": 36
}

so_thang = ky_han_thang[ky_han]

# Số năm
so_nam = so_thang / 12

# ==============================
# TÍNH TOÁN
# ==============================

if st.button("🧮 TÍNH TIỀN LÃI", use_container_width=True):

    if so_tien <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
    
    elif lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
    
    else:

        # ----------------------------------
        # LÃI ĐƠN
        # ----------------------------------
        if hinh_thuc_lai == "Lãi đơn":

            # Công thức:
            # I = P × r × t
            tong_tien_lai = so_tien * (lai_suat / 100) * so_nam

            # Tiền lãi theo tháng
            lai_thang = so_tien * (lai_suat / 100) / 12

            # Tiền lãi theo quý
            lai_quy = so_tien * (lai_suat / 100) / 4

            # Xác định tiền lãi định kỳ
            if hinh_thuc_lanh_lai == "Lãnh lãi hàng tháng":
                tien_lai_dinh_ky = lai_thang

            elif hinh_thuc_lanh_lai == "Lãnh lãi hàng quý":
                tien_lai_dinh_ky = lai_quy

            else:
                tien_lai_dinh_ky = tong_tien_lai

            tong_tien = so_tien + tong_tien_lai

        # ----------------------------------
        # LÃI KÉP
        # ----------------------------------
        else:

            lai = lai_suat / 100

            if hinh_thuc_lanh_lai == "Lãnh lãi hàng tháng":

                # Lãi suất tháng
                lai_thang = lai / 12

                # Số kỳ nhập lãi
                so_ky = so_thang

                # FV = P(1+r)^n
                tong_tien = so_tien * ((1 + lai_thang) ** so_ky)

                tong_tien_lai = tong_tien - so_tien

                # Lãi của kỳ đầu tiên
                tien_lai_dinh_ky = so_tien * lai_thang

            elif hinh_thuc_lanh_lai == "Lãnh lãi hàng quý":

                # Lãi suất quý
                lai_quy = lai / 4

                # Số quý
                so_ky = so_thang / 3

                # FV = P(1+r)^n
                tong_tien = so_tien * ((1 + lai_quy) ** so_ky)

                tong_tien_lai = tong_tien - so_tien

                # Lãi của quý đầu tiên
                tien_lai_dinh_ky = so_tien * lai_quy

            else:

                # Lãnh cuối kỳ:
                # Quy ước nhập lãi theo năm
                # hoặc theo số tháng của kỳ hạn
                lai_thang = lai / 12

                so_ky = so_thang

                tong_tien = so_tien * ((1 + lai_thang) ** so_ky)

                tong_tien_lai = tong_tien - so_tien

                tien_lai_dinh_ky = tong_tien_lai

        # ==============================
        # HIỂN THỊ KẾT QUẢ
        # ==============================

        st.divider()
        st.subheader("📊 KẾT QUẢ")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "💵 Tiền lãi định kỳ",
                format_money(tien_lai_dinh_ky)
            )

        with col2:
            st.metric(
                "📈 Tổng tiền lãi",
                format_money(tong_tien_lai)
            )

        st.success(
            f"💰 **Tổng số tiền gốc + lãi: {format_money(tong_tien)}**"
        )

        # ==============================
        # CHI TIẾT
        # ==============================

        st.divider()

        st.subheader("📝 Chi tiết khoản tiền gửi")

        st.write(f"**Số tiền gốc:** {format_money(so_tien)}")
        st.write(f"**Kỳ hạn:** {ky_han}")
        st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
        st.write(f"**Phương pháp:** {hinh_thuc_lai}")
        st.write(f"**Hình thức lãnh lãi:** {hinh_thuc_lanh_lai}")

        # ==============================
        # CÔNG THỨC
        # ==============================

        st.divider()

        st.subheader("📐 Công thức sử dụng")

        if hinh_thuc_lai == "Lãi đơn":

            st.latex(r"I = P \times r \times t")

            st.caption(
                "Trong đó: I là tiền lãi, P là tiền gốc, "
                "r là lãi suất theo năm và t là thời gian gửi tính theo năm."
            )

        else:

            st.latex(r"FV = PV(1+r)^n")

            st.caption(
                "Trong đó: FV là tổng tiền nhận được, PV là tiền gốc, "
                "r là lãi suất mỗi kỳ và n là số kỳ nhập lãi."
            )

        st.info(
            "Lưu ý: Kết quả trên là mô hình tính toán lý thuyết. "
            "Lãi suất thực tế của ngân hàng có thể áp dụng quy định "
            "riêng về số ngày gửi, cách làm tròn và điều kiện nhận lãi."
        )
