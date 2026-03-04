"use client";

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <html>
      <body style={{ background: "#111", color: "#fff", fontFamily: "sans-serif", display: "flex", alignItems: "center", justifyContent: "center", height: "100vh", margin: 0 }}>
        <div style={{ textAlign: "center" }}>
          <h1>Something went wrong!</h1>
          <p style={{ color: "#f88" }}>{error.message}</p>
          <button onClick={() => reset()} style={{ marginTop: 16, padding: "8px 24px", background: "#6cf", border: "none", borderRadius: 4, cursor: "pointer" }}>
            Try again
          </button>
        </div>
      </body>
    </html>
  );
}
