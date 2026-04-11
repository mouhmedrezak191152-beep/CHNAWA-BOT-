import re

print("🔧 جاري إصلاح مشكلة قطع الاتصال...")

with open('main.py', 'r') as f:
    content = f.read()

# 1. إضافة Keep-Alive إلى TcPOnLine
keep_alive_code = '''
                # إرسال Keep-Alive كل 20 ثانية
                import time
                if 'last_keep_alive' not in dir():
                    last_keep_alive = time.time()
                if time.time() - last_keep_alive > 20:
                    try:
                        ka_packet = await send_keep_alive(key, iv, region)
                        if ka_packet and online_writer:
                            online_writer.write(ka_packet)
                            await online_writer.drain()
                            last_keep_alive = time.time()
                            print("💓 Keep-Alive sent")
                    except Exception as e:
                        print(f"Keep-Alive error: {e}")
'''

# البحث عن while True داخل TcPOnLine وإضافة الكود
pattern = r'(while True:.*?)(data_hex = data2\.hex\(\))'
replacement = r'\1' + keep_alive_code + '\n                ' + r'\2'
content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# 2. إصلاح دالة GeTSQDaTa
old_getsq = r'async def GeTSQDaTa\(packet_json\):.*?return.*?'
new_getsq = '''async def GeTSQDaTa(packet_json):
    """Extract squad data safely"""
    try:
        if not isinstance(packet_json, dict):
            return None, None, None
        if '5' not in packet_json or 'data' not in packet_json['5']:
            return None, None, None
        data = packet_json['5']['data']
        if '1' not in data or 'data' not in data['1']:
            return None, None, None
        owner_uid = data['1']['data']
        chat_code = None
        squad_code = None
        if '8' in data and 'data' in data['8']:
            chat_code = data['8']['data']
        if '9' in data and 'data' in data['9']:
            squad_code = data['9']['data']
        return owner_uid, chat_code, squad_code
    except Exception as e:
        print(f"GeTSQDaTa error: {e}")
        return None, None, None
'''
content = re.sub(old_getsq, new_getsq, content, flags=re.DOTALL)

# 3. إضافة دالة send_keep_alive إذا لم تكن موجودة
if 'async def send_keep_alive' not in content:
    send_ka = '''
async def send_keep_alive(key, iv, region):
    try:
        fields = {1: 99, 2: {1: int(time.time()), 2: 1}}
        if region.lower() == "me":
            packet_type = '0514'
        else:
            packet_type = '0515'
        packet = await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)
        return packet
    except Exception as e:
        print(f"Keep-alive error: {e}")
        return None
'''
    content += send_ka

with open('main_fixed.py', 'w') as f:
    f.write(content)

print("✅ تم إصلاح الملف! تم إنشاء main_fixed.py")
print("🚀 جاري تشغيل البوت بعد الإصلاح...")
