"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import {
  Activity,
  Bell,
  CalendarDays,
  ChevronRight,
  CircleHelp,
  ClipboardList,
  CreditCard,
  FileText,
  FlaskConical,
  HeartPulse,
  Home,
  Image,
  Pill,
  Search,
  Stethoscope,
  UserRound,
  Video,
} from "lucide-react";

import { useAuth } from "@/core/auth";
import { apiClient } from "@/core/api";
import {
  deleteOfflineDashboardSnapshot,
  getOfflineDashboardCacheInfo,
  refreshUnlockedOfflineDashboardSnapshot,
  saveOfflineDashboardSnapshot,
  unlockOfflineDashboardSnapshot,
  clearUnlockedOfflineDashboardKeys,
  type PatientDashboardSnapshot,
  type OfflineDashboardSnapshot,
} from "./offline-dashboard-cache";

const navigation = [
  { id: "home", label: "Home", href: "#home", icon: Home },
  { id: "appointments", label: "Appointments", href: "#appointments", icon: CalendarDays },
  { id: "doctors", label: "Doctors", href: "#service-doctors", icon: Stethoscope },
  { id: "medicines", label: "Medicines", href: "#service-medicines", icon: Pill },
  { id: "lab-reports", label: "Lab reports", href: "#service-lab-reports", icon: FlaskConical },
  { id: "imaging", label: "Imaging", href: "#service-imaging", icon: Image },
  { id: "documents", label: "Documents", href: "#service-documents", icon: FileText },
  { id: "payments", label: "Payments", href: "#service-payments", icon: CreditCard },
  { id: "telemedicine", label: "Telemedicine", href: "#service-telemedicine", icon: Video },
  { id: "profile", label: "Profile", href: "#service-profile", icon: UserRound },
] as const;

const metrics = [
  { label: "Upcoming appointments", key: "upcoming_appointments", icon: CalendarDays },
  { label: "Prescriptions", key: "active_prescriptions", icon: Pill },
  { label: "Lab reports", key: "lab_reports", icon: FlaskConical },
  { label: "Documents", key: "documents", icon: FileText },
] as const;

const patientServices = [
  { id: "appointments", label: "Appointments", icon: CalendarDays },
  { id: "doctors", label: "Doctors", icon: Stethoscope },
  { id: "medicines", label: "Medicines", icon: Pill },
  { id: "lab-reports", label: "Lab reports", icon: FlaskConical },
  { id: "imaging", label: "Imaging", icon: Image },
  { id: "documents", label: "Documents", icon: FileText },
  { id: "payments", label: "Payments", icon: CreditCard },
  { id: "telemedicine", label: "Telemedicine", icon: Video },
] as const;

export function PatientDashboard() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const { user, logout, isAuthenticated, isInitialized, isLoading } = useAuth();
  const [greeting, setGreeting] = useState("Welcome back");
  const [isOnline, setIsOnline] = useState(false);
  const [offlinePassphrase, setOfflinePassphrase] = useState("");
  const [offlinePassphraseConfirm, setOfflinePassphraseConfirm] = useState("");
  const [offlineSnapshot, setOfflineSnapshot] = useState<OfflineDashboardSnapshot | null>(null);
  const [offlineCacheInfo, setOfflineCacheInfo] = useState<{ exists: boolean; updatedAt: string | null; expired: boolean }>({ exists: false, updatedAt: null, expired: false });
  const [offlineCacheChecked, setOfflineCacheChecked] = useState(false);
  const [offlineBusy, setOfflineBusy] = useState(false);
  const [offlineError, setOfflineError] = useState<string | null>(null);
  const [offlineNotice, setOfflineNotice] = useState<string | null>(null);
  const dashboardQuery = useQuery({
    queryKey: ["patient-portal", "dashboard", user?.id],
    queryFn: async () => {
      const response = await apiClient.get<PatientDashboardSnapshot>(
        "/patient-management/portal/me/dashboard/",
      );
      return response.data;
    },
    enabled: isInitialized && isAuthenticated && isOnline,
    retry: 1,
  });

  useEffect(() => {
    const updateOnlineState = () => setIsOnline(navigator.onLine);
    updateOnlineState();
    window.addEventListener("online", updateOnlineState);
    window.addEventListener("offline", updateOnlineState);
    return () => {
      window.removeEventListener("online", updateOnlineState);
      window.removeEventListener("offline", updateOnlineState);
    };
  }, []);

  useEffect(() => {
    if (!("serviceWorker" in navigator)) return;
    void navigator.serviceWorker.register("/patient-service-worker.js").catch(() => undefined);
  }, []);

  useEffect(() => {
    void getOfflineDashboardCacheInfo()
      .then((info) => {
        setOfflineCacheInfo(info);
        setOfflineCacheChecked(true);
      })
      .catch(() => {
        setOfflineCacheInfo({ exists: false, updatedAt: null, expired: false });
        setOfflineCacheChecked(true);
      });
  }, []);

  useEffect(() => {
    if (!isOnline || !user?.email || !dashboardQuery.data) return;
    let cancelled = false;
    void refreshUnlockedOfflineDashboardSnapshot(user.email, dashboardQuery.data)
      .then((snapshot) => {
        if (snapshot && !cancelled) {
          setOfflineSnapshot(snapshot);
          setOfflineCacheInfo({ exists: true, updatedAt: snapshot.updatedAt, expired: false });
        }
      })
      .catch((cause) => {
        if (!cancelled) setOfflineError(cause instanceof Error ? cause.message : "Offline copy could not be refreshed.");
      });
    return () => { cancelled = true; };
  }, [dashboardQuery.data, isOnline, user?.email]);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      const hour = new Date().getHours();
      setGreeting(hour < 12 ? "Good morning" : hour < 17 ? "Good afternoon" : "Good evening");
    }, 0);
    return () => window.clearTimeout(timer);
  }, []);

  useEffect(() => {
    if (isInitialized && !isAuthenticated && isOnline && offlineCacheChecked && !offlineCacheInfo.exists) router.replace("/login");
  }, [isAuthenticated, isInitialized, isOnline, offlineCacheChecked, offlineCacheInfo.exists, router]);

  const dashboardData = isOnline
    ? dashboardQuery.data ?? offlineSnapshot?.data ?? null
    : offlineSnapshot?.data ?? null;
  const showingOfflineCopy = Boolean(dashboardData && (!isOnline || !dashboardQuery.data));
  const patientName = dashboardData?.patient.display_name || user?.first_name?.trim() || "there";

  async function unlockOrEnableOfflineAccess() {
    setOfflineBusy(true);
    setOfflineError(null);
    setOfflineNotice(null);
    try {
      const email = user?.email?.trim() ?? "";

      if (isOnline && isAuthenticated && email && dashboardQuery.data) {
        if (!offlineCacheInfo.exists && offlinePassphrase !== offlinePassphraseConfirm) {
          throw new Error("The offline passphrases do not match.");
        }
        const snapshot = await saveOfflineDashboardSnapshot(email, offlinePassphrase, dashboardQuery.data);
        setOfflineSnapshot(snapshot);
        setOfflineCacheInfo({ exists: true, updatedAt: snapshot.updatedAt, expired: false });
        setOfflineNotice("Your encrypted offline copy has been saved on this device.");
      } else {
        const snapshot = await unlockOfflineDashboardSnapshot(offlinePassphrase);
        setOfflineSnapshot(snapshot);
        const cacheInfo = await getOfflineDashboardCacheInfo();
        setOfflineCacheInfo(cacheInfo);
        setOfflineNotice("Your encrypted offline copy is unlocked.");
      }
      setOfflinePassphrase("");
      setOfflinePassphraseConfirm("");
    } catch (cause) {
      setOfflineError(cause instanceof Error ? cause.message : "Offline access could not be unlocked.");
    } finally {
      setOfflineBusy(false);
    }
  }

  async function removeOfflineCopy() {
    setOfflineBusy(true);
    try {
      await deleteOfflineDashboardSnapshot();
      setOfflineSnapshot(null);
      setOfflineCacheInfo({ exists: false, updatedAt: null, expired: false });
      setOfflineNotice("The encrypted offline copy was removed from this device.");
      setOfflineError(null);
    } catch (cause) {
      setOfflineError(cause instanceof Error ? cause.message : "Offline copy could not be removed.");
    } finally {
      setOfflineBusy(false);
    }
  }

  async function signOut() {
    clearUnlockedOfflineDashboardKeys();
    queryClient.removeQueries({ queryKey: ["patient-portal", "dashboard"] });
    await logout();
  }

  if (!isInitialized || isLoading) {
    if (isOnline) return <main className="min-vh-100 d-flex align-items-center justify-content-center text-body-secondary">Loading your secure patient portal…</main>;
  }

  if (!isAuthenticated && isOnline && (!offlineCacheChecked || !offlineCacheInfo.exists)) {
    return <main className="min-vh-100 d-flex align-items-center justify-content-center text-body-secondary">{offlineCacheChecked ? "Redirecting to sign in…" : "Checking saved offline access…"}</main>;
  }

  return (
    <div className="min-vh-100 bg-body-tertiary" id="home">
      <header className="navbar bg-white border-bottom shadow-sm sticky-top">
        <div className="container-fluid px-3 px-lg-4 gap-3">
          <Link className="navbar-brand fw-bold me-3" href="/patient/dashboard">DatavionOS</Link>
          <div className="d-none d-md-flex flex-grow-1 justify-content-center">
            <div className="position-relative w-100" style={{ maxWidth: "34rem" }}>
              <Search className="position-absolute top-50 translate-middle-y text-body-secondary" style={{ left: ".75rem" }} size={17} aria-hidden="true" />
              <input aria-label="Search your health records" className="form-control ps-5" placeholder="Search your health records…" />
            </div>
          </div>
          <div className="d-flex align-items-center gap-2 gap-lg-3">
            <button className="btn btn-light btn-sm" type="button" title="Notifications"><Bell size={17} aria-hidden="true" /><span className="visually-hidden">Notifications</span></button>
            <button className="btn btn-light btn-sm d-none d-sm-inline-flex align-items-center gap-1" type="button" title="Patient support"><CircleHelp size={17} aria-hidden="true" /><span>Help</span></button>
            <span className="small text-body-secondary">Patient</span>
            {isAuthenticated ? <button className="btn btn-outline-secondary btn-sm" type="button" onClick={() => void signOut()}>Sign out</button> : null}
          </div>
        </div>
      </header>

      <div className="container-fluid">
        <div className="row">
          <aside className="col-12 col-lg-2 border-end bg-white min-vh-100 p-3">
            <nav aria-label="Patient navigation" className="d-flex flex-row flex-lg-column gap-1 overflow-auto">
              {navigation.map(({ id, label, href, icon: Icon }) => (
                <a key={id} className={`d-flex align-items-center gap-2 rounded px-3 py-2 text-decoration-none text-nowrap ${id === "home" ? "bg-primary text-white" : "text-body-secondary"}`} href={href}>
                  <Icon size={18} aria-hidden="true" />
                  <span>{label}</span>
                </a>
              ))}
            </nav>
          </aside>

          <main className="col-12 col-lg-10 p-3 p-lg-4">
            <section className="mb-4">
              <div className="small text-primary text-uppercase fw-semibold mb-2">Patient dashboard</div>
              <h1 className="h2 mb-1">{greeting}, {patientName} <span aria-hidden="true">👋</span></h1>
              <p className="text-body-secondary mb-0">Here&apos;s your health overview.</p>
            </section>

            {showingOfflineCopy ? <div className="alert alert-warning" role="status">Offline copy · Last synced {new Date(offlineSnapshot?.updatedAt ?? "").toLocaleString()}</div> : null}
            {dashboardQuery.isError && !offlineSnapshot ? (
              <div className="alert alert-danger d-flex flex-wrap align-items-center justify-content-between gap-2" role="alert">
                <span><HeartPulse size={18} className="me-2" aria-hidden="true" />Your patient portal data could not be loaded. {dashboardQuery.error instanceof Error ? dashboardQuery.error.message : "Please try again."}</span>
                <button className="btn btn-sm btn-outline-danger" type="button" onClick={() => void dashboardQuery.refetch()}>Retry</button>
              </div>
            ) : dashboardQuery.isPending && !offlineSnapshot ? (
              <div className="alert alert-info border-0" role="status">Loading your health overview…</div>
            ) : null}

            {(isOnline && isAuthenticated) || !isOnline || (!isAuthenticated && offlineCacheInfo.exists) ? (
              <section className="card border-0 shadow-sm mb-4" aria-label="Offline access settings">
                <div className="card-body p-3 p-lg-4">
                  <div className="d-flex flex-wrap justify-content-between align-items-start gap-3">
                    <div>
                      <h2 className="h6 mb-1">{isOnline && isAuthenticated ? "Secure offline access" : "Access your saved health overview"}</h2>
                      <p className="small text-body-secondary mb-2">
                        {isOnline && isAuthenticated
                          ? "Save an encrypted copy on this device. You’ll need this passphrase to unlock it offline."
                          : "Unlock the encrypted copy saved on this device with its passphrase."}
                      </p>
                      {offlineCacheInfo.exists && offlineCacheInfo.updatedAt ? (
                        <p className="small mb-2">Last synced {new Date(offlineCacheInfo.updatedAt).toLocaleString()}{offlineCacheInfo.expired ? " · Expired; save a fresh copy while online." : ` · Available offline for up to 14 days.`}</p>
                      ) : null}
                      <p className="small text-body-secondary mb-3">Your passphrase is never sent to the server or stored. Offline copies expire after 14 days; account changes can only be checked after reconnecting.</p>
                    </div>
                    {offlineCacheInfo.exists ? <button type="button" className="btn btn-sm btn-outline-danger" disabled={offlineBusy} onClick={() => void removeOfflineCopy()}>Remove offline copy</button> : null}
                  </div>

                  {offlineError ? <div className="alert alert-danger py-2" role="alert">{offlineError}</div> : null}
                  {offlineNotice ? <div className="alert alert-success py-2" role="status">{offlineNotice}</div> : null}
                  <form className="row g-2 align-items-end" onSubmit={(event) => { event.preventDefault(); void unlockOrEnableOfflineAccess(); }}>
                    <div className="col-12 col-md-4">
                      <label className="form-label small mb-1" htmlFor="offline-passphrase">Offline passphrase</label>
                      <input id="offline-passphrase" className="form-control" type="password" autoComplete="current-password" minLength={10} required value={offlinePassphrase} onChange={(event) => setOfflinePassphrase(event.target.value)} />
                    </div>
                    {isOnline && isAuthenticated && !offlineCacheInfo.exists ? <div className="col-12 col-md-4">
                      <label className="form-label small mb-1" htmlFor="offline-passphrase-confirm">Confirm passphrase</label>
                      <input id="offline-passphrase-confirm" className="form-control" type="password" autoComplete="new-password" minLength={10} required value={offlinePassphraseConfirm} onChange={(event) => setOfflinePassphraseConfirm(event.target.value)} />
                    </div> : null}
                    <div className="col-12 col-md-auto">
                      <button className="btn btn-primary" type="submit" disabled={offlineBusy || !offlineCacheChecked || (isOnline && isAuthenticated && (!dashboardQuery.data || dashboardQuery.isPending))}>
                        {offlineBusy ? "Working…" : isOnline && isAuthenticated && dashboardQuery.data ? offlineCacheInfo.exists ? "Update encrypted copy" : "Enable offline access" : "Unlock offline copy"}
                      </button>
                    </div>
                  </form>
                  {(!isOnline || !isAuthenticated) && !offlineCacheInfo.exists ? <p className="small text-body-secondary mt-2 mb-0">No encrypted copy is saved on this device. Connect, sign in, and enable offline access first.</p> : null}
                </div>
              </section>
            ) : null}

            <section aria-label="Health overview" className="row g-3 mb-4">
              {metrics.map(({ label, key, icon: Icon }) => (
                <div className="col-6 col-xl-3" key={label}>
                  <article className="card border-0 shadow-sm h-100">
                    <div className="card-body p-3 p-lg-4">
                      <div className="d-flex justify-content-between align-items-start gap-2 mb-3">
                        <span className="small fw-medium text-body-secondary">{label}</span>
                        <span className="rounded-3 bg-primary-subtle text-primary p-2"><Icon size={19} aria-hidden="true" /></span>
                      </div>
                      <div className="display-6 fw-semibold mb-1" aria-label={`${label}: ${dashboardData?.counts[key] ?? "unavailable"}`}>
                        {dashboardQuery.isPending && !dashboardData ? "…" : dashboardData?.counts[key] ?? "—"}
                      </div>
                      <div className="small text-body-secondary">{dashboardData ? showingOfflineCopy ? "Saved on this device" : "Current records" : "Unavailable"}</div>
                    </div>
                  </article>
                </div>
              ))}
            </section>

            <div className="row g-3 mb-4">
              <div className="col-12 col-xl-7" id="appointments">
                <section className="card border-0 shadow-sm h-100">
                  <div className="card-body p-4">
                    <div className="d-flex align-items-center gap-2 mb-3"><CalendarDays size={19} className="text-primary" aria-hidden="true" /><h2 className="h5 mb-0">Upcoming appointment</h2></div>
                    {dashboardQuery.isPending && !dashboardData ? <p className="text-body-secondary mb-0" role="status">Loading appointments…</p> : dashboardData?.upcoming_appointment ? (
                      <div className="rounded-3 border bg-body-tertiary p-3">
                        <div className="fw-semibold">{dashboardData.upcoming_appointment.provider_name}</div>
                        <div className="text-body-secondary">{new Date(dashboardData.upcoming_appointment.scheduled_start).toLocaleString(undefined, { weekday: "long", month: "short", day: "numeric", hour: "numeric", minute: "2-digit" })}</div>
                        <div className="small text-body-secondary mt-1">{dashboardData.upcoming_appointment.appointment_type.replaceAll("_", " ")} · {dashboardData.upcoming_appointment.status}{dashboardData.upcoming_appointment.is_virtual ? " · Virtual" : ""}</div>
                      </div>
                    ) : <div className="rounded-3 border bg-body-tertiary p-4 text-center"><p className="text-body-secondary mb-0">No upcoming appointments.</p></div>}
                  </div>
                </section>
              </div>
              <div className="col-12 col-xl-5" id="health-updates">
                <section className="card border-0 shadow-sm h-100">
                  <div className="card-body p-4">
                    <div className="d-flex align-items-center gap-2 mb-3"><Activity size={19} className="text-primary" aria-hidden="true" /><h2 className="h5 mb-0">Health updates</h2></div>
                    {dashboardQuery.isPending && !dashboardData ? <p className="text-body-secondary mb-0" role="status">Loading health updates…</p> : dashboardData?.health_updates.length ? (
                      <div className="list-group list-group-flush">
                        {dashboardData.health_updates.map((update) => (
                          <div key={update.id} className="list-group-item px-0 d-flex align-items-start gap-3">
                            <span className="rounded-circle bg-primary-subtle text-primary p-2"><HeartPulse size={17} aria-hidden="true" /></span>
                            <div className="min-w-0"><div className="fw-medium">{update.title}</div><div className="small text-body-secondary">{update.category.replaceAll("_", " ")} · {new Date(update.occurred_at).toLocaleDateString()}</div></div>
                          </div>
                        ))}
                      </div>
                    ) : <div className="rounded-3 border bg-body-tertiary p-4 text-center"><p className="text-body-secondary mb-0">You&apos;re all caught up. New updates will appear here when available.</p></div>}
                  </div>
                </section>
              </div>
            </div>

            <section id="patient-services" className="card border-0 shadow-sm mb-4">
              <div className="card-body p-4">
                <div className="d-flex flex-wrap align-items-center justify-content-between gap-2 mb-3">
                  <div><h2 className="h5 mb-1">Your care</h2><p className="small text-body-secondary mb-0">Shortcuts to your patient services.</p></div>
                </div>
                <div className="row g-2">
                  {patientServices.map(({ id, label, icon: Icon }) => (
                    <div className="col-6 col-md-3" key={id}>
                      <a href={`#service-${id}`} className="d-flex align-items-center gap-2 border rounded-3 p-3 text-decoration-none text-body h-100">
                        <Icon size={18} className="text-primary" aria-hidden="true" />
                        <span className="small fw-medium flex-grow-1">{label}</span>
                        <ChevronRight size={16} className="text-body-secondary" aria-hidden="true" />
                      </a>
                    </div>
                  ))}
                </div>
              </div>
            </section>

            <section aria-label="Patient services" className="row g-3">
              {patientServices.map(({ id, label, icon: Icon }) => (
                <div className="col-12 col-md-6 col-xl-3" key={id} id={`service-${id}`}>
                  <article className="card border-0 shadow-sm h-100">
                    <div className="card-body p-3">
                      <div className="d-flex align-items-center gap-2 mb-2"><Icon size={18} className="text-primary" aria-hidden="true" /><h3 className="h6 mb-0">{label}</h3></div>
                      <p className="small text-body-secondary mb-0">{id === "lab-reports" && dashboardData?.counts.lab_reports ? `${dashboardData.counts.lab_reports} released report${dashboardData.counts.lab_reports === 1 ? "" : "s"} available in your dashboard.` : id === "documents" && dashboardData?.counts.documents ? `${dashboardData.counts.documents} document${dashboardData.counts.documents === 1 ? "" : "s"} available in your dashboard.` : id === "medicines" && dashboardData?.counts.active_prescriptions ? `${dashboardData.counts.active_prescriptions} active prescription${dashboardData.counts.active_prescriptions === 1 ? "" : "s"}.` : id === "appointments" && dashboardData ? `${dashboardData.counts.upcoming_appointments} upcoming appointment${dashboardData.counts.upcoming_appointments === 1 ? "" : "s"}.` : "Your care team has not shared records in this service yet."}</p>
                    </div>
                  </article>
                </div>
              ))}
              <div className="col-12 col-md-6 col-xl-3" id="service-profile">
                <article className="card border-0 shadow-sm h-100">
                  <div className="card-body p-3">
                    <div className="d-flex align-items-center gap-2 mb-2"><UserRound size={18} className="text-primary" aria-hidden="true" /><h3 className="h6 mb-0">Profile</h3></div>
                    <p className="small text-body-secondary mb-0">Manage your patient portal profile.</p>
                  </div>
                </article>
              </div>
            </section>

            <nav aria-label="Patient dashboard shortcuts" className="border-top mt-4 pt-3 d-flex flex-wrap gap-3">
              <a href="#appointments" className="small text-decoration-none"><CalendarDays size={15} className="me-1" aria-hidden="true" />Appointments</a>
              <a href="#service-lab-reports" className="small text-decoration-none"><ClipboardList size={15} className="me-1" aria-hidden="true" />Reports</a>
              <a href="#service-medicines" className="small text-decoration-none"><Pill size={15} className="me-1" aria-hidden="true" />Prescriptions</a>
              <a href="#health-updates" className="small text-decoration-none"><Activity size={15} className="me-1" aria-hidden="true" />Messages</a>
            </nav>
          </main>
        </div>
      </div>
    </div>
  );
}
