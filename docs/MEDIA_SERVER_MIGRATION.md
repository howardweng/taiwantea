# Media Server Migration Plan

**Date**: 2025-11-01
**Objective**: Migrate from local file uploads to centralized media server API
**Media Server**: `https://mediaserver.frrut.com/uploadPic/taiwantea`

## Problem Statement

Current local file upload system requires manual rsync between environments (dev/staging/production), causing:
- Image inconsistencies across environments
- Development friction (local dev doesn't have production images)
- Deployment complexity
- Storage management per server

## Solution

Use existing media server API (`mediaserver.frrut.com`) which provides:
- Centralized storage (all environments use same images)
- Automatic thumbnail generation (full, thumbnail, small)
- HTTPS/CDN serving
- No sync required

## Media Server API Spec

**Endpoint**: `POST https://mediaserver.frrut.com/uploadPic/taiwantea`

**Request**:
```bash
curl -X POST "https://mediaserver.frrut.com/uploadPic/taiwantea" \
  -F "file=@image.jpg"
```

**Response**:
```json
{
  "message": "上傳成功",
  "fileName": "1761957064136.jpg",
  "imgUrl": "https://mediaserver.frrut.com/taiwantea/1761957064136.jpg",
  "thumbnailUrl": "https://mediaserver.frrut.com/taiwantea/1761957064136_thumb.jpg",
  "smImgUrl": "https://mediaserver.frrut.com/taiwantea/1761957064136_sm.jpg"
}
```

## Implementation Plan

### Phase 1: Backend Changes

#### 1.1 Configuration (`backend/src/config.py`)

**Changes**:
- Add `MEDIA_SERVER_URL` setting
- Add `MEDIA_SERVER_UPLOAD_ENDPOINT` setting
- Remove feature flag (always enabled)

**New Settings**:
```python
MEDIA_SERVER_URL: str = "https://mediaserver.frrut.com"
MEDIA_SERVER_UPLOAD_ENDPOINT: str = "/uploadPic/taiwantea"
```

**File**: `backend/src/config.py`

---

#### 1.2 Media Service (`backend/src/services/media_service.py`)

**New file** - Create service for media server integration

**Functionality**:
- `upload_to_media_server(file_content: bytes, filename: str) -> dict`
  - Upload file to media server
  - Handle connection errors with retries (3 attempts)
  - Return parsed response with URLs
  - Timeout: 30 seconds
- `validate_media_server_response(response: dict) -> bool`
  - Verify response has required fields
- Error handling for:
  - Network failures
  - Invalid responses
  - Timeout errors

**Dependencies**:
- `httpx` (async HTTP client) - add to `requirements.txt`

**Response Format**:
```python
{
    "success": True,
    "imageUrl": "https://mediaserver.frrut.com/taiwantea/123.jpg",
    "thumbnailUrl": "https://mediaserver.frrut.com/taiwantea/123_thumb.jpg",
    "smImageUrl": "https://mediaserver.frrut.com/taiwantea/123_sm.jpg",
    "filename": "123.jpg"
}
```

**File**: `backend/src/services/media_service.py`

---

#### 1.3 Upload Router Updates (`backend/src/routers/upload.py`)

**Changes**:
- Import new `media_service`
- Update `upload_image()` endpoint logic:
  1. Keep existing validation (file type, size)
  2. Upload to media server via `media_service` (always)
  3. Return media server URLs
  4. No fallback logic - fail if media server fails
- Remove local file saving logic (no longer needed)
- Remove local thumbnail generation (media server handles it)
- Update response to include `smImageUrl` from media server
- **Keep** local serving endpoint `/uploads/products/{filename}` (needed during migration)
- **Remove** delete endpoint - images never deleted from media server

**Updated Response**:
```python
{
    "success": True,
    "imageUrl": "https://mediaserver.frrut.com/taiwantea/123.jpg",
    "thumbnailUrl": "https://mediaserver.frrut.com/taiwantea/123_thumb.jpg",
    "smImageUrl": "https://mediaserver.frrut.com/taiwantea/123_sm.jpg",  # NEW
    "filename": "123.jpg"
}
```

**File**: `backend/src/routers/upload.py`

---

#### 1.4 Dependencies (`backend/requirements.txt`)

**Add**:
```
httpx>=0.25.0  # For async HTTP requests to media server
```

**Install**:
```bash
cd backend
source .venv/bin/activate
pip install httpx
pip freeze > requirements.txt
```

---

#### 1.5 Environment Configuration (`backend/.env.example`)

**Add**:
```env
# Media Server Configuration
MEDIA_SERVER_URL=https://mediaserver.frrut.com
MEDIA_SERVER_UPLOAD_ENDPOINT=/uploadPic/taiwantea
```

**Update** `backend/.env` with same values

---

### Phase 2: Frontend Changes

#### 2.1 Image Utils Update (`frontend/src/utils/imageUtils.js`)

**Changes**:
- Update `getImageUrl()` to handle media server URLs
- Current logic already handles external URLs (starts with `http://` or `https://`)
- **No changes needed** - already compatible!

**Verification**:
```javascript
// Already works:
getImageUrl("https://mediaserver.frrut.com/taiwantea/123.jpg")
// Returns: "https://mediaserver.frrut.com/taiwantea/123.jpg"
```

**File**: `frontend/src/utils/imageUtils.js` - NO CHANGES NEEDED ✓

---

#### 2.2 Admin Image Upload Component (`frontend/src/components/admin/ImageUpload.jsx`)

**Check if exists** - If not, this is the drag-drop component used in product forms

**Changes** (if applicable):
- Verify API response handling includes new `smImageUrl` field
- Update success message to show all 3 image sizes
- Add loading state during upload
- Add error handling for media server failures

**Files to check**:
- `frontend/src/components/admin/ImageUpload.jsx`
- `frontend/src/components/admin/ProductForm.jsx`

---

#### 2.3 Product Schema Updates (Frontend Types)

**If using TypeScript or PropTypes**:
- Add `smImageUrl` to product shape
- Update PropTypes in `ProductCard.jsx`

**Changes**:
```javascript
// frontend/src/components/customer/ProductCard.jsx
product: PropTypes.shape({
  // ... existing fields
  imageUrl: PropTypes.string.isRequired,
  thumbnailUrl: PropTypes.string,
  smImageUrl: PropTypes.string,  // NEW - optional for backward compatibility
})
```

**File**: `frontend/src/components/customer/ProductCard.jsx`

---

### Phase 3: Database Migration

#### 3.1 Schema Updates

**Collections Affected**:
- `products` - imageUrl, thumbnailUrl fields
- `carousel_items` - imageUrl field

**Current Format**:
```json
{
  "imageUrl": "/api/uploads/products/uuid.jpg",
  "thumbnailUrl": "/api/uploads/products/uuid_thumb.jpg"
}
```

**New Format**:
```json
{
  "imageUrl": "https://mediaserver.frrut.com/taiwantea/123.jpg",
  "thumbnailUrl": "https://mediaserver.frrut.com/taiwantea/123_thumb.jpg",
  "smImageUrl": "https://mediaserver.frrut.com/taiwantea/123_sm.jpg"
}
```

#### 3.2 Migration Strategy

**DECISION: Full Migration (Immediate)**
- Create migration script to upload ALL existing images
- Update all database records with media server URLs
- Keep local files as backup (don't delete)
- Clean migration - no mixed state

#### 3.3 Migration Script (REQUIRED)

**File**: `backend/src/scripts/migrate_images_to_media_server.py`

**Functionality**:
1. Connect to database
2. Fetch all products with relative image URLs (`/api/uploads/products/...`)
3. For each product:
   - Read image from `backend/uploads/products/`
   - Upload to media server via media_service
   - Update product record with new URLs (imageUrl, thumbnailUrl, smImageUrl)
   - Log success/failure
4. Also check carousel_items collection
5. Progress reporting (X of Y migrated)
6. **Dry-run mode** (preview changes without applying)

**Safety**:
- Backup database BEFORE running
- Dry-run first to preview changes
- Don't delete local files (keep as backup)
- Transaction-like updates (rollback on failure)
- Detailed logging to file

**Exit Codes**:
- 0: Success
- 1: Database connection failed
- 2: Migration errors occurred (partial success)

**Usage**:
```bash
cd backend
source .venv/bin/activate

# Dry run first
python src/scripts/migrate_images_to_media_server.py --dry-run

# Real migration
python src/scripts/migrate_images_to_media_server.py

# View log
cat logs/image_migration.log
```

---

### Phase 4: Testing Strategy

#### 4.1 Backend Unit Tests

**File**: `backend/tests/unit/test_media_service.py` (NEW)

**Tests**:
- `test_upload_to_media_server_success()` - Mock successful upload
- `test_upload_to_media_server_network_error()` - Mock network failure
- `test_upload_to_media_server_timeout()` - Mock timeout
- `test_upload_to_media_server_invalid_response()` - Mock malformed response
- `test_validate_media_server_response()` - Response validation

**Mocking**:
- Use `pytest-mock` or `unittest.mock`
- Mock `httpx.AsyncClient.post()`

---

#### 4.2 Backend Integration Tests

**File**: `backend/tests/integration/test_upload_integration.py` (UPDATE)

**Tests**:
- `test_upload_image_to_media_server()` - End-to-end upload to media server
- `test_upload_image_media_server_failure()` - Test error when media server down (no fallback)
- `test_upload_validates_file_type()` - File validation still works
- `test_upload_validates_file_size()` - Size validation still works

**Setup**:
- Use test database
- Mock media server for failure scenarios
- Test uploads go to actual media server (taiwantea namespace)
- No cleanup needed (images stay on media server)

---

#### 4.3 Backend Contract Tests

**File**: `backend/tests/contract/test_upload_contract.py` (UPDATE)

**Tests**:
- Verify API response format matches spec
- Check backward compatibility with old clients
- Verify all fields present (imageUrl, thumbnailUrl, smImageUrl)

---

#### 4.4 Frontend Unit Tests

**File**: `frontend/src/components/admin/__tests__/ImageUpload.test.jsx`

**Tests**:
- File upload interaction
- Loading states
- Error handling
- Success message display

---

#### 4.5 Frontend Integration Tests

**File**: `frontend/src/services/__tests__/uploadService.test.js`

**Tests**:
- API call with correct FormData
- Response parsing
- Error handling

---

#### 4.6 Manual Testing Checklist

**Admin Dashboard**:
- [ ] Upload new product image via admin panel
- [ ] Verify all 3 URLs returned in response (imageUrl, thumbnailUrl, smImageUrl)
- [ ] Check image displays correctly in admin preview
- [ ] Edit product and change image (old image stays on media server, new URL in DB)
- [ ] Delete product (image stays on media server - no deletion)

**Customer Frontend**:
- [ ] All products display images from media server
- [ ] Thumbnail loading on product grid
- [ ] Full image in modal
- [ ] Image lazy loading works
- [ ] Broken image handling (if URL invalid)

**Migration Verification**:
- [ ] Run migration script in dry-run mode
- [ ] Verify preview shows all products to migrate
- [ ] Run actual migration
- [ ] Check all products have HTTPS URLs in database
- [ ] Verify all images load from mediaserver.frrut.com
- [ ] No broken images on customer frontend

**Cross-Environment**:
- [ ] Upload image on dev, immediately visible on all environments
- [ ] No sync needed between environments
- [ ] Check image URLs all point to mediaserver.frrut.com

**Error Scenarios**:
- [ ] Media server down - test error message shown (no fallback)
- [ ] Network timeout - test retry logic
- [ ] Invalid file type - test validation
- [ ] File too large - test validation
- [ ] Concurrent uploads - test race conditions

---

### Phase 5: Deployment

#### 5.1 Pre-Deployment

**CRITICAL: Backup First**:
```bash
# Backup database (REQUIRED)
mongodump --uri="mongodb://datavanadmin:datavanabcbvf@128.199.112.130:2700/taiwantea?authSource=admin" --out=/backup/taiwantea-$(date +%Y%m%d)

# Backup local uploads (for safety)
cd /home/datavan/METROPIA/TAIWANTEA
tar -czf uploads-backup-$(date +%Y%m%d).tar.gz backend/uploads/
mv uploads-backup-*.tar.gz ~/backups/
```

**Configuration**:
- Add media server settings to `.env`
- No feature flag - going live immediately

---

#### 5.2 Deployment Steps

**Backend**:
```bash
# 1. Pull latest code
git pull origin main

# 2. Install new dependencies
cd backend
source .venv/bin/activate
pip install -r requirements.txt

# 3. Run tests
pytest -v

# 4. Restart backend
cd ../taiwantea-server
./restart.sh
```

**Frontend**:
```bash
# 1. Pull latest code (already done)
cd frontend

# 2. Install dependencies (if package.json changed)
npm install

# 3. Build for production
npm run build

# 4. Restart frontend
cd ../taiwantea-server
./restart_frontend.sh
```

---

#### 5.3 Migration Execution

**Step 1**: Deploy code (backend + frontend)
- Code deployed but migration not run yet
- App might show errors (old relative URLs invalid)

**Step 2**: Run migration script
```bash
cd backend
source .venv/bin/activate

# Dry run first
python src/scripts/migrate_images_to_media_server.py --dry-run
# Review output

# Run migration
python src/scripts/migrate_images_to_media_server.py
# Monitor progress
```

**Step 3**: Verify migration
- Check database - all URLs should be `https://mediaserver.frrut.com/...`
- Test customer frontend - all images load
- Test admin uploads - new images go to media server

**Step 4**: Monitor
- Watch upload success rate
- Check error logs
- Verify no 404 image errors

---

#### 5.4 Monitoring

**Metrics to Watch**:
- Upload success rate
- Upload latency (should be < 2 seconds)
- Media server availability
- Error rate increase
- Image 404 errors on frontend

**Logs to Check**:
```bash
# Backend logs
tail -f taiwantea-server/logs/api.log | grep upload

# Error logs
tail -f taiwantea-server/logs/error.log
```

---

### Phase 6: Rollback Plan

#### 6.1 Database Rollback (Restore Backup)

**If migration fails or critical issues**:
```bash
# Stop backend
cd taiwantea-server
./stop.sh

# Restore database backup
mongorestore --uri="mongodb://datavanadmin:datavanabcbvf@128.199.112.130:2700/taiwantea?authSource=admin" --drop --db=taiwantea /backup/taiwantea-YYYYMMDD/taiwantea

# Verify restoration
mongosh "mongodb://datavanadmin:datavanabcbvf@128.199.112.130:2700/taiwantea?authSource=admin"
# Check a few products have old relative URLs

# Start backend
./start.sh
```

---

#### 6.2 Full Rollback (Code)

**If critical bugs found**:
```bash
# 1. Revert to previous commit
git revert <commit-hash>

# 2. Redeploy backend
cd backend
source .venv/bin/activate
pip install -r requirements.txt
cd ../taiwantea-server
./restart.sh

# 3. Redeploy frontend
cd ../frontend
npm install
npm run build
cd ../taiwantea-server
./restart_frontend.sh

# 4. Restore database if needed
mongorestore --uri="mongodb://..." --db=taiwantea /backup/taiwantea-YYYYMMDD/taiwantea
```

---

#### 6.3 Data Integrity Check

**After rollback, verify**:
- Products display correctly
- Image uploads work (local or remote)
- No broken images on frontend
- Database image URLs are valid

---

### Phase 7: Post-Migration

#### 7.1 Old Image Cleanup (Optional)

**After 30 days of stable operation**:

```bash
# List local images not in database
cd backend
python src/scripts/find_orphaned_images.py

# Archive old local images
tar -czf uploads-archive-$(date +%Y%m%d).tar.gz uploads/
mv uploads-archive-*.tar.gz /archive/

# Remove local uploads (keep for 90 days in archive)
rm -rf uploads/products/*
```

---

#### 7.2 Documentation Updates

**Files to update**:
- `docs/IMPLEMENTATION_STATUS.md` - Mark media server migration complete
- `docs/使用說明.md` - Update image upload instructions
- `CLAUDE.md` - Update image serving documentation
- `README.md` - Update deployment instructions

---

#### 7.3 Performance Optimization

**Future enhancements**:
- Add CDN in front of media server
- Implement lazy loading for images (already done?)
- Add image compression options
- Implement WebP format support
- Add image caching headers

---

## File Checklist

### New Files
- [ ] `backend/src/services/media_service.py`
- [ ] `backend/tests/unit/test_media_service.py`
- [ ] `backend/src/scripts/migrate_images_to_media_server.py` **(REQUIRED)**

### Modified Files - Backend
- [ ] `backend/src/config.py` - Add media server settings
- [ ] `backend/src/routers/upload.py` - Integrate media service
- [ ] `backend/requirements.txt` - Add httpx
- [ ] `backend/.env.example` - Add media server config
- [ ] `backend/.env` - Add media server config
- [ ] `backend/tests/integration/test_upload_integration.py` - Update tests
- [ ] `backend/tests/contract/test_upload_contract.py` - Update tests

### Modified Files - Frontend
- [ ] `frontend/src/components/customer/ProductCard.jsx` - Add smImageUrl PropType
- [ ] `frontend/src/components/admin/ProductForm.jsx` - Handle smImageUrl (if exists)
- [ ] Check other components using imageUrl/thumbnailUrl

### Documentation
- [ ] `docs/MEDIA_SERVER_MIGRATION.md` - This file
- [ ] `docs/IMPLEMENTATION_STATUS.md` - Update status
- [ ] `CLAUDE.md` - Update image serving docs

---

## Risk Assessment

### High Risk
- **Database migration errors**: Wrong URLs stored, can't rollback easily
- **Media server downtime during migration**: Migration fails partway

**Mitigation**:
- Database backup BEFORE migration (mandatory)
- Dry-run mode tests migration without applying
- Detailed logging of every update
- Can restore from backup if needed

### Medium Risk
- **Media server downtime after migration**: New uploads fail
- **Network latency**: Media server upload slower than local (1-2s vs instant)
- **Image format incompatibility**: Media server rejects some files

**Mitigation**:
- Show clear error message to admin (no fallback)
- Retry logic (3 attempts) for transient failures
- Timeout to prevent hanging requests (30s)
- Pre-upload validation maintains same rules

### Low Risk
- **Storage costs**: Media server storage limits
- **CORS issues**: Media server blocks requests

**Mitigation**:
- Monitor media server capacity
- Media server already has CORS configured (successful test upload)

---

## Success Criteria

- [ ] Migration script completes successfully for all images
- [ ] All database records updated with media server URLs
- [ ] All new image uploads go to media server
- [ ] Zero 404 errors for images on customer frontend
- [ ] Dev environment shows same images as production immediately
- [ ] Upload latency < 3 seconds
- [ ] Test coverage maintained at 87%+
- [ ] No rollbacks required after 7 days
- [ ] Documentation updated

---

## Timeline Estimate

| Phase | Time | Description |
|-------|------|-------------|
| Backend implementation | 2-3 hours | Media service + upload router updates |
| **Migration script** | 1-2 hours | Script to migrate all existing images |
| Frontend updates | 30 min | PropTypes (minimal changes needed) |
| Testing | 2-3 hours | Unit, integration, migration dry-run |
| **Database backup** | 15 min | Backup before migration |
| Deployment | 1 hour | Deploy code + run migration |
| Monitoring | 1 week | Watch for issues |
| **Total** | **1-2 days** | Plus 1 week monitoring |

---

## Decisions (CONFIRMED)

1. **Feature Flag Default**: ✅ Enable immediately - No gradual rollout, go live with media server
2. **Old Image Migration**: ✅ Migrate ALL existing images NOW - No mixed state, clean migration
3. **Fallback Strategy**: ✅ Show error if media server down - No local fallback
4. **Media Server Auth**: ✅ No authentication required
5. **Image Deletion**: ✅ Never delete from media server - Keep all images, just add new URLs

**Result**: Simplified implementation - no feature flags, no fallback logic, no deletion logic

---

## Notes

- Frontend `imageUtils.js` already handles both relative and absolute URLs - no changes needed
- Media server returns 3 sizes (full, thumbnail, small) - more options than current system
- Upload validation (file type, size) remains in backend before sending to media server
- Local serving endpoint `/uploads/products/{filename}` must remain for backward compatibility
- Media server tested successfully with real image - upload works and returns valid URLs
