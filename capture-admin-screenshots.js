const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({
    headless: false,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080 });

  const screenshotsDir = path.join(__dirname, 'docs', 'screenshots');

  try {
    console.log('1. 正在訪問登入頁面...');
    await page.goto('https://taiwantea.frrut.com/admin/login', { waitUntil: 'networkidle0' });
    await page.screenshot({ path: path.join(screenshotsDir, '01-login.png'), fullPage: true });
    console.log('✓ 登入頁面截圖完成');

    console.log('2. 正在登入...');
    await page.type('input[type="email"]', 'admin@taiwantea.com');
    await page.type('input[type="password"]', 'Admin123!');
    await page.click('button[type="submit"]');
    await page.waitForNavigation({ waitUntil: 'networkidle0' });
    console.log('✓ 登入成功');

    console.log('3. 正在截取儀表板...');
    await page.screenshot({ path: path.join(screenshotsDir, '02-dashboard.png'), fullPage: true });
    console.log('✓ 儀表板截圖完成');

    console.log('4. 正在截取產品管理...');
    await page.goto('https://taiwantea.frrut.com/admin/products', { waitUntil: 'networkidle0', timeout: 30000 });
    await new Promise(resolve => setTimeout(resolve, 3000));
    await page.screenshot({ path: path.join(screenshotsDir, '03-products.png'), fullPage: true });
    console.log('✓ 產品管理截圖完成');

    console.log('5. 正在截取分類管理...');
    await page.goto('https://taiwantea.frrut.com/admin/categories', { waitUntil: 'networkidle0', timeout: 30000 });
    await new Promise(resolve => setTimeout(resolve, 3000));
    await page.screenshot({ path: path.join(screenshotsDir, '04-categories.png'), fullPage: true });
    console.log('✓ 分類管理截圖完成');

    console.log('6. 正在截取輪播管理...');
    await page.goto('https://taiwantea.frrut.com/admin/carousel', { waitUntil: 'networkidle0', timeout: 30000 });
    await new Promise(resolve => setTimeout(resolve, 3000));
    await page.screenshot({ path: path.join(screenshotsDir, '05-carousel.png'), fullPage: true });
    console.log('✓ 輪播管理截圖完成');

    console.log('7. 正在截取網站設定...');
    await page.goto('https://taiwantea.frrut.com/admin/settings', { waitUntil: 'networkidle0', timeout: 30000 });
    await new Promise(resolve => setTimeout(resolve, 3000));
    await page.screenshot({ path: path.join(screenshotsDir, '06-settings.png'), fullPage: true });
    console.log('✓ 網站設定截圖完成');

    console.log('\n✅ 所有截圖已完成！');
    console.log(`截圖儲存位置: ${screenshotsDir}`);

  } catch (error) {
    console.error('❌ 錯誤:', error.message);
  } finally {
    await browser.close();
  }
})();
