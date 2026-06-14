# app/models.py
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta  # ✅ اضافه کردن date و timedelta
from .extensions import db
# ============================================================
# مدل User
# ============================================================


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), default="مدیر")
    role = db.Column(db.String(20), default="manager")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ================= RELATIONSHIPS =================
    foreign_products_added = db.relationship(
        "ForeignProduct",
        back_populates="user",
        lazy=True
    )

    sales_created = db.relationship(
        "Sale",
        back_populates="user",
        lazy=True
    )

    debt_payments_created = db.relationship(
        "DebtPayment",
        back_populates="user",
        lazy=True
    )

    expenses_created = db.relationship(
        "DailyExpense",
        back_populates="user",
        lazy=True
    )

    returns_created = db.relationship(
        "ReturnProduct",
        back_populates="user",
        lazy=True
    )

    loans_created = db.relationship(
        "Loan",
        back_populates="user",
        lazy=True
    )

    loan_payments_created = db.relationship(
        "LoanPayment",
        back_populates="user",
        lazy=True
    )

    losses_created = db.relationship(
        "InventoryLoss",
        back_populates="user",
        lazy=True
    )

    transactions_created = db.relationship(
        "DebtTransaction",
        back_populates="user",
        lazy=True
    )

    creditors_created = db.relationship(
        "Creditor",
        back_populates="creator",
        lazy=True
    )

    def set_password(self, password):
        """تنظیم رمز عبور با pbkdf2 (سازگار با Python 3.13)"""
        from werkzeug.security import generate_password_hash
        # استفاده از pbkdf2 به جای scrypt
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        print(f"✅ رمز عبور برای {self.username} تنظیم شد")

    def check_password(self, password):
        """بررسی رمز عبور"""
        from werkzeug.security import check_password_hash
        try:
            return check_password_hash(self.password_hash, password)
        except Exception as e:
            print(f"❌ خطا در بررسی رمز: {e}")
            return False

    def __repr__(self):
        return f"<User {self.username}>"

# ============================================================
# مدل Customer (مشتری)
# ============================================================
class Customer(db.Model):
    __tablename__ = "customers"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    total_debt = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # روابط
    sales = db.relationship('Sale', back_populates='customer', lazy=True, 
                           overlaps="customer_rel")
    debt_payments = db.relationship('DebtPayment', back_populates='customer', lazy=True,
                                   cascade='all, delete-orphan')
    returns = db.relationship('ReturnProduct', back_populates='customer', lazy=True)

    def __repr__(self):
        return f"<Customer {self.name}>"


# ============================================================
# مدل Product (محصول معمولی)
## ============================================================
class ForeignProduct(db.Model):
    __tablename__ = "foreign_products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    batch_no = db.Column(
        db.String(50),
        nullable=False
    )

    buying_price = db.Column(
        db.Float,
        nullable=False,
        default=0.0
    )

    selling_price = db.Column(
        db.Float,
        nullable=False,
        default=0.0
    )

    quantity = db.Column(
        db.Float,
        nullable=False,
        default=0.0
    )

    unit = db.Column(
        db.String(20),
        default="عدد"
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    profit_per_item = db.Column(
        db.Float,
        default=0.0
    )

    added_by = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    sale_id = db.Column(
        db.Integer,
        db.ForeignKey('sales.id'),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    user = db.relationship(
        'User',
        back_populates='foreign_products_added',
        foreign_keys=[added_by]
    )

    sale = db.relationship(
        'Sale',
        back_populates='foreign_products_in_sale',
        foreign_keys=[sale_id]
    )

    def __repr__(self):
        return f"<ForeignProduct {self.name}>"
# مدل Product
# ============================================================
class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    # اطلاعات پایه محصول
    name = db.Column(db.String(100), nullable=False)
    barcode = db.Column(db.String(50), unique=True, nullable=True)

    # قیمت‌ها (واحد: افغانی)
    buying_price = db.Column(db.Float, nullable=False, default=0.0)
    selling_price = db.Column(db.Float, nullable=False, default=0.0)

    # موجودی - سیستم دوگانه (کارتنی + تکی)
    quantity = db.Column(db.Float, nullable=False, default=0)           # تعداد کارتن
    items_per_carton = db.Column(db.Float, nullable=False, default=1)   # تعداد در هر کارتن
    single_quantity = db.Column(db.Integer, nullable=False, default=0)  # تعداد تکی

    # واحد و دسته‌بندی
    unit = db.Column(db.String(20), default="کارتن")
    category = db.Column(db.String(50), default="عمومی")
    min_stock = db.Column(db.Float, default=0)  # حداقل موجودی برای هشدار

    # اطلاعات خرید و انبار
    batch_no = db.Column(db.String(50), nullable=True)
    expiry_date = db.Column(db.Date, nullable=True)
    purchase_description = db.Column(db.Text)
    purchase_type = db.Column(db.String(50), default="cash")  # cash, credit

    # وضعیت محصول
    is_foreign = db.Column(db.Boolean, default=False)  # محصول خارجی/داخلی

    # ارتباط با طلبکار (برای خرید قرضی)
    creditor_id = db.Column(db.Integer, db.ForeignKey("creditors.id"), nullable=True)
    # ✅ اضافه کردن این دو فیلد جدید
    is_credit_purchase = db.Column(db.Boolean, default=False)  # آیا محصول قرضی خریداری شده
    credit_amount = db.Column(db.Float, default=0.0) 

    # زمان‌ها
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # ================= روابط (Relationships) =================
    creditor = db.relationship("Creditor", back_populates="products", foreign_keys=[creditor_id])
    sale_items = db.relationship("SaleItem", back_populates="product", lazy=True, cascade="all, delete-orphan")
    returns = db.relationship("ReturnProduct", back_populates="product", lazy=True)
    inventory_losses = db.relationship("InventoryLoss", back_populates="product", lazy=True, cascade="all, delete-orphan")

    # ================= خصوصیات محاسباتی (Properties) =================

    @property
    def total_items(self):
        """
        محاسبه تعداد کل محصول
        فرمول: (تعداد کارتن × تعداد در کارتن) + تعداد تکی
        مثال: 2 کارتن × 10 عدد + 5 تک = 25 عدد
        """
        try:
            carton_items = (self.quantity or 0) * (self.items_per_carton or 0)
            total = carton_items + (self.single_quantity or 0)
            return round(total, 2)
        except Exception as e:
            print(f"Error in total_items: {e}")
            return 0

    @property
    def is_low_stock(self):
        """بررسی کم بودن موجودی"""
        return self.total_items < (self.min_stock or 5)

    @property
    def is_out_of_stock(self):
        """بررسی تمام شدن موجودی"""
        return self.total_items == 0

    @property
    def profit_per_item(self):
        """سود هر واحد محصول"""
        return self.selling_price - self.buying_price

    @property
    def total_profit(self):
        """سود کل موجودی"""
        return self.profit_per_item * self.total_items

    @property
    def total_value(self):
        """ارزش کل موجودی (بر اساس قیمت فروش)"""
        return self.selling_price * self.total_items

    @property
    def total_cost(self):
        """هزینه کل موجودی (بر اساس قیمت خرید)"""
        return self.buying_price * self.total_items

    @property
    def profit_margin_percent(self):
        """درصد سود"""
        if self.buying_price > 0:
            return (self.profit_per_item / self.buying_price) * 100
        return 0

    @property
    def is_expired(self):
        """بررسی منقضی شدن محصول"""
        if self.expiry_date:
            return date.today() > self.expiry_date
        return False

    @property
    def is_expiring_soon(self, days=30):
        """بررسی نزدیک بودن به تاریخ انقضا"""
        if self.expiry_date and not self.is_expired:
            delta = (self.expiry_date - date.today()).days
            return delta <= days
        return False

    @property
    def expiry_status(self):
        """وضعیت تاریخ انقضا"""
        if not self.expiry_date:
            return "no_expiry"
        if self.is_expired:
            return "expired"
        if self.is_expiring_soon:
            return "expiring_soon"
        return "ok"

    @property
    def stock_status(self):
        """وضعیت موجودی"""
        if self.is_out_of_stock:
            return "out"
        if self.is_low_stock:
            return "low"
        return "normal"

    @property
    def display_quantity(self):
        """نمایش موجودی به صورت فرمت شده"""
        total = self.total_items
        if total >= 1000000:
            return f"{total/1000000:.1f}M"
        if total >= 1000:
            return f"{total/1000:.1f}K"
        return str(int(total))

    # ================= متدهای کاربردی =================

    def add_stock(self, carton_qty=0, single_qty=0):
        """افزودن موجودی"""
        self.quantity += carton_qty
        self.single_quantity += single_qty
        self.updated_at = datetime.utcnow()

    def remove_stock(self, carton_qty=0, single_qty=0):
        """کاهش موجودی"""
        # بررسی موجودی کافی
        if (self.quantity >= carton_qty and 
            self.single_quantity >= single_qty):
            self.quantity -= carton_qty
            self.single_quantity -= single_qty
            self.updated_at = datetime.utcnow()
            return True
        return False

    def update_prices(self, new_buying_price, new_selling_price):
        """به‌روزرسانی قیمت‌ها"""
        old_buying = self.buying_price
        old_selling = self.selling_price
        
        self.buying_price = new_buying_price
        self.selling_price = new_selling_price
        self.updated_at = datetime.utcnow()
        
        return {
            'old_buying': old_buying,
            'old_selling': old_selling,
            'new_buying': self.buying_price,
            'new_selling': self.selling_price
        }

    def to_dict(self):
        """تبدیل محصول به دیکشنری"""
        return {
            'id': self.id,
            'name': self.name,
            'barcode': self.barcode,
            'buying_price': self.buying_price,
            'selling_price': self.selling_price,
            'quantity': self.quantity,
            'items_per_carton': self.items_per_carton,
            'single_quantity': self.single_quantity,
            'total_items': self.total_items,
            'unit': self.unit,
            'category': self.category,
            'min_stock': self.min_stock,
            'batch_no': self.batch_no,
            'expiry_date': self.expiry_date.strftime('%Y-%m-%d') if self.expiry_date else None,
            'is_foreign': self.is_foreign,
            'stock_status': self.stock_status,
            'expiry_status': self.expiry_status,
            'profit_margin': round(self.profit_margin_percent, 2),
            'total_value': self.total_value,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }

    # ================= متدهای آماری =================

    @staticmethod
    def get_low_stock_products(min_qty=5):
        """دریافت محصولات با موجودی کم"""
        return Product.query.filter(Product.total_items < min_qty).all()

    @staticmethod
    def get_expired_products():
        """دریافت محصولات منقضی شده"""
        return Product.query.filter(
            Product.expiry_date < date.today()
        ).all()

    @staticmethod
    def get_expiring_soon_products(days=30):
        """دریافت محصولات نزدیک به انقضا"""
        target_date = date.today() + timedelta(days=days)
        return Product.query.filter(
            Product.expiry_date.between(date.today(), target_date)
        ).all()

    # ================= متدهای نمایشی =================

    def get_stock_display(self):
        """نمایش موجودی به صورت متنی"""
        parts = []
        if self.quantity > 0:
            parts.append(f"{self.quantity:.0f} کارتن")
        if self.single_quantity > 0:
            parts.append(f"{self.single_quantity} تک")
        if not parts:
            return "موجود نیست"
        return " + ".join(parts) + f" = {self.total_items:.0f} عدد"

    def get_price_display(self):
        """نمایش قیمت‌ها به صورت فرمت شده"""
        return {
            'buying': f"{self.buying_price:,.0f}",
            'selling': f"{self.selling_price:,.0f}",
            'profit': f"{self.profit_per_item:,.0f}",
            'margin': f"{self.profit_margin_percent:.1f}%"
        }

    def __repr__(self):
        return f"<Product {self.id}: {self.name} (موجودی: {self.total_items:.0f})>"
# ============================================================
# مدل Sale (فروش)
# ============================================================
class Sale(db.Model):
    __tablename__ = "sales"
    
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=True)
    total_amount = db.Column(db.Float, default=0)
    total_discount = db.Column(db.Float, default=0)
    final_amount = db.Column(db.Float, default=0)
    amount_paid = db.Column(db.Float, default=0)
    remaining_debt = db.Column(db.Float, default=0)
    delivered_by = db.Column(db.String(100), nullable=True)
    booked_by = db.Column(db.String(100), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # روابط
    customer = db.relationship('Customer', back_populates='sales', foreign_keys=[customer_id])
    user = db.relationship('User', back_populates='sales_created', foreign_keys=[created_by])
    items = db.relationship('SaleItem', back_populates='sale', lazy=True, 
                           cascade='all, delete-orphan')
    foreign_products_in_sale = db.relationship(
        "ForeignProduct",
        back_populates="sale",
        lazy=True,
        cascade="all, delete-orphan"
    )
    returns = db.relationship('ReturnProduct', back_populates='sale', lazy=True)

    def __repr__(self):
        return f"<Sale {self.id} - {self.invoice_number}>"


# ============================================================
# مدل SaleItem (آیتم فروش)
class SaleItem(db.Model):
    __tablename__ = "sale_items"

    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sales.id'), nullable=False)

    # اطلاعات محصولات معمولی
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)

    # اطلاعات محصولات خارجی (محل ذخیره مستقیم)
    foreign_name = db.Column(db.String(100), nullable=True)
    foreign_unit = db.Column(db.String(20), nullable=True)
    foreign_selling_price = db.Column(db.Float(), nullable=True)

    quantity = db.Column(db.Float, nullable=False)
    discount_percent = db.Column(db.Float, default=0)
    discount_amount = db.Column(db.Float, default=0)
    selling_price = db.Column(db.Float, nullable=False)  # قیمت واحد نهایی
    final_amount = db.Column(db.Float, nullable=False)   # مبلغ نهایی بعد از تخفیف
    profit = db.Column(db.Float, default=0)  # ✅ فیلد سود

    # روابط
    product = db.relationship(
        "Product",
        back_populates="sale_items",
        foreign_keys=[product_id]
    )

    sale = db.relationship(
        "Sale",
        back_populates="items",
        foreign_keys=[sale_id]
    )

    def display_name(self):
        """نمایش نام محصول یا نام محصول خارجی"""
        if self.product:
            return self.product.name
        return self.foreign_name or "محصول خارجی"

    def display_unit(self):
        """نمایش واحد محصول یا محصول خارجی"""
        if self.product:
            return self.product.unit
        return self.foreign_unit or ""

# ============================================================
# مدل DebtPayment (پرداخت قرض مشتری)
# ============================================================
class DebtPayment(db.Model):
    __tablename__ = "debt_payments"
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    receipt_number = db.Column(db.String(100), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # روابط
    user = db.relationship("User", back_populates='debt_payments_created', foreign_keys=[created_by])
    customer = db.relationship("Customer", back_populates='debt_payments', foreign_keys=[customer_id])

    def __repr__(self):
        return f"<DebtPayment {self.id} - {self.amount}>"


# ============================================================
# مدل DailyExpense (مصرف روزانه)
# ============================================================
# در models.py، کلاس DailyExpense را به این شکل تغییر دهید:
class DailyExpense(db.Model):
    __tablename__ = "daily_expenses"
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), default='سایر')  # ✅ اضافه کنید
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship("User", back_populates="expenses_created", foreign_keys=[created_by])
    
    def __repr__(self):
        return f"<DailyExpense {self.id} - {self.amount}>"
# ============================================================
# مدل ReturnProduct (مرجوعی کالا)
# ============================================================
class ReturnProduct(db.Model):
    __tablename__ = 'return_products'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    sale_id = db.Column(db.Integer, db.ForeignKey('sales.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    return_date = db.Column(db.DateTime, default=datetime.utcnow)
    reason = db.Column(db.String(200), nullable=True)
    refund_amount = db.Column(db.Float, nullable=False)
    
    # ✅ فیلدهای جدید (اختیاری - می‌توانید حذف کنید اگر نمی‌خواهید)
    # original_selling_price = db.Column(db.Float, nullable=True)
    # original_buying_price = db.Column(db.Float, nullable=True)
    
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # روابط
    product = db.relationship('Product', back_populates='returns', foreign_keys=[product_id])
    sale = db.relationship('Sale', back_populates='returns', foreign_keys=[sale_id])
    customer = db.relationship('Customer', back_populates='returns', foreign_keys=[customer_id])
    user = db.relationship('User', back_populates='returns_created', foreign_keys=[created_by])

    def __repr__(self):
        return f"<ReturnProduct {self.id} - {self.product_id}>"

# ============================================================
# مدل Loan (قرض)
# ============================================================
class Loan(db.Model):
    __tablename__ = "loans"
    
    id = db.Column(db.Integer, primary_key=True)
    lender_name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    loan_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=True)
    is_paid = db.Column(db.Boolean, default=False)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # روابط
    user = db.relationship("User", back_populates='loans_created', foreign_keys=[created_by])
    payments = db.relationship("LoanPayment", back_populates="loan", lazy=True, 
                              cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Loan {self.id} - {self.lender_name}>"


# ============================================================
# مدل LoanPayment (پرداخت قرض)
# ============================================================
class LoanPayment(db.Model):
    __tablename__ = "loan_payments"
    
    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey("loans.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    receipt_number = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # روابط
    loan = db.relationship('Loan', back_populates='payments', foreign_keys=[loan_id])
    user = db.relationship('User', back_populates='loan_payments_created', foreign_keys=[created_by])

    def __repr__(self):
        return f"<LoanPayment {self.id} - {self.amount}>"


# ============================================================
# مدل InventoryLoss (زیان موجودی)
# ============================================================
class InventoryLoss(db.Model):
    __tablename__ = "inventory_losses"
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit_cost = db.Column(db.Float, nullable=False)
    total_loss = db.Column(db.Float, nullable=False)
    reason = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    loss_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # روابط
    product = db.relationship('Product', back_populates='inventory_losses', foreign_keys=[product_id])
    user = db.relationship('User', back_populates='losses_created', foreign_keys=[created_by])

    def __repr__(self):
        return f"<InventoryLoss {self.product_id} - {self.quantity}>"


# ============================================================
# مدل Creditor (طلبکار)
# ============================================================
class Creditor(db.Model):
    __tablename__ = "creditors"
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    initial_debt = db.Column(db.Float, default=0.0)
    current_debt = db.Column(db.Float, default=0.0)
    debt_description = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # ✅ فیلدهای جدید برای تاریخ و تشریحات
    last_transaction_date = db.Column(db.DateTime, nullable=True)
    last_transaction_description = db.Column(db.Text, nullable=True)
    
    creator = db.relationship("User", foreign_keys=[created_by])
    debt_transactions = db.relationship("DebtTransaction", back_populates="creditor", lazy=True, cascade='all, delete-orphan')
    products = db.relationship("Product", back_populates="creditor", lazy=True)

    def __repr__(self):
        return f"<Creditor {self.name}>"
# ============================================================
# مدل DebtTransaction (تراکنش طلبکار)
# ============================================================
class DebtTransaction(db.Model):
    __tablename__ = "debt_transactions"
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    creditor_id = db.Column(db.Integer, db.ForeignKey("creditors.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(20))  # 'debt' (قرض جدید) یا 'payment' (پرداخت)
    receipt_number = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)  # ✅ تشریحات
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  # ✅ تاریخ
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="transactions_created", foreign_keys=[user_id])
    creditor = db.relationship("Creditor", back_populates="debt_transactions", foreign_keys=[creditor_id])

    def __repr__(self):
        return f"<DebtTransaction {self.id} - {self.amount}>"

# ============================================================
# مدل License (لایسنس)
# ============================================================
# ============================================================
# مدل License (لایسنس) - نسخه اصلاح شده با مدیریت آزمایشی# app/models.py - بخش License

class License(db.Model):
    __tablename__ = "license"

    id = db.Column(db.Integer, primary_key=True)
    hw_id = db.Column(db.String(128), nullable=False)
    expire_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    trial_count = db.Column(db.Integer, default=0)
    last_trial_date = db.Column(db.DateTime, nullable=True)
    license_type = db.Column(db.String(20), default='trial')
    
    # آخرین تاریخ معتبر ثبت شده (برای تشخیص دستکاری)
    last_valid_date = db.Column(db.DateTime, nullable=True)

    def _clean_datetime(self, dt):
        """تبدیل datetime به فرمت ساده (بدون منطقه زمانی)"""
        if dt is None:
            return None
        if hasattr(dt, 'tzinfo') and dt.tzinfo is not None:
            dt = dt.replace(tzinfo=None)
        return dt

    def is_valid(self):
        """بررسی اعتبار لایسنس با جلوگیری از دستکاری تاریخ"""
        from app.license_config import get_real_time
        from app import db
        
        try:
            # دریافت زمان واقعی و تمیز کردن آن
            real_time = get_real_time()
            real_time = self._clean_datetime(real_time)
            
            # تمیز کردن expire_at
            expire_at = self._clean_datetime(self.expire_at)
            
            # اگر زمان واقعی از تاریخ انقضا گذشته باشد
            if real_time > expire_at:
                return False
            
            # بررسی دستکاری تاریخ (اگر تاریخ قبلی ثبت شده باشد)
            if self.last_valid_date:
                last_valid = self._clean_datetime(self.last_valid_date)
                if real_time < last_valid:
                    # تاریخ به عقب برگردانده شده - لایسنس غیرفعال می‌شود
                    return False
            
            # بروزرسانی آخرین تاریخ معتبر
            self.last_valid_date = real_time
            db.session.commit()
            
            return True
            
        except Exception as e:
            print(f"⚠️ خطا در بررسی لایسنس: {e}")
            # در صورت خطا، بررسی ساده با زمان سیستم
            try:
                return datetime.now() < self._clean_datetime(self.expire_at)
            except:
                return False

    def remaining_days(self):
        """تعداد روزهای باقیمانده با تاریخ واقعی"""
        from app.license_config import get_real_date
        
        try:
            real_date = get_real_date()
            real_date = self._clean_datetime(real_date)
            expire_at = self._clean_datetime(self.expire_at)
            
            delta = expire_at - real_date
            return max(delta.days, 0)
        except:
            return 0

    def can_use_trial(self, max_trials=1, trial_days=30):
        """بررسی امکان استفاده از نسخه آزمایشی"""
        from app.license_config import MAX_TRIAL_COUNT, TRIAL_DAYS, get_real_date
        
        max_allowed = max_trials if max_trials else MAX_TRIAL_COUNT
        required_days = trial_days if trial_days else TRIAL_DAYS
        
        # اگر قبلاً لایسنس کامل داشته
        if self.license_type == 'full':
            return False, "شما قبلاً لایسنس کامل را فعال کرده‌اید"
        
        # اگر تعداد استفاده از حد مجاز بیشتر شده
        if self.trial_count >= max_allowed:
            return False, f"تعداد مجاز استفاده از نسخه آزمایشی ({max_allowed} بار) به پایان رسیده است. لطفاً لایسنس کامل را خریداری کنید."
        
        # اگر آخرین تاریخ استفاده وجود دارد و فاصله کافی نیست
        if self.last_trial_date:
            try:
                real_date = get_real_date()
                real_date = self._clean_datetime(real_date)
                last_trial = self._clean_datetime(self.last_trial_date)
                
                days_passed = (real_date - last_trial).days
                if days_passed < required_days:
                    remaining = required_days - days_passed
                    return False, f"برای استفاده مجدد از نسخه آزمایشی باید {remaining} روز دیگر صبر کنید"
            except:
                pass
        
        return True, "می‌توانید از نسخه آزمایشی استفاده کنید"

    def add_trial(self, days=30):
        """اضافه کردن یک دوره آزمایشی جدید"""
        from app.license_config import get_real_date
        from app import db
        from datetime import timedelta
        
        try:
            can_use, msg = self.can_use_trial()
            if not can_use:
                return False, msg
            
            real_date = get_real_date()
            real_date = self._clean_datetime(real_date)
            
            self.trial_count += 1
            self.last_trial_date = real_date
            self.expire_at = real_date + timedelta(days=days)
            self.license_type = 'trial'
            self.last_valid_date = real_date
            db.session.commit()
            
            return True, f"لایسنس آزمایشی {days} روزه فعال شد. (دفعه {self.trial_count})"
            
        except Exception as e:
            db.session.rollback()
            return False, f"خطا در فعال‌سازی لایسنس آزمایشی: {str(e)}"

    def activate_full_license(self, days=365):
        """فعال‌سازی لایسنس کامل"""
        from app.license_config import get_real_date
        from app import db
        from datetime import timedelta
        
        try:
            real_date = get_real_date()
            real_date = self._clean_datetime(real_date)
            
            self.expire_at = real_date + timedelta(days=days)
            self.license_type = 'full'
            self.last_valid_date = real_date
            db.session.commit()
            
            return True, f"لایسنس کامل تا {self.expire_at.strftime('%Y-%m-%d')} فعال شد"
            
        except Exception as e:
            db.session.rollback()
            return False, f"خطا در فعال‌سازی لایسنس کامل: {str(e)}"

    def get_info(self):
        """دریافت اطلاعات کامل لایسنس"""
        return {
            'hw_id': self.hw_id,
            'expire_at': self.expire_at.strftime('%Y-%m-%d') if self.expire_at else None,
            'remaining_days': self.remaining_days(),
            'is_valid': self.is_valid(),
            'trial_count': self.trial_count,
            'last_trial_date': self.last_trial_date.strftime('%Y-%m-%d') if self.last_trial_date else None,
            'license_type': self.license_type
        }

    def __repr__(self):
        return f"<License hw={self.hw_id} type={self.license_type} expires={self.expire_at}>"

# همچنین نیاز به import timedelta در بالای فایل دارید
from datetime import datetime, timedelta  # ✅ اضافه کنید اگر نیست
# ============================================================
# مدل DailyReport (گزارش روزانه)
# ============================================================
class DailyReport(db.Model):
    __tablename__ = "daily_reports"
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, unique=True)
    total_sales = db.Column(db.Float, default=0.0)
    total_expenses = db.Column(db.Float, default=0.0)
    total_debt_payments = db.Column(db.Float, default=0.0)
    total_profit = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<DailyReport {self.date} - Sales: {self.total_sales}>"


# ============================================================
# مدل MonthlyReport (گزارش ماهانه)
# ============================================================
class MonthlyReport(db.Model):
    __tablename__ = "monthly_reports"
    
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    total_sales = db.Column(db.Float, default=0.0)
    total_expenses = db.Column(db.Float, default=0.0)
    total_profit = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<MonthlyReport {self.year}/{self.month} - Profit: {self.total_profit}>"
    
class CashBalance(db.Model):
    __tablename__ = "cash_balance"
    
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False, default=0.0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    user = db.relationship('User', backref='cash_updates')
    
    def __repr__(self):
        return f"<CashBalance {self.amount:,.0f} افغانی>"

class CashTransaction(db.Model):
    __tablename__ = "cash_transactions"
    
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # 'sale', 'expense', 'adjustment'
    description = db.Column(db.String(200))
    reference_id = db.Column(db.Integer, nullable=True)  # ID سند مرتبط (مثلاً sale_id)
    balance_before = db.Column(db.Float, nullable=False)
    balance_after = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    user = db.relationship('User', backref='cash_transactions')
    
    def __repr__(self):
        return f"<CashTransaction {self.transaction_type} {self.amount:,.0f}>"
    
class CashWithdrawal(db.Model):
    __tablename__ = "cash_withdrawals"
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    purpose = db.Column(db.String(200), nullable=False)  # هدف برداشت
    description = db.Column(db.Text, nullable=True)
    withdrawal_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # روابط
    employee = db.relationship('User', foreign_keys=[employee_id], backref='withdrawals')
    
    def __repr__(self):
        return f"<CashWithdrawal {self.employee.full_name} - {self.amount:,.0f}>"
    
class Notification(db.Model):
    __tablename__ = "notifications"
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)  # 'low_stock', 'expiring'
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    product_name = db.Column(db.String(100), nullable=True)
    current_quantity = db.Column(db.Float, nullable=True)
    min_stock = db.Column(db.Float, nullable=True)
    expiry_date = db.Column(db.Date, nullable=True)
    days_remaining = db.Column(db.Integer, nullable=True)
    is_read = db.Column(db.Boolean, default=False)
    is_urgent = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)  # برای حذف خودکار
    
    def __repr__(self):
        return f"<Notification {self.id} - {self.title}>"
    
    def mark_as_read(self):
        self.is_read = True
        db.session.commit()

class PriceHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(
        db.Integer,
        db.ForeignKey('products.id')
    )

    old_price = db.Column(db.Float)
    new_price = db.Column(db.Float)

    changed_by = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )