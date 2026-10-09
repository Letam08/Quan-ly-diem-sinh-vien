
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==============================
# 1. CẤU HÌNH TRANG WEB
# ==============================
st.set_page_config(
    page_title="QUẢN LÝ ĐIỂM SINH VIÊN",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 QUẢN LÝ ĐIỂM SINH VIÊN")
st.markdown("---")

# ==============================
# 2. TẠO DỮ LIỆU 10 SINH VIÊN
# ==============================
data = {
    "Họ và tên": [
        "Nguyễn Văn An",
        "Trần Thị Bình",
        "Phan Anh Sáng",
        "Phạm Quốc Dũng",
        "Vũ Thị Hà",
        "Đỗ Ngọc Lan",
        "Bùi Chí Dũng",
        "Lý Quốc Cường",
        "Lê Thu Thủy",
        "Hoàng Nhật Minh"
    ],
    "Chuyên cần": [
        8.5, 9.0, 7.0, 9.5, 8.0,
        6.5, 9.0, 7.5, 8.0, 9.5
    ],
    "Giữa kỳ": [
        7.0, 8.0, 6.5, 9.0, 7.5,
        5.0, 8.5, 7.0, 7.5, 9.0
    ],
    "Cuối kỳ": [
        7.5, 8.0, 6.5, 9.0, 7.0,
        4.5, 8.5, 7.0, 7.5, 9.5
    ]
}

df = pd.DataFrame(data)
df.index = range(1, len(df) + 1)
df.index.name = "STT"

# ==============================
# 3. TÍNH ĐIỂM TỔNG KẾT
# ==============================
df["Tong_ket"] = (
    0.2 * df["Chuyên cần"]
    + 0.3 * df["Giữa kỳ"]
    + 0.5 * df["Cuối kỳ"]
).round(2)

# ==============================
# 4. XẾP LOẠI SINH VIÊN
# ==============================
def Xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7.0:
        return "Khá"
    elif diem >= 5.0:
        return "Trung bình"
    else:
        return "Yếu"
df["Xep_loai"] = df["Tong_ket"].apply(Xep_loai)
# ==============================
# 5. BẢNG ĐIỂM SINH VIÊN
# ==============================
st.subheader(" 1. Bảng điểm của 10 sinh viên")
st.dataframe(df, use_container_width=True)
st.markdown("---")

# ==============================
# 6. THỐNG KÊ ĐIỂM CỦA LỚP
# ==============================
st.subheader("2. Thống kê kết quả học tập")
dtb_lop = round(df["Tong_ket"].mean(), 2)
sv_max = df.loc[df["Tong_ket"].idxmax()]
sv_min = df.loc[df["Tong_ket"].idxmin()]
so_sv_dat = int((df["Tong_ket"] >= 5.0).sum())

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="📈 Điểm trung bình lớp", value=f"{dtb_lop}")

with col2:
    st.metric(
        label="🏆 Điểm cao nhất",
        value=f"{sv_max['Tong_ket']}",
        delta=f"{sv_max['Họ và tên']}"
    )

with col3:
    st.metric(
        label="🔻 Điểm thấp nhất",
        value=f"{sv_min['Tong_ket']}",
        delta=f" {sv_min['Họ và tên']}",
        delta_color="inverse"
    )

with col4:
    st.metric(
        label="✅ Số sinh viên đạt (≥ 5.0)",
        value=f"{so_sv_dat}/{len(df)}"
    )
st.markdown("---")
# ==============================
# 7. CHỌN SINH VIÊN BẰNG SELECTBOX
# ==============================
st.subheader("3. Tra cứu điểm từng sinh viên")
selected_student = st.selectbox(
    "Chọn họ tên sinh viên:",
    options=df["Họ và tên"].tolist()
)
if selected_student:
    sv = df[df["Họ và tên"] == selected_student].iloc[0]

    st.write(f"**Họ và tên:** {sv['Họ và tên']}")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("📚 Chuyên cần", f"{sv['Chuyên cần']:.1f}")
    c2.metric("📝 Giữa kỳ", f"{sv['Giữa kỳ']:.1f}")
    c3.metric("🎯 Cuối kỳ", f"{sv['Cuối kỳ']:.1f}")
    c4.metric("⭐ Điểm tổng kết", f"{sv['Tong_ket']:.2f}")
    c5.metric("🏷️ Xếp loại", f"{sv['Xep_loai']}")
st.markdown("---")

# ==============================
# 8. BIỂU ĐỒ CỘT ĐIỂM TỔNG KẾT
# ==============================
st.subheader("4. Biểu đồ điểm tổng kết của 10 sinh viên")
ten_ngan = df["Họ và tên"].apply(lambda x: x.split()[-1])
fig, ax = plt.subplots(figsize=(8, 5))

bars = ax.barh(
    ten_ngan[::-1],
    df["Tong_ket"][::-1],
    color="#5B9BD5",
    height=0.6,
    edgecolor="#5B9BD5",
    linewidth=2,
    capstyle="round"
)
ax.set_title("BIỂU ĐỒ ĐIỂM TỔNG KẾT CỦA 10 SINH VIÊN", fontsize=12,\
             fontweight="bold")
ax.set_xlim(0, 10)
for spine in ax.spines.values():
    spine.set_visible(False)
ax.tick_params(axis="both", which="both", length=0, labelsize=10,\
               labelcolor="#555555")
ax.grid(axis="x", linestyle=":", alpha=0.4, color="gray")
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)
st.markdown("---")

# ==============================
# 9. THÔNG TIN NGƯỜI TẠO
# ==============================
st.markdown("---")
st.caption("Người tạo ứng dụng: LÊ THỊ MINH TÂM  \
| MSSV: 038308020235"
)
