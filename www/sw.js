// ברסלב PRO – service worker מינימלי (התקנה למסך הבית והתראות); לא שומר את הספרים במטמון
self.addEventListener('install',e=>self.skipWaiting());
self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));
