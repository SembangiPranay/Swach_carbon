import type { CSSProperties, ReactNode } from 'react';
import { useState, useEffect } from 'react';
import { useNavigate, useOutletContext } from 'react-router';
import { motion } from 'motion/react';
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer,
} from 'recharts';
import {
  Download,
  RotateCcw,
  ChevronDown,
  ChevronUp,
  Building2,
  Zap,
  Globe,
  TrendingDown,
  Target,
  BarChart2,
} from 'lucide-react';
import { AppContextType, T } from './Root';

// ─── Design helpers ──────────────────────────────────────────────────────────

const card: CSSProperties = {
  background: T.bgCard,
  border: `1px solid ${T.borderCard}`,
  borderRadius: T.radius,
  boxShadow: T.shadowCard,
};

const sectionLabel: CSSProperties = {
  fontSize: '11px',
  fontWeight: 500,
  textTransform: 'uppercase',
  letterSpacing: '0.08em',
  color: T.meta,
  margin: '0 0 4px',
};

// Bloomberg / Stripe-style monumental KPI value
const kpiValue: CSSProperties = {
  fontSize: '40px',
  fontWeight: 800,
  color: T.heading,
  lineHeight: 1,
  letterSpacing: '-0.03em',
  fontVariantNumeric: 'tabular-nums',
  margin: '6px 0 8px',
};

// Numeric display style for secondary values
const numericDisplay: CSSProperties = {
  fontVariantNumeric: 'tabular-nums',
  letterSpacing: '-0.02em',
};

function Badge({
  text,
  bg,
  color,
  border,
}: {
  text: string;
  bg: string;
  color: string;
  border?: string;
}) {
  return (
    <span
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        background: bg,
        color,
        fontSize: '11px',
        fontWeight: 500,
        padding: '2px 8px',
        borderRadius: '999px',
        letterSpacing: '0.01em',
        border: border ? `1px solid ${border}` : 'none',
      }}
    >
      {text}
    </span>
  );
}

// ─── Custom chart elements ────────────────────────────────────────────────────

const SCOPE_COLORS = [T.scope1, T.scope2, T.scope3];

/** Inline % label inside each pie arc */
const PieArcLabel = ({
  cx, cy, midAngle, innerRadius, outerRadius, percent,
}: any) => {
  if (percent < 0.06) return null;
  const RAD = Math.PI / 180;
  const r = innerRadius + (outerRadius - innerRadius) * 0.5;
  const x = cx + r * Math.cos(-midAngle * RAD);
  const y = cy + r * Math.sin(-midAngle * RAD);
  return (
    <text
      x={x}
      y={y}
      fill="white"
      textAnchor="middle"
      dominantBaseline="central"
      fontSize={11}
      fontWeight={700}
      fontFamily="'Inter', system-ui, sans-serif"
    >
      {`${(percent * 100).toFixed(0)}%`}
    </text>
  );
};

const ChartTooltip = ({ active, payload, label }: any) => {
  if (!active || !payload?.length) return null;
  return (
    <div
      style={{
        background: 'white',
        border: `1px solid ${T.borderCard}`,
        borderRadius: '6px',
        padding: '10px 14px',
        boxShadow: T.shadowMd,
        fontSize: '13px',
      }}
    >
      {label && (
        <p style={{ fontWeight: 600, color: T.heading, margin: '0 0 5px' }}>{label}</p>
      )}
      {payload.map((p: any, i: number) => (
        <p key={i} style={{ color: T.body, margin: '2px 0', ...numericDisplay }}>
          {p.name !== 'tCO2e' ? `${p.name}: ` : ''}
          <strong>{Number(p.value).toFixed(0).replace(/\B(?=(\d{3})+(?!\d))/g, ',')}</strong> tCO2e
          {p.payload?.pct && (
            <span style={{ color: T.meta, marginLeft: '6px', fontSize: '12px' }}>
              {p.payload.pct}%
            </span>
          )}
        </p>
      ))}
    </div>
  );
};

// ─── Section wrapper ──────────────────────────────────────────────────────────

function Section({
  title,
  subtitle,
  children,
  delay = 0,
}: {
  title: string;
  subtitle?: string;
  children: ReactNode;
  delay?: number;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: 'easeOut', delay }}
    >
      {(title || subtitle) && (
        <div style={{ marginBottom: '12px' }}>
          <h2
            style={{
              fontSize: '14px',
              fontWeight: 600,
              color: T.heading,
              margin: 0,
              letterSpacing: '-0.1px',
            }}
          >
            {title}
          </h2>
          {subtitle && (
            <p
              style={{
                fontSize: '13px',
                color: T.meta,
                margin: '2px 0 0',
                letterSpacing: '0.01em',
              }}
            >
              {subtitle}
            </p>
          )}
        </div>
      )}
      {children}
    </motion.div>
  );
}

// ─── Main component ───────────────────────────────────────────────────────────

export function ResultsDashboard() {
  const navigate = useNavigate();
  const { formData, results } = useOutletContext<AppContextType>();
  const [showInfo, setShowInfo] = useState(false);
  const [downloading, setDownloading] = useState(false);

  useEffect(() => {
    if (!formData || !results) navigate('/');
  }, []);

  if (!formData || !results) return null;

  const { scope1, scope2, scope3, total, benchmark, reductionPotential, afterReduction, percentBenchmark } = results;

  const s1Pct = ((scope1 / total) * 100).toFixed(1);
  const s2Pct = ((scope2 / total) * 100).toFixed(1);
  const s3Pct = ((scope3 / total) * 100).toFixed(1);
  const redPct = ((reductionPotential / total) * 100).toFixed(1);
  const isBelowBenchmark = percentBenchmark < 100;
  const benchmarkDiff = Math.abs(100 - percentBenchmark).toFixed(1);

  const fmt = (n: number) => n.toFixed(0).replace(/\B(?=(\d{3})+(?!\d))/g, ',');

  const pieData = [
    { name: 'Scope 1 — Direct', value: scope1, pct: s1Pct },
    { name: 'Scope 2 — Electricity', value: scope2, pct: s2Pct },
    { name: 'Scope 3 — Value Chain', value: scope3, pct: s3Pct },
  ];

  const comparisonData = [
    {
      name: formData.companyName.length > 14 ? formData.companyName.slice(0, 14) + '…' : formData.companyName,
      value: Math.round(total),
    },
    { name: `${formData.industry} avg`, value: Math.round(benchmark) },
  ];
  const comparisonColors = [T.primary, '#D1FAE5'];
  const comparisonBorders = [T.primary, '#6EE7B7'];

  const roadmapData = [
    { name: 'Current', value: Math.round(total) },
    { name: 'After Reduction', value: Math.round(afterReduction) },
  ];
  const roadmapColors = [T.primary, '#A7F3D0'];

  // Standardised badge system
  const ACTION_BADGES: Record<string, { bg: string; color: string; border: string }> = {
    'High Impact': { bg: '#FEF3C7', color: '#92400E', border: '#FDE68A' },
    'Quick Win':   { bg: '#D1FAE5', color: '#065F46', border: '#A7F3D0' },
    'Cost Saving': { bg: '#DBEAFE', color: '#1E40AF', border: '#BFDBFE' },
    'Long-term':   { bg: '#F3F4F6', color: '#374151', border: '#E5E7EB' },
    'Compliance':  { bg: '#F3F4F6', color: '#374151', border: '#E5E7EB' },
    'Scope 3':     { bg: '#EDE9FE', color: '#5B21B6', border: '#DDD6FE' },
  };

  const handleDownload = () => {
    setDownloading(true);
    setTimeout(() => {
      const lines = [
        '══════════════════════════════════════════════',
        '       SWACH AI  —  CARBON FOOTPRINT REPORT   ',
        '══════════════════════════════════════════════',
        `Generated  : ${new Date().toLocaleString()}`,
        `Report ID  : ${results.calculationId}`,
        '',
        '──────────────────────────────────────────────',
        'COMPANY',
        '──────────────────────────────────────────────',
        `Name       : ${formData.companyName}`,
        `Sector     : ${formData.industry}`,
        `Headcount  : ${formData.employeeCount.toLocaleString()} FTE`,
        '',
        '──────────────────────────────────────────────',
        'RESULTS (tCO2e / year)',
        '──────────────────────────────────────────────',
        `Scope 1 Direct       : ${scope1.toFixed(1)} tCO2e  (${s1Pct}%)`,
        `Scope 2 Electricity  : ${scope2.toFixed(1)} tCO2e  (${s2Pct}%)`,
        `Scope 3 Value Chain  : ${scope3.toFixed(1)} tCO2e  (${s3Pct}%)`,
        `TOTAL                : ${total.toFixed(1)} tCO2e`,
        '',
        '──────────────────────────────────────────────',
        'BENCHMARK',
        '──────────────────────────────────────────────',
        `${formData.industry} sector avg  : ${benchmark.toFixed(0)} tCO2e`,
        `Performance          : ${isBelowBenchmark ? `${benchmarkDiff}% BELOW avg ✓` : `${benchmarkDiff}% ABOVE avg ⚠`}`,
        '',
        '──────────────────────────────────────────────',
        'REDUCTION PATHWAY',
        '──────────────────────────────────────────────',
        `Reduction potential : ${reductionPotential.toFixed(0)} tCO2e  (${redPct}%)`,
        `After reduction     : ${afterReduction.toFixed(0)} tCO2e`,
        '',
        '══════════════════════════════════════════════',
        'Swach AI  |  GHG Protocol + India CEA 2022–23',
        '══════════════════════════════════════════════',
      ];
      const blob = new Blob([lines.join('\n')], { type: 'text/plain;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${formData.companyName.replace(/\s+/g, '_')}_Carbon_Report.txt`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      setDownloading(false);
    }, 500);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35 }}
      style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}
    >
      {/* ── Page header ──────────────────────────────────────────────── */}
      <div>
        <div
          style={{
            display: 'flex',
            alignItems: 'flex-start',
            justifyContent: 'space-between',
            flexWrap: 'wrap',
            gap: '12px',
          }}
        >
          <div>
            <h1
              style={{
                fontSize: '20px',
                fontWeight: 700,
                color: T.heading,
                margin: '0 0 4px',
                letterSpacing: '-0.3px',
              }}
            >
              Emissions Report
            </h1>
            <p
              style={{
                fontSize: '13px',
                color: T.meta,
                margin: 0,
                letterSpacing: '0.01em',
              }}
            >
              {formData.companyName} · {formData.industry} · {formData.employeeCount.toLocaleString()} FTE
            </p>
          </div>
          {/* Report ID — JetBrains Mono, premium signal */}
          <span
            style={{
              fontFamily: T.mono,
              fontSize: '11px',
              letterSpacing: '0.05em',
              color: T.meta,
              background: '#F9FAFB',
              border: `1px solid ${T.border}`,
              borderRadius: '4px',
              padding: '4px 10px',
              fontVariantNumeric: 'tabular-nums',
            }}
          >
            {results.calculationId}
          </span>
        </div>
      </div>

      {/* ── Primary KPI row ───────────────────────────────────────────── */}
      <Section title="Summary" delay={0.05}>
        <div
          style={{
            ...card,
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
            overflow: 'hidden',
          }}
        >
          {[
            {
              icon: BarChart2,
              label: 'Total Emissions',
              value: fmt(total),
              unit: 'tCO2e / year',
              badge: null as null | { text: string; bg: string; color: string; border: string },
            },
            {
              icon: Target,
              label: 'vs Industry Benchmark',
              value: `${percentBenchmark.toFixed(1)}%`,
              unit: `of ${formData.industry} sector avg`,
              badge: isBelowBenchmark
                ? { text: `↓ ${benchmarkDiff}% below avg`, bg: T.successBg, color: T.successText, border: T.successBorder }
                : { text: `↑ ${benchmarkDiff}% above avg`, bg: '#FEF3C7', color: '#92400E', border: '#FDE68A' },
            },
            {
              icon: TrendingDown,
              label: 'Reduction Potential',
              value: fmt(reductionPotential),
              unit: `tCO2e  ·  ${redPct}% achievable`,
              badge: { text: 'Actionable', bg: '#EDE9FE', color: '#5B21B6', border: '#DDD6FE' },
            },
          ].map((kpi, idx, arr) => {
            const Icon = kpi.icon;
            return (
              <div
                key={idx}
                style={{
                  padding: '22px 24px 20px',
                  borderRight: idx < arr.length - 1 ? `1px solid ${T.border}` : 'none',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '2px' }}>
                  <Icon size={13} color={T.meta} strokeWidth={1.5} />
                  <p style={sectionLabel}>{kpi.label}</p>
                </div>
                {/* Monumental number */}
                <p style={kpiValue}>
                  {kpi.value}
                </p>
                <p
                  style={{
                    fontSize: '12px',
                    color: T.body,
                    margin: '0 0 10px',
                    letterSpacing: '0.01em',
                  }}
                >
                  {kpi.unit}
                </p>
                {kpi.badge && (
                  <Badge
                    text={kpi.badge.text}
                    bg={kpi.badge.bg}
                    color={kpi.badge.color}
                    border={kpi.badge.border}
                  />
                )}
              </div>
            );
          })}
        </div>
      </Section>

      {/* ─�� Scope breakdown — 3 individual cards with colored top borders ── */}
      <Section title="Scope Breakdown" subtitle="GHG Protocol Scope 1, 2 & 3" delay={0.1}>
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(190px, 1fr))',
            gap: '12px',
          }}
        >
          {[
            {
              Icon: Building2,
              scopeLabel: 'SCOPE 1',
              value: scope1,
              pct: s1Pct,
              color: T.scope1,
              desc: 'Direct — Fuel combustion',
            },
            {
              Icon: Zap,
              scopeLabel: 'SCOPE 2',
              value: scope2,
              pct: s2Pct,
              color: T.scope2,
              desc: 'Indirect — Purchased electricity',
            },
            {
              Icon: Globe,
              scopeLabel: 'SCOPE 3',
              value: scope3,
              pct: s3Pct,
              color: T.scope3,
              desc: 'Value chain — Waste & travel',
            },
          ].map(({ Icon, scopeLabel, value, pct, color, desc }) => (
            <div
              key={scopeLabel}
              style={{
                ...card,
                borderTop: `3px solid ${color}`,
                padding: '18px 20px 16px',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '10px' }}>
                <Icon size={13} color={T.meta} strokeWidth={1.5} />
                <p style={sectionLabel}>{scopeLabel}</p>
              </div>
              <p
                style={{
                  fontSize: '26px',
                  fontWeight: 800,
                  color: T.heading,
                  margin: '0 0 2px',
                  letterSpacing: '-0.03em',
                  fontVariantNumeric: 'tabular-nums',
                  lineHeight: 1,
                }}
              >
                {fmt(value)}
              </p>
              <p style={{ fontSize: '11px', color: T.meta, margin: '0 0 12px', letterSpacing: '0.01em' }}>
                {desc}
              </p>
              {/* Progress bar — height 3px, border-radius 999px */}
              <div
                style={{
                  height: '3px',
                  background: T.border,
                  borderRadius: '999px',
                  overflow: 'hidden',
                }}
              >
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${pct}%` }}
                  transition={{ duration: 0.9, delay: 0.35, ease: 'easeOut' }}
                  style={{
                    height: '100%',
                    background: color,
                    borderRadius: '999px',
                  }}
                />
              </div>
              <p
                style={{
                  fontSize: '11px',
                  color: T.meta,
                  margin: '5px 0 0',
                  fontVariantNumeric: 'tabular-nums',
                }}
              >
                {pct}% of total
              </p>
            </div>
          ))}
        </div>
      </Section>

      {/* ── Charts row ───────────────────────────────────────────────── */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
          gap: '16px',
        }}
      >
        {/* Donut — inline arc % labels */}
        <Section title="Emission Sources" subtitle="Distribution by GHG Protocol scope" delay={0.15}>
          <div style={card}>
            <div style={{ padding: '18px 20px 0' }}>
              <p style={{ fontSize: '13px', fontWeight: 600, color: T.heading, margin: '0 0 1px' }}>
                Scope Breakdown
              </p>
              <p style={{ fontSize: '12px', color: T.meta, margin: 0, letterSpacing: '0.01em' }}>
                Annual emissions by category
              </p>
            </div>
            <ResponsiveContainer width="100%" height={220}>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={58}
                  outerRadius={90}
                  paddingAngle={2}
                  dataKey="value"
                  labelLine={false}
                  label={PieArcLabel}
                  animationBegin={200}
                  animationDuration={800}
                >
                  {pieData.map((_, i) => (
                    <Cell key={i} fill={SCOPE_COLORS[i]} />
                  ))}
                </Pie>
                <Tooltip content={<ChartTooltip />} />
              </PieChart>
            </ResponsiveContainer>
            {/* Legend */}
            <div style={{ padding: '0 20px 18px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {pieData.map((item, i) => (
                <div
                  key={i}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    paddingBottom: i < pieData.length - 1 ? '8px' : '0',
                    borderBottom: i < pieData.length - 1 ? `1px solid #F3F4F6` : 'none',
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <div
                      style={{
                        width: '8px',
                        height: '8px',
                        borderRadius: '2px',
                        background: SCOPE_COLORS[i],
                        flexShrink: 0,
                      }}
                    />
                    <span style={{ fontSize: '12px', color: T.body }}>{item.name}</span>
                  </div>
                  <span
                    style={{
                      fontSize: '12px',
                      fontWeight: 700,
                      color: T.heading,
                      fontVariantNumeric: 'tabular-nums',
                    }}
                  >
                    {fmt(item.value)} tCO2e
                  </span>
                </div>
              ))}
            </div>
          </div>
        </Section>

        {/* Bar — benchmark comparison */}
        <Section title="Benchmark Comparison" subtitle={`${formData.industry} sector peer group`} delay={0.2}>
          <div style={card}>
            <div style={{ padding: '18px 20px 0' }}>
              <p style={{ fontSize: '13px', fontWeight: 600, color: T.heading, margin: '0 0 1px' }}>
                Company vs. Industry Average
              </p>
              <p style={{ fontSize: '12px', color: T.meta, margin: 0, letterSpacing: '0.01em' }}>
                tCO2e per year
              </p>
            </div>
            <div style={{ padding: '8px 4px 16px' }}>
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={comparisonData} margin={{ top: 16, right: 20, left: 0, bottom: 4 }}>
                  <CartesianGrid
                    strokeDasharray="4 4"
                    stroke="#E5E7EB"
                    vertical={false}
                  />
                  <XAxis
                    dataKey="name"
                    tick={{ fontSize: 11, fill: T.meta }}
                    axisLine={false}
                    tickLine={false}
                  />
                  <YAxis
                    tick={{ fontSize: 10, fill: T.meta }}
                    axisLine={false}
                    tickLine={false}
                    tickFormatter={(v) => `${(v / 1000).toFixed(0)}K`}
                    width={36}
                  />
                  <Tooltip content={<ChartTooltip />} />
                  <Bar dataKey="value" radius={[4, 4, 0, 0]} animationDuration={700} name="tCO2e">
                    {comparisonData.map((_, i) => (
                      <Cell key={i} fill={comparisonColors[i]} stroke={comparisonBorders[i]} strokeWidth={1} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </Section>
      </div>

      {/* ── Reduction roadmap ─────────────────────────────────────────── */}
      <Section title="Reduction Roadmap" subtitle="Projected impact of key sustainability initiatives" delay={0.25}>
        <div style={{ ...card, padding: '22px 24px' }}>
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
              gap: '28px',
              alignItems: 'center',
            }}
          >
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={roadmapData} margin={{ top: 16, right: 20, left: 0, bottom: 4 }}>
                <CartesianGrid
                  strokeDasharray="4 4"
                  stroke="#E5E7EB"
                  vertical={false}
                />
                <XAxis
                  dataKey="name"
                  tick={{ fontSize: 11, fill: T.meta }}
                  axisLine={false}
                  tickLine={false}
                />
                <YAxis
                  tick={{ fontSize: 10, fill: T.meta }}
                  axisLine={false}
                  tickLine={false}
                  tickFormatter={(v) => `${(v / 1000).toFixed(0)}K`}
                  width={36}
                />
                <Tooltip content={<ChartTooltip />} />
                <Bar dataKey="value" radius={[4, 4, 0, 0]} animationDuration={700} name="tCO2e">
                  {roadmapData.map((_, i) => (
                    <Cell key={i} fill={roadmapColors[i]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>

            <div>
              <p style={sectionLabel}>POTENTIAL SAVINGS</p>
              <p
                style={{
                  fontSize: '40px',
                  fontWeight: 800,
                  color: T.primary,
                  margin: '6px 0 8px',
                  letterSpacing: '-0.03em',
                  fontVariantNumeric: 'tabular-nums',
                  lineHeight: 1,
                }}
              >
                −{fmt(reductionPotential)}
                <span
                  style={{
                    fontSize: '16px',
                    fontWeight: 400,
                    color: T.body,
                    marginLeft: '8px',
                  }}
                >
                  tCO2e
                </span>
              </p>
              <Badge
                text={`${redPct}% reduction achievable`}
                bg={T.successBg}
                color={T.successText}
                border={T.successBorder}
              />
              <div style={{ marginTop: '20px', display: 'flex', flexDirection: 'column', gap: '1px' }}>
                {[
                  { label: 'Current baseline', value: total, color: T.heading },
                  { label: 'After reduction', value: afterReduction, color: T.primary },
                  { label: 'Savings', value: reductionPotential, color: T.successText },
                ].map((row, ri, arr) => (
                  <div
                    key={row.label}
                    style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      padding: '9px 12px',
                      background: '#F9FAFB',
                      borderRadius: ri === 0 ? '5px 5px 0 0' : ri === arr.length - 1 ? '0 0 5px 5px' : '0',
                      borderBottom: ri < arr.length - 1 ? `1px solid #F3F4F6` : 'none',
                    }}
                  >
                    <span style={{ fontSize: '12px', color: T.body }}>{row.label}</span>
                    <span
                      style={{
                        fontSize: '13px',
                        fontWeight: 700,
                        color: row.color,
                        fontVariantNumeric: 'tabular-nums',
                        letterSpacing: '-0.02em',
                      }}
                    >
                      {fmt(row.value)} tCO2e
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </Section>

      {/* ── Recommended actions ───────────────────────────────────────── */}
      <Section title="Recommended Actions" subtitle="Prioritised carbon reduction strategies for your sector" delay={0.3}>
        <div style={card}>
          {[
            {
              title: 'Renewable Energy Transition',
              desc: 'Switch to solar/wind via Power Purchase Agreements (PPAs) — directly eliminates Scope 2 emissions.',
              tag: 'High Impact',
              scope: 'Scope 2',
            },
            {
              title: 'Energy Efficiency Audit & LED Retrofit',
              desc: 'Building and equipment efficiency upgrades typically deliver 15–25% electricity savings with sub-3yr payback.',
              tag: 'Cost Saving',
              scope: 'Scope 2',
            },
            {
              title: 'Green Fleet Transition',
              desc: 'Replace diesel/petrol fleet with EV or CNG vehicles. High priority for manufacturing and logistics.',
              tag: 'Quick Win',
              scope: 'Scope 1',
            },
            {
              title: 'Waste Diversion & Circular Economy',
              desc: 'Divert waste from landfill through recycling programmes. Engage supply chain on packaging reduction.',
              tag: 'Scope 3',
              scope: 'Scope 3',
            },
            {
              title: 'Verified Carbon Offsets',
              desc: 'Purchase Gold Standard or Verra-verified offsets to address residual emissions while implementing reductions.',
              tag: 'Compliance',
              scope: 'All Scopes',
            },
            {
              title: 'Reforestation & Afforestation (India)',
              desc: 'Invest in verified reforestation in India. Supports biodiversity and CCTS compliance from 2026.',
              tag: 'Long-term',
              scope: 'Net Zero',
            },
          ].map((item, idx, arr) => {
            const badge = ACTION_BADGES[item.tag] ?? ACTION_BADGES['Compliance'];
            return (
              <div
                key={idx}
                style={{
                  display: 'flex',
                  alignItems: 'flex-start',
                  borderBottom: idx < arr.length - 1 ? `1px solid #F3F4F6` : 'none',
                }}
              >
                {/* Left accent line */}
                <div
                  style={{
                    width: '3px',
                    alignSelf: 'stretch',
                    background: T.primary,
                    flexShrink: 0,
                    borderRadius:
                      idx === 0 ? '8px 0 0 0' : idx === arr.length - 1 ? '0 0 0 8px' : '0',
                    opacity: 0.6 + idx * 0.04,
                  }}
                />
                <div
                  style={{
                    flex: 1,
                    padding: '14px 18px',
                    display: 'flex',
                    alignItems: 'flex-start',
                    justifyContent: 'space-between',
                    gap: '12px',
                    flexWrap: 'wrap',
                  }}
                >
                  <div style={{ flex: 1, minWidth: '200px' }}>
                    <p
                      style={{
                        fontSize: '13px',
                        fontWeight: 600,
                        color: T.heading,
                        margin: '0 0 3px',
                      }}
                    >
                      {item.title}
                    </p>
                    <p
                      style={{
                        fontSize: '12px',
                        color: T.body,
                        margin: 0,
                        lineHeight: 1.6,
                      }}
                    >
                      {item.desc}
                    </p>
                  </div>
                  <div
                    style={{
                      display: 'flex',
                      gap: '6px',
                      flexShrink: 0,
                      alignItems: 'flex-start',
                      paddingTop: '1px',
                    }}
                  >
                    <Badge
                      text={item.tag}
                      bg={badge.bg}
                      color={badge.color}
                      border={badge.border}
                    />
                    <span
                      style={{
                        background: '#F3F4F6',
                        color: T.meta,
                        fontSize: '10px',
                        fontWeight: 500,
                        padding: '2px 7px',
                        borderRadius: '999px',
                        border: `1px solid ${T.border}`,
                        whiteSpace: 'nowrap' as const,
                      }}
                    >
                      {item.scope}
                    </span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </Section>

      {/* ── Methodology (collapsible) ─────────────────────────────────── */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.35 }}
        style={{
          border: `1px solid ${T.borderCard}`,
          borderRadius: T.radius,
          overflow: 'hidden',
          background: T.bgCard,
          boxShadow: T.shadowCard,
        }}
      >
        <button
          onClick={() => setShowInfo(!showInfo)}
          style={{
            width: '100%',
            padding: '13px 18px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            background: 'transparent',
            border: 'none',
            cursor: 'pointer',
            fontFamily: 'inherit',
          }}
        >
          <span style={{ fontSize: '13px', fontWeight: 500, color: T.body }}>
            Methodology & Disclosure
          </span>
          {showInfo
            ? <ChevronUp size={14} color={T.meta} />
            : <ChevronDown size={14} color={T.meta} />}
        </button>
        {showInfo && (
          <div style={{ padding: '0 18px 16px', borderTop: `1px solid #F3F4F6` }}>
            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
                gap: '10px',
                marginTop: '14px',
              }}
            >
              {[
                { scope: 'Scope 1', color: T.scope1, text: 'Direct GHG emissions from sources owned or controlled by the organisation — fuel combustion in boilers, furnaces, vehicles.' },
                { scope: 'Scope 2', color: T.scope2, text: 'Indirect GHG from purchased electricity. Calculated using India CEA grid factor: 0.82 kgCO2e/kWh (2022–23).' },
                { scope: 'Scope 3', color: T.scope3, text: 'All other indirect emissions — business travel, waste disposal, water consumption, upstream/downstream activities.' },
              ].map((item) => (
                <div
                  key={item.scope}
                  style={{
                    padding: '12px',
                    background: '#F9FAFB',
                    borderRadius: '5px',
                    borderLeft: `3px solid ${item.color}`,
                  }}
                >
                  <p style={{ fontSize: '12px', fontWeight: 700, color: item.color, margin: '0 0 4px' }}>
                    {item.scope}
                  </p>
                  <p style={{ fontSize: '12px', color: T.body, margin: 0, lineHeight: 1.55 }}>
                    {item.text}
                  </p>
                </div>
              ))}
            </div>
            <p style={{ fontSize: '11px', color: T.meta, margin: '14px 0 0', lineHeight: 1.6 }}>
              Emission factors: IPCC AR6, India CEA 2022–23, GHG Protocol Corporate Standard.
              Benchmarks: India CCTS sector intensity data. All figures in metric tonnes CO2 equivalent (tCO2e).
              This report is for internal sustainability reporting and does not constitute third-party verification.
            </p>
          </div>
        )}
      </motion.div>

      {/* ── Footer actions ────────────────────────────────────────────── */}
      <div
        style={{
          display: 'flex',
          gap: '10px',
          justifyContent: 'flex-end',
          flexWrap: 'wrap',
          paddingBottom: '8px',
        }}
      >
        <button
          onClick={() => navigate('/')}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            height: '38px',
            padding: '0 16px',
            background: T.bgCard,
            border: `1px solid ${T.borderInput}`,
            borderRadius: T.radiusSm,
            fontSize: '13px',
            fontWeight: 500,
            color: T.body,
            cursor: 'pointer',
            fontFamily: 'inherit',
            transition: 'border-color 0.15s ease',
          }}
          onMouseEnter={(e) => { (e.currentTarget as HTMLButtonElement).style.borderColor = T.primary; }}
          onMouseLeave={(e) => { (e.currentTarget as HTMLButtonElement).style.borderColor = T.borderInput; }}
        >
          <RotateCcw size={13} />
          New Calculation
        </button>
        <button
          onClick={handleDownload}
          disabled={downloading}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '7px',
            height: '38px',
            padding: '0 18px',
            background: downloading ? '#5a9080' : T.primary,
            border: 'none',
            borderRadius: T.radiusSm,
            fontSize: '13px',
            fontWeight: 600,
            color: 'white',
            cursor: downloading ? 'wait' : 'pointer',
            fontFamily: 'inherit',
            transition: 'background 0.15s ease',
          }}
          onMouseEnter={(e) => { if (!downloading) (e.currentTarget as HTMLButtonElement).style.background = T.primaryHover; }}
          onMouseLeave={(e) => { if (!downloading) (e.currentTarget as HTMLButtonElement).style.background = T.primary; }}
        >
          <Download size={13} />
          {downloading ? 'Preparing…' : 'Export Report'}
        </button>
      </div>
    </motion.div>
  );
}
