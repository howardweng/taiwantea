# SEO 實施計劃

> 網站：https://taiwantea.frrut.com/
> 建立日期：2025-11-01
> 狀態：待實施

---

## 📋 目錄

1. [現況分析](#現況分析)
2. [Google Search Console 設定](#google-search-console-設定)
3. [必要檔案建立](#必要檔案建立)
4. [Meta 標籤優化](#meta-標籤優化)
5. [Sitemap 動態生成](#sitemap-動態生成)
6. [結構化資料](#結構化資料)
7. [實施時程](#實施時程)
8. [SEO 最佳實踐](#seo-最佳實踐)

---

## 🔍 現況分析

### 已具備項目 ✅
- ✅ 基本 HTML title：「台灣茗茶大師 TeaMaster」
- ✅ Favicon 已設定
- ✅ 正確的 charset 和 viewport meta 標籤
- ✅ HTTPS 已啟用
- ✅ 響應式設計

### 缺少項目 ❌
- ❌ Meta description（描述標籤）
- ❌ Meta keywords（關鍵字標籤）
- ❌ Open Graph 標籤（Facebook/LinkedIn 分享）
- ❌ Twitter Card 標籤
- ❌ robots.txt 檔案
- ❌ sitemap.xml 檔案
- ❌ 結構化資料（Schema.org markup）
- ❌ Canonical URL（標準網址）

---

## 🚀 Google Search Console 設定

### 步驟一：檢查網站是否已被索引

在 Google 搜尋框輸入：
```
site:taiwantea.frrut.com
```

如果有結果顯示，表示已被索引。如果沒有，請繼續以下步驟。

### 步驟二：註冊 Google Search Console

1. **前往 Google Search Console**
   - 網址：https://search.google.com/search-console/

2. **新增資源**
   - 點擊「新增資源」
   - 輸入：`https://taiwantea.frrut.com`
   - 選擇「網址前置字元」方法

3. **驗證網站所有權**

   **方法 A：HTML 檔案上傳**（最簡單）
   - 從 Google 下載驗證用的 HTML 檔案
   - 將檔案上傳至 `/frontend/public/` 資料夾
   - 部署後進行驗證

   **方法 B：HTML Meta 標籤**
   - Google 會提供類似以下的 meta 標籤：
     ```html
     <meta name="google-site-verification" content="YOUR_CODE_HERE" />
     ```
   - 將此標籤加入 `index.html` 的 `<head>` 區段

   **方法 C：DNS 記錄**
   - 在網域的 DNS 設定中新增 TXT 記錄
   - 如果有網域註冊商管理權限，此方法最為永久

4. **提交 Sitemap**
   - 驗證完成後，前往左側選單的「Sitemap」
   - 提交：`https://taiwantea.frrut.com/sitemap.xml`

5. **要求建立索引**
   - 使用「網址審查」工具
   - 輸入首頁網址
   - 點擊「要求建立索引」

### 步驟三：設定 Bing Webmaster Tools

不要忽略 Bing！在台灣仍有使用者。

1. 前往：https://www.bing.com/webmasters/
2. 使用 Microsoft 帳號登入
3. 可以直接從 Google Search Console 匯入網站資料

---

## 📁 必要檔案建立

### 1. robots.txt

**位置**：`/frontend/public/robots.txt`

**內容**：
```txt
User-agent: *
Allow: /

# 禁止索引管理員頁面
Disallow: /admin/
Disallow: /admin/*

# 禁止索引 API 端點
Disallow: /api/

# Sitemap 位置
Sitemap: https://taiwantea.frrut.com/sitemap.xml
```

**說明**：
- `User-agent: *` - 適用於所有搜尋引擎爬蟲
- `Allow: /` - 允許爬取所有公開頁面
- `Disallow: /admin/` - 不讓搜尋引擎索引管理介面
- `Sitemap:` - 告訴搜尋引擎 sitemap 的位置

---

### 2. sitemap.xml

**位置**：`/frontend/public/sitemap.xml`

**基本版本**：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">

  <!-- 首頁 -->
  <url>
    <loc>https://taiwantea.frrut.com/</loc>
    <lastmod>2025-11-01</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>

  <!-- 產品頁面 - 需要動態生成 -->
  <!-- 範例：
  <url>
    <loc>https://taiwantea.frrut.com/products/PRODUCT_ID</loc>
    <lastmod>2025-11-01</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  -->

</urlset>
```

**說明**：
- `<loc>` - 頁面的完整 URL
- `<lastmod>` - 最後修改日期（YYYY-MM-DD 格式）
- `<changefreq>` - 更新頻率（always, hourly, daily, weekly, monthly, yearly, never）
- `<priority>` - 優先順序（0.0 到 1.0，首頁通常是 1.0）

**注意**：由於產品是動態的，建議建立「動態 Sitemap 生成器」（見下方）。

---

## 🏷️ Meta 標籤優化

### 更新 index.html

**位置**：`/frontend/index.html`

**完整優化版本**：
```html
<!DOCTYPE html>
<html lang="zh-TW">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/x-icon" href="/favicon.ico" />
    <link rel="icon" type="image/png" sizes="256x256" href="/tea-logo.png" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <!-- 主要 Meta 標籤 -->
    <title>台灣茗茶大師 TeaMaster - 精選台灣高山茶｜烏龍茶、紅茶、綠茶</title>
    <meta name="title" content="台灣茗茶大師 TeaMaster - 精選台灣高山茶｜烏龍茶、紅茶、綠茶" />
    <meta name="description" content="台灣茗茶大師提供100%台灣高山茶葉，包括烏龍茶、紅茶、白茶、綠茶及茶葉禮盒。手工採摘，天然無添加，品質保證。立即選購優質台灣茶！" />
    <meta name="keywords" content="台灣茶葉, 高山茶, 烏龍茶, 紅茶, 綠茶, 白茶, 茶葉禮盒, 台灣茗茶, TeaMaster, 工藝窨花茶, 茶具週邊, 手工採摘, 天然茶葉" />
    <meta name="author" content="台灣茗茶大師 TeaMaster" />
    <meta name="robots" content="index, follow" />
    <link rel="canonical" href="https://taiwantea.frrut.com/" />

    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website" />
    <meta property="og:url" content="https://taiwantea.frrut.com/" />
    <meta property="og:title" content="台灣茗茶大師 TeaMaster - 精選台灣高山茶" />
    <meta property="og:description" content="台灣茗茶大師提供100%台灣高山茶葉，手工採摘，天然無添加，品質保證。探索烏龍茶、紅茶、綠茶等優質茶品。" />
    <meta property="og:image" content="https://taiwantea.frrut.com/tea-logo.png" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:locale" content="zh_TW" />
    <meta property="og:site_name" content="台灣茗茶大師 TeaMaster" />

    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image" />
    <meta property="twitter:url" content="https://taiwantea.frrut.com/" />
    <meta property="twitter:title" content="台灣茗茶大師 TeaMaster - 精選台灣高山茶" />
    <meta property="twitter:description" content="台灣茗茶大師提供100%台灣高山茶葉，手工採摘，天然無添加，品質保證。" />
    <meta property="twitter:image" content="https://taiwantea.frrut.com/tea-logo.png" />

    <!-- Google Fonts - Noto Sans TC -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

### Meta 標籤說明

#### 主要標籤
- **title**：顯示在瀏覽器分頁和搜尋結果中（建議 50-60 字元）
- **description**：顯示在搜尋結果的描述文字（建議 150-160 字元）
- **keywords**：幫助搜尋引擎理解頁面主題
- **robots**：告訴搜尋引擎可以索引並追蹤連結

#### Open Graph 標籤（社群媒體分享）
- 當有人在 Facebook、LinkedIn 分享連結時，會顯示這些資訊
- `og:image` 建議尺寸：1200x630 像素

#### Twitter Card 標籤
- 在 Twitter/X 分享連結時的顯示格式
- `summary_large_image` 會顯示大圖預覽

---

## 🗺️ Sitemap 動態生成

### 後端 API 端點

**位置**：`/backend/src/routers/sitemap.py`（新建）

```python
from fastapi import APIRouter
from fastapi.responses import Response
from datetime import datetime
from ..models.product import ProductModel

router = APIRouter(tags=["sitemap"])

@router.get("/sitemap.xml")
async def generate_sitemap():
    """
    動態生成 sitemap.xml
    包含所有產品頁面
    """
    # 取得所有上架產品
    products = await ProductModel.find_all(in_stock_only=True)

    # 生成 XML
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    # 首頁
    xml_content += '  <url>\n'
    xml_content += '    <loc>https://taiwantea.frrut.com/</loc>\n'
    xml_content += f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n'
    xml_content += '    <changefreq>daily</changefreq>\n'
    xml_content += '    <priority>1.0</priority>\n'
    xml_content += '  </url>\n'

    # 產品頁面
    for product in products:
        xml_content += '  <url>\n'
        xml_content += f'    <loc>https://taiwantea.frrut.com/products/{product["_id"]}</loc>\n'
        xml_content += f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n'
        xml_content += '    <changefreq>weekly</changefreq>\n'
        xml_content += '    <priority>0.8</priority>\n'
        xml_content += '  </url>\n'

    xml_content += '</urlset>'

    return Response(content=xml_content, media_type="application/xml")
```

### 註冊路由

**位置**：`/backend/src/main.py`

```python
from .routers import sitemap

# 在現有路由後新增
app.include_router(sitemap.router, prefix="/api")
```

### Nginx 設定（如果使用）

確保 `/sitemap.xml` 可以被存取：

```nginx
location /sitemap.xml {
    proxy_pass http://backend:8585/api/sitemap.xml;
}
```

---

## 📊 結構化資料（Schema.org）

結構化資料讓 Google 更了解你的網站內容，可以在搜尋結果中顯示豐富的摘要（Rich Snippets）。

### 產品頁面結構化資料

**位置**：`/frontend/src/pages/ProductDetailPage.jsx`

在產品頁面的 `<head>` 中加入：

```javascript
// 在 ProductDetailPage 組件中
useEffect(() => {
  if (!product) return;

  // 建立結構化資料
  const structuredData = {
    "@context": "https://schema.org/",
    "@type": "Product",
    "name": product.name,
    "image": product.imageUrls || [],
    "description": product.description,
    "brand": {
      "@type": "Brand",
      "name": "台灣茗茶大師 TeaMaster"
    },
    "offers": {
      "@type": "Offer",
      "url": `https://taiwantea.frrut.com/products/${product._id}`,
      "priceCurrency": "TWD",
      "price": product.price,
      "availability": product.inStock
        ? "https://schema.org/InStock"
        : "https://schema.org/OutOfStock"
    }
  };

  // 加入到頁面
  const script = document.createElement('script');
  script.type = 'application/ld+json';
  script.text = JSON.stringify(structuredData);
  document.head.appendChild(script);

  // 清理
  return () => {
    document.head.removeChild(script);
  };
}, [product]);
```

### 組織資訊結構化資料

**位置**：`/frontend/src/App.jsx` 或 `HomePage.jsx`

```javascript
const organizationData = {
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "台灣茗茶大師 TeaMaster",
  "url": "https://taiwantea.frrut.com",
  "logo": "https://taiwantea.frrut.com/tea-logo.png",
  "description": "提供100%台灣高山茶葉，包括烏龍茶、紅茶、白茶、綠茶及茶葉禮盒",
  "address": {
    "@type": "PostalAddress",
    "addressCountry": "TW",
    "addressLocality": "台灣"
  },
  "sameAs": [
    // 如果有社群媒體連結，在此加入
    // "https://www.facebook.com/taiwantea",
    // "https://www.instagram.com/taiwantea"
  ]
};
```

---

## 📅 實施時程

### 第一階段：立即執行（今天）

**優先順序：高**

- [ ] 建立 `robots.txt` 檔案
- [ ] 建立基本的 `sitemap.xml` 檔案
- [ ] 更新 `index.html` 加入完整的 meta 標籤
- [ ] 部署更新

**預計時間**：1-2 小時

---

### 第二階段：本週內完成

**優先順序：高**

- [ ] 註冊 Google Search Console
- [ ] 驗證網站所有權
- [ ] 提交 sitemap 至 Google
- [ ] 要求建立首頁索引
- [ ] 註冊 Bing Webmaster Tools
- [ ] 建立動態 sitemap 生成器

**預計時間**：2-3 小時

---

### 第三階段：兩週內完成

**優先順序：中**

- [ ] 在所有產品頁面加入結構化資料
- [ ] 在首頁加入組織資訊結構化資料
- [ ] 優化產品描述（加入關鍵字）
- [ ] 確保所有圖片都有 alt 屬性
- [ ] 檢查網站載入速度並優化

**預計時間**：4-6 小時

---

### 第四階段：持續進行

**優先順序：中低**

- [ ] 建立部落格或內容專區（茶知識、沖泡方法等）
- [ ] 定期更新內容
- [ ] 監控 Google Search Console 的報告
- [ ] 分析搜尋關鍵字表現
- [ ] 建立反向連結（與茶葉相關網站合作）
- [ ] 社群媒體經營

**預計時間**：持續進行

---

## 🎯 SEO 最佳實踐

### 1. 內容優化

#### 產品描述
- **長度**：每個產品至少 100-200 字的描述
- **關鍵字**：自然地包含相關關鍵字
  - 主要關鍵字：台灣茶葉、高山茶、[茶種名稱]
  - 長尾關鍵字：「手工採摘烏龍茶」、「天然無添加台灣紅茶」
- **避免**：關鍵字堆砌（看起來不自然）

#### 產品標題
```
✅ 好的範例：「阿里山高山烏龍茶 - 手工採摘 天然無添加 150g」
❌ 不好的範例：「tea 001」
```

#### 圖片優化
- **檔名**：使用描述性的檔名
  - ✅ `alishan-oolong-tea.jpg`
  - ❌ `IMG_0001.jpg`
- **Alt 屬性**：每張圖片都要加
  ```html
  <img src="alishan-oolong.jpg" alt="阿里山高山烏龍茶 - 手工採摘" />
  ```
- **壓縮**：使用 WebP 格式，減少檔案大小

---

### 2. 技術 SEO

#### 頁面載入速度
- **目標**：首次內容繪製（FCP）< 2 秒
- **工具**：
  - Google PageSpeed Insights
  - GTmetrix
  - WebPageTest

#### 改善方法
- 圖片壓縮和延遲載入
- 使用 CDN
- 啟用瀏覽器快取
- 最小化 CSS 和 JavaScript

#### 行動裝置友善
- 使用響應式設計（已完成 ✅）
- 測試工具：Google Mobile-Friendly Test
- 確保按鈕和連結易於點擊（至少 48x48 像素）

#### HTTPS
- 已啟用 ✅
- 確保所有資源（圖片、CSS、JS）都使用 HTTPS

---

### 3. 內容策略

#### 建立部落格
在 `/blog` 或 `/articles` 建立內容區域：

**主題建議**：
- 「如何選購台灣高山茶」
- 「烏龍茶的沖泡方法」
- 「認識台灣茶葉產區」
- 「茶葉保存指南」
- 「春茶、夏茶、秋茶、冬茶的差異」
- 「送禮首選：茶葉禮盒推薦」

**頻率**：每週 1-2 篇文章

**長度**：每篇至少 800-1500 字

---

### 4. 關鍵字研究

#### 主要關鍵字
- 台灣茶葉
- 高山茶
- 烏龍茶
- 台灣紅茶
- 阿里山茶
- 凍頂烏龍

#### 長尾關鍵字
- 台灣高山烏龍茶推薦
- 手工採摘台灣茶
- 天然無添加茶葉
- 台灣茶葉禮盒
- 梨山高冷茶
- 東方美人茶推薦

#### 工具
- Google Keyword Planner
- Google Trends
- Ahrefs（付費）
- Ubersuggest

---

### 5. 反向連結策略

#### 建立高品質反向連結
- 在茶葉論壇發表專業文章
- 與茶藝部落客合作評測
- 提交到台灣在地商家目錄
- 參與相關社群活動
- 客座文章發表

#### 本地 SEO
- Google 我的商家（如果有實體店面）
- 台灣黃頁網站登錄
- 在地部落格和新聞媒體曝光

---

### 6. 社群媒體整合

雖然社群媒體連結不是直接的 SEO 排名因素，但可以：
- 增加品牌曝光
- 帶來流量
- 建立品牌權威

**建議平台**：
- Facebook 粉絲專頁
- Instagram（視覺化產品展示）
- LINE 官方帳號（台灣使用者多）
- YouTube（茶葉沖泡教學影片）

---

## 📈 監控與分析

### Google Search Console 重點指標

每週檢查：
- **覆蓋率**：確保沒有索引錯誤
- **成效**：點擊次數、曝光次數、平均排名
- **查詢**：使用者搜尋哪些關鍵字找到你的網站

### Google Analytics

設定追蹤：
- 網站流量來源
- 使用者行為
- 轉換率
- 熱門產品頁面

### 定期檢查事項

**每週**：
- Google Search Console 錯誤報告
- 網站載入速度
- 新產品 sitemap 更新

**每月**：
- 關鍵字排名變化
- 競爭對手分析
- 內容效能評估
- 反向連結狀況

---

## ✅ 檢查清單

### 立即執行
- [ ] 建立 robots.txt
- [ ] 建立 sitemap.xml
- [ ] 更新 index.html meta 標籤
- [ ] 部署到生產環境

### 一週內
- [ ] Google Search Console 註冊與驗證
- [ ] 提交 sitemap
- [ ] Bing Webmaster Tools 註冊
- [ ] 建立動態 sitemap 生成器

### 兩週內
- [ ] 加入產品結構化資料
- [ ] 優化所有產品描述
- [ ] 圖片 alt 屬性優化
- [ ] 網站速度優化

### 持續進行
- [ ] 建立部落格內容
- [ ] 監控 Search Console
- [ ] 建立反向連結
- [ ] 社群媒體經營

---

## 📚 參考資源

### 官方文件
- [Google Search Console 說明](https://support.google.com/webmasters/)
- [Google SEO 入門指南](https://developers.google.com/search/docs/beginner/seo-starter-guide)
- [Schema.org 文件](https://schema.org/)
- [Sitemap 協議](https://www.sitemaps.org/)

### 工具
- [Google PageSpeed Insights](https://pagespeed.web.dev/)
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [Google Mobile-Friendly Test](https://search.google.com/test/mobile-friendly)
- [Screaming Frog SEO Spider](https://www.screamingfrog.co.uk/seo-spider/)（免費版）

### 學習資源
- Google Search Central YouTube 頻道
- Moz 初學者指南
- Ahrefs 部落格

---

## 🎯 預期成效

### 短期（1-3 個月）
- Google 開始索引網站
- 出現在品牌名稱的搜尋結果
- 網站流量逐漸增加

### 中期（3-6 個月）
- 主要關鍵字開始出現在搜尋結果（可能在第 2-3 頁）
- 自然搜尋流量顯著成長
- 部分長尾關鍵字排名進入前 20 名

### 長期（6-12 個月）
- 主要關鍵字排名進入首頁
- 建立品牌權威
- 持續穩定的自然流量
- 轉換率提升

---

## 💡 注意事項

### ⚠️ 避免的做法（Black Hat SEO）
- ❌ 購買反向連結
- ❌ 關鍵字堆砌
- ❌ 隱藏文字或連結
- ❌ 複製其他網站的內容
- ❌ 使用自動化工具大量建立連結

### ✅ 推薦的做法（White Hat SEO）
- ✅ 建立高品質、原創內容
- ✅ 提供良好的使用者體驗
- ✅ 自然地使用關鍵字
- ✅ 建立真實的反向連結
- ✅ 持續優化和改進

---

## 📞 需要協助？

如果在實施過程中遇到問題：
1. 參考本文件的相關章節
2. 查閱 Google Search Console 說明中心
3. 搜尋相關問題的解決方案
4. 諮詢 SEO 專業人士

---

**最後更新**：2025-11-01
**下次審查**：2025-11-15

---

> 💡 **記住**：SEO 是一個持續的過程，不是一次性的工作。需要耐心、持續優化，並根據數據調整策略。成功的 SEO 需要時間累積，通常需要 3-6 個月才能看到顯著成效。
