
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==============================
# 1. CẤU HÌNH TRANG WEB
# ==============================
st.set_page_config(
    page_title="Quản lý điểm sinh viên",
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
df["Tổng kết"] = (
    0.2 * df["Chuyên cần"]
    + 0.3 * df["Giữa kỳ"]
    + 0.5 * df["Cuối kỳ"]
).round(2)

# ==============================
# 4. XẾP LOẠI SINH VIÊN
# ==============================
def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7.0:
        return "Khá"
    elif diem >= 5.0:
        return "Trung bình"
    else:
        return "Yếu"
df["Xếp loại"] = df["Tổng kết"].apply(xep_loai)
# ==============================
# 5. BẢNG ĐIỂM SINH VIÊN
# ==============================
st.subheader(" 1. Bảng điểm của 10 sinh viên")
st.subheader("1. Bảng điểm của 10 sinh viên")

st.dataframe(
    df.reset_index(),
    use_container_width=True,
    hide_index=True
)

# ==============================
# 6. THỐNG KÊ ĐIỂM CỦA LỚP
# ==============================
diem_tb = df["Tổng kết"].mean()
diem_max = df["Tổng kết"].max()
diem_min = df["Tổng kết"].min()
so_sv_dat = int((df["Tổng kết"] >= 5.0).sum())

sv_max = df[df["Tổng kết"] == diem_max]
sv_min = df[df["Tổng kết"] == diem_min]

st.subheader("2. Thống kê kết quả học tập")

c1, c2, c3 = st.columns(3)

c1.metric("Điểm trung bình lớp", f"{diem_tb:.2f}")
c2.metric("Điểm cao nhất", f"{diem_max:.2f}")
c3.metric("Điểm thấp nhất", f"{diem_min:.2f}")

st.write("**Sinh viên có điểm tổng kết cao nhất:**")
for _, sv in sv_max.iterrows():
    st.write(f"- {sv['Họ và tên']} — {sv['Tổng kết']:.2f} điểm")
st.write("**Sinh viên có điểm tổng kết thấp nhất:**")
for _, sv in sv_min.iterrows():
    st.write(f"- {sv['Họ và tên']} — {sv['Tổng kết']:.2f} điểm")

st.metric(
    "Số sinh viên đạt (Tổng kết ≥ 5,0)",
    f"{so_sv_dat}/{len(df)}"
)
# ==============================
# 7. CHỌN SINH VIÊN BẰNG SELECTBOX
# ==============================
st.subheader("3. Tra cứu điểm từng sinh viên")
ten_sv = st.selectbox(
    "Chọn họ tên sinh viên:",
    df["Họ và tên"].tolist()
)

sv = df[df["Họ và tên"] == ten_sv].iloc[0]

st.write(f"**Họ và tên:** {sv['Họ và tên']}")

a, b, c = st.columns(3)
a.metric("Chuyên cần", f"{sv['Chuyên cần']:.1f}")
b.metric("Giữa kỳ", f"{sv['Giữa kỳ']:.1f}")
c.metric("Cuối kỳ", f"{sv['Cuối kỳ']:.1f}")

d, e = st.columns(2)
d.metric("Điểm tổng kết", f"{sv['Tổng kết']:.2f}")
e.metric("Xếp loại", sv["Xếp loại"])

# ==============================
# 8. BIỂU ĐỒ CỘT ĐIỂM TỔNG KẾT
# ==============================
st.subheader("4. Biểu đồ điểm tổng kết của 10 sinh viên")
ten_ngan = df["Họ và tên"].apply(lambda x: x.split()[-1])

fig, ax = plt.subplots(figsize=(8, 6))

bars = ax.barh(
    ten_ngan[::-1],
    df["Tong_ket"][::-1],
    color="#5B9BD5",
    height=0.6,
    edgecolor="#5B9BD5",
    linewidth=4,
    capstyle="round"
)
ax.set_title(
    "BIỂU ĐỒ ĐIỂM TỔNG KẾT CỦA 10 SINH VIÊN",
    fontsize=14,
    fontweight="bold"
)
ax.set_xlim(0, 10)

for spine in ax.spines.values():
    spine.set_visible(False)

ax.tick_params(axis="both", which="both", length=0, labelsize=11, labelcolor="#555555")
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
| MSSV: 038308020235")
