import { useState, useCallback } from "react";

interface UseApiReturn<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
  execute: (...args: unknown[]) => Promise<T | null>;
}

export function useApi<T>(
  apiFn: (...args: unknown[]) => Promise<T>
): UseApiReturn<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const execute = useCallback(
    async (...args: unknown[]): Promise<T | null> => {
      setLoading(true);
      setError(null);
      try {
        const result = await apiFn(...args);
        setData(result);
        return result;
      } catch (err: unknown) {
        const message =
          err instanceof Error ? err.message : "An error occurred";
        setError(message);
        return null;
      } finally {
        setLoading(false);
      }
    },
    [apiFn]
  );

  return { data, loading, error, execute };
}
