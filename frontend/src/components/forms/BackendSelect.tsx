"use client";

import type { SelectOption } from "@/lib/backend/types";

type Props = {
  id: string;
  name: string;
  label: string;
  value: string;
  options: SelectOption[];
  onChange: (value: string) => void;
  disabled?: boolean;
  required?: boolean;
  placeholder?: string;
  helpText?: string;
};

export function BackendSelect({
  id,
  name,
  label,
  value,
  options,
  onChange,
  disabled,
  required,
  placeholder = "Select",
  helpText,
}: Props) {
  return (
    <div className="mb-3">
      <label htmlFor={id} className="form-label fw-semibold">
        {label}
        {required ? " *" : ""}
      </label>

      <select
        id={id}
        name={name}
        className="form-select"
        value={value}
        onChange={(event) => onChange(event.target.value)}
        disabled={disabled}
        required={required}
      >
        <option value="">{placeholder}</option>

        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>

      {helpText ? (
        <div className="form-text">{helpText}</div>
      ) : null}
    </div>
  );
}
