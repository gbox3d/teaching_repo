---
marp: true
theme: default
paginate: true
header: Web Programming Special Lecture
footer: A Kakao Aerial-Map Canvas Shared by Humans and AI
---

# A Page Shared by Humans and AI

## Empathy Between AI and Humans

Kakao SKYVIEW · restricted relay · Canvas · an explicit collaboration API

---

## The Flow We'll Build Today

~~~text
Address / GPS → Kakao Map
                  ↓
       One official StaticMap SKYVIEW image
                  ↓
          A strict local relay
                  ↓
              Canvas
                  ↕
        Human·AI collaboration API
~~~

---

## Empathy Is a Capability Contract

- What can we read together?
- Which commands can we run together?
- What can only a human start?
- Who ran what?
- Can it be undone?

"Can AI do this" matters less than "within what boundary can it do this."

---

## Human-Only Capabilities

| capability | reason |
|---|---|
| GPS permission | consent to location data |
| Local file selection | personal data boundary |
| Final download | has an external effect |

A human starts these three features directly, from the UI.

Requesting one through <code>execute()</code> is rejected with <code>PROTECTED_COMMAND</code>.

---

## Shared Human·AI Capabilities

- Read the current state
- Search an address
- Move to coordinates
- Change map type
- Prepare one static aerial view
- Rotate, brightness, contrast
- Add text
- Undo
- Read the current Canvas Blob or Data URL

Each command exposes a name and reversibility metadata.

---

## Overall Module Structure

~~~text
main.js
 ├─ map.js
 ├─ static-map.js ── /api/kakao-static-image
 ├─ image-loader.js
 ├─ collaboration-bridge.js
 └─ canvas-editor.js
       └─ editor-core.js

server.mjs
 └─ static-map-relay.mjs
~~~

---

## Configuration Lives in One Place at the Git Root

~~~json
{
  "kakaoMaps": {
    "javascriptKey": "REPLACE_WITH_YOUR_JAVASCRIPT_KEY"
  }
}
~~~

Path:

~~~text
<repository root>\config.json
~~~

- <code>/config.json</code> is excluded from Git
- JavaScript SDK domain: <code>http://localhost:3000</code>
- No REST API key or Admin key is used

---

## The JavaScript Key Is Visible in the Browser

~~~text
config.json
  → /runtime-config.json
  → Kakao JavaScript SDK
~~~

- Excluding it from the repository and keeping it private at runtime are different problems
- Manage this with allowed domains and usage limits
- The runtime response only carries the key and whether setup is done
- The relay, too, only ever uses the image URL the JavaScript SDK generated

---

## Address to Coordinates

~~~js
const first = results[0];
const position = new kakao.maps.LatLng(
  Number(first.y),
  Number(first.x)
);
~~~

- <code>x</code>: longitude
- <code>y</code>: latitude
- <code>LatLng</code>: latitude, longitude

Even when AI proposes coordinates, this contract is validated.

---

## A Human Decides on GPS

~~~js
navigator.geolocation.getCurrentPosition(
  usePosition,
  showAlternative
);
~~~

- A human requests it by pressing a button
- Approval, denial, and timeout are handled separately
- Address and coordinate input still work even if denied
- Nothing is auto-saved to a server or file

---

## SKYVIEW and HYBRID

~~~js
map.setMapTypeId(kakao.maps.MapTypeId.SKYVIEW);
map.setMapTypeId(kakao.maps.MapTypeId.HYBRID);
~~~

- The dynamic map is only for finding a location and choosing a zoom level
- Only the official <code>MapTypeId</code> values are allowed
- Dynamic tile URLs are never enumerated or assembled

---

## The Official SDK Builds the Static Aerial View

~~~js
new kakao.maps.StaticMap(container, {
  center: new kakao.maps.LatLng(latitude, longitude),
  level,
  mapTypeId: kakao.maps.MapTypeId.SKYVIEW
});
~~~

The app never assembles the image URL itself.

It checks that the container the official SDK built holds exactly one fully loaded image.

---

## What If You Draw It Straight to Canvas?

The StaticMap image is a cross-origin resource from the Kakao origin.

~~~text
Kakao image element
  → drawImage directly into a localhost Canvas
  → tainted Canvas
  → getImageData / toBlob / toDataURL blocked
~~~

You have to fetch it again as a same-origin Blob before Canvas can read or save it.

---

## What the Restricted Relay Is For

~~~text
The single image URL the SDK built
  → one cross-origin GET to verify the image directly
  → browser checks the exact origin/path
  → localhost relay
  → one more GET, re-requesting the same image resource
  → server re-checks it against an allowlist
  → JPEG/PNG response, no-store
  → same-origin Blob
~~~

This is not a general-purpose proxy.

---

## Browser-Side Validation

- Latitude −90 to 90, longitude −180 to 180
- Width 160–1280
- Height 120–960
- Map level 1–14
- Exact HTTPS origin and path
- Request Host matches same-origin Sec-Fetch-Site/Referer (and any forwarded Origin)
- No username, password, port, or fragment
- Decoded image, at most 2 million pixels
- Response size matches the requested size

Query fields are never built or parsed.

---

## Server-Side Validation

- GET only, exactly one source
- URL length, at most 2048
- Exact origin and path
- Only the fixed set of parameters, each once
- <code>service=open</code>
- Redirects are rejected
- 10-second timeout
- Response must be JPEG or PNG, at most 8MB
- One request at a time, at least 500ms apart
- <code>cache-control: no-store</code>

---

## What This Never Does

- Enumerate dynamic map tiles
- Collect and assemble multiple tiles
- Relay arbitrary URLs
- Follow redirects
- Read the full screen
- Capture the screen
- Cache relay responses
- Store data in bulk

It keeps to one boundary: the same StaticMap image resource for one location. There are exactly two network GETs total — one direct check, and one origin-clean relay request.

---

## The Kakao Attribution Area

~~~text
┌──────────────────────┐
│ full original StaticMap │ fixed size · scale 1 · rotates about center
│                          │ only clips what falls off-screen
│ attribution 80×32px     │ composited last, bottom-left
└──────────────────────┘
~~~

- Canvas size stays the same before and after rotation
- The bottom-left attribution mark is kept separately
- It's composited back into the same bottom-left spot last, after filters, annotations, and rotation

---

## Local Files Use the Same Editor

- PNG, JPEG, or WebP a human selected
- 20MB or smaller
- At most 24 million pixels
- No external URL input
- No server upload
- Attribution width and height are 0

A StaticMap Blob and a local file take different source paths, but share the same editing-state model.

---

## The Explicit Collaboration API

~~~js
const lab = window.aerialCanvasLab;

lab.getState();
await lab.execute("setMapType", { type: "HYBRID" });
await lab.execute("loadAerialView");
const blob = await lab.getImageBlob("png");
~~~

The global object and its capability list are frozen.
On this public interface, the actor is always fixed as AI — a caller can't pose as human or overwrite the summary.

---

## getState()

~~~text
location
  latitude, longitude, label

map
  ready, busy, type

workspace
  sourceKind, transform, size, annotations

boundaries
  browserScreenAccess=false
  gpsPermission=human-only
  fileSelection=human-only
  download=human-only
~~~

---

## execute() and the Allowlist

| command | reversible |
|---|---|
| findAddress | true |
| setLocation | true |
| setMapType | true |
| loadAerialView | false |
| setTransform | true |
| addText | true |
| undo | false |

Commands run one at a time, in sequence. <code>loadAerialView</code> uses the current shared location; it takes no separate coordinate payload. Even an unknown or protected command is logged to the activity log as a rejection.

---

## Activity Log

~~~json
{
  "actor": "ai",
  "command": "setTransform",
  "status": "success",
  "summary": "회전 0°, 밝기 105%, 대비 115% 적용",
  "timestamp": "2026-08-26T04:00:00.000Z"
}
~~~

- Logs UI collaboration
- A <code>collaboration-activity</code> event
- Distinguishes what a human did from what AI did
- Checks the capability list for whether a command is reversible

---

## Sharing the Image Explicitly

~~~js
const blob = await lab.getImageBlob("png");
const dataUrl = await lab.getImageDataUrl("jpeg");
~~~

- Returns only the current Canvas
- Never reads any other part of the browser
- Never starts a download
- Logged as a <code>readAerialImage</code> activity, with a status on both success and failure
- A read-only snapshot; it never ends or commits an in-progress human stroke

Human-only is a collaboration API contract. It is not a security sandbox that isolates an automation tool granted full control of the browser.

---

## Downloading Is Human-Only

| Action | AI | Human |
|---|---:|---:|
| Read Canvas Blob | Yes | Yes |
| Edit commands | allowlist | allowlist |
| Save PNG/JPEG file | No | Via button |

Shared data access is kept separate from external effects.

---

## Different from the REST Static Map API

<code>GET /v2/maps/staticmap</code>:

- Uses a REST API key
- Returns PNG/JPEG binary
- Current docs have no parameter for selecting SKYVIEW

What this implementation does:

- Uses a JavaScript key
- Uses the official Web SDK's StaticMap (SKYVIEW)
- Restricts the relay to the single image URL the SDK generated

---

## 70-Minute Lab

~~~text
Setup, 5 min
  → Location & human-only, 15 min
  → Single StaticMap relay, 15 min
  → Collaboration API, 20 min
  → Editing, sharing, and saving images, 15 min
~~~

For each stage:

**Problem → Predict → Implement → Observe → Explain the error → Extend**

[Special lecture lab](lab.md#준비-5분)

---

## Wrap-Up Questions

1. What's the difference between a general-purpose proxy and this relay?
2. Why accept only the one image the official SDK built?
3. At what point does the Canvas become same-origin?
4. Which capabilities are human-only?
5. What metadata records an AI's actions?
6. How does <code>getImageBlob()</code> differ from a download?
7. Where is the evidence that the full screen is never read?

---

## Check Before You Deploy

A restricted-relay design by itself doesn't automatically guarantee compliance with Kakao's usage policy.

Before deploying or operating this outside class, check the current Kakao Maps API terms of use and attribution policy. This does not assert legal permission.

---

## Official Documentation

- [Kakao Web API Reference](https://apis.map.kakao.com/web/documentation/)
- [Kakao StaticMap Sample](https://apis.map.kakao.com/web/sample/staticMap/)
- [Kakao Map REST API](https://developers.kakao.com/docs/ko/kakaomap/rest-api)
- [MDN CORS enabled images](https://developer.mozilla.org/en-US/docs/Web/HTML/How_to/CORS_enabled_image)
- [MDN Canvas.toBlob](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/toBlob)
- [MDN Geolocation](https://developer.mozilla.org/en-US/docs/Web/API/Geolocation/getCurrentPosition)
