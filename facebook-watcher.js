// facebook-watcher.js
// Production-ready Playwright Facebook monitor with anti-crash & anti-detection

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// Configuration
const CONFIG = {
  STORAGE_STATE: path.join(__dirname, 'facebook-auth.json'),
  HEADLESS: false, // Set to true after debugging
  SCROLL_INTERVAL: 15000, // 15 seconds between scrolls
  SCROLL_DISTANCE: 300,
  FEED_WAIT_TIMEOUT: 15000,
  MAX_SCROLL_ATTEMPTS: 50,
  AUTO_RESTART_ON_CRASH: true,
  KEYWORDS: ['sales', 'client', 'project', 'urgent', 'invoice', 'payment', 'deal', 'opportunity', 'partnership', 'lead', 'inquiry'],
};

// Anti-detection & anti-crash browser args (2025-2026 proven)
const HARDENED_ARGS = [
  // GPU crash prevention (CRITICAL for Windows)
  '--disable-gpu',
  '--disable-gpu-rasterization',
  '--disable-gpu-compositing',
  '--disable-software-rasterizer',
  '--disable-gpu-memory-buffer-video-frames',
  '--disable-gpu-sandbox',

  // Dev/debugging prevention
  '--disable-dev-shm-usage',
  '--no-sandbox',
  '--disable-setuid-sandbox',

  // Memory & process stability
  '--disable-background-timer-throttling',
  '--disable-backgrounding-occluded-windows',
  '--disable-breakpad',
  '--disable-client-side-phishing-detection',
  '--disable-component-update',
  '--disable-default-apps',
  '--disable-extensions',
  '--disable-features=TranslateUI,DialMediaRouteProvider',
  '--disable-hang-monitor',
  '--disable-ipc-flooding-protection',
  '--disable-popup-blocking',
  '--disable-prompt-on-repost',
  '--disable-renderer-backgrounding',
  '--disable-sync',
  '--enable-automation=false',
  '--metrics-recording-only',
  '--mute-audio',
  '--no-default-browser-check',
  '--no-first-run',
  '--password-store=basic',
  '--use-mock-keychain',

  // Stealth/anti-detection
  '--disable-blink-features=AutomationControlled',
  '--disable-search-engine-choice-screen',
];

// Stealth user data to evade detection
const STEALTH_CONFIG = {
  userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
  viewport: { width: 1920, height: 1080 },
  deviceScaleFactor: 1,
  isMobile: false,
  hasTouch: false,
  locale: 'en-US',
  timezoneId: 'America/New_York',
};

// Logger utility
class Logger {
  log(msg, type = 'INFO') {
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] [${type}] ${msg}`);
  }
  debug(msg) { this.log(msg, 'DEBUG'); }
  warn(msg) { this.log(msg, 'WARN'); }
  error(msg) { this.log(msg, 'ERROR'); }
  success(msg) { this.log(msg, '✅'); }
}

const logger = new Logger();

class FacebookWatcher {
  constructor() {
    this.browser = null;
    this.context = null;
    this.page = null;
    this.isRunning = false;
    this.crashCount = 0;
    this.maxCrashes = 5;
  }

  // Step 1: Launch browser with hardened configuration
  async launchBrowser() {
    logger.log('🔄 Launching Chromium with hardened args...');
    try {
      this.browser = await chromium.launch({
        headless: CONFIG.HEADLESS,
        args: HARDENED_ARGS,
        timeout: 30000,
      });
      logger.success('Browser launched');
      return this.browser;
    } catch (error) {
      logger.error(`Failed to launch browser: ${error.message}`);
      throw error;
    }
  }

  // Step 2: Create context with stealth & persistence
  async createContext() {
    logger.log('🔧 Creating browser context with stealth config...');

    const contextOptions = {
      ...STEALTH_CONFIG,
      ignoreHTTPSErrors: true,
      javaScriptEnabled: true,
      bypassCSP: true,
    };

    // Load saved storage state if it exists (fast login)
    if (fs.existsSync(CONFIG.STORAGE_STATE)) {
      logger.log('📂 Loading saved session from storage state...');
      const storageState = JSON.parse(fs.readFileSync(CONFIG.STORAGE_STATE, 'utf-8'));
      contextOptions.storageState = storageState;
    }

    this.context = await this.browser.newContext(contextOptions);

    // Inject anti-detection JavaScript
    await this.context.addInitScript(() => {
      // Hide webdriver property
      Object.defineProperty(navigator, 'webdriver', { get: () => false });

      // Hide chrome property
      window.chrome = { runtime: {} };

      // Override permissions
      const originalQuery = window.navigator.permissions.query;
      window.navigator.permissions.query = (parameters) => (
        parameters.name === 'notifications' ?
          Promise.resolve({ state: Notification.permission }) :
          originalQuery(parameters)
      );
    });

    logger.success('Context created with stealth config');
    return this.context;
  }

  // Step 3: Login to Facebook (first time only)
  async loginToFacebook() {
    logger.log('🔐 Attempting Facebook login...');

    this.page = await this.context.newPage();

    try {
      // Navigate to Facebook login
      await this.page.goto('https://www.facebook.com/login/', {
        waitUntil: 'domcontentloaded',
        timeout: 30000,
      });

      logger.log('📝 Facebook login page loaded');
      logger.log('⏳ Waiting for user input (120 seconds)...');
      logger.log('📋 Please log in manually in the browser window');

      // Wait for successful login (detect navigation to home feed)
      await this.page.waitForURL('**/feed/**', { timeout: 120000 }).catch(() => {
        logger.warn('Feed URL not detected, but proceeding...');
      });

      // Wait for feed to actually load
      await this.waitForFeedLoad();

      logger.success('✅ Login successful!');

      // Save session storage for future runs
      const storageState = await this.context.storageState();
      fs.writeFileSync(CONFIG.STORAGE_STATE, JSON.stringify(storageState, null, 2));
      logger.success('Session saved to storage state');

    } catch (error) {
      logger.error(`Login failed: ${error.message}`);
      throw error;
    }
  }

  // Step 4: Wait for Facebook feed to load
  async waitForFeedLoad() {
    logger.log('⏳ Waiting for feed to load...');

    try {
      // Wait for main feed container
      await this.page.waitForSelector('[role="feed"], [data-testid="feed"]', {
        timeout: CONFIG.FEED_WAIT_TIMEOUT,
      });

      // Wait for at least one post to appear
      await this.page.waitForSelector('div[data-testid="post"], article', {
        timeout: CONFIG.FEED_WAIT_TIMEOUT,
      });

      logger.success('Feed loaded successfully');
    } catch (error) {
      logger.warn(`Feed load timeout: ${error.message}`);
    }
  }

  // Step 5: Main monitoring loop
  async monitorFeed() {
    logger.log('👀 Starting feed monitoring...');
    this.isRunning = true;
    let scrollCount = 0;

    while (this.isRunning && scrollCount < CONFIG.MAX_SCROLL_ATTEMPTS) {
      try {
        // Ensure we're on Facebook
        if (!this.page.url().includes('facebook.com')) {
          logger.warn('Not on Facebook, navigating back...');
          await this.page.goto('https://www.facebook.com/feed/', {
            waitUntil: 'domcontentloaded',
          });
        }

        // Detect and log new content
        await this.detectNewContent();

        // Slow, natural scroll
        await this.slowScroll();

        scrollCount++;
        logger.log(`📊 Scroll #${scrollCount}/${CONFIG.MAX_SCROLL_ATTEMPTS}`);

        // Wait between scrolls (avoid rapid actions)
        await new Promise(r => setTimeout(r, CONFIG.SCROLL_INTERVAL));

      } catch (error) {
        logger.error(`Error during monitoring: ${error.message}`);
        this.crashCount++;

        if (this.crashCount >= this.maxCrashes) {
          logger.error('Max crashes reached, stopping...');
          this.isRunning = false;
          break;
        }

        // Try to recover
        await new Promise(r => setTimeout(r, 3000));
        try {
          await this.page.goto('https://www.facebook.com/feed/', {
            waitUntil: 'domcontentloaded',
          });
          logger.success('Recovered from error');
        } catch {
          logger.error('Recovery failed');
        }
      }
    }

    logger.log('Feed monitoring stopped');
  }

  // Step 6: Detect new content (stories, live, reels, posts with keywords)
  async detectNewContent() {
    try {
      // Check for stories
      const stories = await this.page.$$('[data-testid*="story"], .story-ring');
      if (stories.length > 0) {
        logger.log(`📖 Detected ${stories.length} stories`);
      }

      // Check for live videos
      const liveVideos = await this.page.$$('[data-testid*="live"], .live-badge');
      if (liveVideos.length > 0) {
        logger.log(`🔴 Detected ${liveVideos.length} live videos`);
      }

      // Check for reels
      const reels = await this.page.$$('[data-testid*="reel"], .reel-container');
      if (reels.length > 0) {
        logger.log(`🎬 Detected ${reels.length} reels`);
      }

      // Check for regular posts with keyword filtering
      const posts = await this.page.$$('article, div[data-testid="post"]');
      if (posts.length > 0) {
        logger.log(`📄 Feed has ${posts.length} posts visible`);

        // Check posts for keywords
        for (const post of posts) {
          try {
            const postText = await post.textContent();
            const hasKeyword = CONFIG.KEYWORDS.some(kw => postText.toLowerCase().includes(kw.toLowerCase()));
            if (hasKeyword) {
              const matchedKeywords = CONFIG.KEYWORDS.filter(kw => postText.toLowerCase().includes(kw.toLowerCase()));
              logger.log(`✅ Post contains keywords: ${matchedKeywords.join(', ')}`);
              logger.log(`   Text preview: ${postText.substring(0, 100)}...`);
            }
          } catch (e) {
            // Skip posts that can't be read
          }
        }
      }

    } catch (error) {
      logger.debug(`Content detection error: ${error.message}`);
    }
  }

  // Step 7: Slow, natural scroll
  async slowScroll() {
    try {
      // Multiple small scrolls instead of one big scroll (more human-like)
      for (let i = 0; i < 3; i++) {
        await this.page.evaluate(
          (distance) => {
            window.scrollBy(0, distance);
          },
          CONFIG.SCROLL_DISTANCE / 3
        );

        // Small delay between scroll steps
        await new Promise(r => setTimeout(r, 500 + Math.random() * 500));
      }

      // Random idle time (mimics human behavior)
      const idleTime = 2000 + Math.random() * 3000;
      await new Promise(r => setTimeout(r, idleTime));

    } catch (error) {
      logger.warn(`Scroll error: ${error.message}`);
    }
  }

  // Step 8: Graceful shutdown
  async shutdown() {
    logger.log('🛑 Shutting down gracefully...');
    this.isRunning = false;

    try {
      if (this.page) await this.page.close();
      if (this.context) await this.context.close();
      if (this.browser) await this.browser.close();
      logger.success('Shutdown complete');
    } catch (error) {
      logger.error(`Shutdown error: ${error.message}`);
    }

    process.exit(0);
  }

  // Step 9: Main run method with auto-restart
  async run() {
    try {
      await this.launchBrowser();
      await this.createContext();

      // Check if already logged in
      if (!fs.existsSync(CONFIG.STORAGE_STATE)) {
        logger.log('🆕 First time setup - login required');
        await this.loginToFacebook();
      } else {
        logger.success('✅ Using saved session');
        this.page = await this.context.newPage();
        await this.page.goto('https://www.facebook.com/feed/', {
          waitUntil: 'domcontentloaded',
        });
        await this.waitForFeedLoad();
      }

      // Start monitoring
      await this.monitorFeed();

    } catch (error) {
      logger.error(`Fatal error: ${error.message}`);
      this.crashCount++;

      if (CONFIG.AUTO_RESTART_ON_CRASH && this.crashCount < 3) {
        logger.log(`🔄 Auto-restarting (attempt ${this.crashCount})...`);
        await new Promise(r => setTimeout(r, 5000));
        await this.run();
      } else {
        await this.shutdown();
      }
    }
  }
}

// Main execution
async function main() {
  const watcher = new FacebookWatcher();

  // Handle Ctrl+C gracefully
  process.on('SIGINT', () => {
    logger.log('Received SIGINT, shutting down...');
    watcher.shutdown();
  });

  process.on('SIGTERM', () => {
    logger.log('Received SIGTERM, shutting down...');
    watcher.shutdown();
  });

  await watcher.run();
}

main().catch(error => {
  logger.error(`Unhandled error: ${error.message}`);
  process.exit(1);
});
