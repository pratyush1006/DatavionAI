export type DomainApiContract = Readonly<{
  identifier: string;
  prefix: string;
  group: string;
  routes: readonly string[];
  sources: readonly string[];
  confidence: "high" | "medium";
  evidenceScore: number;
}>;

export type DomainApiMap = Readonly<
  Record<string, readonly DomainApiContract[]>
>;

export type DomainApiDefinition = Readonly<{
  id:
    | "patients"
    | "appointments"
    | "pharmacy"
    | "laboratory"
    | "documents"
    | "billing";
  label: string;
  contracts: readonly DomainApiContract[];
}>;
