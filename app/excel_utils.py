# app/excel_utils.py
import io
import pandas as pd
from datetime import datetime
from flask import send_file

def generate_creditor_excel_report(creditor, transactions):
    """
    تولید گزارش Excel برای تراکنش‌های یک طلبکار
    """
    try:
        # ایجاد DataFrame از تراکنش‌ها
        data = []
        for i, t in enumerate(transactions, 1):
            data.append({
                'ردیف': i,
                'تاریخ تراکنش': t.date_created.strftime('%Y-%m-%d %H:%M'),
                'نوع تراکنش': 'افزایش بدهی' if t.transaction_type == 'debt' else 'پرداخت بدهی',
                'مبلغ (افغانی)': t.amount,
                'شماره رسید': t.receipt_number or '',
                'توضیحات': t.description or '',
                'ثبت کننده': t.user.full_name
            })
        
        df = pd.DataFrame(data)
        
        # محاسبات مالی
        total_debt = sum(t.amount for t in transactions if t.transaction_type == 'debt')
        total_payment = sum(t.amount for t in transactions if t.transaction_type == 'payment')
        
        # ایجاد Excel writer
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # صفحه تراکنش‌ها
            df.to_excel(writer, sheet_name='تراکنش‌ها', index=False)
            
            # صفحه خلاصه
            summary_data = {
                'آمار': [
                    ['نام طلبکار', creditor.name],
                    ['تاریخ گزارش', datetime.now().strftime('%Y-%m-%d %H:%M')],
                    ['تعداد کل تراکنش‌ها', len(transactions)],
                    ['تعداد افزایش بدهی', sum(1 for t in transactions if t.transaction_type == 'debt')],
                    ['تعداد پرداخت', sum(1 for t in transactions if t.transaction_type == 'payment')],
                    ['کل افزایش بدهی', f"{total_debt:,.0f} افغانی"],
                    ['کل پرداخت‌ها', f"{total_payment:,.0f} افغانی"],
                    ['بدهی اولیه', f"{creditor.initial_debt:,.0f} افغانی"],
                    ['بدهی فعلی', f"{creditor.current_debt:,.0f} افغانی"],
                    ['مانده نهایی', f"{creditor.current_debt:,.0f} افغانی"]
                ]
            }
            
            summary_df = pd.DataFrame(summary_data['آمار'], columns=['عنوان', 'مقدار'])
            summary_df.to_excel(writer, sheet_name='خلاصه', index=False)
            
            # تنظیم عرض ستون‌ها
            for sheet in writer.sheets:
                worksheet = writer.sheets[sheet]
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
        
        output.seek(0)
        
        return output
        
    except Exception as e:
        print(f"❌ خطا در تولید Excel: {str(e)}")
        raise