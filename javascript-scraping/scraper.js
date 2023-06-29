import puppeteer from "puppeteer";

async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  await page.goto("https://sosbiz.idaho.gov/search/business");

  // Set screen size
  await page.setViewport({ width: 1080, height: 1024 });

  // Type into search box
  await page.type(".search-input", "");
};
