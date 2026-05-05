import { describe, it, expect } from "vitest";
import { formatDate, getDaysUntil, getUrgencyClass, generateId } from "./utils";

describe("formatDate", () => {
  it("formats a date string correctly", () => {
    const result = formatDate("2026-06-15");
    expect(result).toBe("Jun 15, 2026");
  });
});

describe("getDaysUntil", () => {
  it("returns 0 for today", () => {
    const today = new Date().toISOString().split("T")[0];
    expect(getDaysUntil(today)).toBe(0);
  });

  it("returns positive for future dates", () => {
    const future = new Date();
    future.setDate(future.getDate() + 5);
    const result = getDaysUntil(future.toISOString().split("T")[0]);
    expect(result).toBe(5);
  });

  it("returns negative for past dates", () => {
    const past = new Date();
    past.setDate(past.getDate() - 3);
    const result = getDaysUntil(past.toISOString().split("T")[0]);
    expect(result).toBe(-3);
  });
});

describe("getUrgencyClass", () => {
  it("returns green for completed items", () => {
    expect(getUrgencyClass(5, true)).toBe("text-green-600");
  });

  it("returns red for overdue items", () => {
    expect(getUrgencyClass(-1, false)).toBe("text-red-600");
  });

  it("returns orange for items due within 3 days", () => {
    expect(getUrgencyClass(2, false)).toBe("text-orange-500");
  });

  it("returns yellow for items due within 7 days", () => {
    expect(getUrgencyClass(5, false)).toBe("text-yellow-600");
  });

  it("returns default for items further out", () => {
    expect(getUrgencyClass(10, false)).toBe("text-zinc-600");
  });
});

describe("generateId", () => {
  it("generates unique IDs", () => {
    const id1 = generateId();
    const id2 = generateId();
    expect(id1).not.toBe(id2);
  });

  it("generates string IDs", () => {
    expect(typeof generateId()).toBe("string");
  });
});
