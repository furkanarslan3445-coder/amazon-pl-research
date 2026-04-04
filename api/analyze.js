export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const body = typeof req.body === 'string' ? JSON.parse(req.body) : (req.body || {});
  const { keyword, apiKey } = body;
  if (!keyword || !apiKey) {
    return res.status(400).json({ error: `keyword ve apiKey gerekli`, received: { keyword: !!keyword, apiKey: !!apiKey, bodyType: typeof req.body } });
  }

  const SYSTEM_PROMPT = `Sen Amazon Private Label (PL) konusunda 10+ yıl deneyimli uzman bir ürün araştırma danışmanısın.
Kullanıcı sana bir anahtar kelime veya ürün verdiğinde şu başlıklar altında analiz yap:

## 🔍 Pazar Genel Bakış
## 🚀 Ürün Geliştirme & Yenilik Fırsatları
## ⚔️ Rakiplerin Önüne Geçme Stratejileri
## 📦 Ürün Farklılaştırma Önerileri
## ⚠️ Dikkat Edilmesi Gerekenler
## 💡 Aksiyon Planı

Somut ve uygulanabilir öneriler ver. Türkçe yanıt ver.
Analizinin en sonuna, başka bir şey eklemeden, tam olarak şu formatı kullan:
SKOR: X.X/10`;

  try {
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: 'claude-haiku-4-5-20251001',
        max_tokens: 2000,
        system: SYSTEM_PROMPT,
        messages: [{ role: 'user', content: `Amazon PL analizi yap: "${keyword}"` }],
      }),
    });

    if (!response.ok) {
      const err = await response.json().catch(() => ({}));
      return res.status(response.status).json({ error: err?.error?.message || 'API hatası' });
    }

    const data = await response.json();
    const text = data.content?.map(b => b.type === 'text' ? b.text : '').join('') || '';
    const scoreMatch = text.match(/SKOR:\s*(\d+(?:\.\d+)?)\/10/i);
    const score = scoreMatch ? parseFloat(scoreMatch[1]) : null;
    const analysis = text.replace(/SKOR:\s*\d+(?:\.\d+)?\/10/gi, '').trim();

    res.status(200).json({ score, analysis });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
}
