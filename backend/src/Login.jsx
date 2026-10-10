
import React, { useState } from "react";

function Login({ onLogin, onRegister, error }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (loading) return;

    setLoading(true);

    try {
      const data = await onLogin(email.trim(), password);

      if (data?.success && data.token && data.user) {
        localStorage.setItem("token", data.token);
        localStorage.setItem("user", JSON.stringify(data.user));
        window.location.href = "/";
      }
    } catch (err) {
      console.error("Login error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="auth-page">
      <section className="auth-showcase">
        <div className="auth-brand">
          <div className="auth-brand-icon">R</div>
          <span>Resume<span className="auth-brand-accent">IQ</span></span>
        </div>

        <div className="auth-showcase-content">
          <span className="auth-eyebrow">
            <span className="auth-status-dot" />
            YOUR CAREER, UPGRADED
          </span>

          <h1>
            Your next opportunity
            <br />
            starts <span>with a better resume.</span>
          </h1>

          <p className="auth-showcase-description">
            Get intelligent resume feedback, discover skill gaps,
            and prepare for your next career move — all in one place.
          </p>

          <div className="auth-feature-list">
            <div className="auth-feature">
              <span className="auth-feature-icon">✦</span>
              <div>
                <strong>AI-powered resume insights</strong>
                <p>Understand your strengths and weaknesses.</p>
              </div>
            </div>

            <div className="auth-feature">
              <span className="auth-feature-icon">↗</span>
              <div>
                <strong>Smarter job matching</strong>
                <p>Find skills to improve your job readiness.</p>
              </div>
            </div>

            <div className="auth-feature">
              <span className="auth-feature-icon">✓</span>
              <div>
                <strong>Your progress in one place</strong>
                <p>Review previous analyses and track your scores.</p>
              </div>
            </div>
          </div>
        </div>

        <p className="auth-showcase-footer">
          Built to help you take the next step in your career.
        </p>
      </section>

      <section className="auth-form-side">
        <div className="auth-mobile-brand">
          <div className="auth-brand-icon">R</div>
          <span>Resume<span className="auth-brand-accent">IQ</span></span>
        </div>

        <div className="auth-card">
          <div className="auth-card-heading">
            <span className="auth-card-kicker">WELCOME BACK</span>
            <h2>Sign in to your account</h2>
            <p>Enter your details to continue to your dashboard.</p>
          </div>

          <form onSubmit={handleSubmit} className="auth-form">
            <label htmlFor="login-email">Email address</label>
            <input
              id="login-email"
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              autoComplete="email"
              required
            />

            <div className="auth-password-heading">
              <label htmlFor="login-password">Password</label>
            </div>

            <div className="auth-password-wrap">
              <input
                id="login-password"
                type={showPassword ? "text" : "password"}
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                autoComplete="current-password"
                required
              />

              <button
                type="button"
                className="auth-show-password"
                onClick={() => setShowPassword((previous) => !previous)}
                aria-label={showPassword ? "Hide password" : "Show password"}
              >
                {showPassword ? "Hide" : "Show"}
              </button>
            </div>

            {error && (
              <div className="auth-error" role="alert">
                <span>!</span>
                {error}
              </div>
            )}

            <button
              type="submit"
              className="auth-submit"
              disabled={loading}
            >
              {loading ? "Signing in..." : "Sign in"}
              {!loading && <span aria-hidden="true">→</span>}
            </button>
          </form>

          <div className="auth-divider">
            <span>YOUR CAREER JOURNEY</span>
          </div>

          <p className="auth-register-text">
            New here?{" "}
            <button
              type="button"
              onClick={onRegister}
              className="auth-register-button"
            >
              Create an account
            </button>
          </p>

          <div className="auth-security-note">
            <span>▣</span>
            Your account helps keep your analyses organized.
          </div>
        </div>

        <p className="auth-legal">
          AI Resume Analyzer · Career tools for your next move
        </p>
      </section>
    </main>
  );
}

export default Login;
