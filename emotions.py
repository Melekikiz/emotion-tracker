import json
import os
from datetime import datetime

# Matplotlib yalnızca grafik göstermek için gerekli
import matplotlib.pyplot as plt
from collections import Counter

# 👉 Menü seçeneklerini gösteren fonksiyon
def menuyu_goster():
    print("\n📋 Lütfen bir seçim yap:")
    print("1 - Yeni duygu ekle")
    print("2 - Günlükleri listele")
    print("3 - Duygu grafiğini göster")
    print("4 - Çıkış")

# 👉 JSON dosyasını yükleyen fonksiyon
def verileri_yukle(dosya):
    if os.path.exists(dosya):
        with open(dosya, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

# 👉 JSON dosyasına veri kaydeden fonksiyon
def verileri_kaydet(dosya, veriler):
    with open(dosya, "w", encoding="utf-8") as f:
        json.dump(veriler, f, indent=4, ensure_ascii=False)

# 👉 Yeni günlük kaydı ekleyen fonksiyon
def yeni_kayit_ekle(veriler):
    print("\n🧠 Bugün kendini nasıl hissediyorsun?")
    duygular = {
        "1": "Mutlu",
        "2": "Üzgün",
        "3": "Stresli",
        "4": "Motive",
        "5": "Kararsız"
    }

    for key, val in duygular.items():
        print(f"{key} - {val}")

    secim = input("Seçimin (1-5): ")
    duygu = duygular.get(secim, "Belirsiz")
    not_ekle = input("Bugünle ilgili bir not yaz (isteğe bağlı): ")
    bugun = datetime.now().strftime("%Y-%m-%d")

    # Bugün daha önce kayıt var mı?
    if any(k["tarih"] == bugun for k in veriler):
        print("⚠️ Bugün zaten bir kayıt var!")
        return veriler

    veriler.append({
        "tarih": bugun,
        "duygu": duygu,
        "not": not_ekle
    })
    print("✅ Kayıt eklendi.")
    return veriler

# 👉 Kayıtları tarih sırasına göre listeleyen fonksiyon
def gunlukleri_listele(veriler):
    if not veriler:
        print("📭 Hiç kayıt bulunamadı.")
        return
    print("\n📖 Günlük Kayıtlar:")
    for k in sorted(veriler, key=lambda x: x["tarih"]):
        print(f"{k['tarih']} - {k['duygu']} | Not: {k['not']}")

# 👉 Duygu dağılım grafiği çizen fonksiyon
def duygu_grafigi(veriler):
    if not veriler:
        print("📭 Görselleştirilecek veri yok.")
        return

    duygu_listesi = [v["duygu"] for v in veriler]
    sayim = Counter(duygu_listesi)

    plt.bar(sayim.keys(), sayim.values(), color="skyblue")
    plt.title("Duygu Dağılımı")
    plt.ylabel("Kayıt Sayısı")
    plt.xlabel("Duygular")
    plt.tight_layout()
    plt.show()

# 👉 Ana program akışı
dosya_adi = "emotions.json"
veriler = verileri_yukle(dosya_adi)

while True:
    menuyu_goster()
    secim = input("Seçiminiz (1-4): ")

    if secim == "1":
        veriler = yeni_kayit_ekle(veriler)
        verileri_kaydet(dosya_adi, veriler)
    elif secim == "2":
        gunlukleri_listele(veriler)
    elif secim == "3":
        duygu_grafigi(veriler)
    elif secim == "4":
        print("👋 Görüşmek üzere!")
        break
    else:
        print("❌ Geçersiz seçim.")
