import os
import asyncio
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

# Ganti API ID & Hash kamu
api_id = 28491841
api_hash = '9261d10a133e3aca10f0932da4311b6d'

async def login_or_load_session(phone_number):
    session_name = phone_number.replace("+", "").replace(" ", "")
    client = TelegramClient(session_name, api_id, api_hash)

    await client.connect()

    if not await client.is_user_authorized():
        print(f"🔐 Belum login untuk {phone_number}. Mulai proses login...")
        await client.send_code_request(phone_number)
        code = input("📩 Masukkan kode verifikasi dari Telegram: ")
        try:
            await client.sign_in(phone_number, code)
        except SessionPasswordNeededError:
            password = input("🔑 Masukkan password dua langkah (jika ada): ")
            await client.sign_in(password=password)
        print(f"✅ Login berhasil dan session disimpan sebagai {session_name}.session\n")
    else:
        print(f"✅ Session ditemukan. Login otomatis untuk {phone_number}!\n")

    me = await client.get_me()
    print(f"👤 Anda login sebagai: {me.first_name} (@{me.username})\n📱 Phone: {me.phone}\n🆔 ID: {me.id}")

    await client.disconnect()

# Program utama
if __name__ == '__main__':
    phone = input("📱 Masukkan nomor telepon kamu (ex: +628123xxxx): ").strip()
    if phone.startswith('+'):
        asyncio.run(login_or_load_session(phone))
    else:
        print("⚠️ Format nomor salah. Harus pakai tanda '+' di depan.")
