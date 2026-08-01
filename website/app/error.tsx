"use client";

import { useEffect } from "react";
import { ErrorPageShell } from "@/components/errors/ErrorPageShell";

type ErrorPageProps = {
  error: Error & { digest?: string };
  reset: () => void;
};

export default function ErrorPage({ error, reset }: ErrorPageProps) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <ErrorPageShell
      statusCode="Error"
      title="Something went wrong"
      description="An unexpected error occurred while loading this page. You can try again or return to a safe starting point."
      showRetry
      onRetry={reset}
    />
  );
}
