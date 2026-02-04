import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  scenarios: {
    notes_load: {
      executor: "ramping-vus",
      startVUs: 0,
      stages: [
        { duration: "10s", target: 5 },   // ramp up
        { duration: "20s", target: 5 },   // steady
        { duration: "10s", target: 0 },   // ramp down
      ],
      gracefulRampDown: "5s",
    },
  },

  // Performance thresholds that MUST be met
  thresholds: {
    http_req_failed: ["rate<0.01"],       // < 1% request failures
    http_req_duration: ["p(95)<200"],     // 95% of requests < 200ms
  },
};

const BASE_URL = __ENV.BASE_URL || "http://127.0.0.1:5000";

export default function () {
  // 1) Read existing notes
  const listRes = http.get(`${BASE_URL}/api/notes`);
  check(listRes, {
    "GET /api/notes status is 200": (r) => r.status === 200,
  });

  // 2) Create a new note
  const payload = JSON.stringify({
    title: `perf-title-${__VU}-${__ITER}`,
    body: "perf-body",
  });

  const headers = { "Content-Type": "application/json" };
  const createRes = http.post(`${BASE_URL}/api/notes`, payload, { headers });

  check(createRes, {
    "POST /api/notes status is 201": (r) => r.status === 201,
  });

  sleep(1);
}

