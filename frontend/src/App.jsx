import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

const API = "http://127.0.0.1:8000";

function App() {
  const [summary, setSummary] = useState(null);
  const [invoices, setInvoices] = useState([]);
  const [matches, setMatches] = useState([]);
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");

  // =========================
  // NAVIGATION
  // =========================

  const goTo = (id) => {
    document.getElementById(id)?.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  };

  // =========================
  // LOAD DASHBOARD
  // =========================

  const loadDashboard = async () => {
    try {
      const [summaryRes, invoicesRes, matchesRes] =
        await Promise.all([
          axios.get(`${API}/dashboard/summary`),
          axios.get(`${API}/dashboard/invoices`),
          axios.get(`${API}/dashboard/matches`),
        ]);

      setSummary(summaryRes.data);
      setInvoices(invoicesRes.data);
      setMatches(matchesRes.data);

      setMessage("");
    } catch (error) {
      console.error("Dashboard error:", error);

      setMessage(
        "Backend connection failed. Make sure FastAPI is running."
      );
    }
  };

  // =========================
  // INITIAL LOAD
  // =========================

  useEffect(() => {
    loadDashboard();
  }, []);

  // =========================
  // UPLOAD DOCUMENT
  // =========================

  const uploadDocument = async () => {
    if (!file) {
      setMessage("Please select a document first.");
      return;
    }

    const formData = new FormData();

    formData.append("file", file);

    try {
      setUploading(true);

      setMessage(
        "DocuMind AI is analyzing your document..."
      );

      const response = await axios.post(
        `${API}/documents/upload`,
        formData
      );

      const data = response.data;

      if (data.duplicate?.is_duplicate) {
        setMessage(
          "⚠️ Duplicate invoice detected!"
        );
      } else if (
        data.matching?.status === "MISMATCH"
      ) {
        setMessage(
          "⚠️ PO / Invoice mismatch detected!"
        );
      } else {
        setMessage(
          "✅ Document processed successfully!"
        );
      }

      setFile(null);

      await loadDashboard();

      // Go back to overview after processing
      setTimeout(() => {
        goTo("overview");
      }, 500);

    } catch (error) {
      console.error("Upload error:", error);

      setMessage(
        error.response?.data?.detail ||
          "Document processing failed."
      );
    } finally {
      setUploading(false);
    }
  };

  const riskCount =
    summary?.high_risk_invoices || 0;

  return (
    <div className="dashboard">

      {/* =====================================================
          SIDEBAR
      ====================================================== */}

      <aside className="sidebar">

        {/* BRAND */}

        <div className="brand">

          <div className="brand-icon">
            D
          </div>

          <div>
            <h2>DocuMind</h2>

            <span>
              AI Intelligence
            </span>
          </div>

        </div>


        {/* COMPANY */}

        <div className="company-box">

          <span>
            WORKSPACE
          </span>

          <strong>
            Demo Company
          </strong>

        </div>


        {/* NAVIGATION */}

        <nav>

          <div className="nav-title">
            WORKSPACE
          </div>


          {/* OVERVIEW */}

          <button
            className="nav-item active"
            onClick={() => goTo("overview")}
          >
            <span>▦</span>
            Overview
          </button>


          {/* DOCUMENTS */}

          <button
            className="nav-item"
            onClick={() => goTo("documents")}
          >
            <span>▤</span>
            Documents
          </button>


          {/* INVOICES */}

          <button
            className="nav-item"
            onClick={() => goTo("invoices")}
          >
            <span>◫</span>
            Invoices
          </button>


          {/* PURCHASE ORDERS */}

          <button
            className="nav-item"
            onClick={() => goTo("matching")}
          >
            <span>▱</span>
            Purchase Orders
          </button>


          <div className="nav-title">
            INTELLIGENCE
          </div>


          {/* RISK */}

          <button
            className="nav-item"
            onClick={() => goTo("risk")}
          >
            <span>◈</span>
            Risk & Anomalies
          </button>


          {/* MATCHING */}

          <button
            className="nav-item"
            onClick={() => goTo("matching")}
          >
            <span>⇄</span>
            PO Matching
          </button>


          {/* ANALYTICS */}

          <button
            className="nav-item"
            onClick={() => goTo("analytics")}
          >
            <span>◉</span>
            Analytics
          </button>

        </nav>


        {/* SIDEBAR FOOTER */}

        <div className="sidebar-bottom">

          <div>
            ⚙ Settings
          </div>

          <div>
            ?
          </div>

        </div>

      </aside>


      {/* =====================================================
          MAIN CONTENT
      ====================================================== */}

      <main
        className="main"
        id="overview"
      >


        {/* =================================================
            TOP BAR
        ================================================== */}

        <div className="topbar">

          <div className="search">

            🔍

            <input
              placeholder="Search documents, invoices..."
            />

          </div>


          <div className="top-actions">

            <span>
              ◐
            </span>

            <span>
              🔔
            </span>

            <div className="avatar">
              C
            </div>

          </div>

        </div>


        {/* =================================================
            PAGE HEADER
        ================================================== */}

        <section
          className="page-header"
          id="documents"
        >

          <div>

            <p className="eyebrow">
              BUSINESS INTELLIGENCE
            </p>

            <h1>
              Document Intelligence
            </h1>

            <p>
              Monitor invoices, purchase orders,
              risks and financial anomalies.
            </p>

          </div>


          <div className="header-actions">

            {/* REFRESH */}

            <button
              className="secondary-btn"
              onClick={loadDashboard}
            >
              ↻ Refresh
            </button>


            {/* FILE SELECT */}

            <label className="primary-btn">

              + Upload Document

              <input
                type="file"
                hidden
                accept=".pdf,.png,.jpg,.jpeg"
                onChange={(event) => {
                  setFile(
                    event.target.files[0]
                  );
                }}
              />

            </label>


            {/* ANALYZE */}

            {file && (

              <button
                className="analyze-btn"
                onClick={uploadDocument}
                disabled={uploading}
              >
                {uploading
                  ? "Analyzing..."
                  : "Analyze"}
              </button>

            )}

          </div>

        </section>


        {/* =================================================
            MESSAGE
        ================================================== */}

        {message && (

          <div className="alert">
            {message}
          </div>

        )}


        {/* =================================================
            KPI CARDS
        ================================================== */}

        <section className="metrics">

          {/* INVOICES */}

          <Metric
            label="Total Invoices"
            value={
              summary?.total_invoices ?? "-"
            }
            icon="▤"
            subtitle="Processed documents"
          />


          {/* VALUE */}

          <Metric
            label="Invoice Volume"
            value={
              summary
                ? `₹${summary.total_invoice_value.toLocaleString()}`
                : "-"
            }
            icon="₹"
            subtitle="Total processed value"
          />


          {/* PURCHASE ORDERS */}

          <Metric
            label="Purchase Orders"
            value={
              summary?.total_purchase_orders ?? "-"
            }
            icon="▱"
            subtitle="Active records"
          />


          {/* RISK */}

          <Metric
            label="High Risk"
            value={riskCount}
            icon="!"
            subtitle="Needs attention"
            danger
          />

        </section>


        {/* =================================================
            ANALYTICS
        ================================================== */}

        <section
          className="analytics-grid"
          id="analytics"
        >


          {/* AI INSIGHT */}

          <div className="panel insight-panel">

            <div className="panel-header">

              <div>

                <span className="panel-label">
                  AI INSIGHT
                </span>

                <h2>
                  Financial Overview
                </h2>

              </div>

              <span className="ai-badge">
                ✦ AI Powered
              </span>

            </div>


            <div className="insight-content">

              <div className="big-number">

                ₹
                {summary
                  ? summary.total_invoice_value.toLocaleString()
                  : "0"}

              </div>

              <p>
                Total invoice value processed
                through DocuMind AI.
              </p>


              <div className="mini-stats">

                <div>

                  <strong>
                    {summary?.matched_documents ?? 0}
                  </strong>

                  <span>
                    Matched
                  </span>

                </div>


                <div>

                  <strong>
                    {summary?.mismatched_documents ?? 0}
                  </strong>

                  <span>
                    Mismatched
                  </span>

                </div>


                <div>

                  <strong>
                    {summary?.duplicate_invoices ?? 0}
                  </strong>

                  <span>
                    Duplicates
                  </span>

                </div>

              </div>

            </div>

          </div>


          {/* RISK */}

          <div
            className="panel"
            id="risk"
          >

            <div className="panel-header">

              <div>

                <span className="panel-label">
                  RISK MONITOR
                </span>

                <h2>
                  Risk Overview
                </h2>

              </div>

              <span className="risk-symbol">
                !
              </span>

            </div>


            <div className="risk-content">

              <div className="risk-circle">

                <strong>
                  {riskCount}
                </strong>

                <span>
                  High Risk
                </span>

              </div>


              <div className="risk-bars">

                <RiskBar
                  label="High Risk"
                  value={riskCount}
                  total={
                    summary?.total_invoices || 1
                  }
                />


                <RiskBar
                  label="Matched"
                  value={
                    summary?.matched_documents || 0
                  }
                  total={
                    summary?.total_invoices || 1
                  }
                />


                <RiskBar
                  label="Mismatched"
                  value={
                    summary?.mismatched_documents || 0
                  }
                  total={
                    summary?.total_invoices || 1
                  }
                />

              </div>

            </div>

          </div>

        </section>


        {/* =================================================
            PO MATCHING
        ================================================== */}

        <section
          className="panel"
          id="matching"
        >

          <div className="panel-header">

            <div>

              <span className="panel-label">
                AI VERIFICATION
              </span>

              <h2>
                PO ↔ Invoice Matching
              </h2>

            </div>

            <span className="view-all">
              {matches.length} checks
            </span>

          </div>


          <div className="matching-summary">

            <div className="match-stat">

              <span>
                Matched
              </span>

              <strong>
                {summary?.matched_documents ?? 0}
              </strong>

            </div>


            <div className="match-stat warning-stat">

              <span>
                Mismatched
              </span>

              <strong>
                {summary?.mismatched_documents ?? 0}
              </strong>

            </div>


            <div className="match-stat">

              <span>
                Total Checks
              </span>

              <strong>
                {matches.length}
              </strong>

            </div>

          </div>


          {/* MATCH TABLE */}

          {matches.length > 0 && (

            <div className="table-container matching-table">

              <table>

                <thead>

                  <tr>

                    <th>
                      PO ID
                    </th>

                    <th>
                      Invoice ID
                    </th>

                    <th>
                      Status
                    </th>

                    <th>
                      Mismatches
                    </th>

                  </tr>

                </thead>


                <tbody>

                  {matches.slice(0, 5).map(
                    (match) => (

                      <tr key={match.id}>

                        <td>
                          PO #{match.purchase_order_id}
                        </td>

                        <td>
                          Invoice #{match.invoice_id}
                        </td>

                        <td>

                          <span
                            className={
                              match.status === "MATCHED"
                                ? "status safe"
                                : "status danger"
                            }
                          >
                            {match.status}
                          </span>

                        </td>

                        <td>
                          {match.mismatch_count}
                        </td>

                      </tr>

                    )
                  )}

                </tbody>

              </table>

            </div>

          )}

        </section>


        {/* =================================================
            INVOICES
        ================================================== */}

        <section
          className="panel"
          id="invoices"
        >

          <div className="panel-header">

            <div>

              <span className="panel-label">
                DOCUMENT ACTIVITY
              </span>

              <h2>
                Recent Invoices
              </h2>

            </div>

            <span className="view-all">
              {invoices.length} records
            </span>

          </div>


          <div className="table-container">

            <table>

              <thead>

                <tr>

                  <th>
                    Invoice
                  </th>

                  <th>
                    Vendor
                  </th>

                  <th>
                    Amount
                  </th>

                  <th>
                    Risk
                  </th>

                  <th>
                    Status
                  </th>

                </tr>

              </thead>


              <tbody>

                {invoices
                  .slice(0, 10)
                  .map((invoice) => (

                    <tr key={invoice.id}>

                      <td>

                        <strong>
                          {invoice.invoice_number}
                        </strong>

                      </td>


                      <td>
                        Vendor #{invoice.vendor_id}
                      </td>


                      <td>
                        ₹
                        {Number(
                          invoice.total || 0
                        ).toLocaleString()}
                      </td>


                      <td>

                        <span
                          className={
                            invoice.risk_score >= 50
                              ? "status danger"
                              : "status safe"
                          }
                        >
                          {invoice.risk_score >= 50
                            ? `High (${invoice.risk_score})`
                            : `Low (${invoice.risk_score})`}
                        </span>

                      </td>


                      <td>

                        <span className="status neutral">
                          {invoice.status}
                        </span>

                      </td>

                    </tr>

                  ))}

              </tbody>

            </table>


            {invoices.length === 0 && (

              <div className="empty">
                No invoices processed yet.
              </div>

            )}

          </div>

        </section>


        {/* =================================================
            FOOTER
        ================================================== */}

        <footer>

          <span>
            DocuMind AI · Document Intelligence Platform
          </span>

          <span>
            Gemini AI · FastAPI · MySQL
          </span>

        </footer>

      </main>

    </div>
  );
}


/* =========================================================
   METRIC COMPONENT
========================================================= */

function Metric({
  label,
  value,
  icon,
  subtitle,
  danger,
}) {

  return (

    <div className="metric">

      <div className="metric-top">

        <div className="metric-icon">
          {icon}
        </div>

        {danger && (
          <span className="danger-dot">
            ●
          </span>
        )}

      </div>


      <span className="metric-label">
        {label}
      </span>


      <strong className="metric-value">
        {value}
      </strong>


      <span className="metric-subtitle">
        {subtitle}
      </span>

    </div>

  );
}


/* =========================================================
   RISK BAR COMPONENT
========================================================= */

function RiskBar({
  label,
  value,
  total,
}) {

  const percentage =
    Math.min(
      (value / total) * 100,
      100
    );

  return (

    <div className="risk-bar">

      <div className="risk-bar-label">

        <span>
          {label}
        </span>

        <strong>
          {value}
        </strong>

      </div>


      <div className="bar">

        <div
          style={{
            width: `${percentage}%`,
          }}
        />

      </div>

    </div>

  );
}


export default App;