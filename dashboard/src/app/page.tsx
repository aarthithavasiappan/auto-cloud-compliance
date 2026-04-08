import findingsData from './data/findings.json';

export default function Dashboard() {
  const findings = findingsData || [];
  
  const criticalCount = findings.filter((f: any) => f.severity === "CRITICAL" && !f.is_compliant).length;
  const highCount = findings.filter((f: any) => f.severity === "HIGH" && !f.is_compliant).length;
  const passCount = findings.filter((f: any) => f.is_compliant).length;

  return (
    <>
      <header className="glass-header">
        <div className="brand">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
          </svg>
          Antigravity CSPM
        </div>
        <div>
          <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Connected to AWS Org</span>
        </div>
      </header>

      <main style={{ padding: '32px', maxWidth: '1200px', margin: '0 auto' }}>
        <h1 style={{ fontSize: '2rem', marginBottom: '8px' }}>Security Posture</h1>
        <p style={{ color: 'var(--text-muted)', marginBottom: '32px' }}>AI-driven continuous monitoring and automated remediation.</p>
        
        {/* Metric Cards */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '24px' }}>
          <div className="glass-panel animate-fade-in" style={{ animationDelay: '0.1s' }}>
            <h3 style={{ fontSize: '0.85rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Critical Risks</h3>
            <div style={{ fontSize: '2.5rem', fontWeight: 700, color: 'var(--severity-critical)', marginTop: '8px' }}>{criticalCount}</div>
          </div>
          <div className="glass-panel animate-fade-in" style={{ animationDelay: '0.2s' }}>
            <h3 style={{ fontSize: '0.85rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>High Risks</h3>
            <div style={{ fontSize: '2.5rem', fontWeight: 700, color: 'var(--severity-high)', marginTop: '8px' }}>{highCount}</div>
          </div>
          <div className="glass-panel animate-fade-in" style={{ animationDelay: '0.3s' }}>
            <h3 style={{ fontSize: '0.85rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Compliant Resources</h3>
            <div style={{ fontSize: '2.5rem', fontWeight: 700, color: 'var(--severity-pass)', marginTop: '8px' }}>{passCount}</div>
          </div>
        </div>

        {/* Findings Table */}
        <div className="glass-panel mt-8 animate-fade-in" style={{ animationDelay: '0.4s', padding: 0, overflow: 'hidden' }}>
          <div style={{ padding: '24px 24px 0 24px' }}>
            <h2>Active Findings</h2>
          </div>
          <div style={{ overflowX: 'auto' }}>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Severity</th>
                  <th>Resource</th>
                  <th>Rule / Description</th>
                  <th style={{ width: '40%' }}>AI Assessment (Gemini)</th>
                </tr>
              </thead>
              <tbody>
                {findings.map((finding: any, idx: number) => {
                  const badgeClass = finding.is_compliant ? "pass" : finding.severity.toLowerCase();
                  const score = finding.ai_evaluation?.ai_risk_score || 0;
                  const scoreColor = score >= 85 ? 'var(--severity-critical)' : score > 50 ? 'var(--severity-high)' : 'var(--accent-primary)';
                  
                  return (
                    <tr key={idx} className="row">
                      <td>
                        <span className={`badge ${badgeClass}`}>
                          {finding.is_compliant ? 'PASS' : finding.severity}
                        </span>
                      </td>
                      <td>
                        <div style={{ fontWeight: 600 }}>{finding.resource_id}</div>
                        <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '4px' }}>Account: {finding.account_id}</div>
                      </td>
                      <td>
                        <div style={{ fontWeight: 500, color: 'var(--text-main)' }}>{finding.rule_id}</div>
                        <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '4px' }}>{finding.title}</div>
                        {!finding.is_compliant && finding.remediation_action && (
                          <div className="remediation-badge">
                            Action: {finding.remediation_action}
                          </div>
                        )}
                      </td>
                      <td>
                        {!finding.is_compliant && finding.ai_evaluation ? (
                          <>
                            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem' }}>
                              <span>Risk Score</span>
                              <span style={{ fontWeight: 700, color: scoreColor }}>{score}/100</span>
                            </div>
                            <div className="score-bar-bg">
                              <div className="score-bar-fill" style={{ width: `${score}%`, backgroundColor: scoreColor }}></div>
                            </div>
                            <div className="ai-reasoning">
                              {finding.ai_evaluation.ai_rationale}
                            </div>
                            {finding.remediation_outcome && (
                              <div style={{ marginTop: '8px', fontSize: '0.75rem', fontWeight: 600, color: finding.remediation_outcome === 'MANUAL_INTERVENTION_REQUIRED' ? 'var(--severity-critical)' : 'var(--severity-medium)' }}>
                                Orchestrator Outcome: {finding.remediation_outcome.replace(/_/g, ' ')}
                              </div>
                            )}
                          </>
                        ) : (
                          <div style={{ color: 'var(--severity-pass)', fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '6px' }}>
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
                            Evaluated as Compliant
                          </div>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </>
  );
}
