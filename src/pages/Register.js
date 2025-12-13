import { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../services/api";
import { AuthContext } from "../context/AuthContext";

export default function Register() {
  const { setUser, setToken } = useContext(AuthContext);
  const [form, setForm] = useState({ username: "", email: "", password: "", is_admin: false });
  const navigate = useNavigate();

  const submit = async (e) => {
    e.preventDefault();
    const data = await api("/auth/register", { method: "POST", body: form });
    setUser({ id: data.id, username: data.username, is_admin: data.is_admin });
    setToken(data.token);
    navigate("/");
  };

  return (
    <form onSubmit={submit} className="card" style={{ maxWidth: 480, margin: "32px auto" }}>
      <h2>Register</h2>
      <input placeholder="Username" value={form.username} onChange={e => setForm({ ...form, username: e.target.value })} />
      <input placeholder="Email" value={form.email} onChange={e => setForm({ ...form, email: e.target.value })} />
      <input type="password" placeholder="Password" value={form.password} onChange={e => setForm({ ...form, password: e.target.value })} />
      <label style={{ display: "flex", gap: 8, alignItems: "center" }}>
        <input type="checkbox" checked={form.is_admin} onChange={e => setForm({ ...form, is_admin: e.target.checked })} />
        Register as Admin
      </label>
      <button className="btn btn-primary" type="submit">Create account</button>
    </form>
  );
}
