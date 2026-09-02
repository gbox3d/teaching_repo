import { seedCards } from "./data.js";

let failMode = false;

export function setFailMode(value) {
  failMode = value;
}

export async function fetchCards() {
  await new Promise((resolve) => setTimeout(resolve, 300));
  if (failMode) throw new TypeError("mock network failure");
  return structuredClone(seedCards);
}
