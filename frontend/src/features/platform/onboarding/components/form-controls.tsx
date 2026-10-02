"use client";

export function Field({ label, value, onChange, required = false, type = "text", placeholder }: { readonly label: string; readonly value: string; readonly onChange: (value: string) => void; readonly required?: boolean; readonly type?: string; readonly placeholder?: string }) {
  return <label className="block">
    <span className="mb-2 block text-sm font-medium">{label}{required ? <span className="ml-1 text-destructive">*</span> : null}</span>
    <input type={type} value={value} placeholder={placeholder} onChange={(event) => onChange(event.target.value)} className="h-11 w-full rounded-lg border bg-background px-3 text-sm outline-none focus:border-primary focus:ring-2 focus:ring-primary/20" />
  </label>;
}

export function TextArea({ label, value, onChange, required = false, className = "" }: { readonly label: string; readonly value: string; readonly onChange: (value: string) => void; readonly required?: boolean; readonly className?: string }) {
  return <label className={`block ${className}`}>
    <span className="mb-2 block text-sm font-medium">{label}{required ? <span className="ml-1 text-destructive">*</span> : null}</span>
    <textarea value={value} onChange={(event) => onChange(event.target.value)} rows={4} className="w-full rounded-lg border bg-background px-3 py-2.5 text-sm outline-none focus:border-primary focus:ring-2 focus:ring-primary/20" />
  </label>;
}

export function Select({ label, value, onChange, options, loading = false, disabled = false, required = false }: { readonly label: string; readonly value: string; readonly onChange: (value: string) => void; readonly options: readonly { value: string; label: string }[]; readonly loading?: boolean; readonly disabled?: boolean; readonly required?: boolean }) {
  return <label className="block">
    <span className="mb-2 block text-sm font-medium">{label}{required ? <span className="ml-1 text-destructive">*</span> : null}</span>
    <select value={value} onChange={(event) => onChange(event.target.value)} disabled={disabled || loading} className="h-11 w-full rounded-lg border bg-background px-3 text-sm outline-none disabled:opacity-50 focus:border-primary focus:ring-2 focus:ring-primary/20">
      <option value="">{loading ? "Loading..." : `Select ${label.toLowerCase()}`}</option>
      {options.map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}
    </select>
  </label>;
}

export function StepSection({ title, description, children }: { readonly title: string; readonly description: string; readonly children: import("react").ReactNode }) {
  return <section className="rounded-xl border bg-background p-5 shadow-sm md:p-6">
    <div className="mb-5"><h2 className="text-lg font-semibold">{title}</h2><p className="mt-1 text-sm text-muted-foreground">{description}</p></div>
    <div className="grid gap-5 md:grid-cols-2">{children}</div>
  </section>;
}
