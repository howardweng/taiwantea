const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  console.log('Launching browser...');
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();

  // Set viewport to desktop size
  await page.setViewport({
    width: 1920,
    height: 1080,
    deviceScaleFactor: 1,
  });

  try {
    console.log('Navigating to homepage...');
    await page.goto('https://taiwantea.frrut.com/', {
      waitUntil: 'domcontentloaded',
      timeout: 60000
    });

    // Wait for content and images to load (longer wait)
    console.log('Waiting for page and images to fully load...');
    await new Promise(resolve => setTimeout(resolve, 8000));

    // Take full page screenshot
    const screenshotPath = path.join(__dirname, 'screenshots', 'customer-homepage.png');
    console.log(`Taking screenshot: ${screenshotPath}`);

    await page.screenshot({
      path: screenshotPath,
      fullPage: true
    });

    console.log('Screenshot saved successfully!');

  } catch (error) {
    console.error('Error capturing screenshot:', error);
  } finally {
    await browser.close();
    console.log('Browser closed.');
  }
})();
