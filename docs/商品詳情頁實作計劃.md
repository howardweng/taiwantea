# 商品詳情頁功能規劃

## 📋 功能需求總覽

### 客戶端（顧客）看到的內容

1. ✅ 商品多圖輪播（主圖 + 多角度細節圖，最多 6 張）
2. ✅ 商品基本資訊（名稱、價格、庫存狀態）
3. ✅ 完整商品描述（純文字）
4. ✅ 富文本詳細介紹（圖文混排，WYSIWYG 編輯）
5. ✅ 購買按鈕（連結到蝦皮）
6. ✅ 導航麵包屑（首頁 > 分類 > 商品名稱）
7. ✅ 返回按鈕

### 管理端（Admin）功能

1. ✅ 上傳多張商品圖片（最多 6 張）
2. ✅ 設定主圖（第一張圖）
3. ✅ 複製貼上調整圖片順序（類似 Intro Section 的操作方式）
4. ✅ 編輯完整商品描述（原有文字欄位）
5. ✅ 使用 WYSIWYG 編輯器（react-quill）編輯詳細介紹（圖文混排）
6. ✅ 預覽詳情頁效果

---

## 一、資料庫結構修改

### 在現有 `products` collection 新增欄位

```javascript
{
  // 現有欄位保持不變
  "name": "阿里山高山烏龍茶",
  "description": "簡短描述文字...",
  "imageUrl": "/uploads/main.png",        // 主圖（保留，向後兼容）
  "thumbnailUrl": "/uploads/thumb.png",    // 縮圖（保留）

  // 新增欄位
  "images": [                              // 新增：多圖陣列（最多 6 張）
    {
      "url": "/uploads/main.png",         // 完整圖片 URL
      "thumbnailUrl": "/uploads/thumb.png", // 縮圖 URL
      "displayOrder": 0,                   // 排序（0 = 主圖）
      "alt": "商品正面圖"                   // 替代文字（無障礙）
    },
    {
      "url": "/uploads/detail-1.png",
      "thumbnailUrl": "/uploads/detail-1-thumb.png",
      "displayOrder": 1,
      "alt": "商品側面圖"
    }
  ],
  "detailContent": "<h2>產品介紹</h2><p>詳細內容...</p><img src='...'>"  // 新增：富文本內容
}
```

### 欄位說明

- `images` 陣列：儲存所有商品圖片（最多 6 張），第一張（displayOrder=0）為主圖
- `imageUrl` 保留：確保舊資料相容性，從 `images[0].url` 同步
- `detailContent`：儲存 WYSIWYG 編輯器的 HTML 內容

---

## 二、後端 API 修改

### 2.1 更新 Schema (`backend/src/schemas/product.py`)

```python
# 新增圖片物件 Schema
class ProductImage(BaseModel):
    url: str
    thumbnailUrl: Optional[str] = None
    displayOrder: int = 0
    alt: Optional[str] = None

# 更新 ProductResponse
class ProductResponse(BaseModel):
    id: str = Field(alias="_id")
    name: str
    # ... 現有欄位 ...
    images: Optional[List[ProductImage]] = []  # 新增
    detailContent: Optional[str] = ""          # 新增

# 更新 ProductCreateRequest 和 ProductUpdateRequest
class ProductCreateRequest(BaseModel):
    # ... 現有欄位 ...
    images: Optional[List[ProductImage]] = []
    detailContent: Optional[str] = ""
```

### 2.2 API 端點（無需新增，使用現有）

- ✅ `GET /api/products/{id}` - 已存在，返回商品詳情
- ✅ `PUT /api/admin/products/{id}` - 已存在，更新商品資料

### 2.3 資料遷移策略

- 舊商品自動轉換：若 `images` 為空，從 `imageUrl` 建立第一張圖
- 保持向後相容：更新時同步 `images[0]` 到 `imageUrl`

---

## 三、前端實作

### 3.1 新增路由 (`frontend/src/App.jsx`)

```jsx
<Route path="/products/:productId" element={<ProductDetailPage />} />
```

### 3.2 新建頁面與元件

**檔案結構：**
```
frontend/src/
├── pages/
│   └── ProductDetailPage.jsx           // 商品詳情頁面
├── components/
│   └── customer/
│       ├── ProductDetail.jsx           // 詳情主要元件
│       ├── ProductDetail.module.css
│       ├── ProductImageGallery.jsx     // 圖片輪播元件
│       ├── ProductImageGallery.module.css
│       └── Breadcrumb.jsx              // 麵包屑導航
```

### 3.3 客戶端元件設計

**ProductDetailPage.jsx：**
- 使用 `useParams()` 取得 `productId`
- 呼叫 API `GET /api/products/{productId}`
- 處理 loading、error 狀態
- 渲染 `ProductDetail` 元件

**ProductDetail.jsx：**
- 顯示商品資訊區塊
- 整合 `ProductImageGallery` 元件
- 顯示價格、庫存、描述
- 渲染 `detailContent` HTML（使用 `dangerouslySetInnerHTML`，需淨化）
- 購買按鈕（連結蝦皮）
- 麵包屑導航

**ProductImageGallery.jsx：**
- 主圖顯示區（大圖）
- 縮圖列表（可點擊切換）
- 支援左右箭頭切換
- 支援放大鏡或燈箱效果（重用現有 `ImageModal`）

### 3.4 管理端元件修改

**ProductForm.jsx（後台商品表單）新增功能：**

1. **多圖上傳區塊：**
   - 顯示已上傳圖片列表（可複製貼上調整順序）
   - 新增圖片按鈕（最多 6 張）
   - 每張圖片可刪除
   - 使用現有 `ImageUpload` 元件

2. **WYSIWYG 編輯器（react-quill）：**
   - 支援功能：
     - ✅ 粗體、斜體、底線
     - ✅ 標題（H2, H3）
     - ✅ 列表（有序、無序）
     - ✅ 插入圖片（可上傳）
     - ✅ 插入連結
     - ✅ 文字顏色
   - 即時預覽功能

**安裝 react-quill：**
```bash
cd frontend
npm install react-quill
npm install dompurify  # HTML 淨化（安全性）
```

---

## 四、實作步驟（分階段進行）

### **階段一：後端資料結構準備** ⭐ 當前階段

1. ✅ 更新 Product Schema（新增 `images` 和 `detailContent` 欄位）
2. ✅ 更新 Product Model 的 CRUD 方法
3. ✅ 資料遷移腳本（將舊資料的 `imageUrl` 轉換為 `images` 陣列）
4. ✅ 測試 API 端點

### **階段二：前端商品詳情頁（客戶端）**

1. 建立 `ProductDetailPage.jsx`
2. 建立 `ProductDetail.jsx` 元件
3. 建立 `ProductImageGallery.jsx` 圖片輪播
4. 建立 `Breadcrumb.jsx` 麵包屑導航
5. CSS 樣式設計（RWD 適配）
6. 更新 `ProductCard.jsx`，點擊後導向詳情頁
7. 測試客戶端顯示

### **階段三：後台管理功能**

1. 更新 `ProductForm.jsx`：新增多圖上傳區塊
2. 實作複製貼上調整圖片順序功能
3. 整合 WYSIWYG 編輯器（react-quill）
4. 圖片上傳功能（重用現有 `/api/upload/image`）
5. 預覽功能（彈窗顯示詳情頁效果）
6. 表單驗證與錯誤處理
7. 測試管理端功能

### **階段四：優化與測試**

1. SEO 優化（meta tags、og:image）
2. 無障礙測試（ARIA labels、鍵盤導航）
3. 效能優化（圖片懶載入、代碼分割）
4. 跨瀏覽器測試
5. 手機版 RWD 測試
6. 撰寫測試案例（Pytest + Vitest）

---

## 五、技術選型

### WYSIWYG 編輯器：react-quill

- ✅ 輕量級（bundle size 小）
- ✅ 易於整合
- ✅ 支援圖片上傳
- ✅ 免費開源
- ✅ 維護良好

### 圖片輪播實作：自行實作

- ✅ 完全客製化
- ✅ 程式碼簡潔
- ✅ 重用現有 ImageModal

---

## 六、資料庫遷移腳本範例

```python
# backend/src/scripts/migrate_product_images.py
async def migrate_products():
    """將現有商品的 imageUrl 轉換為 images 陣列格式"""
    products = await product_model.get_all()

    for product in products:
        # 若 images 欄位不存在或為空
        if not product.get('images'):
            images = [{
                "url": product.get('imageUrl', ''),
                "thumbnailUrl": product.get('thumbnailUrl', ''),
                "displayOrder": 0,
                "alt": f"{product['name']} 商品圖"
            }]

            await product_model.update(product['_id'], {
                "images": images,
                "detailContent": ""  # 預設空白
            })

    print(f"已遷移 {len(products)} 個商品")
```

---

## 七、預估工作量

| 階段 | 預估時間 | 難度 |
|------|---------|------|
| 階段一：後端準備 | 2-3 小時 | ⭐⭐ |
| 階段二：客戶端詳情頁 | 4-6 小時 | ⭐⭐⭐ |
| 階段三：管理端功能 | 6-8 小時 | ⭐⭐⭐⭐ |
| 階段四：測試優化 | 3-4 小時 | ⭐⭐ |
| **總計** | **15-21 小時** | |

---

## 八、優先度排序

### 必要功能（MVP）

1. 商品詳情頁顯示（單圖 → 多圖輪播）
2. 麵包屑導航
3. 管理端多圖上傳
4. 基本的詳細描述欄位

### 進階功能（第二階段）

1. WYSIWYG 編輯器
2. 複製貼上調整圖片順序
3. 預覽功能

### 可選功能（未來擴充）

1. 相關商品推薦
2. 商品評價功能
3. 分享到社群媒體

---

## 九、風險與注意事項

### 1. XSS 安全風險

- `detailContent` 需要 HTML 淨化（使用 `DOMPurify`）
- 只允許安全的 HTML 標籤
- 後台編輯器需要限制可用標籤

### 2. 圖片儲存空間

- 多圖上傳會增加儲存空間需求
- 建議限制每張圖片 < 2MB
- 總圖片數 <= 6 張

### 3. SEO 考量

- 商品詳情頁需要 meta tags
- Open Graph 標籤（社群分享）
- 結構化資料（JSON-LD）

### 4. 效能考量

- 圖片懶載入
- 縮圖預載入（hover 效果）
- 代碼分割（Code Splitting）

---

## 十、確認事項

- [x] 從階段一開始實作
- [x] 使用 react-quill 作為 WYSIWYG 編輯器
- [x] 圖片數量上限：6 張
- [x] 圖片排序：複製貼上方式（不使用拖曳）

---

## 相關文件

- [API 規格說明](./specs/001-i-wnat-to/contracts/api.yaml)
- [測試指南](./TESTING.md)
- [實作狀態追蹤](./IMPLEMENTATION_STATUS.md)

---

**建立日期：** 2025-11-01
**最後更新：** 2025-11-01
**狀態：** 規劃完成，準備實作
