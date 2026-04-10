# LiteBridge: Lightweight OpenAI-Compatible API for LiteRT

LiteBridge, Google'ın **LiteRT-LM** modellerini OpenAI uyumlu bir API üzerinden sunan, yüksek performanslı ve "hafif" bir köprü (gateway) uygulamasıdır. 

Ollama'ya benzer bir amaç güder fakat çok daha düşük kaynak tüketimi ve LiteRT'nin kenar cihazlar için optimize edilmiş gücünü kullanır.

## 🚀 Özellikler

- **OpenAI Uyumlu:** `/v1/chat/completions` endpoint'i sayesinde Cursor, Zed, Aider gibi araçlarla anında entegrasyon.
- **Düşük RAM Tüketimi:** LiteRT altyapısı sayesinde sadece ihtiyacı olan belleği kullanır.
- **Streaming (SSE) Desteği:** Tokens-by-token akış hızı.
- **Otomatik Kurulum:** Sunucu başladığında eksik modelleri otomatik indirir.
- **Hızlı Swagger Dökümantasyonu:** Deneysel arayüz ile API testi.

---

## 🛠️ Kurulum

1. **Gereksinimler:** Python 3.10+
2. **Kütüphaneleri Yükle:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Konfigürasyon:** `.env.example` dosyasını `.env` olarak kopyalayın ve model ID'nizi belirleyin.

---

## 🖥️ Çalıştırma

Sunucuyu başlatmak için:
```bash
python main.py
```
Sunucu varsayılan olarak `http://localhost:8080` adresinde çalışacaktır.

---

## 📖 API Kullanımı

### 1. Modelleri Listele
**GET** `/v1/models`

### 2. Sohbet Tamamlama (Chat Completion)
**POST** `/v1/chat/completions`

#### Parametreler:
- `messages`: Mesaj listesi (Sistem, Kullanıcı, Asistan).
- `stream`: `true` ise yanıtlar parça parça gelir.
- `model`: `gemma-4-E2B-it` vb.

#### Örnek (JSON Bedeni):
```json
{
  "model": "gemma-4-E2B-it",
  "messages": [
    {"role": "system", "content": "Sen yardımcı bir asistansın."},
    {"role": "user", "content": "Python'da liste nasıl sıralanır?"}
  ],
  "stream": false
}
```

### 🧠 Sohbet Devamı (Stateless History)
LiteBridge stateless çalışır. Sohbetin devam etmesi için tüm geçmiş mesajları her istekte göndermelisiniz:

```json
{
  "messages": [
    {"role": "user", "content": "Merhaba, ismim Ali."},
    {"role": "assistant", "content": "Merhaba Ali! Sana nasıl yardımcı olabilirim?"},
    {"role": "user", "content": "Benim ismim neydi?"}
  ]
}
```

---

## 🧪 Terminalden Test (cURL)

```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma-4-E2B-it",
    "messages": [{"role": "user", "content": "Naber?"}],
    "stream": true
  }'
```

---

## 📚 Otomatik Dokümantasyon (Swagger)

Sunucu çalışırken şu adreslerden etkileşimli dokümantasyona erişebilirsiniz:
- **Swagger UI:** [http://localhost:8080/docs](http://localhost:8080/docs)
- **ReDoc:** [http://localhost:8080/redoc](http://localhost:8080/redoc)

---

## 🔌 IDE Entegrasyonları
Detaylı kurulum adımları için [IDE_SETUP.md](docs/ide_setup.md) dosyasına göz atın.
