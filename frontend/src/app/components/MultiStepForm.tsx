import { useState, useCallback } from 'react';
import { useNavigate, useOutletContext } from 'react-router';
import { motion, AnimatePresence } from 'motion/react';
import { Check, ChevronRight, ChevronLeft, Loader2, Info } from 'lucide-react';
import { AppContextType, calculateResults, T } from './Root';

const INDUSTRIES = [
  'Technology',
  'Manufacturing',
  'Retail',
  'Healthcare',
  'Finance',
  'Energy',
  'Transportation',
  'Agriculture',
  'Construction',
  'Education',
  'Other',
];

const STEPS = [
  { id: 1, label: 'Company Information' },
  { id: 2, label: 'Energy & Fuel' },
  { id: 3, label: 'Other Sources' },
];

// ─── Field Subcomponents ─────────────────────────────────────────────────────

function FieldLabel({
  htmlFor,
  children,
  required,
}: {
  htmlFor: string;
  children: React.ReactNode;
  required?: boolean;
}) {
  return (
    <label
      htmlFor={htmlFor}
      style={{
        display: 'block',
        fontSize: '13px',
        fontWeight: 500,
        color: '#374151',
        marginBottom: '6px',
      }}
    >
      {children}
      {required && (
        <span style={{ color: '#DC2626', marginLeft: '3px' }}>*</span>
      )}
    </label>
  );
}

function InputField({
  label,
  name,
  type = 'text',
  placeholder,
  value,
  onChange,
  unit,
  error,
  required,
  helper,
  disabled,
}: {
  label: string;
  name: string;
  type?: string;
  placeholder?: string;
  value: string;
  onChange: (v: string) => void;
  unit?: string;
  error?: string;
  required?: boolean;
  helper?: string;
  disabled?: boolean;
}) {
  const [focused, setFocused] = useState(false);

  return (
    <div>
      <FieldLabel htmlFor={name} required={required}>
        {label}
      </FieldLabel>
      <div style={{ position: 'relative' }}>
        <input
          id={name}
          type={type}
          inputMode={type === 'number' ? 'decimal' : undefined}
          placeholder={placeholder}
          value={value}
          disabled={disabled}
          onChange={(e) => onChange(e.target.value)}
          onFocus={() => setFocused(true)}
          onBlur={() => setFocused(false)}
          style={{
            width: '100%',
            height: '44px',
            padding: unit ? '0 52px 0 12px' : '0 12px',
            border: `1px solid ${
              error ? '#DC2626' : focused ? T.primary : '#E5E7EB'
            }`,
            borderRadius: T.radiusSm,
            fontSize: '14px',
            fontWeight: 400,
            color: disabled ? T.meta : '#111827',
            background: disabled ? '#F5F5F5' : '#FAFAFA',
            outline: 'none',
            transition: 'border-color 0.15s ease, box-shadow 0.15s ease',
            boxSizing: 'border-box',
            cursor: disabled ? 'not-allowed' : 'text',
            fontFamily: 'inherit',
            boxShadow: focused && !error
              ? '0 0 0 3px rgba(13,79,60,0.12)'
              : 'none',
          }}
        />
        {unit && (
          <span
            style={{
              position: 'absolute',
              right: '12px',
              top: '50%',
              transform: 'translateY(-50%)',
              fontSize: '12px',
              color: T.meta,
              pointerEvents: 'none',
              fontWeight: 500,
              letterSpacing: '0.02em',
            }}
          >
            {unit}
          </span>
        )}
      </div>
      {error ? (
        <p
          style={{
            fontSize: '12px',
            color: '#DC2626',
            marginTop: '4px',
          }}
        >
          {error}
        </p>
      ) : helper ? (
        <p style={{ fontSize: '12px', color: T.meta, marginTop: '4px' }}>
          {helper}
        </p>
      ) : null}
    </div>
  );
}

function SelectField({
  label,
  name,
  value,
  onChange,
  options,
  error,
  required,
  disabled,
}: {
  label: string;
  name: string;
  value: string;
  onChange: (v: string) => void;
  options: string[];
  error?: string;
  required?: boolean;
  disabled?: boolean;
}) {
  const [focused, setFocused] = useState(false);

  return (
    <div>
      <FieldLabel htmlFor={name} required={required}>
        {label}
      </FieldLabel>
      <select
        id={name}
        value={value}
        disabled={disabled}
        onChange={(e) => onChange(e.target.value)}
        onFocus={() => setFocused(true)}
        onBlur={() => setFocused(false)}
        style={{
          width: '100%',
          height: '44px',
          padding: '0 36px 0 12px',
          border: `${focused && !error ? '1.5px' : '1px'} solid ${
            error ? '#DC2626' : focused ? T.primary : T.borderInput
          }`,
          borderRadius: T.radiusSm,
          fontSize: '14px',
          color: value ? '#111827' : T.meta,
          background: `${focused ? T.primaryLight : T.bgCard} url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='%236B7280' viewBox='0 0 16 16'%3E%3Cpath d='M7.247 11.14L2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z'/%3E%3C/svg%3E") no-repeat right 12px center`,
          appearance: 'none',
          outline: 'none',
          transition: 'border-color 0.15s ease, background 0.15s ease',
          cursor: disabled ? 'not-allowed' : 'pointer',
          boxSizing: 'border-box',
          fontFamily: 'inherit',
        }}
      >
        <option value="" disabled>
          Select industry...
        </option>
        {options.map((opt) => (
          <option key={opt} value={opt}>
            {opt}
          </option>
        ))}
      </select>
      {error && (
        <p style={{ fontSize: '12px', color: '#DC2626', marginTop: '4px' }}>
          {error}
        </p>
      )}
    </div>
  );
}

// ─── Step Indicator ──────────────────────────────────────────────────────────

function StepIndicator({ currentStep }: { currentStep: number }) {
  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        marginBottom: '32px',
      }}
    >
      {STEPS.map((step, idx) => {
        const isActive = step.id === currentStep;
        const isCompleted = step.id < currentStep;
        const isLast = idx === STEPS.length - 1;

        return (
          <div
            key={step.id}
            style={{ display: 'flex', alignItems: 'center', flex: isLast ? 0 : 1 }}
          >
            {/* Circle */}
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '6px' }}>
              <div
                style={{
                  width: '28px',
                  height: '28px',
                  borderRadius: '50%',
                  background:
                    isActive || isCompleted ? T.primary : T.bgCard,
                  border: `1.5px solid ${
                    isActive || isCompleted ? T.primary : T.borderInput
                  }`,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  transition: 'all 0.2s ease',
                  flexShrink: 0,
                }}
              >
                {isCompleted ? (
                  <Check size={13} color="white" strokeWidth={2.5} />
                ) : (
                  <span
                    style={{
                      fontSize: '12px',
                      fontWeight: 600,
                      color: isActive ? 'white' : T.meta,
                      lineHeight: 1,
                    }}
                  >
                    {step.id}
                  </span>
                )}
              </div>
              <span
                style={{
                  fontSize: '11px',
                  fontWeight: isActive ? 600 : 400,
                  color: isActive ? T.primary : isCompleted ? T.body : T.meta,
                  whiteSpace: 'nowrap' as const,
                  letterSpacing: '0.01em',
                }}
              >
                {step.label}
              </span>
            </div>

            {/* Connector line */}
            {!isLast && (
              <div
                style={{
                  flex: 1,
                  height: '1.5px',
                  background: isCompleted ? T.primary : T.border,
                  margin: '0 8px',
                  marginBottom: '20px',
                  transition: 'background 0.3s ease',
                }}
              />
            )}
          </div>
        );
      })}
    </div>
  );
}

// ─── Info Box ────────────────────────────────────────────────────────────────

function InfoBox({ text }: { text: string }) {
  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'flex-start',
        gap: '10px',
        background: '#F9FAFB',
        border: `1px solid ${T.border}`,
        borderRadius: T.radiusSm,
        padding: '12px 14px',
        marginTop: '4px',
      }}
    >
      <Info size={14} color={T.meta} style={{ flexShrink: 0, marginTop: '1px' }} />
      <p
        style={{
          fontSize: '12px',
          color: T.body,
          margin: 0,
          lineHeight: 1.6,
        }}
      >
        {text}
      </p>
    </div>
  );
}

// ─── Section Divider ─────────────────────────────────────────────────────────

function SectionMeta({ text }: { text: string }) {
  return (
    <p
      style={{
        fontSize: '11px',
        fontWeight: 500,
        textTransform: 'uppercase' as const,
        letterSpacing: '0.08em',
        color: T.meta,
        margin: '0 0 16px',
      }}
    >
      {text}
    </p>
  );
}

// ─── Main Form Component ─────────────────────────────────────────────────────

interface Step1Data { companyName: string; industry: string; employeeCount: string }
interface Step2Data { electricity: string; diesel: string; petrol: string; naturalGas: string; lpg: string }
interface Step3Data { coal: string; water: string; waste: string; businessTravel: string }

export function MultiStepForm() {
  const navigate = useNavigate();
  const { setFormData, setResults } = useOutletContext<AppContextType>();

  const [currentStep, setCurrentStep] = useState(1);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [direction, setDirection] = useState(1);

  const [step1, setStep1] = useState<Step1Data>({ companyName: '', industry: '', employeeCount: '' });
  const [step2, setStep2] = useState<Step2Data>({ electricity: '', diesel: '', petrol: '', naturalGas: '', lpg: '' });
  const [step3, setStep3] = useState<Step3Data>({ coal: '', water: '', waste: '', businessTravel: '' });
  const [errors, setErrors] = useState<Record<string, string>>({});

  const validateStep1 = useCallback(() => {
    const errs: Record<string, string> = {};
    if (!step1.companyName.trim()) errs.companyName = 'Company name is required';
    else if (step1.companyName.trim().length < 2) errs.companyName = 'Must be at least 2 characters';
    if (!step1.industry) errs.industry = 'Please select an industry';
    if (!step1.employeeCount) errs.employeeCount = 'Employee count is required';
    else if (parseInt(step1.employeeCount) < 1) errs.employeeCount = 'Must be at least 1';
    return errs;
  }, [step1]);

  const handleNext = () => {
    if (currentStep === 1) {
      const errs = validateStep1();
      if (Object.keys(errs).length > 0) { setErrors(errs); return; }
      setErrors({});
    }
    setDirection(1);
    setCurrentStep((s) => s + 1);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handlePrev = () => {
    setDirection(-1);
    setCurrentStep((s) => s - 1);
    setErrors({});
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);
    try {
      const num = (v: string) => parseFloat(v) || 0;
      const fd = {
        companyName: step1.companyName.trim(),
        industry: step1.industry,
        employeeCount: parseInt(step1.employeeCount) || 1,
        electricity: num(step2.electricity),
        diesel: num(step2.diesel),
        petrol: num(step2.petrol),
        naturalGas: num(step2.naturalGas),
        lpg: num(step2.lpg),
        coal: num(step3.coal),
        water: num(step3.water),
        waste: num(step3.waste),
        businessTravel: num(step3.businessTravel),
      };

      // Import and call the API service
      const { startCalculation } = await import('../services/api');
      const calcResponse = await startCalculation(fd);

      setFormData(fd);
      // Store calculation ID for streaming panel
      sessionStorage.setItem('calculationId', calcResponse.calculation_id);
      navigate('/streaming');
    } catch (error) {
      console.error('Submission error:', error);
      alert(`Error: ${error instanceof Error ? error.message : 'Failed to start calculation'}`);
      setIsSubmitting(false);
    }
  };

  const variants = {
    enter: (d: number) => ({ opacity: 0, x: d > 0 ? 32 : -32 }),
    center: { opacity: 1, x: 0 },
    exit: (d: number) => ({ opacity: 0, x: d > 0 ? -32 : 32 }),
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35, ease: 'easeOut' }}
    >
      {/* Page title */}
      <div style={{ marginBottom: '24px' }}>
        <h1
          style={{
            fontSize: '20px',
            fontWeight: 700,
            color: T.heading,
            margin: '0 0 4px',
            letterSpacing: '-0.3px',
          }}
        >
          Carbon Footprint Calculator
        </h1>
        <p style={{ fontSize: '14px', color: T.body, margin: 0 }}>
          Enter your company's annual activity data to calculate GHG emissions (GHG Protocol, India CEA 2022–23)
        </p>
      </div>

      {/* Form card */}
      <div
        style={{
          background: T.bgCard,
          border: `1px solid ${T.border}`,
          borderRadius: T.radius,
          boxShadow: T.shadowCard,
          padding: 'clamp(20px, 4vw, 36px)',
        }}
      >
        <StepIndicator currentStep={currentStep} />

        <AnimatePresence mode="wait" custom={direction}>
          <motion.div
            key={currentStep}
            custom={direction}
            variants={variants}
            initial="enter"
            animate="center"
            exit="exit"
            transition={{ duration: 0.22, ease: 'easeInOut' }}
          >
            {/* ── Step 1 ── */}
            {currentStep === 1 && (
              <div>
                <SectionMeta text="Step 1 of 3 — Organisation Details" />
                <div
                  style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
                    gap: '18px',
                    marginBottom: '20px',
                  }}
                >
                  <InputField
                    label="Legal Company Name"
                    name="companyName"
                    placeholder="e.g. Tata Consultancy Services Ltd."
                    value={step1.companyName}
                    onChange={(v) => { setStep1((s) => ({ ...s, companyName: v })); if (errors.companyName) setErrors((e) => ({ ...e, companyName: '' })); }}
                    error={errors.companyName}
                    required
                  />
                  <SelectField
                    label="Primary Industry Sector"
                    name="industry"
                    value={step1.industry}
                    onChange={(v) => { setStep1((s) => ({ ...s, industry: v })); if (errors.industry) setErrors((e) => ({ ...e, industry: '' })); }}
                    options={INDUSTRIES}
                    error={errors.industry}
                    required
                  />
                  <InputField
                    label="Total Headcount (FTE)"
                    name="employeeCount"
                    type="number"
                    placeholder="e.g. 500"
                    value={step1.employeeCount}
                    onChange={(v) => { setStep1((s) => ({ ...s, employeeCount: v })); if (errors.employeeCount) setErrors((e) => ({ ...e, employeeCount: '' })); }}
                    unit="employees"
                    error={errors.employeeCount}
                    required
                    helper="Full-time equivalent (FTE)"
                  />
                </div>
                <InfoBox text="Use your most recent annual report or HR system for headcount. Benchmarks are calculated per employee using India-specific sector intensity data." />
              </div>
            )}

            {/* ── Step 2 ── */}
            {currentStep === 2 && (
              <div>
                <SectionMeta text="Step 2 of 3 — Energy & Fuel Consumption (Scope 1 & 2)" />
                
                {/* AI Upload Feature */}
                <div style={{ marginBottom: '24px', background: T.primaryLight, padding: '16px', borderRadius: T.radius, border: `1px dashed ${T.primary}` }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                      <h4 style={{ margin: '0 0 4px', fontSize: '14px', color: T.primary, fontWeight: 600 }}>✨ AI Auto-Fill</h4>
                      <p style={{ margin: 0, fontSize: '12px', color: T.body }}>Upload an electricity bill and let Swach AI extract your consumption.</p>
                    </div>
                    <label style={{ 
                      background: isSubmitting ? '#5a9080' : T.primary, color: 'white', padding: '8px 16px', 
                      borderRadius: T.radiusSm, fontSize: '13px', fontWeight: 500,
                      cursor: isSubmitting ? 'wait' : 'pointer', display: 'flex', alignItems: 'center', gap: '6px',
                      opacity: isSubmitting ? 0.8 : 1
                    }}>
                      {isSubmitting ? "Analyzing..." : "Upload Bill"}
                      <input 
                        type="file" 
                        accept="image/*,.pdf" 
                        style={{ display: 'none' }}
                        disabled={isSubmitting}
                        onChange={async (e) => {
                          const file = e.target.files?.[0];
                          if (!file) return;
                          
                          setIsSubmitting(true);
                          try {
                            const { analyzeBill } = await import('../services/api');
                            const result = await analyzeBill(file, 'electricity');
                            
                            if (result.error) throw new Error(result.error);
                            
                            if (result.electricity_kwh) {
                              setStep2(s => ({ ...s, electricity: result.electricity_kwh.toString() }));
                            }
                            
                            alert(`Upload Done! Found ${result.electricity_kwh} kWh from ${result.company_name || 'bill'}.`);
                          } catch (error: any) {
                            alert("Failed to analyze bill: " + error.message);
                          } finally {
                            setIsSubmitting(false);
                            // Reset the input so the same file can be selected again
                            e.target.value = '';
                          }
                        }}
                      />
                    </label>
                  </div>
                </div>

                <div
                  style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
                    gap: '18px',
                    marginBottom: '20px',
                  }}
                >
                  <InputField label="Electricity Consumption" name="electricity" type="number" placeholder="0" value={step2.electricity} onChange={(v) => setStep2((s) => ({ ...s, electricity: v }))} unit="kWh / yr" helper="From utility bills — annual total" />
                  <InputField label="Diesel" name="diesel" type="number" placeholder="0" value={step2.diesel} onChange={(v) => setStep2((s) => ({ ...s, diesel: v }))} unit="litres / yr" helper="Generators, vehicles, boilers" />
                  <InputField label="Petrol" name="petrol" type="number" placeholder="0" value={step2.petrol} onChange={(v) => setStep2((s) => ({ ...s, petrol: v }))} unit="litres / yr" helper="Company fleet" />
                  <InputField label="Natural Gas" name="naturalGas" type="number" placeholder="0" value={step2.naturalGas} onChange={(v) => setStep2((s) => ({ ...s, naturalGas: v }))} unit="MMBtu / yr" helper="Heating, industrial processes" />
                  <InputField label="LPG" name="lpg" type="number" placeholder="0" value={step2.lpg} onChange={(v) => setStep2((s) => ({ ...s, lpg: v }))} unit="kg / yr" helper="Cylinders used on premises" />
                </div>
                <InfoBox text="All fields default to 0 if left blank. Emission factors: India grid 0.82 kgCO2e/kWh (CEA 2022–23), IPCC AR6 for fuels." />
              </div>
            )}

            {/* ── Step 3 ── */}
            {currentStep === 3 && (
              <div>
                <SectionMeta text="Step 3 of 3 — Value Chain & Other Sources (Scope 3)" />
                <div
                  style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
                    gap: '18px',
                    marginBottom: '20px',
                  }}
                >
                  <InputField label="Coal" name="coal" type="number" placeholder="0" value={step3.coal} onChange={(v) => setStep3((s) => ({ ...s, coal: v }))} unit="tonnes / yr" helper="On-site industrial usage" />
                  <InputField label="Water Consumption" name="water" type="number" placeholder="0" value={step3.water} onChange={(v) => setStep3((s) => ({ ...s, water: v }))} unit="m³ / yr" helper="Total facility usage" />
                  <InputField label="Waste to Landfill" name="waste" type="number" placeholder="0" value={step3.waste} onChange={(v) => setStep3((s) => ({ ...s, waste: v }))} unit="tonnes / yr" helper="Annual waste sent to landfill" />
                  <InputField label="Business Travel" name="businessTravel" type="number" placeholder="0" value={step3.businessTravel} onChange={(v) => setStep3((s) => ({ ...s, businessTravel: v }))} unit="km / yr" helper="Air + road, all employees" />
                </div>
                <InfoBox text="Scope 3 typically represents 70–80% of total footprint. Use annual employee travel reports and facility waste manifests for best accuracy." />
              </div>
            )}
          </motion.div>
        </AnimatePresence>

        {/* Navigation */}
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginTop: '28px',
            paddingTop: '20px',
            borderTop: `1px solid ${T.border}`,
            gap: '12px',
          }}
        >
          <button
            onClick={handlePrev}
            disabled={currentStep === 1}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              height: '38px',
              padding: '0 16px',
              background: T.bgCard,
              border: `1px solid ${currentStep === 1 ? T.border : T.borderInput}`,
              borderRadius: T.radiusSm,
              fontSize: '13px',
              fontWeight: 500,
              color: currentStep === 1 ? T.meta : T.body,
              cursor: currentStep === 1 ? 'not-allowed' : 'pointer',
              opacity: currentStep === 1 ? 0.5 : 1,
              transition: 'all 0.15s ease',
              fontFamily: 'inherit',
            }}
            onMouseEnter={(e) => {
              if (currentStep !== 1) (e.currentTarget as HTMLButtonElement).style.borderColor = T.primary;
            }}
            onMouseLeave={(e) => {
              if (currentStep !== 1) (e.currentTarget as HTMLButtonElement).style.borderColor = T.borderInput;
            }}
          >
            <ChevronLeft size={15} />
            Back
          </button>

          {/* Step counter */}
          <span
            style={{
              fontSize: '12px',
              color: T.meta,
              fontVariantNumeric: 'tabular-nums',
              letterSpacing: '0.01em',
            }}
          >
            {currentStep} / {STEPS.length}
          </span>

          {currentStep < 3 ? (
            <button
              onClick={handleNext}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                height: '38px',
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
              Continue
              <ChevronRight size={15} />
            </button>
          ) : (
            <button
              onClick={handleSubmit}
              disabled={isSubmitting}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '7px',
                height: '38px',
                padding: '0 22px',
                background: isSubmitting ? '#5a9080' : T.primary,
                border: 'none',
                borderRadius: T.radiusSm,
                fontSize: '13px',
                fontWeight: 600,
                color: 'white',
                cursor: isSubmitting ? 'wait' : 'pointer',
                transition: 'background 0.15s ease',
                fontFamily: 'inherit',
                minWidth: '180px',
                justifyContent: 'center',
              }}
            >
              {isSubmitting ? (
                <>
                  <Loader2 size={14} style={{ animation: 'spin 0.9s linear infinite' }} />
                  Running analysis...
                </>
              ) : (
                <>
                  Run Emissions Analysis
                  <ChevronRight size={15} />
                </>
              )}
            </button>
          )}
        </div>
      </div>

      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    </motion.div>
  );
}