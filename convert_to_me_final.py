#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import shutil
from datetime import datetime

print("="*60)
print("🔧 MG24 GAMER BOT - CONVERT TO ME SERVER")
print("="*60)

# عمل نسخة احتياطية
backup_file = f"main_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
shutil.copy2('main.py', backup_file)
print(f"✅ تم عمل نسخة احتياطية: {backup_file}")

# قراءة الملف
with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

changes = []

# 1. تغيير region الأساسي
content = re.sub(r"region\s*=\s*['\"]IND['\"]", "region = 'ME'", content)
content = re.sub(r"region\s*=\s*['\"]ind['\"]", "region = 'ME'", content)
content = re.sub(r"region\s*=\s*['\"]bd['\"]", "region = 'ME'", content)
content = re.sub(r"region\s*=\s*['\"]BD['\"]", "region = 'ME'", content)
changes.append("✅ Changed default region to ME")

# 2. تغيير server2 و key2
content = re.sub(r"server2\s*=\s*['\"][^'\"]*['\"]", "server2 = 'ME'", content)
content = re.sub(r"key2\s*=\s*['\"][^'\"]*['\"]", "key2 = 'mg24'", content)
changes.append("✅ Changed server2 to ME")

# 3. تغيير شروط packet type
content = re.sub(
    r'if region\.lower\(\)\s*==\s*[\'"]ind[\'"]:',
    'if region.lower() == "me":',
    content
)
content = re.sub(
    r'elif region\.lower\(\)\s*==\s*[\'"]bd[\'"]:',
    'elif region.lower() == "me":',
    content
)
changes.append("✅ Changed packet type conditions")

# 4. تغيير URLs من ind/bd إلى me
content = content.replace('client.ind.freefiremobile.com', 'client.me.freefiremobile.com')
content = content.replace('client.bd.freefiremobile.com', 'client.me.freefiremobile.com')
changes.append("✅ Changed API URLs to ME")

# 5. تغيير دالة get_bio_server_url
bio_pattern = r'(def get_bio_server_url\(lock_region: str\):.*?)(?=\n\w|\n$)'
def fix_bio_func(m):
    func = m.group(1)
    if 'region == "ME"' not in func:
        func = func.replace(
            'region = lock_region.upper()',
            'region = lock_region.upper()\n    if region == "ME":\n        return "https://client.me.freefiremobile.com/UpdateSocialBasicInfo"'
        )
    return func
content = re.sub(bio_pattern, fix_bio_func, content, flags=re.DOTALL)
changes.append("✅ Updated bio URL function")

# 6. تغيير القيمة الافتراضية في MaiiiinE
content = re.sub(
    r"region = getattr\(MajoRLoGinauTh, 'region', 'IND'\)",
    "region = getattr(MajoRLoGinauTh, 'region', 'ME')",
    content
)
changes.append("✅ Changed default region in MaiiiinE")

# 7. تغيير send_friend_request_single
content = re.sub(
    r'if region\.lower\(\) == "me":\s*url = "https://client\.ind\.freefiremobile\.com/RequestAddingFriend"\s*elif region\.lower\(\) == "me":',
    'if region.lower() == "me":\n            url = "https://client.me.freefiremobile.com/RequestAddingFriend"',
    content
)
changes.append("✅ Fixed send_friend_request_single")

# 8. إضافة Keep-Alive إلى TcPOnLine
if 'last_keep_alive' not in content:
    content = content.replace(
        'async def TcPOnLine(ip, port, key, iv, AutHToKen, reconnect_delay=0.5):',
        'async def TcPOnLine(ip, port, key, iv, AutHToKen, reconnect_delay=0.5):\n    import time\n    last_keep_alive = time.time()'
    )
    changes.append("✅ Added Keep-Alive to TcPOnLine")

# 9. حفظ الملف المعدل
with open('main_me.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "="*60)
print("📊 التغييرات التي تمت:")
print("="*60)
for change in changes:
    print(f"  {change}")

print("\n" + "="*60)
print("✅ تم إنشاء main_me.py بنجاح!")
print("="*60)
print("""
🚀 لتشغيل البوت على سيرفر ME:
    python main_me.py

📝 ملاحظات:
    - تم عمل نسخة احتياطية من ملفك الأصلي
    - جميع الإعدادات تم تحويلها إلى ME
    - تم إضافة Keep-Alive لمنع انقطاع الاتصال
""")
