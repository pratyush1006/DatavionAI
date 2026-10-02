const SHELL_CACHE = "datavion-patient-shell-v1";
const STATIC_CACHE = "datavion-patient-static-v1";
const DASHBOARD_PATH = "/patient/dashboard";

self.addEventListener("install", (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(SHELL_CACHE);
    try {
      await cache.add(DASHBOARD_PATH);
    } catch {
      // The first HTML shell can still be cached from the next online visit.
    }
    await self.skipWaiting();
  })());
});

self.addEventListener("activate", (event) => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys
      .filter((key) => key.startsWith("datavion-patient-") && key !== SHELL_CACHE && key !== STATIC_CACHE)
      .map((key) => caches.delete(key)));
    await self.clients.claim();
  })());
});

self.addEventListener("fetch", (event) => {
  const request = event.request;
  if (request.method !== "GET") return;

  const url = new URL(request.url);
  if (url.origin !== self.location.origin || url.pathname.startsWith("/api/")) return;

  if (request.mode === "navigate" && url.pathname.replace(/\/$/, "") === DASHBOARD_PATH) {
    event.respondWith((async () => {
      try {
        const response = await fetch(request);
        if (response.ok && response.type === "basic") {
          const cache = await caches.open(SHELL_CACHE);
          await cache.put(DASHBOARD_PATH, response.clone());
        }
        return response;
      } catch {
        const cached = await caches.match(DASHBOARD_PATH);
        return cached ?? new Response(
          "<main><h1>Patient dashboard unavailable offline</h1><p>Open the dashboard while online once, then save an encrypted offline copy.</p></main>",
          { status: 503, headers: { "Content-Type": "text/html; charset=utf-8" } },
        );
      }
    })());
    return;
  }

  if (url.pathname.startsWith("/_next/static/")) {
    event.respondWith((async () => {
      const cache = await caches.open(STATIC_CACHE);
      const cached = await cache.match(request);
      if (cached) return cached;
      try {
        const response = await fetch(request);
        if (response.ok && response.type === "basic") await cache.put(request, response.clone());
        return response;
      } catch {
        return cached ?? Response.error();
      }
    })());
  }
});
