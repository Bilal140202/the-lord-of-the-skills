---
name: frontend-glassmorphism
description: Builds premium glassmorphism (3D-like, soft blur) frontend UI components and landing pages using React/Next.js + Tailwind conventions. Use when designing modern SaaS pages, hero sections, pricing, navbars, feature grids, and animations with accessible contrast and performance constraints.
---

# Frontend Glassmorphism Skill

Bu skill, modern SaaS landing page ve UI bileşenlerini **glassmorphism** estetiğiyle üretmek için kurallar ve şablonlar sağlar.

## Ne zaman kullanılır?

- “Landing page”, “hero”, “pricing”, “features”, “navbar”, “CTA”, “dashboard UI” gibi isteklerde
- “3D glassmorphism”, “blur”, “frosted glass”, “neon”, “soft shadow”, “premium UI” gibi ifadeler geçtiğinde
- UI üretimi istenirken **tasarım dili + kod kalitesi** birlikte istendiğinde

## Çıktı hedefleri

1. **Görsel kalite:** premium, yormayan, modern
2. **Okunabilirlik:** kontrast, tipografi, spacing
3. **Uygulanabilir kod:** React/Next.js + Tailwind ile copy/paste çalışır
4. **Performans:** blur ve gölgeler ölçülü, gereksiz animasyon yok
5. **Erişilebilirlik:** buton/Link states, focus ring, semantik yapı

---

## Tasarım İlkeleri (Glassmorphism Standardı)

### A) Cam katman (glass surface)
- Arka plan: gradient + yumuşak noise hissi
- Kart: `backdrop-blur` + yarı şeffaf beyaz/siyah katman
- Border: ince ve yarı saydam (ışık kırılması efekti)
- Shadow: soft, çok yayık, “floating” hissi

Önerilen Tailwind pattern:
- `bg-white/5` veya `bg-black/20`
- `backdrop-blur-xl`
- `border border-white/10`
- `shadow-2xl shadow-black/20`
- `rounded-2xl`

### B) Renk ve kontrast
- Metin kontrastı “cam üstünde” okunacak şekilde ayarlanmalı
- Minimum: body metinlerinde yeterli kontrast
- Parlak neon sadece vurgu (accent) olarak kullanılmalı

### C) Tipografi ve hiyerarşi
- Hero başlık: büyük, kısa, net
- Alt metin: 2-3 satır, fayda odaklı
- CTA: 1 ana + 1 ikincil

### D) Layout
- Grid tabanlı düzen (12-col veya 2/3 kolon)
- Bol whitespace
- Kartlar arası tutarlı spacing

---

## Kod Kuralları (Frontend)

- React bileşenleri: tek sorumluluk
- Tailwind: className’ler aşırı şişmesin, gerektiğinde yardımcı fonksiyon kullanılabilir
- State yönetimi gerekiyorsa minimal
- Animasyon: framer-motion kullanımı varsa kontrollü
- Her bileşende:
  - hover/focus/active state
  - mobile responsive
  - semantik tag (nav, header, main, section)

---

## İş Akışı (Decision Tree)

1) Kullanıcı “sadece tasarım konsepti” istiyorsa:
- `resources/prompt-templates.md` içinden uygun prompt şablonu ver

2) Kullanıcı “kod” istiyorsa:
- `examples/` dosyalarına benzer şekilde TSX bileşeni üret
- Tailwind tokenlarını `resources/tokens.json` ile uyumlu tut

3) Kullanıcı “tam landing page” istiyorsa:
- Hero + Social proof + Features + Pricing + FAQ + CTA bloklarını üret
- Her blok glass kart temasıyla tutarlı olsun

4) Kullanıcı “performans” diyorsa:
- Blur seviyesini azalt, gölgeleri sadeleştir, animasyonları minimuma indir

---

## Script Kullanımı

Skill içindeki scriptler “black box”tır:
- Önce `--help` çalıştır
- Sonra amaca uygun parametrelerle kullan

Scriptler:
- `scripts/check-ui.sh`: proje içinde UI hygiene check (opsiyonel)
- `scripts/generate-component.ts`: örnek bileşen şablonu üretir (opsiyonel)

---

## Çıktı Formatı

- Kod istenirse: tek bir TSX dosyası veya bileşen blokları
- Tasarım yönergesi istenirse: bullet list + tokenlar + örnek className pattern’leri
- Gereksiz uzun açıklama yok, direkt kullanılabilir çıktı

