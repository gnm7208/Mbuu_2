import { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../services/api";
import { AuthContext } from "../context/AuthContext";

export default function Login() {
  const { setUser, setToken } = useContext(AuthContext);
  const [form, setForm] = useState({ username: "", password: "" });
  const navigate = useNavigate();

  const submit = async (e) => {
    e.preventDefault();
    const data = await api("/auth/login", { method: "POST", body: form });
    setUser({ id: data.id, username: data.username, is_admin: data.is_admin });
    setToken(data.token);
    navigate("/");
  };

  return (
    <form onSubmit={submit} className="card" style={{ maxWidth: 420, margin: "32px auto" }}>
      <h2>Login</h2>
      <input placeholder="Username" value={form.username} onChange={e => setForm({ ...form, username: e.target.value })} />
      <input type="password" placeholder="Password" value={form.password} onChange={e => setForm({ ...form, password: e.target.value })} />
      <button className="btn btn-primary" type="submit">Login</button>
    </form>
  );
}
