import { useState } from 'react';
import { Outlet } from 'react-router';

export interface FormData {
  companyName: string;
  industry: string;
  employeeCount: number;
  electricity: number;
  diesel: number;
  petrol: number;
  naturalGas: number;
  lpg: number;
  coal: number;
  water: number;
  waste: number;
  businessTravel: number;
}

export interface EmissionResults {
  scope1: number;
  scope2: number;
  scope3: number;
  total: number;
  benchmark: number;
  reductionPotential: number;
  afterReduction: number;
  percentBenchmark: number;
  calculationId: string;
}

export interface AppContextType {
  formData: FormData | null;
  setFormData: (data: FormData) => void;
  results: EmissionResults | null;
  setResults: (results: EmissionResults) => void;
}

export function calculateResults(data: FormData): EmissionResults {
  const scope1 =
    (data.diesel * 2.68) / 1000 +
    (data.petrol * 2.31) / 1000 +
    (data.naturalGas * 56.1) / 1000 +
    (data.lpg * 1.51) / 1000 +
    data.coal * 2.42;

  const scope2 = (data.electricity * 0.82) / 1000;

  const scope3 =
    data.waste * 0.467 +
    data.water * 0.000344 +
    data.businessTravel * 0.00021;

  const baselineScope1 = Math.max(scope1, 50 + data.employeeCount * 0.05);
  const baselineScope2 = Math.max(scope2, 100 + data.employeeCount * 0.1);
  const baselineScope3 = Math.max(scope3, 20 + data.employeeCount * 0.02);

  const total = baselineScope1 + baselineScope2 + baselineScope3;

  const benchmarkRates: Record<string, number> = {
    Technology: 15,
    Manufacturing: 45,
    Retail: 20,
    Healthcare: 25,
    Finance: 12,
    Energy: 60,
    Transportation: 40,
    Agriculture: 35,
    Construction: 38,
    Education: 10,
    Other: 25,
  };
  const rate = benchmarkRates[data.industry] ?? 25;
  const benchmark = rate * data.employeeCount;
  const reductionPotential = total * 0.216;
  const afterReduction = total - reductionPotential;
  const percentBenchmark = benchmark > 0 ? (total / benchmark) * 100 : 100;

  const calculationId = `SWACH-${Date.now().toString(36).toUpperCase()}-${Math.random()
    .toString(36)
    .substring(2, 6)
    .toUpperCase()}`;

  return {
    scope1: baselineScope1,
    scope2: baselineScope2,
    scope3: baselineScope3,
    total,
    benchmark,
    reductionPotential,
    afterReduction,
    percentBenchmark,
    calculationId,
  };
}

// ─── Design Tokens ───────────────────────────────────────────────────────────
export const T = {
  primary: '#0D4F3C',
  primaryHover: '#0A4034',
  primaryLight: '#F0FAF5',
  heading: '#1A1A2E',
  body: '#4B5563',
  meta: '#9CA3AF',
  border: '#E5E7EB',
  borderInput: '#D1D5DB',
  borderCard: 'rgba(0,0,0,0.07)',
  bgPage: '#F5F4F1',
  bgCard: '#ffffff',
  successBg: '#DCFCE7',
  successText: '#15803D',
  successBorder: '#A7F3D0',
  scope1: '#DC2626',
  scope2: '#2563EB',
  scope3: '#7C3AED',
  shadowCard: '0 1px 2px rgba(0,0,0,0.05), 0 4px 16px rgba(0,0,0,0.04)',
  shadowMd: '0 4px 12px rgba(0,0,0,0.1)',
  radius: '8px',
  radiusSm: '6px',
  mono: "'JetBrains Mono', 'SF Mono', 'Fira Code', monospace",
};

export default function Root() {
  const [formData, setFormData] = useState<FormData | null>(null);
  const [results, setResults] = useState<EmissionResults | null>(null);

  return (
    <div
      style={{
        minHeight: '100vh',
        background: T.bgPage,
        fontFamily: "'Inter', system-ui, -apple-system, sans-serif",
      }}
    >
      {/* ── Header ──────────────────────────────────────────────────────── */}
      <header
        style={{
          background: T.primary,
          borderBottom: '1px solid rgba(255,255,255,0.1)',
        }}
      >
        <div
          style={{
            maxWidth: '960px',
            margin: '0 auto',
            padding: '0 1.5rem',
            height: '56px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
          }}
        >
          {/* Logo group */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <svg
              width="20"
              height="20"
              viewBox="0 0 20 20"
              fill="none"
              aria-hidden="true"
            >
              <path
                d="M10 2C6.13 2 3 5.13 3 9c0 2.61 1.41 4.89 3.5 6.17V17h7v-1.83C15.59 13.89 17 11.61 17 9c0-3.87-3.13-7-7-7z"
                fill="rgba(255,255,255,0.25)"
              />
              <path
                d="M10 4C7.24 4 5 6.24 5 9c0 1.85.99 3.46 2.46 4.35l.54.31V15h4v-1.34l.54-.31A4.97 4.97 0 0015 9c0-2.76-2.24-5-5-5z"
                fill="rgba(255,255,255,0.5)"
              />
              <circle cx="10" cy="9" r="2" fill="white" />
            </svg>
            <span
              style={{
                color: 'white',
                fontSize: '15px',
                fontWeight: 600,
                letterSpacing: '-0.2px',
              }}
            >
              Swach AI
            </span>
            <span
              style={{
                color: 'rgba(255,255,255,0.4)',
                fontSize: '14px',
                fontWeight: 400,
                margin: '0 2px',
              }}
            >
              /
            </span>
            <span
              style={{
                color: 'rgba(255,255,255,0.65)',
                fontSize: '13px',
                fontWeight: 400,
              }}
            >
              Carbon Management
            </span>
          </div>

          {/* Right tag */}
          <div
            style={{
              background: 'transparent',
              border: '1px solid rgba(255,255,255,0.3)',
              borderRadius: '4px',
              padding: '3px 10px',
              fontSize: '11px',
              fontWeight: 500,
              color: 'white',
              letterSpacing: '0.08em',
              textTransform: 'uppercase' as const,
            }}
          >
            Enterprise
          </div>
        </div>
      </header>

      {/* ── Page Content ────────────────────────────────────────────────── */}
      <main
        style={{
          maxWidth: '960px',
          margin: '0 auto',
          padding: '2rem 1.5rem 3rem',
        }}
      >
        <Outlet
          context={
            { formData, setFormData, results, setResults } as AppContextType
          }
        />
      </main>
    </div>
  );
}