from wallet import Wallet

def main():
    wallet = Wallet()
    while True:
        print("\n--- MyWallet ---")
        print("1. Gelir/Gider Ekle")
        print("2. Kayıtları Listele")
        print("3. Kayıt Düzenle")
        print("4. Kayıt Sil")
        print("5. Raporlar")
        print("6. CSV'ye Aktar")
        print("7. CSV'den İçe Aktar")
        print("8. Görselleştir")
        print("9. Çıkış")
        secim = input("Seçiminiz: ")
        if secim == '1':
            wallet.add_record()
        elif secim == '2':
            wallet.list_records()
        elif secim == '3':
            wallet.edit_record()
        elif secim == '4':
            wallet.delete_record()
        elif secim == '5':
            wallet.show_reports()
        elif secim == '6':
            wallet.export_csv()
        elif secim == '7':
            wallet.import_csv()
        elif secim == '8':
            wallet.visualize()
        elif secim == '9':
            print("Çıkılıyor...")
            break
        else:
            print("Geçersiz seçim!")

if __name__ == "__main__":
    main()
