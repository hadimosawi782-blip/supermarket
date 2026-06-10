from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, DateField, SubmitField, SelectField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, Length, Optional, ValidationError

from datetime import datetime

from wtforms import DecimalField, DateTimeField
from flask_wtf import FlaskForm
from wtforms.validators import Optional, Length, Email

from wtforms import StringField, IntegerField, FloatField, DateField, SubmitField, SelectField, PasswordField, TextAreaField, BooleanField, DecimalField, DateTimeField




# فرم ورود
class LoginForm(FlaskForm):
    username = StringField("نام کاربری", validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField("رمز عبور", validators=[DataRequired(), Length(min=4)])
    submit = SubmitField("ورود")


# فرم محصولات
# فرم محصولات - کامل
class ProductForm(FlaskForm):

    name = StringField(
        "نام جنس",
        validators=[DataRequired()]
    )

    barcode = StringField(
        "بارکد",
        validators=[Optional()]
    )

    batch_no = StringField(
        "شماره بچ",
        validators=[Optional()]
    )

    quantity = FloatField(
    "تعداد",
    validators=[DataRequired(), NumberRange(min=0)]
    )

    items_per_carton = FloatField(
    "تعداد در کارتن",
    default=1,
    validators=[Optional(), NumberRange(min=0.01)]
    )

    buying_price = FloatField(
        "قیمت خرید",
        validators=[DataRequired(), NumberRange(min=0)]
    )

    selling_price = FloatField(
        "قیمت فروش",
        validators=[DataRequired(), NumberRange(min=0)]
    )

    unit = StringField(
        "واحد شمارش",
        validators=[DataRequired()]
    )

    expiry_date = DateField(
        "تاریخ انقضا",
        format='%Y-%m-%d',
        validators=[Optional()]
    )

    purchase_type = SelectField(
        "نوع خرید",
        choices=[('cash', '💰 نقدی'), ('credit', '📝 قرضی')],
        default='cash'
    )

    creditor_id = SelectField(
        "طلبکار",
        coerce=int,
        validators=[Optional()]
    )

    purchase_description = TextAreaField(
        "توضیحات خرید"
    )

    # فیلدهای جدید
    category = StringField(
        "دسته‌بندی",
        default="عمومی",
        validators=[Optional()]
    )

    min_stock = FloatField(
        "حداقل موجودی",
        default=5,
        validators=[Optional(), NumberRange(min=0)]
    )

    is_foreign = BooleanField(
        "محصول خارجی",
        default=False
    )

    submit = SubmitField("ثبت جنس")
# فرم حذف
class DeleteForm(FlaskForm):
    submit = SubmitField("حذف")

# فرم مشتری
class CustomerForm(FlaskForm):
    name = StringField("نام مشتری", validators=[DataRequired()])
    phone = StringField("شماره تماس", validators=[Optional()])
    address = StringField("آدرس", validators=[Optional()])
    total_debt = FloatField("قرض اولیه", default=0, validators=[NumberRange(min=0)])
    submit = SubmitField("ثبت")

# فرم پرداخت بدهی
class DebtPaymentForm(FlaskForm):
    amount = FloatField("مقدار پرداختی (افغانی)", validators=[DataRequired(), NumberRange(min=0.01)])
    submit = SubmitField("ثبت پرداخت")

# فرم فروش
class SaleForm(FlaskForm):
    customer_id = SelectField("مشتری", coerce=int, validators=[Optional()])
    product_id = SelectField("جنس", coerce=int, validators=[DataRequired()])
    quantity = FloatField("تعداد", validators=[DataRequired(), NumberRange(min=0.1)])
    selling_price = FloatField("قیمت فروش (افغانی)", validators=[DataRequired(), NumberRange(min=0)])
    amount_paid = FloatField("مبلغ پرداختی (افغانی)", validators=[Optional()])
    submit = SubmitField("ثبت فروش")

# فرم مصارف روزانه
class DailyExpenseForm(FlaskForm):
    description = StringField("توضیحات", validators=[DataRequired()])
    amount = FloatField("مبلغ (افغانی)", validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("ثبت مصرف")

# فرم کاربر جدید
class UserForm(FlaskForm):
    username = StringField("نام کاربری", validators=[DataRequired(), Length(min=3, max=50)])
    full_name = StringField("نام کامل", validators=[DataRequired()])
    password = PasswordField("رمز عبور", validators=[DataRequired(), Length(min=4)])
    role = SelectField("سطح دسترسی", choices=[
        ('manager', 'مدیر'),
        ('admin', 'مدیر کل')
    ], default='manager')
    submit = SubmitField("ثبت کاربر")

# فرم تغییر رمز عبور
class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("رمز عبور فعلی", validators=[DataRequired()])
    new_password = PasswordField("رمز عبور جدید", validators=[DataRequired(), Length(min=4)])
    confirm_password = PasswordField("تکرار رمز عبور", validators=[DataRequired(), Length(min=4)])
    submit = SubmitField("تغییر رمز عبور")
    
    def validate_confirm_password(self, field):
        if field.data != self.new_password.data:
            raise ValidationError("رمز عبور و تکرار آن باید یکسان باشند")

# فرم مرجوعی محصول
class ReturnProductForm(FlaskForm):
    product_id = SelectField('محصول', coerce=int, validators=[DataRequired()])
    sale_id = SelectField('فاکتور فروش', coerce=int, validators=[DataRequired()])
    customer_id = SelectField('مشتری', coerce=int, validators=[DataRequired()])
    quantity = FloatField('تعداد مرجوعی', validators=[DataRequired(), NumberRange(min=0.1)])
    reason = TextAreaField('دلیل مرجوعی')
    refund_amount = FloatField('مبلغ مرجوعی', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('ثبت مرجوعی')
    
# فرم ویرایش فروش
class EditSaleForm(FlaskForm):
    customer_id = SelectField("مشتری", coerce=int, validators=[Optional()])
    amount_paid = FloatField("مبلغ پرداختی (افغانی)", validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField("ذخیره تغییرات")
    
    
# فرم پرداخت بدهی با بل نمبر
class DebtPaymentForm(FlaskForm):
    amount = FloatField("مقدار پرداختی (افغانی)", validators=[DataRequired(), NumberRange(min=0.01)])
    receipt_number = StringField("بل نمبر رسید", validators=[Optional()])  # فیلد جدید
    submit = SubmitField("ثبت پرداخت")

# فرم قرض‌داری
class LoanForm(FlaskForm):
    lender_name = StringField("نام قرض‌دهنده", validators=[DataRequired()])
    amount = FloatField("مبلغ قرض (افغانی)", validators=[DataRequired(), NumberRange(min=1)])
    description = TextAreaField("توضیحات", validators=[Optional()])
    loan_date = DateField("تاریخ قرض", format='%Y-%m-%d', validators=[DataRequired()])
    due_date = DateField("تاریخ سررسید", format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField("ثبت قرض")

# فرم پرداخت قرض
class LoanPaymentForm(FlaskForm):
    amount = FloatField("مبلغ پرداختی (افغانی)", validators=[DataRequired(), NumberRange(min=0.01)])
    payment_date = DateField("تاریخ پرداخت", format='%Y-%m-%d', validators=[DataRequired()])
    receipt_number = StringField("بل نمبر رسید", validators=[Optional()])
    description = TextAreaField("توضیحات", validators=[Optional()])
    submit = SubmitField("ثبت پرداخت")

# فرم جستجوی فروش
class SaleSearchForm(FlaskForm):
    invoice_number = StringField("شماره فاکتور", validators=[Optional()])
    customer_name = StringField("نام مشتری", validators=[Optional()])
    start_date = DateField("از تاریخ", format='%Y-%m-%d', validators=[Optional()])
    end_date = DateField("تا تاریخ", format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField("جستجو")

# فرم ویرایش کامل فروش
class EditSaleFullForm(FlaskForm):
    customer_id = SelectField("مشتری", coerce=int, validators=[Optional()])
    submit = SubmitField("بروزرسانی فاکتور")

class InventoryWriteOffForm(FlaskForm):
    product_id = SelectField('محصول', coerce=int, validators=[DataRequired()])
    quantity = FloatField('تعداد برای حذف', validators=[DataRequired(), NumberRange(min=0.1)])
    reason = SelectField('دلیل استاک‌اوت', choices=[
        ('expired', '🕒 انقضای تاریخ'),
        ('damaged', '💔 آسیب فیزیکی'),
        ('stolen', '🚫 مفقودی/سرقت'),
        ('quality_issue', '⚠️ مشکل کیفی'),
        ('count_error', '📊 خطای شمارش'),
        ('other', '📝 سایر موارد')
    ], validators=[DataRequired()])
    description = TextAreaField('توضیحات کامل', validators=[Optional()])
    submit = SubmitField('ثبت استاک‌اوت')
    
    


class WriteOffForm(FlaskForm):
    product_id = SelectField('محصول', coerce=int, validators=[DataRequired()])
    quantity = IntegerField('تعداد', validators=[DataRequired(), NumberRange(min=1)])
    reason = SelectField('دلیل', choices=[
        ('damaged', 'آسیب دیده'),
        ('expired', 'منقضی شده'),
        ('lost', 'گم شده'),
        ('theft', 'سرقت'),
        ('other', 'سایر')
    ], validators=[DataRequired()])
    description = TextAreaField('توضیحات اضافی')
    submit = SubmitField('ثبت استاک‌اوت')

class CreditorForm(FlaskForm):
    name = StringField("نام طلبکار", validators=[DataRequired()])
    phone = StringField("شماره تماس", validators=[Optional()])
    address = StringField("آدرس", validators=[Optional()])
    initial_debt = FloatField("بدهی اولیه", default=0, validators=[NumberRange(min=0)])
    debt_description = TextAreaField("توضیحات بدهی")  # 🔥 اضافه شده
    submit = SubmitField("ثبت طلبکار")
# بعد از کلاس CreditorForm اضافه کنید:
# فرم کالای خارجی (برای افزودن در فاکتور)
class ForeignProductSaleForm(FlaskForm):
    name = StringField(
        "نام کالای خارجی *",
        validators=[DataRequired()],
        render_kw={
            'placeholder': 'نام کامل کالا',
            'class': 'form-control',
            'dir': 'rtl'
        }
    )
    
    batch_no = StringField(
        "شماره بچ *",
        validators=[DataRequired()],
        render_kw={
            'placeholder': 'شماره سریال یا بچ',
            'class': 'form-control',
            'dir': 'rtl'
        }
    )
    
    buying_price = FloatField(
        "قیمت خرید (افغانی) *",
        validators=[DataRequired(), NumberRange(min=0.01)],
        render_kw={
            'placeholder': 'قیمت خرید هر واحد',
            'class': 'form-control',
            'dir': 'rtl'
        }
    )
    
    selling_price = FloatField(
        "قیمت فروش (افغانی) *",
        validators=[DataRequired(), NumberRange(min=0.01)],
        render_kw={
            'placeholder': 'قیمت فروش هر واحد',
            'class': 'form-control',
            'dir': 'rtl'
        }
    )
    
    quantity = FloatField(
        "تعداد *",
        validators=[DataRequired(), NumberRange(min=0.1)],
        default=1.0,
        render_kw={
            'placeholder': 'تعداد',
            'class': 'form-control',
            'dir': 'rtl'
        }
    )
    
    unit = SelectField(
        "واحد شمارش",
        choices=[
            ('عدد', 'عدد'),
            ('کیلو', 'کیلو'),
            ('لیتر', 'لیتر'),
            ('بسته', 'بسته'),
            ('کارتن', 'کارتن')
        ],
        default='عدد',
        render_kw={'class': 'form-control', 'dir': 'rtl'}
    )
    
    description = TextAreaField(
        "توضیحات (اختیاری)",
        render_kw={
            'placeholder': 'توضیحات درباره کالا',
            'rows': 2,
            'class': 'form-control',
            'dir': 'rtl'
        }
    )
    
    submit = SubmitField(
        "➕ افزودن به فاکتور",
        render_kw={'class': 'btn btn-warning w-100 py-2'}
    )   
class DebtTransactionForm(FlaskForm):
    creditor_id = SelectField("طلبکار", coerce=int, validators=[DataRequired()])
    amount = FloatField("مبلغ", validators=[DataRequired(), NumberRange(min=0.01)])
    transaction_type = SelectField("نوع تراکنش", choices=[
        ('debt', 'افزایش بدهی'),
        ('payment', 'پرداخت بدهی')
    ], validators=[DataRequired()])
    description = TextAreaField("توضیحات")
    receipt_number = StringField("شماره رسید")
    submit = SubmitField("ثبت تراکنش")
    
class TransactionForm(FlaskForm):
    transaction_type = SelectField(
        'نوع تراکنش',
        choices=[
            ('debt', '➕ افزایش بدهی (طلبکار به ما بدهکار می‌شود)'),
            ('payment', '➖ پرداخت بدهی (ما به طلبکار پرداخت می‌کنیم)')
        ],
        validators=[DataRequired()],
        render_kw={
            'class': 'form-control',
            'onchange': 'toggleAmountLabel()'
        }
    )
    
    amount = DecimalField(
        'مبلغ (افغانی)',
        validators=[DataRequired(), NumberRange(min=0.01)],
        render_kw={
            'placeholder': 'مقدار مثبت وارد کنید',
            'class': 'form-control',
            'id': 'amount_field'
        }
    )
    
    description = TextAreaField(
        'توضیحات',
        validators=[DataRequired()],
        render_kw={
            'rows': 3,
            'placeholder': 'شرح کامل تراکنش',
            'class': 'form-control'
        }
    )
    
    transaction_date = DateField(
        'تاریخ تراکنش',
        format='%Y-%m-%d',
        default=datetime.utcnow().date,
        validators=[Optional()],
        render_kw={'class': 'form-control'}
    )
    
    receipt_number = StringField(
        'شماره رسید',
        validators=[Optional()],
        render_kw={
            'placeholder': 'اختیاری',
            'class': 'form-control'
        }
    )
    
    submit = SubmitField(
        '💾 ثبت تراکنش',
        render_kw={'class': 'btn btn-success btn-lg w-100'}
    )



class PaymentForm(FlaskForm):
    amount = FloatField('مبلغ پرداخت (افغانی)', validators=[DataRequired(), NumberRange(min=0.01)])
    payment_date = DateField('تاریخ پرداخت', validators=[Optional()])
    payment_method = SelectField('روش پرداخت', choices=[
        ('cash', 'نقد'),
        ('bank', 'انتقال بانکی'),
        ('check', 'چک')
    ], default='cash')
    description = TextAreaField('توضیحات', validators=[Optional()])
    receipt_number = StringField('شماره رسید', validators=[Optional()])
    submit = SubmitField('ثبت پرداخت')