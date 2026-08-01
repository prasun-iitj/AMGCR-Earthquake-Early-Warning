"use client";

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-[#f8f9fb] font-sans text-[#1a1a2e] antialiased">
        <main className="flex min-h-screen items-center justify-center px-4">
          <div className="max-w-md text-center">
            <p className="text-sm font-semibold uppercase tracking-wider text-[#c45c26]">
              Application error
            </p>
            <h1 className="mt-3 font-serif text-3xl font-semibold">
              Unable to load the application
            </h1>
            <p className="mt-4 text-[#5c6370]">
              A critical error prevented the site from rendering. Please refresh or try again.
            </p>
            <button
              type="button"
              onClick={reset}
              className="mt-8 rounded-lg bg-[#1e3a5f] px-5 py-2.5 text-sm font-medium text-white hover:bg-[#2d5a87] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#1e3a5f]/40"
            >
              Try again
            </button>
          </div>
        </main>
      </body>
    </html>
  );
}
