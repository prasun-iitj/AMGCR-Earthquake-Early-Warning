import type { BinaryMetrics, ModelSet, PerEventRow } from "@/lib/ml/loader";

const palette = ["#1f77b4", "#2ca02c", "#ff7f0e", "#8c6bb1", "#d62728"];

function pct(v: number) {
  return `${(v * 100).toFixed(1)}%`;
}

/** Grouped horizontal bars: one group per metric, one bar per model. Values from saved JSON. */
export function MetricBars({
  models,
  metrics,
}: {
  models: ModelSet;
  metrics: { key: keyof BinaryMetrics; label: string }[];
}) {
  const names = Object.keys(models);
  return (
    <div className="space-y-5" role="img" aria-label="Grouped bar chart of model metrics">
      <ul className="flex flex-wrap gap-4 text-xs text-text-muted">
        {names.map((n, i) => (
          <li key={n} className="flex items-center gap-2">
            <span className="inline-block h-3 w-3 rounded-sm" style={{ background: palette[i % palette.length] }} />
            {n}
          </li>
        ))}
      </ul>
      {metrics.map((m) => (
        <div key={m.key as string}>
          <p className="mb-1 text-sm font-medium text-text">{m.label}</p>
          <div className="space-y-1">
            {names.map((n, i) => {
              const v = models[n][m.key] as number;
              return (
                <div key={n} className="flex items-center gap-3">
                  <div className="h-4 flex-1 overflow-hidden rounded bg-surface">
                    <div
                      className="h-full rounded"
                      style={{ width: `${Math.max(0, Math.min(1, v)) * 100}%`, background: palette[i % palette.length] }}
                    />
                  </div>
                  <span className="w-16 text-right font-mono text-xs text-text">{v.toFixed(4)}</span>
                </div>
              );
            })}
          </div>
        </div>
      ))}
    </div>
  );
}

export function ConfusionMatrix({ title, m }: { title: string; m: BinaryMetrics }) {
  const max = Math.max(m.tn, m.fp, m.fn, m.tp);
  const cells = [
    { label: "True noise / Pred noise (TN)", v: m.tn },
    { label: "True noise / Pred P-wave (FP)", v: m.fp },
    { label: "True P-wave / Pred noise (FN)", v: m.fn },
    { label: "True P-wave / Pred P-wave (TP)", v: m.tp },
  ];
  return (
    <figure className="rounded-xl border border-border bg-surface-elevated p-4">
      <figcaption className="mb-3 text-sm font-semibold text-text">{title}</figcaption>
      <div className="grid grid-cols-2 gap-1">
        {cells.map((c) => (
          <div
            key={c.label}
            title={c.label}
            className="flex aspect-[3/2] flex-col items-center justify-center rounded"
            style={{ background: `rgba(30,58,95,${0.08 + 0.85 * (c.v / max)})`, color: c.v / max > 0.5 ? "#fff" : "#1a1a2e" }}
          >
            <span className="font-mono text-2xl font-semibold">{c.v}</span>
            <span className="px-1 text-center text-[10px] leading-tight opacity-80">{c.label}</span>
          </div>
        ))}
      </div>
      <p className="mt-3 text-xs text-text-muted">
        accuracy {pct(m.accuracy)} · recall {pct(m.recall)} · precision {pct(m.precision)}
      </p>
    </figure>
  );
}

export function FeatureImportance({
  rf,
  xgb,
  top = 12,
}: {
  rf: Record<string, number>;
  xgb: Record<string, number>;
  top?: number;
}) {
  const names = Object.keys(rf)
    .sort((a, b) => rf[b] + xgb[b] - (rf[a] + xgb[a]))
    .slice(0, top);
  const maxRf = Math.max(...names.map((n) => rf[n]));
  const maxX = Math.max(...names.map((n) => xgb[n]));
  return (
    <div className="overflow-x-auto" role="img" aria-label="Feature importance for Random Forest and XGBoost">
      <table className="w-full min-w-[560px] text-sm">
        <thead>
          <tr className="text-left text-xs uppercase tracking-wide text-text-muted">
            <th className="py-2 pr-3">Feature</th>
            <th className="py-2 pr-3">Random Forest (Gini)</th>
            <th className="py-2">XGBoost (normalised gain)</th>
          </tr>
        </thead>
        <tbody>
          {names.map((n) => (
            <tr key={n} className="border-t border-border">
              <td className="py-1.5 pr-3 font-mono text-xs">{n}</td>
              <td className="py-1.5 pr-3">
                <div className="flex items-center gap-2">
                  <div className="h-3 rounded" style={{ width: `${(rf[n] / maxRf) * 70}%`, background: palette[0] }} />
                  <span className="font-mono text-xs">{rf[n].toFixed(4)}</span>
                </div>
              </td>
              <td className="py-1.5">
                <div className="flex items-center gap-2">
                  <div className="h-3 rounded" style={{ width: `${(xgb[n] / maxX) * 70}%`, background: palette[1] }} />
                  <span className="font-mono text-xs">{xgb[n].toFixed(4)}</span>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <p className="mt-2 text-xs text-text-muted">
        Source: saved vertical models (trained on Set A only). Each model&apos;s importances sum to 1; scales differ between
        models. <code>sta_lta_*</code> features use STA 0.5 s (Set A) vs 1.0 s (Set C); numerical impact unverified.
      </p>
    </div>
  );
}

export function PerEventTable({ rows }: { rows: PerEventRow[] }) {
  return (
    <div className="overflow-x-auto rounded-xl border border-border">
      <table className="w-full min-w-[640px] text-sm">
        <thead className="bg-surface text-left text-xs uppercase tracking-wide text-text-muted">
          <tr>
            <th className="px-3 py-2">Event</th>
            <th className="px-3 py-2">Mag.</th>
            <th className="px-3 py-2">Windows</th>
            <th className="px-3 py-2">RF recall</th>
            <th className="px-3 py-2">XGB recall</th>
            <th className="px-3 py-2">STA/LTA recall</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.id} className="border-t border-border">
              <td className="px-3 py-1.5 font-mono text-xs">{r.id}</td>
              <td className="px-3 py-1.5">{r.magnitude?.toFixed(2) ?? "-"}</td>
              <td className="px-3 py-1.5">{r.samples ?? "-"}</td>
              <td className="px-3 py-1.5">{r.rfRecall.toFixed(3)}</td>
              <td className="px-3 py-1.5">{r.xgbRecall.toFixed(3)}</td>
              <td className="px-3 py-1.5">{r.staRecall?.toFixed(3) ?? "-"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
