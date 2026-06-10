import os
import qrcode

data = "عمده فروشی ادویه اقبال نظری | واتساپ: 0744021732"

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)
qr.add_data(data)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")

# مسیر درست داخل app/static
output_path = os.path.join("app", "static", "qr_sale.png")

# اگر پوشه وجود ندارد، بساز
os.makedirs(os.path.dirname(output_path), exist_ok=True)

img.save(output_path)
print(f"QR ساخته شد و ذخیره شد در: {output_path}")
