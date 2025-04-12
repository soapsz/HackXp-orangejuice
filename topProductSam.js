const puppeteer = require('puppeteer');
const fs = require('fs');

async function getTopProducts(keyword) {
  const browser = await puppeteer.launch({
    headless: "new",
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-blink-features=AutomationControlled']
  });

  const page = await browser.newPage();
  await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36");

  await page.evaluateOnNewDocument(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => false });
  });

  const query = keyword.trim().replace(/ /g, '+');
  const url = `https://www.amazon.com/s?k=${query}`;
  await page.goto(url, { waitUntil: 'domcontentloaded' });

  const products = await page.evaluate(() => {
    const nodes = document.querySelectorAll('[data-component-type="s-search-result"]');
    const results = [];
    nodes.forEach(node => {
      const title = node.querySelector('h2 span')?.innerText;
      const image = node.querySelector('img')?.src;
      const desc = node.querySelector('.a-text-normal')?.innerText || "";
      const link = node.querySelector('.a-link-normal')?.href;
      if (title && image) {
        results.push({ title, image, description: desc, link });
      }
    });
    return results.slice(0, 5);
  });

  await browser.close();

  const html = `
<!DOCTYPE html>
<html><head>
  <meta charset="UTF-8">
  <title>Amazon Results</title>
  <style>
    body { font-family: Arial; padding: 40px; text-align: center; }
    .item { border: 1px solid #ccc; padding: 15px; margin: 15px auto; width: 300px; background: #fff; }
    img { max-width: 100%; }
    button { padding: 10px 20px; margin-top: 10px; }
  </style>
</head>
<body>
  <a href="/wishlist_view_sam.html">🛒 View My Wishlist</a>
  <h1>Amazon Search Results</h1>
  ${products.map((p, i) => `
    <div class="item">
      <a href="${p.link}" target="_blank"><img src="${p.image}" alt="Product Image"></a>
      <h3>${p.title}</h3>
      <p>${p.description}</p>
      <button onclick='addToCart(${JSON.stringify(p)})'>Add to Cart</button>
    </div>
  `).join('')}
  <br>
  <a href="/wishlist_view_sam.html">🛒 View My Wishlist</a>

  <script>
    function addToCart(product) {
      const items = JSON.parse(localStorage.getItem("wishlistSam") || "[]");
      items.push(product);
      localStorage.setItem("wishlistSam", JSON.stringify(items));
      alert("✅ Added to wishlist!");
    }
  </script>
</body></html>
  `;
  fs.writeFileSync("wishlist_search_sam.html", html);
}

const keyword = process.argv[2] || "gift";
getTopProducts(keyword);
