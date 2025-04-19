import os
import asyncio
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

# Ganti ini dengan API ID dan API Hash kamu dari https://my.telegram.org
api_id = 123456  # <- ganti ini
api_hash = 'APIHASH'  # <- ganti ini

async def save_session(phone_number):
    session_name = phone_number.replace("+", "").replace(" ", "")
    client = TelegramClient(session_name, api_id, api_hash)

    await client.connect()

    if not await client.is_user_authorized():
        print(f"🔐 Belum login untuk {phone_number}. Mulai proses login...")
        await client.send_code_request(phone_number)
        code = input("📩 Masukkan kode verifikasi (dari Telegram): ")
        try:
            await client.sign_in(phone_number, code)
        except SessionPasswordNeededError:
            password = input("🔑 Masukkan password dua langkah (jika ada): ")
            await client.sign_in(password=password)
        print(f"✅ Autentikasi berhasil! Session disimpan sebagai: {session_name}.session\n")
    else:
        print(f"🔁 Session untuk {phone_number} sudah ada. Tidak perlu login ulang.\n")

    await client.disconnect()


async def save_sessions_for_multiple_phones():
    print("🔧 Multi-Akun Telegram - Auto Save Session")
    print("Ketik 'exit' untuk keluar.\n")
    
    while True:
        phone = input("📱 Masukkan nomor telepon (dengan kode negara, ex: +628xxxx): ")
        if phone.lower() == 'exit':
            print("\n🚪 Selesai. Semua session sudah diproses.")
            break
        if phone.startswith('+'):
            await save_session(phone)
        else:
            print("⚠️ Format nomor salah. Harus dimulai dengan '+'. Contoh: +628123xxxx\n")

# Jalankan program
if __name__ == '__main__':
    asyncio.run(save_sessions_for_multiple_phones())
