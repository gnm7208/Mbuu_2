import React from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import { ThemeProvider } from "./context/ThemeContext";
import { AuthProvider, AuthContext } from "./context/AuthContext";
import ThemeToggle from "./components/ThemeToggle";
import ProtectedRoute from "./components/ProtectedRoute";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import MyPurchases from "./pages/MyPurchases";
import "./index.css";

function Header() {
  const { user, logout } = React.useContext(AuthContext);
  return (
    <header style={{ padding: 12, display: "flex", gap: 12, alignItems: "center" }}>
      <Link to="/" style={{ fontWeight: 700 }}>Mbuu</Link>
      <Link to="/">Cars</Link>
      <Link to="/purchases">My Purchases</Link>
      {user?.is_admin && <Link to="/dashboard">Admin</Link>}
      <div style={{ marginLeft: "auto", display: "flex", gap: 8, alignItems: "center" }}>
        <ThemeToggle />
        {user ? (
          <>
            <span>{user.username}</span>
            <button className="btn" onClick={logout}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
      </div>
    </header>
  );
}

export default function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <BrowserRouter>
          <Header />
          <main style={{ padding: 16, maxWidth: 1100, margin: "0 auto" }}>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/dashboard" element={
                <ProtectedRoute role="admin"><Dashboard /></ProtectedRoute>
              } />
              <Route path="/purchases" element={
                <ProtectedRoute role="customer"><MyPurchases /></ProtectedRoute>
              } />
            </Routes>
          </main>
        </BrowserRouter>
      </AuthProvider>
    </ThemeProvider>
  );
}
