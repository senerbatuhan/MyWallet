import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt

class Wallet:
    def __init__(self):
        self.filename = 'data.csv'
        self.records = []
        self.load_records()

    def load_records(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.records = list(reader)
        else:
            self.records = []

    def save_records(self):
        with open(self.filename, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['id', 'tarih', 'tip', 'kategori', 'tutar', 'aciklama']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for rec in self.records:
                writer.writerow(rec)

    def add_record(self):
        tip = input('Gelir mi Gider mi? (gelir/gider): ')
        kategori = input('Kategori: ')
        tutar = input('Tutar: ')
        aciklama = input('Açıklama: ')
        tarih = input('Tarih (YYYY-MM-DD, boş bırak günün tarihi): ')
        if not tarih:
            tarih = datetime.now().strftime('%Y-%m-%d')
        rec_id = str(len(self.records) + 1)
        # Yeni kaydı sözlük olarak oluşturup kayıtlar listesine ekliyoruz
        self.records.append({'id': rec_id, 'tarih': tarih, 'tip': tip, 'kategori': kategori, 'tutar': tutar, 'aciklama': aciklama})
        self.save_records()
        print('Kayıt eklendi.')

    def list_records(self):
        if not self.records:
            print('Kayıt yok.')
            return
        for rec in self.records:
            # Her kaydı ekrana düzenli şekilde yazdırıyoruz
            print(f"{rec['id']}: {rec['tarih']} | {rec['tip']} | {rec['kategori']} | {rec['tutar']} | {rec['aciklama']}")

    def edit_record(self):
        self.list_records()
        rec_id = input('Düzenlenecek kayıt id: ')
        for rec in self.records:
            if rec['id'] == rec_id:
                rec['tarih'] = input(f"Tarih [{rec['tarih']}]: ") or rec['tarih']
                rec['tip'] = input(f"Tip [{rec['tip']}]: ") or rec['tip']
                rec['kategori'] = input(f"Kategori [{rec['kategori']}]: ") or rec['kategori']
                rec['tutar'] = input(f"Tutar [{rec['tutar']}]: ") or rec['tutar']
                rec['aciklama'] = input(f"Açıklama [{rec['aciklama']}]: ") or rec['aciklama']
                self.save_records()
                print('Kayıt güncellendi.')
                return
        print('Kayıt bulunamadı.')

    def delete_record(self):
        self.list_records()
        rec_id = input('Silinecek kayıt id: ')
        # Seçilen id'ye sahip kaydı listeden çıkarıyoruz
        self.records = [rec for rec in self.records if rec['id'] != rec_id]
        # id'leri güncelle
        # Kalan kayıtların id'lerini baştan sona güncelliyoruz
        for i, rec in enumerate(self.records, 1):
            rec['id'] = str(i)
        self.save_records()
        print('Kayıt silindi.')

    def show_reports(self):
        aylik = {}
        yillik = {}
        for rec in self.records:
            yil = rec['tarih'][:4]  # Tarihten yılı alıyoruz (örn: 2025)
            ay = rec['tarih'][:7]   # Tarihten yıl-ay bilgisini alıyoruz (örn: 2025-07)
            tutar = float(rec['tutar'])
            if rec['tip'] == 'gider':
                # Aylık ve yıllık toplam giderleri hesaplıyoruz
                aylik[ay] = aylik.get(ay, 0) + tutar
                yillik[yil] = yillik.get(yil, 0) + tutar
        print('Aylık Harcama:')
        for ay, tutar in aylik.items():
            print(f'{ay}: {tutar:.2f} TL')
        print('Yıllık Harcama:')
        for yil, tutar in yillik.items():
            print(f'{yil}: {tutar:.2f} TL')

    def export_csv(self):
        fname = input('Dışa aktarılacak dosya adı (örn: export.csv): ')
        with open(fname, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['id', 'tarih', 'tip', 'kategori', 'tutar', 'aciklama']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for rec in self.records:
                writer.writerow(rec)
        print('CSV olarak dışa aktarıldı.')

    def import_csv(self):
        fname = input('İçe aktarılacak dosya adı (örn: import.csv): ')
        if not os.path.exists(fname):
            print('Dosya bulunamadı.')
            return
        with open(fname, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            imported = list(reader)
            last_id = len(self.records)
            for i, rec in enumerate(imported, 1):
                rec['id'] = str(last_id + i)
                self.records.append(rec)
        self.save_records()
        print('CSV içe aktarıldı.')

    def visualize(self):
        import matplotlib.pyplot as plt
        gelirler = {}
        giderler = {}
        for rec in self.records:
            kategori = rec['kategori']
            tutar = float(rec['tutar'])
            if rec['tip'] == 'gelir':
                gelirler[kategori] = gelirler.get(kategori, 0) + tutar
            elif rec['tip'] == 'gider':
                giderler[kategori] = giderler.get(kategori, 0) + tutar
        kategoriler = sorted(set(list(gelirler.keys()) + list(giderler.keys())))
        if not kategoriler:
            print('Gelir veya gider kaydı yok.')
            return
        gelir_list = [gelirler.get(k, 0) for k in kategoriler]
        gider_list = [giderler.get(k, 0) for k in kategoriler]
        x = range(len(kategoriler))
        plt.figure(figsize=(10,6))
        plt.bar(x, gelir_list, width=0.4, label='Gelir', align='center', color='green')
        plt.bar(x, gider_list, width=0.4, label='Gider', align='edge', color='red')
        plt.xticks(x, kategoriler, rotation=45)
        plt.title('Kategoriye Göre Gelir ve Giderler')
        plt.xlabel('Kategori')
        plt.ylabel('Tutar (TL)')
        plt.legend()
        plt.tight_layout()
        plt.show()
