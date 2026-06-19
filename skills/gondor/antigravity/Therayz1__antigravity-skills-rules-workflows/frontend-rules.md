---
trigger: always_on
---

# Frontend Workspace Rules

Activation: Always On

Bu dosya, bu workspace içindeki tüm frontend çalışmalarında
Agent’ın uyması gereken proje özel kuralları tanımlar.

---

## 1. Kullanılacak Teknoloji Stack’i

- React veya Next.js kullanılacaktır
- Tailwind CSS zorunludur
- Inline CSS veya styled-components KULLANILMAZ
- Harici UI library (MUI, AntD vb.) KULLANILMAZ
  (shadcn/ui hariçtir)

---

## 2. Bileşen (Component) Kuralları

- SADECE function component kullanılacaktır
- Class component YASAKTIR
- Her bileşen:
  - Tek sorumluluk ilkesine uymalıdır
  - Yeniden kullanılabilir olacak şekilde yazılmalıdır
  - Açık ve anlamlı isimlendirme içermelidir

---

## 3. Dosya ve Klasör Disiplini

- Her bileşen ayrı dosyada tanımlanmalıdır
- Büyük bileşenler alt parçalara bölünmelidir
- `index.tsx` içinde karmaşık logic bulunamaz
- Dosya isimleri:
  - `PascalCase.tsx` (component)
  - `kebab-case.md` (dokümantasyon)

---

## 4. Tailwind Kullanım Standartları

- Aşırı uzun `className` zincirleri YASAKTIR
- Tekrarlanan class’lar için:
  - yardımcı fonksiyon
  - veya ortak bileşen
  tercih edilmelidir

- Blur ve shadow:
  - Glassmorphism UI’da ölçülü kullanılmalıdır
  - Performansı düşürecek yoğunlukta olmamalıdır

---

## 5. Responsive & UX Kuralları

- Mobile-first yaklaşım zorunludur
- Tüm bileşenler:
  - Mobil
  - Tablet
  - Desktop
  ekranlarında çalışmalıdır

- Hover, focus ve active state’ler eksiksiz olmalıdır

---

## 6. Scope Disiplini

Agent:
- Bu dosyada tanımlı olmayan ek teknoloji öneremez
- Kapsam dışı refactor yapamaz
- “İstersen bunu da yapabilirim” önerisinde bulunamaz

SADECE istenen görevi yerine getirir.

---

## 7. Belirsizlik Durumu

Eğer:
- İstek eksikse
- Çelişkili bir durum varsa

Agent:
1. DURUR
2. NETLEŞTİRME SORAR
3. Cevap gelene kadar ilerlemez

---

Bu kuralların ihlali, proje standartlarının ihlali sayılır.
