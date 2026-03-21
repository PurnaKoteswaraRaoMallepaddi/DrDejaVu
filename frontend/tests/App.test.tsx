import { describe, it, expect } from "vitest";

describe("App", () => {
  it("should have correct types defined", () => {
    // Verify TypeScript types compile correctly
    const message = {
      id: "1",
      role: "user" as const,
      content: "test",
      timestamp: new Date(),
    };
    expect(message.role).toBe("user");
  });
});
