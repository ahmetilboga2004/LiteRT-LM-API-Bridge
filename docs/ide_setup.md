# LiteBridge IDE Kurulum Rehberi

LiteBridge, OpenAI uyumlu bir API sunduğu için birçok modern IDE ve kodlama asistanı ile doğrudan çalışabilir.

## Genel Bağlantı Bilgisi
- **Base URL:** `http://localhost:8080/v1`
- **Model Name:** `gemma-4-E2B-it` (veya .env'de ne yazdıysanız)
- **API Key:** Gerekli değil (herhangi bir şey yazabilirsiniz)

---

## 1. Cursor IDE
1. **Settings > Models** kısmına gidin.
2. **OpenAI API Key** kısmına rastgele bir şeyler yazın.
3. **Override OpenAI Base URL** kısmına `http://localhost:8080/v1` yazın.
4. Alt kısımdaki model listesine `gemma-4-E2B-it` (veya kullandığınız model ID) ekleyin ve aktif edin.

## 2. Zed Editor
`settings.json` dosyanıza şu yapılandırmayı ekleyin:

```json
{
  "language_models": {
    "openai": {
      "version": "1",
      "api_url": "http://localhost:8080/v1"
    }
  }
}
```

## 3. Aider (CLI)
Terminalde şu komutla çalıştırın:
```bash
aider --openai-api-base http://localhost:8080/v1 --model openai/gemma-4-E2B-it
```

## 4. VS Code (Continue Extension)
`config.json` dosyanıza şu modeli ekleyin:

```json
{
  "models": [
    {
      "title": "LiteBridge (Gemma)",
      "model": "gemma-4-E2B-it",
      "apiBase": "http://localhost:8080/v1",
      "completionOptions": {},
      "provider": "openai"
    }
  ]
}
```

## 5. Cline / Roo Code
1. API Provider olarak **OpenAI Compatible** seçin.
2. Base URL: `http://localhost:8080/v1`
3. Model ID: `gemma-4-E2B-it`
