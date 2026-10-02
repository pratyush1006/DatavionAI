type Props = {
  eyebrow: string;
  title: string;
  description?: string;
};

export function SectionTitle({
  eyebrow,
  title,
  description,
}: Props) {
  return (
    <div className="section-title">
      <div className="section-eyebrow">{eyebrow}</div>
      <h2>{title}</h2>
      {description ? <p>{description}</p> : null}
    </div>
  );
}
