import { useState, useEffect, useRef } from 'react';
import { useNavigate, useOutletContext } from 'react-router';
import { motion, AnimatePresence } from 'motion/react';
import {
  Brain,
  Zap,
  Eye,
  CheckCircle2,
  AlertCircle,
  ArrowRight,
  RotateCcw,
  Clock,
  Hash,
  Activity,
} from 'lucide-react';
import { AppContextType, FormData, EmissionResults, T, calculateResults } from './Root';

interface StreamEvent {
  id: number;
  type: 'thought' | 'action' | 'observation' | 'complete' | 'error';
  message: string;
  timestamp: string;
}

const EVENT_CONFIG: Record<StreamEvent['type'], {
  label: string;
  borderColor: string;
  bgColor: string;
  badgeBg: string;
  badgeText: string;
  icon: React.ElementType;
}> = {
  thought: {
    label: 'Reasoning',
    borderColor: '#4F46E5',
    bgColor: '#FAFAFA',
    badgeBg: '#EEF2FF',
    badgeText: '#4338CA',
    icon: Brain,
  },
  action: {
    label: 'Action',
    borderColor: '#D97706',
    bgColor: '#FAFAFA',
    badgeBg: '#FEF3C7',
    badgeText: '#92400E',
    icon: Zap,
  },
  observation: {
    label: 'Observation',
    borderColor: '#7C3AED',
    bgColor: '#FAFAFA',
    badgeBg: '#EDE9FE',
    badgeText: '#5B21B6',
    icon: Eye,
  },
  complete: {
    label: 'Complete',
    borderColor: T.primary,
    bgColor: '#F0FAF5',
    badgeBg: T.successBg,
    badgeText: T.successText,
    icon: CheckCircle2,
  },
  error: {
    label: 'Error',
    borderColor: '#DC2626',
    bgColor: '#FFF8F8',
    badgeBg: '#FEE2E2',
    badgeText: '#991B1B',
    icon: AlertCircle,
  },
};

const EVENT_DELAYS = [600, 1100, 1400, 800, 1300, 1600, 900, 1200, 1500, 800, 1300, 1600, 700, 1200, 1500, 1000];

function generateStreamEvents(fd: FormData, r: EmissionResults): Omit<StreamEvent, 'timestamp'>[] {
  const s1Pct = ((r.scope1 / r.total) * 100).toFixed(1);
  const s2Pct = ((r.scope2 / r.total) * 100).toFixed(1);
  const s3Pct = ((r.scope3 / r.total) * 100).toFixed(1);
  const diff = r.percentBenchmark > 100
    ? `${(r.percentBenchmark - 100).toFixed(1)}% above`
    : `${(100 - r.percentBenchmark).toFixed(1)}% below`;
  const redPct = ((r.reductionPotential / r.total) * 100).toFixed(1);

  return [
    { id: 1, type: 'thought', message: `Initialising emissions analysis for "${fd.companyName}" (${fd.industry}, ${fd.employeeCount.toLocaleString()} FTE). Loading IPCC AR6 emission factor database and India CEA 2022–23 grid coefficients...` },
    { id: 2, type: 'action', message: `Connecting to ${fd.industry} sector benchmark registry. Retrieving India-specific intensity data for ${fd.employeeCount.toLocaleString()}-person organisations...` },
    { id: 3, type: 'observation', message: `Emission factors confirmed — Grid (India): 0.82 kgCO2e/kWh · Diesel: 2.68 kg/L · Petrol: 2.31 kg/L · Natural Gas: 56.1 kg/MMBtu · LPG: 1.51 kg/kg` },
    { id: 4, type: 'thought', message: `Calculating Scope 1 direct emissions. Processing stationary combustion (diesel, petrol, natural gas, LPG, coal) and mobile combustion sources...` },
    { id: 5, type: 'action', message: `Scope 1 computation: Diesel(${fd.diesel.toLocaleString()}L)×2.68 + Petrol(${fd.petrol.toLocaleString()}L)×2.31 + NatGas(${fd.naturalGas} MMBtu)×56.1 + LPG(${fd.lpg}kg)×1.51 + Coal(${fd.coal}T)×2420` },
    { id: 6, type: 'observation', message: `Scope 1 Direct Emissions: ${r.scope1.toFixed(1)} tCO2e (${s1Pct}% of total footprint). Stationary combustion is the primary Scope 1 driver.` },
    { id: 7, type: 'thought', message: `Calculating Scope 2 purchased electricity emissions. India's grid is 60%+ coal-dependent, resulting in a high emission intensity of 0.82 kgCO2e/kWh...` },
    { id: 8, type: 'action', message: `Scope 2 computation: ${fd.electricity.toLocaleString()} kWh × 0.82 kgCO2e/kWh (India CEA 2022–23) → converting to metric tCO2e...` },
    { id: 9, type: 'observation', message: `Scope 2 Indirect Emissions: ${r.scope2.toFixed(1)} tCO2e (${s2Pct}% of total). Purchased electricity typically dominates Scope 2 for Indian enterprises.` },
    { id: 10, type: 'thought', message: `Processing Scope 3 value chain emissions — waste to landfill, water treatment, and employee business travel (air + road combined across all staff)...` },
    { id: 11, type: 'action', message: `Scope 3 computation: Waste(${fd.waste}T)×0.467 + Water(${fd.water.toLocaleString()}m³)×0.000344 + Travel(${fd.businessTravel.toLocaleString()}km)×0.00021` },
    { id: 12, type: 'observation', message: `Scope 3 Value Chain Emissions: ${r.scope3.toFixed(1)} tCO2e (${s3Pct}% of total). Covers downstream waste, water consumption, and business travel.` },
    { id: 13, type: 'thought', message: `Running benchmark comparison against ${fd.industry} sector. Applying India-specific emission intensity data for ${fd.employeeCount.toLocaleString()}-employee peer group...` },
    { id: 14, type: 'action', message: `${fd.industry} sector benchmark retrieved: ${r.benchmark.toFixed(0)} tCO2e (${fd.employeeCount.toLocaleString()} employees). Identifying primary reduction pathways...` },
    { id: 15, type: 'observation', message: `Benchmark result: ${fd.companyName} is ${diff} the ${fd.industry} sector average (${r.benchmark.toFixed(0)} tCO2e). Reduction potential identified: ${r.reductionPotential.toFixed(0)} tCO2e (${redPct}%).` },
    { id: 16, type: 'complete', message: `Analysis finalised. Total footprint for ${fd.companyName}: ${r.total.toFixed(0)} tCO2e/year — Scope 1: ${r.scope1.toFixed(0)} · Scope 2: ${r.scope2.toFixed(0)} · Scope 3: ${r.scope3.toFixed(0)} tCO2e. Full report ready.` },
  ];
}

// ─── Event Card ──────────────────────────────────────────────────────────────

function EventCard({ event, isLast }: { event: StreamEvent; isLast: boolean }) {
  const cfg = EVENT_CONFIG[event.type];
  const Icon = cfg.icon;

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, ease: 'easeOut' }}
      style={{ position: 'relative', marginLeft: '32px', marginBottom: isLast ? '4px' : '12px' }}
    >
      {/* Timeline line — 2px, #E5E7EB */}
      {!isLast && (
        <div
          style={{
            position: 'absolute',
            left: '-20px',
            top: '28px',
            width: '2px',
            height: 'calc(100% + 12px)',
            background: '#E5E7EB',
          }}
        />
      )}

      {/* Dot — 8px circle, 2px colored border, white fill */}
      <motion.div
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ duration: 0.2, ease: 'easeOut' }}
        style={{
          position: 'absolute',
          left: '-26px',
          top: '10px',
          width: '8px',
          height: '8px',
          borderRadius: '50%',
          background: 'white',
          border: `2px solid ${cfg.borderColor}`,
          zIndex: 2,
        }}
      />

      {/* Card — 3px left border matching type color */}
      <div
        style={{
          background: cfg.bgColor,
          border: `1px solid ${T.borderCard}`,
          borderLeft: `3px solid ${cfg.borderColor}`,
          borderRadius: '6px',
          padding: '12px 14px',
          boxShadow: '0 1px 2px rgba(0,0,0,0.04)',
        }}
      >
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: '7px',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <Icon size={12} color={cfg.borderColor} />
            <span
              style={{
                background: cfg.badgeBg,
                color: cfg.badgeText,
                padding: '2px 7px',
                borderRadius: '3px',
                fontSize: '10px',
                fontWeight: 600,
                letterSpacing: '0.05em',
                textTransform: 'uppercase' as const,
              }}
            >
              {cfg.label}
            </span>
          </div>
          <span
            style={{
              fontSize: '11px',
              color: T.meta,
              fontFamily: T.mono,
              fontVariantNumeric: 'tabular-nums',
            }}
          >
            #{event.id.toString().padStart(2, '0')} · {event.timestamp}
          </span>
        </div>
        <p
          style={{
            fontSize: '13px',
            lineHeight: 1.6,
            color: '#374151',
            margin: 0,
          }}
        >
          {event.message}
        </p>
      </div>
    </motion.div>
  );
}

// ─── Spinner ─────────────────────────────────────────────────────────────────

function AnalysisSpinner() {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', padding: '16px 0' }}>
      <div
        style={{
          width: '18px',
          height: '18px',
          border: `2px solid ${T.border}`,
          borderTopColor: T.primary,
          borderRadius: '50%',
          animation: 'spin 0.8s linear infinite',
          flexShrink: 0,
        }}
      />
      <span style={{ fontSize: '13px', color: T.meta }}>Connecting to analysis engine...</span>
    </div>
  );
}

// ─── Main Component ───────────────────────────────────────────────────────────

export function StreamingPanel() {
  const navigate = useNavigate();
  const { formData, setResults } = useOutletContext<AppContextType>();

  const [visibleEvents, setVisibleEvents] = useState<StreamEvent[]>([]);
  const [isComplete, setIsComplete] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [elapsed, setElapsed] = useState(0);
  const [error, setError] = useState<string | null>(null);

  const timelineRef = useRef<HTMLDivElement>(null);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const startRef = useRef(Date.now());
  const abortRef = useRef(new AbortController());

  useEffect(() => {
    if (!formData) { navigate('/'); return; }

    const calculationId = sessionStorage.getItem('calculationId');
    if (!calculationId) { navigate('/'); return; }

    startRef.current = Date.now();
    let eventId = 0;

    timerRef.current = setInterval(() => {
      setElapsed(Math.floor((Date.now() - startRef.current) / 1000));
    }, 1000);

    // Stream from backend
    (async () => {
      try {
        const { streamCalculationEvents } = await import('../services/api');
        setIsLoading(false);

        for await (const event of streamCalculationEvents(calculationId)) {
          const ts = new Date().toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
          });

          const streamEvent: StreamEvent = {
            id: ++eventId,
            type: (event.type as any) || 'observation',
            message: event.content,
            timestamp: ts,
          };

          setVisibleEvents((prev) => [...prev, streamEvent]);

          if (event.type === 'complete' || event.type === 'error') {
            setIsComplete(true);
            if (timerRef.current) clearInterval(timerRef.current);

            // Calculate and save results to context BEFORE navigation
            if (event.type === 'complete' && formData) {
              const results = calculateResults(formData);
              setResults(results);
            }
          }
        }
      } catch (err) {
        const errMsg = err instanceof Error ? err.message : 'Stream error';
        console.error('Stream error:', err);
        setError(errMsg);
        setIsComplete(true);
        if (timerRef.current) clearInterval(timerRef.current);
      }
    })();

    return () => {
      abortRef.current.abort();
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [formData, navigate, setResults]);

  useEffect(() => {
    if (timelineRef.current) {
      timelineRef.current.scrollTo({ top: timelineRef.current.scrollHeight, behavior: 'smooth' });
    }
  }, [visibleEvents]);

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35, ease: 'easeOut' }}
    >
      {/* Page title */}
      <div style={{ marginBottom: '20px' }}>
        <h1 style={{ fontSize: '20px', fontWeight: 700, color: T.heading, margin: '0 0 4px', letterSpacing: '-0.3px' }}>
          AI Emissions Analysis
        </h1>
        <p style={{ fontSize: '14px', color: T.body, margin: 0 }}>
          Real-time agent reasoning — GHG Protocol Scope 1, 2 &amp; 3
        </p>
      </div>

      {error && (
        <div style={{
          background: '#FEE2E2',
          border: '1px solid #FCA5A5',
          borderRadius: T.radiusSm,
          padding: '12px 14px',
          marginBottom: '16px',
          display: 'flex',
          alignItems: 'flex-start',
          gap: '10px'
        }}>
          <AlertCircle size={16} color="#DC2626" style={{ flexShrink: 0, marginTop: '2px' }} />
          <div>
            <p style={{ fontSize: '13px', fontWeight: 600, color: '#991B1B', margin: '0 0 2px' }}>Stream Error</p>
            <p style={{ fontSize: '12px', color: '#7F1D1D', margin: 0 }}>{error}</p>
          </div>
        </div>
      )}

      <div
        style={{
          background: T.bgCard,
          border: `1px solid ${T.border}`,
          borderRadius: T.radius,
          boxShadow: T.shadowCard,
          overflow: 'hidden',
        }}
      >
        {/* Panel header */}
        <div
          style={{
            padding: '16px 20px',
            borderBottom: `1px solid ${T.border}`,
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}
        >
          <div>
            <p
              style={{
                fontSize: '11px',
                fontWeight: 500,
                textTransform: 'uppercase' as const,
                letterSpacing: '0.08em',
                color: T.meta,
                margin: '0 0 2px',
              }}
            >
              Reasoning Engine
            </p>
            <p style={{ fontSize: '14px', fontWeight: 600, color: T.heading, margin: 0 }}>
              {formData?.companyName ?? 'Company'} · Emission Calculation
            </p>
          </div>

          {/* Status pill */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              padding: '5px 12px',
              background: error ? '#FEE2E2' : isComplete ? T.successBg : '#EFF6FF',
              border: `1px solid ${error ? '#FCA5A5' : isComplete ? T.successBorder : '#BFDBFE'}`,
              borderRadius: '20px',
            }}
          >
            {error ? (
              <>
                <AlertCircle size={12} color="#DC2626" />
                <span style={{ fontSize: '12px', fontWeight: 600, color: '#DC2626' }}>
                  Error
                </span>
              </>
            ) : isComplete ? (
              <>
                <CheckCircle2 size={12} color={T.successText} />
                <span style={{ fontSize: '12px', fontWeight: 600, color: T.successText }}>
                  Complete
                </span>
              </>
            ) : (
              <>
                <span
                  style={{
                    width: '6px',
                    height: '6px',
                    borderRadius: '50%',
                    background: '#3B82F6',
                    animation: 'blink 1.4s ease-in-out infinite',
                    display: 'inline-block',
                  }}
                />
                <span style={{ fontSize: '12px', fontWeight: 600, color: '#1D4ED8' }}>
                  Processing
                </span>
              </>
            )}
          </div>
        </div>

        {/* Timeline */}
        <div
          ref={timelineRef}
          style={{
            padding: '20px 20px 20px 40px',
            minHeight: '300px',
            maxHeight: '520px',
            overflowY: 'auto',
            overflowX: 'hidden',
          }}
        >
          {isLoading && <AnalysisSpinner />}

          {visibleEvents.map((ev, idx) => (
            <EventCard
              key={ev.id}
              event={ev}
              isLast={idx === visibleEvents.length - 1}
            />
          ))}

          {/* Completion banner */}
          <AnimatePresence>
            {isComplete && !error && (
              <motion.div
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.35, delay: 0.15 }}
                style={{
                  marginTop: '16px',
                  marginLeft: '-20px',
                  padding: '16px 20px',
                  background: T.primaryLight,
                  border: `1px solid ${T.successBorder}`,
                  borderRadius: '6px',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '12px',
                }}
              >
                <CheckCircle2 size={18} color={T.primary} />
                <div>
                  <p style={{ fontSize: '14px', fontWeight: 600, color: T.primary, margin: '0 0 2px' }}>
                    Analysis complete
                  </p>
                  <p style={{ fontSize: '12px', color: T.body, margin: 0 }}>
                    All scopes calculated. Report ready for review.
                  </p>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Stats bar */}
        <div
          style={{
            background: '#FAFAFA',
            borderTop: `1px solid ${T.border}`,
            padding: '10px 20px',
            display: 'flex',
            alignItems: 'center',
            gap: '20px',
          }}
        >
          {[
            { Icon: Hash, label: `${visibleEvents.length} events` },
            { Icon: Clock, label: `${elapsed}s elapsed` },
            { Icon: Activity, label: error ? 'Failed' : isComplete ? 'Finished' : 'Running' },
          ].map(({ Icon, label }, i) => (
            <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
              <Icon size={12} color={T.meta} />
              <span
                style={{
                  fontSize: '11px',
                  color: T.meta,
                  fontFamily: T.mono,
                  fontVariantNumeric: 'tabular-nums',
                }}
              >
                {label}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Actions */}
      <AnimatePresence>
        {isComplete && !error && (
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.4 }}
            style={{
              display: 'flex',
              gap: '12px',
              marginTop: '20px',
              flexWrap: 'wrap',
            }}
          >
            <button
              onClick={() => navigate('/results')}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '7px',
                height: '40px',
                padding: '0 20px',
                background: T.primary,
                border: 'none',
                borderRadius: T.radiusSm,
                fontSize: '13px',
                fontWeight: 600,
                color: 'white',
                cursor: 'pointer',
                transition: 'background 0.15s ease',
                fontFamily: 'inherit',
              }}
              onMouseEnter={(e) => { (e.currentTarget as HTMLButtonElement).style.background = T.primaryHover; }}
              onMouseLeave={(e) => { (e.currentTarget as HTMLButtonElement).style.background = T.primary; }}
            >
              View Results &amp; Report
              <ArrowRight size={14} />
            </button>
            <button
              onClick={() => navigate('/')}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                height: '40px',
                padding: '0 16px',
                background: T.bgCard,
                border: `1px solid ${T.borderInput}`,
                borderRadius: T.radiusSm,
                fontSize: '13px',
                fontWeight: 500,
                color: T.body,
                cursor: 'pointer',
                transition: 'border-color 0.15s ease',
                fontFamily: 'inherit',
              }}
            >
              <RotateCcw size={13} />
              New Calculation
            </button>
          </motion.div>
        )}
      </AnimatePresence>

      <style>{`
        @keyframes spin { to { transform: rotate(360deg); } }
        @keyframes blink { 0%,100% { opacity:1; } 50% { opacity:0.3; } }
      `}</style>
    </motion.div>
  );
}