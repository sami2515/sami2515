import { chromium } from 'playwright';
import fs from 'node:fs/promises';
const pages = [
  ['testtayar', 'https://testtayar.pk/'],
  ['assurex', 'https://assurex.pythonanywhere.com/'],
];
await fs.mkdir('site-screenshots',{recursive:true});
const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
for(const [name,url] of pages){
  const page=await browser.newPage({viewport:{width:1400,height:875},deviceScaleFactor:1,reducedMotion:'reduce'});
  try {
    const response=await page.goto(url,{waitUntil:'domcontentloaded',timeout:60000});
    if (!response || response.status() >= 400) throw new Error(`HTTP ${response?.status() ?? 'missing'}`);
    await page.waitForLoadState('networkidle',{timeout:16000}).catch(()=>{});
    await page.waitForTimeout(2500);
    // Skip cookie/promotional overlay only if it is explicitly dismissible.
    for(const selector of ['button[aria-label="Close"]','button[aria-label="Dismiss"]','[data-testid="modal-close"]']){
      const el=page.locator(selector).first();
      if(await el.count() && await el.isVisible()) {await el.click({timeout:1200}).catch(()=>{});break;}
    }
    await page.screenshot({path:`site-screenshots/${name}.png`,fullPage:false,animations:'disabled'});
    console.log(`${name}: captured`,url);
  } catch(e) {
    console.log(`${name}: capture skipped`,String(e));
  } finally {await page.close();}
}
await browser.close();
