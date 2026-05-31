export default function Home() {
  return (
    <>
      {/* LOGIN SCREEN */}
      <div id="loginScreen" className="login-screen">
        <div className="login-card">
          <div className="login-brand">
            <div id="loginLogo" className="brand-icon"></div>
            <h1 id="loginTitle">DSWOPS</h1>
            <p id="loginOrg">
              Directorate of Wildlife, Khyber Pakhtunkhwa
            </p>
          </div>

          <div className="form-group">
            <label>Username</label>
            <input
              id="loginUsername"
              type="text"
              autoComplete="username"
              placeholder="Enter username"
            />
          </div>

          <div className="form-group">
            <label>Password</label>
            <input
              id="loginPassword"
              type="password"
              autoComplete="current-password"
              placeholder="Enter password"
            />
          </div>

          <div
            id="loginError"
            className="login-error"
            style={{ display: "none" }}
          ></div>

          <button
            id="loginBtn"
            className="btn btn-primary btn-full"
          >
            Sign In
          </button>

          <p id="loginFooter" className="login-footer">
            Document Scanner & Work Order Processing System
          </p>
        </div>
      </div>

      {/* MAIN APP */}
      <div id="app" style={{ display: "none" }}>
        <header className="topbar">
          <div className="topbar-left">
            <div
              id="appLogoImg"
              className="topbar-logo-img"
              style={{ display: "none" }}
            ></div>
            <span id="appTitle" className="topbar-title">
              DSWOPS
            </span>
          </div>

          <nav className="topbar-nav">
            <button className="nav-btn active">
              Scan Document
            </button>
            <button className="nav-btn">Records</button>
            <button className="nav-btn">Activity Log</button>
            <button className="nav-btn admin-only" style={{ display: "none" }}>
              Admin
            </button>
          </nav>

          <div className="topbar-user">
            <span id="userDisplayName" className="user-name"></span>
            <span id="userRoleBadge" className="role-badge"></span>
            <button className="btn btn-ghost btn-sm">
              Sign Out
            </button>
          </div>
        </header>

        {/* SCAN VIEW (ONLY STRUCTURE FOR NOW) */}
        <div id="view-scan" className="view active">
          <h2>Scan Document</h2>
        </div>

        {/* OTHER VIEWS (PLACEHOLDERS FOR NOW) */}
        <div id="view-records" className="view"></div>
        <div id="view-activity" className="view"></div>
        <div id="view-admin" className="view"></div>
      </div>
    </>
  );
}